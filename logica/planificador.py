# logica/planificador.py
# Busca la secuencia de operaciones de menor coste que separa una fracción en
# fracciones de un solo componente principal. Como cada operación actúa sobre
# una fracción y produce fracciones independientes, el problema se resuelve
# por recursión con memoria: coste(fr) = min_metodo [coste(metodo) + Σ coste(productos)].

from datos.materiales import MATERIALES
from datos.metodos import METODOS
from datos.reacciones import reacciones_posibles
from datos.sustancias import SUSTANCIAS
from logica.modelo import (Comp, _min, datos, describir, es_colorante, es_liquido,
                           estructura, fraccion, pendiente, principales,
                           tipo_mezcla)
from logica.reglas import (AUXILIARES, ORDEN_PREFERENCIA, Contexto,
                           NoAplicable, aplicar)

COSTE_NO_RESUELTO = 25.0
PROFUNDIDAD_MAXIMA = 16

RAZON_ORDEN = {
    "magnetismo": "Va primero porque es rápida, no altera nada y evita que el hierro acabe mezclado con otros sólidos (o reaccione en disolución).",
    "decantacion": "Conviene separar pronto los líquidos inmiscibles: mientras haya dos capas no se puede filtrar bien ni destilar.",
    "filtracion": "Los sólidos insolubles se retiran antes de calentar: en una destilación o evaporación estorbarían y contaminarían el residuo.",
    "sedimentacion": "Retira el sólido insoluble antes de tratar el líquido.",
    "disolucion": "Prepara la mezcla de sólidos para poder separar lo soluble de lo insoluble.",
    "destilacion": "Se hace cuando ya no quedan sólidos sin disolver ni líquidos inmiscibles; así se recupera el disolvente en lugar de perderlo.",
    "destilacion_fraccionada": "Se hace cuando ya solo quedan líquidos miscibles (y lo que llevan disuelto).",
    "evaporacion": "Es el último paso para obtener el sólido disuelto cuando no hace falta recuperar el líquido.",
    "cristalizacion": "Se usa al final para obtener el sólido disuelto como cristales.",
    "recristalizacion": "Se aplica cuando ya solo quedan las sales (y agua), para separarlas entre sí.",
    "cromatografia": "Se aplica a una pequeña muestra de la disolución que contiene los colorantes, para separarlos e identificarlos.",
}


def contexto(permitidos=None, recuperar_disolvente=True, cuantitativo=True, solubilidades=()):
    if permitidos is None:
        permitidos = ORDEN_PREFERENCIA
    return Contexto(frozenset(permitidos) | AUXILIARES, recuperar_disolvente, cuantitativo, tuple(solubilidades))


def comp_publico(c):
    d = SUSTANCIAS[c.clave]
    return {"clave": c.clave, "nombre": d["nombre"], "formula": d.get("formula"), "simbolo": d.get("simbolo"),
            "rol": c.rol, "masa": c.masa, "nota": c.nota, "estado": d["estado"]}


def fraccion_publica(fr):
    return [comp_publico(c) for c in fr]


def vaso_publico(fr):
    """Estructura física para dibujar la fracción como un vaso: fases líquidas
    (de la menos densa a la más densa), lo disuelto en cada una y los sólidos."""
    if not fr:
        return {"fases": [], "solidos": []}
    est = estructura(fr)
    fases = sorted(est.fases, key=lambda f: f["densidad"] if f["densidad"] is not None else 1.0)
    return {
        "fases": [{"liquidos": [c.clave for c in f["liquidos"]], "solutos": [c.clave for c in f["solutos"]]} for f in fases],
        "solidos": [c.clave for c in est.solidos],
        "incierto": bool(est.incertidumbres),
    }


class Planificador:
    def __init__(self, ctx):
        self.ctx = ctx
        self.memo = {}

    # ---------------------------------------------------------- búsqueda
    def opciones(self, fr, todas=False):
        """[(metodo, Resultado)] aplicables (y permitidos, salvo todas=True)."""
        salida = []
        for metodo in ORDEN_PREFERENCIA:
            if not todas and metodo not in self.ctx.permitidos:
                continue
            try:
                salida.append((metodo, aplicar(metodo, fr, self.ctx)))
            except NoAplicable:
                continue
        return salida

    def coste_productos(self, res, pila):
        return sum(self.resolver(p.fraccion, pila)[0] for p in res.productos if not p.analitico)

    def resolver(self, fr, pila=frozenset()):
        n = len(principales(fr))
        if not pendiente(fr):
            return 0.0, None
        if fr in self.memo:
            return self.memo[fr]
        no_resuelto = (COSTE_NO_RESUELTO * max(n - 1, 0.4), None)
        if fr in pila or len(pila) >= PROFUNDIDAD_MAXIMA:
            return no_resuelto
        mejor = no_resuelto
        for metodo, res in self.opciones(fr):
            total = res.coste + self.coste_productos(res, pila | {fr})
            if total < mejor[0] - 1e-9:
                mejor = (total, (metodo, res))
        self.memo[fr] = mejor
        return mejor

    # ---------------------------------------------------------- evaluación de una elección
    def evaluar(self, fr, metodo):
        """Clasifica la elección de un método para una fracción (modo práctica)."""
        nombre = METODOS.get(metodo, {}).get("nombre", metodo)
        if metodo not in self.ctx.permitidos:
            return {"estado": "no_permitido", "mensaje": f"{nombre} no está entre los métodos permitidos en este ejercicio."}
        try:
            res = aplicar(metodo, fr, self.ctx)
        except NoAplicable as e:
            return {"estado": "no_aplicable", "mensaje": str(e)}
        total = res.coste + self.coste_productos(res, frozenset())
        mejor, eleccion = self.resolver(fr)
        mejores = [m for m, r in self.opciones(fr)
                   if abs(r.coste + self.coste_productos(r, frozenset()) - mejor) < 1e-6]
        if total <= mejor + 1e-6:
            estado = "optima"
        elif total <= mejor + 3.6:
            estado = "valida"
        else:
            estado = "desaconsejada"
        return {"estado": estado, "resultado": res, "coste": total, "mejor": mejor, "mejores": mejores}

    # ---------------------------------------------------------- diagnóstico
    def diagnosticar(self, fr):
        motivos = []
        est = estructura(fr)
        motivos.extend(est.incertidumbres)
        prohibidos = []
        for metodo in ORDEN_PREFERENCIA:
            if metodo in self.ctx.permitidos:
                continue
            try:
                aplicar(metodo, fr, self.ctx)
                prohibidos.append(METODOS[metodo]["nombre"].lower())
            except NoAplicable:
                pass
        if prohibidos:
            motivos.append("Se podría continuar con " + " o ".join(prohibidos) + ", pero no está entre los métodos permitidos.")
        princ = principales(fr)
        insolubles = [c for c in princ if not es_liquido(c) and SUSTANCIAS[c.clave].get("solubilidad", {}).get("agua") != "soluble"
                      and not datos(c)["magnetico"]]
        if len(insolubles) >= 2:
            nombres = " y ".join(_min(datos(c)["nombre"]) for c in insolubles)
            motivos.append(
                f"SEPARALAB no tiene un método físico para separar {nombres}: son sólidos insolubles y no magnéticos. "
                "En la práctica podría probarse el tamizado o una sedimentación lenta si sus partículas tienen tamaños muy distintos."
            )
        colorantes = [c for c in princ if es_colorante(c)]
        if len(colorantes) >= 2 and "cromatografia" not in self.ctx.permitidos:
            motivos.append("Los colorantes solo se separan por cromatografía, que no está permitida.")
        sales = [c for c in princ if not es_liquido(c) and SUSTANCIAS[c.clave].get("solubilidad", {}).get("agua") == "soluble"
                 and not es_colorante(c)]
        if len(sales) >= 2 and "recristalizacion" in self.ctx.permitidos:
            try:
                aplicar("recristalizacion", fr, self.ctx)
            except NoAplicable as e:
                motivos.append(str(e))
        if len(princ) == 1 and pendiente(fr):
            motivos.append(f"{datos(princ[0])['nombre']} sigue disuelto: haría falta evaporar, cristalizar o destilar, y ninguno de esos métodos está permitido.")
        if not motivos:
            motivos.append("Ningún método disponible separa estos componentes con las reglas actuales.")
        return list(dict.fromkeys(motivos))

    # ---------------------------------------------------------- explicación de un paso
    def paso(self, numero, nombre_fraccion, fr, metodo, res):
        info = METODOS[metodo]
        alternativas = []
        coste_elegido = res.coste + self.coste_productos(res, frozenset())
        for otro, r in self.opciones(fr):
            if otro == metodo:
                continue
            total = r.coste + self.coste_productos(r, frozenset())
            motivo = r.avisos[0] if r.avisos else "Lleva a una secuencia más larga o con más pérdidas."
            if abs(total - coste_elegido) < 1e-6:
                motivo = "Igual de válida en este punto."
            alternativas.append({"metodo": otro, "nombre": METODOS[otro]["nombre"], "motivo": motivo})
        productos = []
        for p in res.productos:
            n = len(principales(p.fraccion))
            estado = "analitico" if p.analitico else ("sigue" if pendiente(p.fraccion) else "recuperado" if n == 1 else "auxiliar")
            productos.append({"nombre": p.nombre, "estado": estado, "componentes": fraccion_publica(p.fraccion),
                              "texto": describir(p.fraccion), "vaso": vaso_publico(p.fraccion)})
        return {
            "numero": numero,
            "metodo": metodo,
            "nombre": info["nombre"],
            "propiedad": info["propiedad"],
            "fundamento": info["fundamento"],
            "explicacion": res.explicacion,
            "por_que_aqui": RAZON_ORDEN.get(metodo, ""),
            "alternativas": alternativas,
            "entrada": {"nombre": nombre_fraccion, "componentes": fraccion_publica(fr), "texto": describir(fr),
                        "vaso": vaso_publico(fr)},
            "productos": productos,
            "perdidos": fraccion_publica(res.perdidos),
            "avisos": res.avisos,
            "detalle": res.detalle,
            "materiales": [{"clave": m, **MATERIALES[m]} for m in info["materiales"]],
            "procedimiento": info["procedimiento"],
            "precauciones": info["precauciones"],
            "limitaciones": info["limitaciones"],
            "montaje": info["montaje"],
            "auxiliar": metodo in AUXILIARES,
        }

    # ---------------------------------------------------------- plan completo
    def plan(self, fr):
        pasos, recuperados, sin_resolver, analiticos, auxiliares, perdidos = [], [], [], [], [], []

        def visitar(fr, nombre):
            n = len(principales(fr))
            if n == 0:
                if fr:
                    auxiliares.append({"nombre": nombre, "texto": describir(fr)})
                return
            if n == 1 and not pendiente(fr):
                recuperados.append({"nombre": nombre, "componentes": fraccion_publica(fr), "texto": describir(fr),
                                    "vaso": vaso_publico(fr),
                                    "principal": comp_publico(principales(fr)[0]),
                                    "impurezas": [comp_publico(c) for c in fr if c.rol == "impureza"]})
                return
            _, eleccion = self.resolver(fr)
            if eleccion is None:
                sin_resolver.append({"nombre": nombre, "componentes": fraccion_publica(fr), "texto": describir(fr),
                                     "vaso": vaso_publico(fr),
                                     "motivos": self.diagnosticar(fr)})
                return
            metodo, res = eleccion
            pasos.append(self.paso(len(pasos) + 1, nombre, fr, metodo, res))
            perdidos.extend(comp_publico(c) for c in res.perdidos)
            for p in res.productos:
                if p.analitico:
                    analiticos.append({"nombre": p.nombre, "componentes": fraccion_publica(p.fraccion)})
                else:
                    visitar(p.fraccion, p.nombre)

        visitar(fr, "Mezcla inicial")
        return {"pasos": pasos, "recuperados": recuperados, "sin_resolver": sin_resolver,
                "analiticos": analiticos, "auxiliares": auxiliares, "perdidos": perdidos}


# ---------------------------------------------------------------- análisis inicial

def construir_fraccion(claves, cantidades=None):
    """Crea la fracción inicial. cantidades: {clave: número} en g (sólidos) o mL (líquidos)."""
    cantidades = cantidades or {}
    comps = []
    for clave in claves:
        valor = cantidades.get(clave)
        masa = None
        if valor is not None:
            d = SUSTANCIAS[clave]
            masa = float(valor) * d["densidad"] if d["estado"] == "liquido" and d.get("densidad") else float(valor)
            masa = round(masa, 2)
        comps.append(Comp(clave, "principal", masa))
    return fraccion(comps)


def analizar(fr):
    """Descripción química de la mezcla antes de separarla."""
    est = estructura(fr)
    claves = [c.clave for c in fr]
    hay_agua = any(c.clave == "agua" for c in fr)
    fases = []
    for f in est.fases:
        fases.append({"tipo": "liquida", "liquidos": [datos(c)["nombre"] for c in f["liquidos"]],
                      "disueltos": [datos(c)["nombre"] for c in f["solutos"]], "densidad": f["densidad"]})
    for c in est.solidos:
        fases.append({"tipo": "solida", "componente": datos(c)["nombre"]})
    componentes = []
    for c in fr:
        d = datos(c)
        componentes.append({
            "clave": c.clave, "nombre": d["nombre"], "formula": d.get("formula"), "simbolo": d.get("simbolo"),
            "tipo": d["tipo"], "estado": d["estado"], "magnetico": d["magnetico"],
            "densidad": d.get("densidad"), "punto_ebullicion": d.get("punto_ebullicion"),
            "solubilidad_agua": d.get("solubilidad", {}).get("agua"), "descripcion": d.get("descripcion", ""),
            "peligros": d.get("peligros", []), "masa": c.masa,
        })
    reacciones = [{"ecuacion": r["ecuacion"], "explicacion": r["explicacion"], "consejo": r["consejo"], "activa": r["activa"]}
                  for r in reacciones_posibles(claves, hay_agua)]
    if len(fr) == 1:
        d = datos(fr[0])
        if d["tipo"] in ("elemento", "compuesto"):
            nota = (f"{d['nombre']} es una sustancia pura ({d['tipo']}): tiene composición fija y no se separa por métodos físicos."
                    + (" Un compuesto solo se descompone por métodos químicos." if d["tipo"] == "compuesto" else ""))
        else:
            nota = f"{d['nombre']} se trata en el modelo como un único componente."
    else:
        nota = ""
    return {
        "tipo": tipo_mezcla(fr),
        "num_fases": len(fases),
        "fases": fases,
        "componentes": componentes,
        "reacciones": reacciones,
        "supuestos": est.supuestos,
        "incertidumbres": est.incertidumbres,
        "nota_sustancia_pura": nota,
    }


def resolver_mezcla(claves, cantidades=None, permitidos=None, recuperar_disolvente=True, solubilidades=()):
    """Punto de entrada principal: análisis + plan completo."""
    fr = construir_fraccion(claves, cantidades)
    cuantitativo = bool(cantidades)
    ctx = contexto(permitidos, recuperar_disolvente, cuantitativo, solubilidades)
    plan = Planificador(ctx).plan(fr) if len(fr) > 1 else {"pasos": [], "recuperados": [], "sin_resolver": [],
                                                          "analiticos": [], "auxiliares": [], "perdidos": []}
    analisis = analizar(fr)
    completo = not plan["sin_resolver"] and len(fr) > 1
    plan["completo"] = completo
    plan["analisis"] = analisis
    plan["vaso_inicial"] = vaso_publico(fr)
    plan["resumen"] = _resumen(plan, fr)
    return plan


def _resumen(plan, fr):
    if len(fr) == 1:
        return plan.get("analisis", {}).get("nota_sustancia_pura", "")
    partes = []
    if plan["pasos"]:
        nombres = [p["nombre"].split(" (")[0].lower() for p in plan["pasos"]]
        partes.append(f"Secuencia de {len(nombres)} operaci{'ones' if len(nombres) > 1 else 'ón'}: " + " → ".join(nombres) + ".")
    if plan["sin_resolver"]:
        partes.append("La separación es parcial: quedan fracciones que las reglas disponibles no pueden separar.")
    else:
        partes.append("Todos los componentes quedan separados.")
    impuros = [r for r in plan["recuperados"] if r["impurezas"] or r["principal"]["nota"] == "enriquecido"]
    if impuros:
        partes.append("Algunos se obtienen con impurezas o enriquecidos, no puros: revisa los avisos de cada paso.")
    if plan["perdidos"]:
        partes.append("No se recupera: " + ", ".join(_min(p["nombre"]) for p in plan["perdidos"]) + ".")
    return " ".join(partes)
