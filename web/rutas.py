# web/rutas.py
# Rutas de la aplicación: páginas HTML y API JSON. Aquí no hay química: solo
# validación de la entrada, llamadas al motor y formato de la respuesta.

from flask import Blueprint, abort, jsonify, render_template, request

from datos.cromatografia import EJERCICIOS, IDENTIFICACION, PREGUNTAS_CONCEPTUALES, SIMULACIONES
from datos.materiales import MATERIALES
from datos.metodos import METODOS, METODOS_SEPARACION
from datos.recursos import VIDEOS, videos_de
from datos.retos import NIVELES, RETOS, obtener_reto
from datos.sustancias import ORDEN_CATALOGO, SUSTANCIAS
from logica import practica as practica_logica
from logica import retos as retos_logica
from logica.cromatografia import ErrorRf, calcular_rf, calcular_varias, comprobar_respuesta
from logica.planificador import resolver_mezcla
from web import validacion as v

bp = Blueprint("separalab", __name__)


def catalogo():
    salida = []
    for clave in ORDEN_CATALOGO:
        d = SUSTANCIAS[clave]
        salida.append({
            "clave": clave, "nombre": d["nombre"], "formula": d.get("formula"), "simbolo": d.get("simbolo"),
            "estado": d["estado"], "tipo": d["tipo"], "magnetico": d["magnetico"], "densidad": d.get("densidad"),
            "punto_ebullicion": d.get("punto_ebullicion"), "solubilidad_agua": d.get("solubilidad", {}).get("agua"),
            "descripcion": d.get("descripcion", ""), "categoria": d.get("categoria"),
        })
    return salida


def metodos_publicos():
    return [{"clave": m, "nombre": METODOS[m]["nombre"], "propiedad": METODOS[m]["propiedad"]} for m in METODOS_SEPARACION]


# --------------------------------------------------------------------- páginas

@bp.get("/")
def inicio():
    return render_template("inicio.html", activo="inicio", num_sustancias=len(SUSTANCIAS),
                           num_retos=len(RETOS), num_metodos=len(METODOS_SEPARACION))


@bp.get("/resolver")
def resolver():
    return render_template("resolver.html", activo="resolver", sustancias=catalogo(), metodos=metodos_publicos())


@bp.get("/practica")
def practica():
    return render_template("practica.html", activo="practica", sustancias=catalogo(), metodos=metodos_publicos())


@bp.get("/retos")
def retos():
    return render_template("retos.html", activo="retos", niveles=NIVELES,
                           retos=[retos_logica.resumen(r) for r in RETOS], sustancias=catalogo())


@bp.get("/cromatografia")
def cromatografia():
    return render_template("cromatografia.html", activo="cromatografia", ejercicios=EJERCICIOS,
                           preguntas=PREGUNTAS_CONCEPTUALES, identificacion=IDENTIFICACION, simulaciones=SIMULACIONES)


@bp.get("/laboratorio")
def laboratorio():
    metodos = [{"clave": m, **METODOS[m], "videos": videos_de(m),
                "materiales_info": [{"clave": x, **MATERIALES[x]} for x in METODOS[m]["materiales"]]}
               for m in METODOS_SEPARACION + ["disolucion"]]
    return render_template("laboratorio.html", activo="laboratorio", metodos=metodos,
                           materiales=[{"clave": k, **d} for k, d in MATERIALES.items()])


@bp.get("/videos")
def videos():
    agrupados = []
    for m in METODOS_SEPARACION:
        agrupados.append({"clave": m, "nombre": METODOS[m]["nombre"], "videos": videos_de(m)})
    return render_template("videos.html", activo="videos", grupos=agrupados, total=len(VIDEOS))


# --------------------------------------------------------------------- API

@bp.get("/api/sustancias")
def api_sustancias():
    return jsonify({"sustancias": catalogo(), "metodos": metodos_publicos()})


@bp.post("/api/resolver")
def api_resolver():
    datos = v.cuerpo(request)
    claves = v.sustancias(datos.get("sustancias"), minimo=1)
    cantidades = v.cantidades(datos.get("cantidades"), claves)
    permitidos = v.permitidos(datos.get("permitidos"))
    recuperar = datos.get("recuperar_disolvente", True)
    if not isinstance(recuperar, bool):
        raise v.ErrorEntrada("La opción de recuperar el disolvente no es válida.")
    return jsonify(resolver_mezcla(claves, cantidades, permitidos, recuperar))


@bp.post("/api/analizar")
def api_analizar():
    """Ruta de la versión anterior; se mantiene por compatibilidad."""
    datos = v.cuerpo(request)
    claves = v.sustancias(datos.get("sustancias"), minimo=2)
    return jsonify(resolver_mezcla(claves))


def _practica(datos):
    m = v.mezcla_practica(datos)
    fr, ctx = practica_logica.preparar(m["sustancias"], m["cantidades"], m["permitidos"], m["solubilidades"],
                                       m["usar_cantidades"], m["recuperar_disolvente"])
    return fr, ctx, v.historial(datos.get("historial"))


@bp.post("/api/practica/estado")
def api_practica_estado():
    fr, ctx, historial = _practica(v.cuerpo(request))
    return jsonify(practica_logica.estado(fr, ctx, historial))


@bp.post("/api/practica/evaluar")
def api_practica_evaluar():
    datos = v.cuerpo(request)
    fr, ctx, historial = _practica(datos)
    fid = datos.get("fraccion")
    if not isinstance(fid, str):
        raise v.ErrorEntrada("Indica a qué fracción aplicas el método.")
    prediccion = datos.get("prediccion")
    if prediccion is not None:
        if not isinstance(prediccion, list) or not all(isinstance(p, str) and p in SUSTANCIAS for p in prediccion):
            raise v.ErrorEntrada("La predicción no es válida.")
    r = practica_logica.evaluar(fr, ctx, historial, fid, v.metodo(datos.get("metodo")), prediccion)
    return jsonify(r)


@bp.post("/api/practica/pista")
def api_practica_pista():
    datos = v.cuerpo(request)
    fr, ctx, historial = _practica(datos)
    fid = datos.get("fraccion")
    if not isinstance(fid, str):
        raise v.ErrorEntrada("Indica la fracción.")
    return jsonify(practica_logica.pista(fr, ctx, historial, fid, v.entero(datos.get("nivel", 1), 1, 3, "nivel de pista")))


@bp.post("/api/practica/materiales")
def api_practica_materiales():
    datos = v.cuerpo(request)
    metodo = v.metodo(datos.get("metodo"))
    if "seleccion" not in datos:
        return jsonify({"opciones": practica_logica.opciones_materiales(metodo)})
    seleccion = datos.get("seleccion")
    if not isinstance(seleccion, list) or not all(isinstance(m, str) and m in MATERIALES for m in seleccion):
        raise v.ErrorEntrada("La selección de materiales no es válida.")
    return jsonify(practica_logica.corregir_materiales(metodo, seleccion))


@bp.post("/api/practica/procedimiento")
def api_practica_procedimiento():
    datos = v.cuerpo(request)
    metodo = v.metodo(datos.get("metodo"))
    if "orden" not in datos:
        return jsonify({"pasos": practica_logica.pasos_desordenados(metodo)})
    if not isinstance(datos.get("orden"), list):
        raise v.ErrorEntrada("El orden no es válido.")
    return jsonify(practica_logica.corregir_procedimiento(metodo, datos["orden"]))


@bp.get("/api/retos/aleatorio")
def api_reto_aleatorio():
    nivel = request.args.get("nivel") or None
    if nivel is not None and nivel not in NIVELES:
        raise v.ErrorEntrada("Nivel desconocido.")
    reto = retos_logica.aleatorio(nivel, request.args.get("excluir"))
    return jsonify(retos_logica.resumen(reto))


@bp.get("/api/retos/<id_reto>")
def api_reto(id_reto):
    reto = obtener_reto(id_reto) or abort(404)
    return jsonify(retos_logica.resumen(reto))


@bp.post("/api/retos/<id_reto>/pista")
def api_reto_pista(id_reto):
    reto = obtener_reto(id_reto) or abort(404)
    nivel = v.entero(v.cuerpo(request).get("nivel", 1), 1, 10, "nivel de pista")
    return jsonify({"nivel": nivel, "texto": retos_logica.pista(reto, nivel), "total": len(reto.get("pistas", []))})


@bp.post("/api/retos/<id_reto>/pregunta")
def api_reto_pregunta(id_reto):
    reto = obtener_reto(id_reto) or abort(404)
    datos = v.cuerpo(request)
    r = retos_logica.corregir_pregunta(reto, v.entero(datos.get("indice"), 0, 20, "número de pregunta"),
                                       v.entero(datos.get("opcion"), 0, 20, "opción"))
    if r is None:
        raise v.ErrorEntrada("Esa pregunta no existe.")
    return jsonify(r)


@bp.get("/api/retos/<id_reto>/solucion")
def api_reto_solucion(id_reto):
    reto = obtener_reto(id_reto) or abort(404)
    return jsonify(retos_logica.solucion(reto))


@bp.post("/api/rf")
def api_rf():
    datos = v.cuerpo(request)
    try:
        if "manchas" in datos:
            return jsonify(calcular_varias(datos.get("manchas"), datos.get("frente")))
        return jsonify(calcular_rf(datos.get("distancia"), datos.get("frente")))
    except ErrorRf as e:
        raise v.ErrorEntrada(str(e)) from e


@bp.post("/api/rf/comprobar")
def api_rf_comprobar():
    datos = v.cuerpo(request)
    ejercicio = next((e for e in EJERCICIOS if e["id"] == datos.get("ejercicio")), None)
    if ejercicio is None:
        raise v.ErrorEntrada("Ese ejercicio no existe.")
    mancha = next((m for m in ejercicio["manchas"] if m["nombre"] == datos.get("mancha")), None)
    if mancha is None:
        raise v.ErrorEntrada("Esa mancha no existe.")
    correcto = calcular_rf(mancha["distancia"], ejercicio["frente"])
    try:
        acierto = comprobar_respuesta(datos.get("respuesta"), correcto["rf"])
    except ErrorRf as e:
        raise v.ErrorEntrada(str(e)) from e
    return jsonify({"correcta": acierto, "solucion": correcto})
