# logica/practica.py
# Modo práctica: el estudiante elige paso a paso qué método aplicar a qué
# fracción. El servidor no guarda nada: el navegador envía el historial de
# decisiones aceptadas y aquí se reconstruye el estado con el mismo motor.

import random

from datos.materiales import MATERIALES
from datos.metodos import METODOS, METODOS_SEPARACION
from logica.modelo import describir, pendiente, principales, tipo_mezcla
from logica.planificador import (Planificador, comp_publico,
                                 construir_fraccion, contexto, fraccion_publica,
                                 vaso_publico)
from logica.reglas import AUXILIARES, NoAplicable, aplicar


class ErrorPractica(ValueError):
    pass


def preparar(sustancias, cantidades=None, permitidos=None, solubilidades=(), usar_cantidades=True,
             recuperar_disolvente=True):
    fr = construir_fraccion(sustancias, cantidades if usar_cantidades else None)
    ctx = contexto(permitidos, recuperar_disolvente, bool(cantidades) and usar_cantidades, solubilidades)
    return fr, ctx


def reconstruir(fr, ctx, historial):
    """Aplica el historial y devuelve el estado actual."""
    pendientes = {"1": {"nombre": "Mezcla inicial", "fraccion": fr}}
    recuperados, analiticos, perdidos, auxiliares = [], [], [], []
    orden = ["1"]
    for i, accion in enumerate(historial):
        fid, metodo = str(accion.get("fraccion")), accion.get("metodo")
        if fid not in pendientes:
            raise ErrorPractica(f"La decisión {i + 1} se refiere a una fracción que no existe.")
        if metodo not in ctx.permitidos:
            raise ErrorPractica(f"La decisión {i + 1} usa un método no permitido.")
        try:
            res = aplicar(metodo, pendientes[fid]["fraccion"], ctx)
        except NoAplicable as e:
            raise ErrorPractica(f"La decisión {i + 1} no es aplicable: {e}") from e
        del pendientes[fid]
        orden.remove(fid)
        perdidos.extend(comp_publico(c) for c in res.perdidos)
        for k, p in enumerate(res.productos, start=1):
            nid = f"{fid}.{k}"
            n = len(principales(p.fraccion))
            if p.analitico:
                analiticos.append({"id": nid, "nombre": p.nombre, "componentes": fraccion_publica(p.fraccion)})
            elif pendiente(p.fraccion):
                pendientes[nid] = {"nombre": p.nombre, "fraccion": p.fraccion}
                orden.append(nid)
            elif n == 1:
                recuperados.append({"id": nid, "nombre": p.nombre, "texto": describir(p.fraccion),
                                    "componentes": fraccion_publica(p.fraccion), "vaso": vaso_publico(p.fraccion)})
            elif p.fraccion:
                auxiliares.append({"id": nid, "nombre": p.nombre, "texto": describir(p.fraccion)})
    return pendientes, orden, recuperados, analiticos, perdidos, auxiliares


def estado(fr, ctx, historial):
    pendientes, orden, recuperados, analiticos, perdidos, auxiliares = reconstruir(fr, ctx, historial)
    plan = Planificador(ctx)
    lista = []
    for fid in orden:
        f = pendientes[fid]["fraccion"]
        aplicables = [m for m, _ in plan.opciones(f)]
        lista.append({
            "id": fid, "nombre": pendientes[fid]["nombre"], "texto": describir(f),
            "componentes": fraccion_publica(f), "tipo": tipo_mezcla(f), "vaso": vaso_publico(f),
            "sin_salida": not aplicables,
            "motivos": plan.diagnosticar(f) if not aplicables else [],
        })
    metodos = [{"clave": m, "nombre": METODOS[m]["nombre"], "propiedad": METODOS[m]["propiedad"],
                "auxiliar": m in AUXILIARES}
               for m in METODOS_SEPARACION + sorted(AUXILIARES) if m in ctx.permitidos]
    return {
        "pendientes": lista,
        "recuperados": recuperados,
        "analiticos": analiticos,
        "perdidos": perdidos,
        "auxiliares": auxiliares,
        "terminado": all(p["sin_salida"] for p in lista),
        "completo": not lista,
        "metodos": metodos,
    }


def _texto_mejores(mejores):
    return " o ".join(METODOS[m]["nombre"].lower() for m in mejores)


def evaluar(fr, ctx, historial, fid, metodo, prediccion=None):
    """Evalúa la elección del estudiante y explica el razonamiento."""
    pendientes, *_ = reconstruir(fr, ctx, historial)
    if fid not in pendientes:
        raise ErrorPractica("Esa fracción ya no está pendiente.")
    f = pendientes[fid]["fraccion"]
    plan = Planificador(ctx)
    ev = plan.evaluar(f, metodo)
    info = METODOS.get(metodo, {})
    salida = {"estado": ev["estado"], "metodo": metodo, "nombre": info.get("nombre", metodo),
              "propiedad": info.get("propiedad", ""), "aceptada": ev["estado"] in ("optima", "valida", "desaconsejada")}
    if ev["estado"] in ("no_permitido", "no_aplicable"):
        salida["mensaje"] = ev["mensaje"]
        salida["consejo"] = "Revisa el estado físico de cada componente: ¿qué está disuelto, qué es sólido y qué líquidos hay?"
        return salida
    res = ev["resultado"]
    salida["explicacion"] = res.explicacion
    salida["avisos"] = res.avisos
    if ev["estado"] == "optima":
        salida["mensaje"] = "¡Bien elegido! " + info.get("fundamento", "")
        otras = [m for m in ev["mejores"] if m != metodo]
        if otras:
            salida["mensaje"] += f" (También era igual de válido: {_texto_mejores(otras)}.)"
    elif ev["estado"] == "valida":
        salida["mensaje"] = ("Es una elección posible, pero hay una opción mejor en este punto: "
                             f"{_texto_mejores(ev['mejores'])}. "
                             + (res.avisos[0] if res.avisos else "Lleva a una secuencia más larga."))
    else:
        salida["mensaje"] = ("Se puede hacer, pero empeora el resultado final. "
                             + (" ".join(res.avisos[:2]) if res.avisos else "Hay una secuencia más sencilla.")
                             + f" Mejor opción: {_texto_mejores(ev['mejores'])}.")
    # Productos y predicción
    recuperados = []
    productos = []
    for p in res.productos:
        n = len(principales(p.fraccion))
        estado_p = "analitico" if p.analitico else ("sigue" if pendiente(p.fraccion) else "recuperado" if n == 1 else "auxiliar")
        productos.append({"nombre": p.nombre, "texto": describir(p.fraccion), "estado": estado_p,
                          "vaso": vaso_publico(p.fraccion)})
        if estado_p in ("recuperado", "analitico"):
            recuperados.extend(c.clave for c in principales(p.fraccion))
    salida["productos"] = productos
    if prediccion is not None:
        esperado, dicho = set(recuperados), set(prediccion)
        aciertos = esperado & dicho
        salida["prediccion"] = {
            "correcta": esperado == dicho,
            "aciertos": sorted(aciertos),
            "faltan": sorted(esperado - dicho),
            "sobran": sorted(dicho - esperado),
        }
    return salida


def pista(fr, ctx, historial, fid, nivel):
    pendientes, *_ = reconstruir(fr, ctx, historial)
    if fid not in pendientes:
        raise ErrorPractica("Esa fracción ya no está pendiente.")
    plan = Planificador(ctx)
    f = pendientes[fid]["fraccion"]
    _, eleccion = plan.resolver(f)
    if eleccion is None:
        motivos = plan.diagnosticar(f)
        return {"nivel": nivel, "texto": "Con los métodos permitidos esta fracción no se puede separar más. " + motivos[0]}
    metodo, _ = eleccion
    info = METODOS[metodo]
    if nivel <= 1:
        texto = f"Fíjate en esta propiedad: {info['propiedad'].lower()}."
    elif nivel == 2:
        texto = f"Pista: {info['cuando']}"
    else:
        texto = f"El método más adecuado ahora es: {info['nombre']}."
    return {"nivel": nivel, "texto": texto}


def opciones_materiales(metodo, semilla=None):
    """Material correcto mezclado con distractores (para elegir)."""
    info = METODOS[metodo]
    correctos = list(info["materiales"])
    otros = [m for m in MATERIALES if m not in correctos]
    rnd = random.Random(semilla)
    distractores = rnd.sample(otros, k=min(4, len(otros)))
    opciones = correctos + distractores
    rnd.shuffle(opciones)
    return [{"clave": m, "nombre": MATERIALES[m]["nombre"], "icono": MATERIALES[m]["icono"]} for m in opciones]


def corregir_materiales(metodo, seleccion):
    correctos = set(METODOS[metodo]["materiales"])
    elegidos = set(seleccion)
    faltan = correctos - elegidos
    sobran = elegidos - correctos
    def nom(ms):
        return [{"clave": m, "nombre": MATERIALES[m]["nombre"], "funcion": MATERIALES[m]["funcion"]} for m in sorted(ms)]
    return {"correcta": not faltan and not sobran, "faltan": nom(faltan), "sobran": nom(sobran),
            "aciertos": len(correctos & elegidos), "total": len(correctos)}


def pasos_desordenados(metodo, semilla=None):
    pasos = list(enumerate(METODOS[metodo]["procedimiento"]))
    rnd = random.Random(semilla)
    for _ in range(5):
        rnd.shuffle(pasos)
        if [i for i, _ in pasos] != list(range(len(pasos))) or len(pasos) < 2:
            break
    return [{"id": i, "texto": t} for i, t in pasos]


def corregir_procedimiento(metodo, orden):
    correcto = list(range(len(METODOS[metodo]["procedimiento"])))
    try:
        orden = [int(x) for x in orden]
    except (TypeError, ValueError) as e:
        raise ErrorPractica("El orden enviado no es válido.") from e
    if sorted(orden) != correcto:
        raise ErrorPractica("El orden debe incluir cada paso una sola vez.")
    bien = [i == j for i, j in zip(orden, correcto)]
    return {"correcta": all(bien), "posiciones_correctas": sum(bien), "total": len(correcto),
            "orden_correcto": METODOS[metodo]["procedimiento"]}
