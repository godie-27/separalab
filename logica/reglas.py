# logica/reglas.py
# Cada método de separación es una OPERACIÓN con:
#   - una condición (¿se puede aplicar a esta fracción?), que si no se cumple
#     devuelve un motivo explicado al estudiante;
#   - un efecto: las fracciones que produce, lo que se pierde, avisos y coste.
# El coste sirve para comparar secuencias: base del método + penalizaciones
# (pérdida de un componente, pureza baja, alteración por calor, etc.).

from dataclasses import dataclass, field
from typing import NamedTuple, Optional

from datos.metodos import METODOS
from datos.sustancias import (AZEOTROPOS, SUSTANCIAS, agua_por_gramo_anhidro,
                              masa_anhidra, solubilidad)
from logica.modelo import (Comp, clave_base, datos, es_colorante, es_liquido,
                           estructura, fraccion, principales)


class Contexto(NamedTuple):
    permitidos: frozenset
    recuperar_disolvente: bool = True
    cuantitativo: bool = True
    # Datos de solubilidad propios del ejercicio: ((clave_base, s20, s80, unidad, fuente), ...)
    solubilidades: tuple = ()


@dataclass
class Producto:
    nombre: str
    fraccion: tuple
    analitico: bool = False


@dataclass
class Resultado:
    metodo: str
    productos: list
    explicacion: str
    coste: float
    perdidos: list = field(default_factory=list)
    avisos: list = field(default_factory=list)
    detalle: dict = field(default_factory=dict)


class NoAplicable(Exception):
    """El método no puede aplicarse; el mensaje explica por qué."""


# ----------------------------------------------------------------- utilidades

def _n(c):
    return datos(c)["nombre"]


def _min(texto):
    """Primera letra en minúscula (respeta símbolos como (II) o CuSO₄)."""
    return texto[:1].lower() + texto[1:] if texto else texto


def _corto(c):
    """Nombre sin la aclaración entre paréntesis, en minúscula: 'etanol', 'aceite vegetal'."""
    return _min(_n(c).split(" (")[0])


def _lista(comps):
    nombres = [_min(_n(c)) if i else _n(c) for i, c in enumerate(comps)]
    if not nombres:
        return ""
    if len(nombres) == 1:
        return nombres[0]
    return ", ".join(nombres[:-1]) + " y " + nombres[-1]


def _fmt(x, dec=1):
    return f"{x:.{dec}f}".replace(".", ",")


def datos_solubilidad(ctx, clave):
    """Solubilidad numérica en agua (20 y 80 °C) de una sal, o None."""
    base = clave_base(clave)
    for (k, s20, s80, unidad, fuente) in ctx.solubilidades:
        if k == base:
            return {20: s20, 80: s80, "unidad": unidad, "fuente": fuente}
    d = SUSTANCIAS[base].get("solubilidad_agua")
    return dict(d) if d else None


def _hay_cobre_disuelto(est):
    return any(clave_base(s.clave) == "sulfato_de_cobre" for f in est.fases for s in f["solutos"])


def _penalizacion_hierro_cobre(fr, est, avisos):
    hierro = any(c.clave == "hierro" and c.rol == "principal" for c in fr)
    if hierro and _hay_cobre_disuelto(est):
        avisos.append(
            "El hierro sigue en contacto con la disolución de Cu²⁺ y puede reaccionar "
            "(Fe + Cu²⁺ → Fe²⁺ + Cu): conviene retirarlo antes con el imán."
        )
        return 3.0
    return 0.0


def _altera_calor(c):
    return SUSTANCIAS[c.clave].get("se_altera_al_calentar")


def _a_seco(comps):
    """Componentes que quedan como sólido tras eliminar el disolvente calentando."""
    salida = []
    for c in comps:
        nota = c.nota
        if _altera_calor(c) and c.rol == "principal":
            nota = "alterado por el calor"
        salida.append(Comp(c.clave, c.rol, c.masa, nota))
    return salida


# ----------------------------------------------------------------- operaciones

def magnetismo(fr, ctx):
    magneticos = [c for c in fr if c.rol == "principal" and datos(c)["magnetico"]]
    if not magneticos:
        compuestos_fe = [c for c in fr if c.clave in ("sulfuro_de_hierro", "oxido_de_hierro")]
        if compuestos_fe:
            raise NoAplicable(
                f"{_n(compuestos_fe[0])} contiene hierro, pero no es hierro metálico: no es magnético y el imán no lo separa."
            )
        raise NoAplicable("No hay ningún sólido magnético. Solo el hierro metálico es atraído por el imán.")
    resto = [c for c in fr if c not in magneticos]
    if not principales(resto):
        raise NoAplicable("Ya no queda nada de lo que separar el hierro.")
    avisos = []
    if any(es_liquido(c) for c in resto):
        avisos.append("Las limaduras salen mojadas: hay que secarlas.")
    return Resultado(
        "magnetismo",
        [Producto("Sólido atraído por el imán", fraccion(magneticos)),
         Producto("Resto de la mezcla", fraccion(resto))],
        "El imán atrae las limaduras de hierro, que son ferromagnéticas. "
        f"{_lista(principales(resto))} {'no son magnéticos y se quedan' if len(principales(resto)) > 1 else 'no es magnético y se queda'} en el recipiente.",
        1.0, avisos=avisos,
    )


def decantacion(fr, ctx):
    est = estructura(fr)
    if est.incertidumbres:
        raise NoAplicable(est.incertidumbres[0])
    if len(est.fases) < 2:
        if not est.fases:
            raise NoAplicable("No hay líquidos: la decantación separa líquidos inmiscibles.")
        liquidos = est.fases[0]["liquidos"]
        if len(liquidos) >= 2:
            raise NoAplicable(
                f"{_lista(liquidos)} son miscibles: forman una sola fase y no se separan en capas."
            )
        raise NoAplicable("Solo hay una fase líquida: no hay dos capas que separar.")
    if any(f["densidad"] is None for f in est.fases):
        raise NoAplicable("Falta la densidad de algún líquido para saber qué capa queda arriba.")
    superior = min(est.fases, key=lambda f: f["densidad"])
    otras = [f for f in est.fases if f is not superior]
    arriba = superior["liquidos"] + superior["solutos"]
    abajo = [c for c in fr if c not in arriba]
    avisos = []
    coste = 1.5 + _penalizacion_hierro_cobre(fr, est, avisos)
    if est.solidos:
        avisos.append("Los sólidos se depositan en el fondo con la fase inferior: dejar reposar y vigilar que no tapen la llave.")
    densa = otras[0]
    nombre_inf = "Fase inferior" + (" y sólidos" if est.solidos else "")
    return Resultado(
        "decantacion",
        [Producto(f"Fase superior ({', '.join(_corto(l) for l in superior['liquidos'])})", fraccion(arriba)),
         Producto(nombre_inf, fraccion(abajo))],
        f"{_lista(superior['liquidos'])} ({_fmt(superior['densidad'], 2)} g/mL) no se mezcla con "
        f"{_min(_lista(densa['liquidos']))} ({_fmt(densa['densidad'], 2)} g/mL) y es menos densa: queda arriba. "
        "Se vacía la capa inferior por la llave y la superior se recoge aparte.",
        coste, avisos=avisos,
    )


def _requisitos_solido_liquido(fr, est):
    if not est.fases:
        solubles = [c for c in fr if solubilidad(c.clave, "agua") == "soluble"]
        if solubles:
            raise NoAplicable(
                "La mezcla es de sólidos secos. Primero hay que disolver en agua lo soluble "
                f"({_min(_lista(solubles))}) y después filtrar."
            )
        raise NoAplicable("No hay ningún líquido: este método separa un sólido de un líquido.")
    if not [c for c in est.solidos if c.rol == "principal"]:
        raise NoAplicable(
            "No hay sólidos sin disolver: lo que está disuelto atraviesa el papel de filtro. "
            "Para recuperar un sólido disuelto hace falta evaporar, cristalizar o destilar."
        )


def filtracion(fr, ctx):
    est = estructura(fr)
    _requisitos_solido_liquido(fr, est)
    residuo = est.solidos
    filtrado = [c for c in fr if c not in residuo]
    avisos = []
    coste = 2.0 + _penalizacion_hierro_cobre(fr, est, avisos)
    if len(est.fases) >= 2:
        coste += 3.0
        avisos.append("Hay dos líquidos inmiscibles: es mejor separarlos antes por decantación (el aceite ensucia y frena el filtro).")
    if any(datos(c).get("particula") == "muy_fina" for c in residuo):
        avisos.append("La arcilla tiene partículas muy finas: parte puede atravesar el papel (filtrado turbio). Conviene dejar sedimentar antes.")
    for c in residuo:
        for f in est.fases:
            for l in f["liquidos"]:
                if solubilidad(c.clave, l.clave) == "poco_soluble":
                    avisos.append(f"{_n(c)} es muy poco soluble en {_min(_n(l))}: casi todo queda en el filtro.")
    explicacion = (
        f"{_lista(residuo)} no se disuelve{'n' if len(residuo) > 1 else ''} y sus partículas son mayores que los poros del papel: "
        f"{'quedan retenidos' if len(residuo) > 1 else 'queda retenido'} como residuo. "
    )
    disueltos = [s for f in est.fases for s in f["solutos"] if s.rol == "principal"]
    if disueltos:
        explicacion += f"{_lista(disueltos)} está{'n' if len(disueltos) > 1 else ''} disuelto{'s' if len(disueltos) > 1 else ''} y pasa{'n' if len(disueltos) > 1 else ''} con el líquido al filtrado."
    else:
        explicacion += "El líquido atraviesa el papel y se recoge como filtrado."
    return Resultado(
        "filtracion",
        [Producto("Residuo del filtro", fraccion(residuo)), Producto("Filtrado", fraccion(filtrado))],
        explicacion, coste, avisos=avisos,
    )


def sedimentacion(fr, ctx):
    est = estructura(fr)
    _requisitos_solido_liquido(fr, est)
    if len(est.fases) >= 2:
        raise NoAplicable("Hay dos líquidos inmiscibles: primero hay que separarlos por decantación.")
    sedimento = est.solidos
    liquido = [c for c in fr if c not in sedimento]
    avisos = ["La separación es aproximada: el líquido arrastra partículas finas y el sedimento queda húmedo."]
    coste = 3.0 + _penalizacion_hierro_cobre(fr, est, avisos)
    return Resultado(
        "sedimentacion",
        [Producto("Sedimento", fraccion(sedimento)), Producto("Líquido decantado", fraccion(liquido))],
        f"{_lista(sedimento)} {'son más densos' if len(sedimento) > 1 else 'es más denso'} que el líquido y no se "
        f"{'disuelven: se depositan' if len(sedimento) > 1 else 'disuelve: se deposita'} en el fondo y se vierte el líquido de encima.",
        coste, avisos=avisos,
    )


def _destilar(fr, ctx, fraccionada):
    metodo = "destilacion_fraccionada" if fraccionada else "destilacion"
    est = estructura(fr)
    if est.incertidumbres:
        raise NoAplicable(est.incertidumbres[0])
    if not est.fases:
        raise NoAplicable("No hay ningún líquido que destilar.")
    if len(est.fases) > 1:
        raise NoAplicable("Hay líquidos inmiscibles: primero hay que separarlos por decantación.")
    if [c for c in est.solidos if c.rol == "principal"]:
        raise NoAplicable(f"Hay sólidos sin disolver ({_min(_lista(est.solidos))}): primero hay que retirarlos, por ejemplo filtrando.")
    fase = est.fases[0]
    liquidos, solutos = fase["liquidos"], fase["solutos"]
    avisos = []
    coste_hc = _penalizacion_hierro_cobre(fr, est, avisos)

    if len(liquidos) >= 2:
        if any(datos(l).get("punto_ebullicion") is None for l in liquidos):
            raise NoAplicable("Falta el punto de ebullición de algún líquido.")
        orden = sorted(liquidos, key=lambda l: datos(l)["punto_ebullicion"])
        volatil, resto_liq = orden[0], orden[1:]
        diferencia = datos(resto_liq[0])["punto_ebullicion"] - datos(volatil)["punto_ebullicion"]
        pares = frozenset({volatil.clave, resto_liq[0].clave})
        destilado = [Comp(volatil.clave, volatil.rol, volatil.masa, "enriquecido" if (not fraccionada or pares in AZEOTROPOS) else "")]
        if not fraccionada or pares in AZEOTROPOS:
            destilado += [Comp(l.clave, "impureza") for l in resto_liq if l.rol == "principal"]
        residuo = resto_liq + solutos
        if fraccionada:
            coste = 3.5
            explicacion = (
                f"{_n(volatil)} hierve a {_fmt(datos(volatil)['punto_ebullicion'])} °C y {_min(_n(resto_liq[0]))} a "
                f"{_fmt(datos(resto_liq[0])['punto_ebullicion'])} °C. En la columna el vapor se condensa y se vuelve a evaporar "
                f"muchas veces y sale cada vez más rico en {_min(_n(volatil))}."
            )
        else:
            coste = 3.0 + (1.5 if "destilacion_fraccionada" in ctx.permitidos else 0.0)
            explicacion = (
                f"{_n(volatil)} hierve a {_fmt(datos(volatil)['punto_ebullicion'])} °C, antes que {_min(_n(resto_liq[0]))} "
                f"({_fmt(datos(resto_liq[0])['punto_ebullicion'])} °C): se vaporiza primero, se condensa y se recoge. "
                f"Como la diferencia es de solo {_fmt(diferencia, 0)} °C, el vapor también arrastra {_min(_n(resto_liq[0]))}: "
                "el destilado sale enriquecido, no puro."
            )
            if "destilacion_fraccionada" in ctx.permitidos:
                avisos.append("La destilación fraccionada separaría mejor estos líquidos miscibles.")
        if pares in AZEOTROPOS:
            avisos.append(AZEOTROPOS[pares])
        if volatil.clave == "etanol":
            avisos.append("El etanol es inflamable: calentar con placa o manta, sin llama.")
        if solutos:
            avisos.append(f"{_lista(solutos)} no {'son' if len(solutos) > 1 else 'es'} volátil{'es' if len(solutos) > 1 else ''}: queda{'n' if len(solutos) > 1 else ''} en el matraz.")
        return Resultado(
            metodo,
            [Producto(f"Destilado ({_corto(volatil)})", fraccion(destilado)),
             Producto("Residuo en el matraz", fraccion(residuo))],
            explicacion, coste + coste_hc, avisos=avisos,
        )

    if fraccionada:
        raise NoAplicable("Solo hay un líquido: la destilación fraccionada sirve para separar líquidos miscibles entre sí.")
    if not solutos:
        raise NoAplicable("Solo hay un líquido sin nada disuelto: no hay nada que separar.")
    liquido = liquidos[0]
    residuo = _a_seco(solutos)
    coste = 3.0 + coste_hc
    principales_residuo = [c for c in residuo if c.rol == "principal"]
    if len(principales_residuo) == 1 and _altera_calor(principales_residuo[0]):
        coste += 3.0
    for c in solutos:
        if _altera_calor(c) and c.rol == "principal":
            avisos.append(f"Si se destila hasta sequedad: {_altera_calor(c)}")
    if liquido.rol == "auxiliar":
        coste += 1.0  # recuperar agua añadida no aporta nada frente a evaporar
    return Resultado(
        "destilacion",
        [Producto(f"Destilado ({_corto(liquido)})", fraccion([liquido])),
         Producto("Residuo sólido en el matraz", fraccion(residuo))],
        f"{_n(liquido)} hierve a {_fmt(datos(liquido)['punto_ebullicion'])} °C; {_min(_lista(solutos))} no es volátil. "
        f"Se recupera {_min(_n(liquido))} como destilado y el sólido queda en el matraz. A diferencia de la evaporación, "
        "aquí el disolvente no se pierde.",
        coste, avisos=avisos,
    )


def destilacion(fr, ctx):
    return _destilar(fr, ctx, fraccionada=False)


def destilacion_fraccionada(fr, ctx):
    return _destilar(fr, ctx, fraccionada=True)


def _una_fase_sin_solidos(fr, est):
    if est.incertidumbres:
        raise NoAplicable(est.incertidumbres[0])
    if not est.fases:
        raise NoAplicable("No hay disolución: este método recupera un sólido disuelto en un líquido.")
    if len(est.fases) > 1:
        raise NoAplicable("Hay dos líquidos inmiscibles: primero hay que separarlos por decantación.")
    if [c for c in est.solidos if c.rol == "principal"]:
        raise NoAplicable(f"Hay sólidos sin disolver ({_min(_lista(est.solidos))}): primero hay que filtrarlos.")


def evaporacion(fr, ctx):
    est = estructura(fr)
    _una_fase_sin_solidos(fr, est)
    fase = est.fases[0]
    solutos = fase["solutos"]
    if not [s for s in solutos if s.rol == "principal"]:
        raise NoAplicable("No hay ningún sólido disuelto que recuperar.")
    perdidos = [l for l in fase["liquidos"] if l.rol == "principal"]
    avisos = []
    coste = 2.5 + _penalizacion_hierro_cobre(fr, est, avisos)
    if perdidos:
        coste += 8.0 if ctx.recuperar_disolvente else 0.0
        avisos.append(f"{_lista(perdidos)} se pierde{'n' if len(perdidos) > 1 else ''} en el aire: si interesa recuperarlo, hay que destilar.")
    residuo = _a_seco(solutos)
    principales_res = [c for c in residuo if c.rol == "principal"]
    if len(principales_res) > 1:
        avisos.append(f"{_lista(principales_res)} quedan juntos en la cápsula: la evaporación no los separa entre sí.")
    for c in solutos:
        if _altera_calor(c) and c.rol == "principal":
            avisos.append(_altera_calor(c))
            if len(principales_res) == 1:
                coste += 3.0
    return Resultado(
        "evaporacion",
        [Producto("Residuo sólido en la cápsula", fraccion(residuo))],
        f"Al calentar, {_min(_lista(fase['liquidos']))} se evapora; {_min(_lista(solutos))} no es volátil y queda como sólido.",
        coste, perdidos=perdidos, avisos=avisos,
    )


def cristalizacion(fr, ctx):
    est = estructura(fr)
    _una_fase_sin_solidos(fr, est)
    fase = est.fases[0]
    solutos_p = [s for s in fase["solutos"] if s.rol == "principal"]
    if not solutos_p:
        raise NoAplicable("No hay ningún sólido disuelto que cristalizar.")
    if len(solutos_p) > 1:
        raise NoAplicable(
            f"Hay varios sólidos disueltos ({_min(_lista(solutos_p))}): cristalizarían juntos. "
            "Para separarlos hace falta la recristalización (o la cromatografía si son colorantes)."
        )
    soluto = solutos_p[0]
    if es_colorante(soluto):
        raise NoAplicable("Un colorante en pequeña cantidad no se recupera por cristalización.")
    hidrato = SUSTANCIAS[clave_base(soluto.clave)].get("cristaliza_como", soluto.clave)
    cristal = Comp(hidrato, "principal", None, "" if hidrato == soluto.clave else f"de {_n(soluto)}")
    madres = fase["liquidos"] + [Comp(soluto.clave, "impureza")] + [s for s in fase["solutos"] if s.rol != "principal"]
    s = datos_solubilidad(ctx, soluto.clave)
    if s and s[80] / s[20] > 1.5:
        mecanismo = (f"Su solubilidad baja mucho al enfriar ({_fmt(s[80])} → {_fmt(s[20])} {s['unidad']} de 80 a 20 °C): "
                     "al enfriar la disolución concentrada, el exceso cristaliza.")
    else:
        mecanismo = "Al evaporar lentamente parte del disolvente, la disolución se satura y el soluto forma cristales."
    coste = 3.0
    avisos = []
    if any(l.rol == "principal" for l in fase["liquidos"]):
        coste += 1.5
        avisos.append("Parte del disolvente se evapora y el resto (aguas madres) conserva algo de soluto disuelto.")
    if hidrato != soluto.clave:
        avisos.append(f"Se recupera como {SUSTANCIAS[hidrato]['formula']}, la forma que cristaliza desde el agua.")
    return Resultado(
        "cristalizacion",
        [Producto("Cristales", fraccion([cristal])), Producto("Aguas madres", fraccion(madres))],
        f"{mecanismo} Se obtienen cristales de {_min(SUSTANCIAS[hidrato]['nombre'])} sin calentar hasta sequedad.",
        coste, avisos=avisos,
    )


def _cristaliza(m_x, m_y_list, W, s20x, s20y_list, f):
    """Masa de X (anhidro) y de cada Y que cristalizan a 20 °C con W g de agua."""
    x = max(0.0, (m_x - s20x * W / 100) / (1 - s20x / 100 * f))
    w_libre = W - f * x
    ys = [max(0.0, m - s * w_libre / 100) for m, s in zip(m_y_list, s20y_list)]
    return x, ys


def recristalizacion(fr, ctx):
    est = estructura(fr)
    if est.incertidumbres:
        raise NoAplicable(est.incertidumbres[0])
    if len(est.fases) > 1:
        raise NoAplicable("Hay líquidos inmiscibles: primero hay que decantarlos.")
    liquidos = est.fases[0]["liquidos"] if est.fases else []
    otros_liq = [l for l in liquidos if l.clave != "agua"]
    if otros_liq:
        raise NoAplicable(f"La disolución contiene {_min(_lista(otros_liq))}: primero hay que separarlo (por destilación).")
    insolubles = [c for c in est.solidos if c.rol == "principal" and solubilidad(c.clave, "agua") != "soluble"]
    if insolubles:
        raise NoAplicable(f"Hay sólidos insolubles ({_min(_lista(insolubles))}): primero hay que retirarlos.")
    sales = [c for c in fr if c.rol == "principal" and not es_liquido(c) and solubilidad(c.clave, "agua") == "soluble"
             and not es_colorante(c)]
    con_datos = [c for c in sales if datos_solubilidad(ctx, c.clave)]
    if len(sales) < 2:
        raise NoAplicable("La recristalización separa dos o más sales solubles; aquí no las hay.")
    if len(con_datos) < 2:
        raise NoAplicable("Faltan datos de solubilidad a 20 y 80 °C para decidir qué sal cristaliza.")
    razon = {c: datos_solubilidad(ctx, c.clave)[80] / datos_solubilidad(ctx, c.clave)[20] for c in con_datos}
    x_comp = max(con_datos, key=lambda c: razon[c])
    otras = [c for c in con_datos if c is not x_comp]
    if razon[x_comp] < 1.3 * max(razon[c] for c in otras):
        raise NoAplicable("Las solubilidades de las sales cambian de forma parecida con la temperatura: al enfriar no cristalizaría una sola.")
    sx = datos_solubilidad(ctx, x_comp.clave)
    sy = [datos_solubilidad(ctx, c.clave) for c in otras]
    hidrato = SUSTANCIAS[clave_base(x_comp.clave)].get("cristaliza_como", x_comp.clave)
    f = agua_por_gramo_anhidro(clave_base(x_comp.clave))
    resto_solutos = [c for c in fr if not es_liquido(c) and c is not x_comp and c not in otras]
    agua_presente = [l for l in liquidos if l.clave == "agua"]
    avisos, detalle = [], {}
    coste = 3.0 + _penalizacion_hierro_cobre(fr, est, avisos)
    if any(l.rol == "principal" for l in agua_presente):
        coste += 4.0
        avisos.append("Al concentrar la disolución se evapora parte del agua; si interesa recuperarla, conviene destilarla antes.")
    agua_aux = [] if agua_presente else [Comp("agua", "auxiliar")]
    tabla = [{"sal": _n(c), "s20": datos_solubilidad(ctx, c.clave)[20], "s80": datos_solubilidad(ctx, c.clave)[80],
              "unidad": datos_solubilidad(ctx, c.clave)["unidad"], "fuente": datos_solubilidad(ctx, c.clave)["fuente"]}
             for c in [x_comp] + otras]
    detalle["datos"] = tabla
    explicacion = (
        f"De 20 a 80 °C la solubilidad de {_min(_n(x_comp))} pasa de {_fmt(sx[20])} a {_fmt(sx[80])} {sx['unidad']}, "
        f"mientras que la de {_min(_lista(otras))} apenas cambia ({_fmt(sy[0][20])} → {_fmt(sy[0][80])}). "
        f"Al enfriar la disolución caliente, {_min(_n(x_comp))} supera su solubilidad y cristaliza como "
        f"{SUSTANCIAS[hidrato]['formula']}; {_min(_lista(otras))} sigue disuelto en las aguas madres."
    )

    masas = [x_comp] + otras
    if ctx.cuantitativo and all(c.masa is not None for c in masas):
        m_x = masa_anhidra(x_comp.clave, x_comp.masa)
        m_y = [masa_anhidra(c.clave, c.masa) for c in otras]
        s20y = [s[20] for s in sy]
        w80 = max([m_x / sx[80] * 100] + [m / s[80] * 100 for m, s in zip(m_y, sy)])
        ventana = []
        w = w80
        while w <= m_x / sx[20] * 100 + 0.05:
            x, ys = _cristaliza(m_x, m_y, w, sx[20], s20y, f)
            if x > 0.0005 and all(y <= 1e-9 for y in ys):
                ventana.append((w, x))
            w += 0.1
        x_min, ys_min = _cristaliza(m_x, m_y, w80, sx[20], s20y, f)
        detalle["agua_minima_80"] = round(w80, 1)
        detalle["con_agua_minima"] = {"x": round(x_min * (1 + f), 2), "ys": [round(y, 2) for y in ys_min]}
        if not ventana:
            otras_txt = ", ".join(f"{_fmt(y, 2)} g de {_min(_n(c))}" for y, c in zip(ys_min, otras))
            raise NoAplicable(
                f"Con estas cantidades no hay separación limpia. Con el agua mínima para disolverlo todo a 80 °C "
                f"({_fmt(w80)} g), al enfriar a 20 °C cristalizarían {_fmt(x_min * (1 + f), 2)} g de "
                f"{SUSTANCIAS[hidrato]['formula']} y {otras_txt}: no existe una cantidad de agua que haga cristalizar "
                f"solo {_min(_n(x_comp))}. (Cálculo con los datos de solubilidad indicados, suponiendo que las sales "
                "no se afectan entre sí; 1 mL de agua ≈ 1 g.)"
            )
        w_opt, x_opt = ventana[0]
        detalle.update({"ventana": [round(ventana[0][0], 1), round(ventana[-1][0], 1)],
                        "agua_usada": round(w_opt, 1), "cristales_g": round(x_opt * (1 + f), 2),
                        "rendimiento": round(100 * x_opt / m_x)})
        avisos.append(
            f"Cálculo: la cristalización es selectiva con entre {_fmt(ventana[0][0])} y {_fmt(ventana[-1][0])} g de agua. "
            f"Con {_fmt(w_opt)} g cristalizan {_fmt(x_opt * (1 + f), 2)} g de {SUSTANCIAS[hidrato]['formula']} "
            f"({round(100 * x_opt / m_x)} % del {_min(_n(x_comp)).split(' ')[0]} de la muestra); el resto queda en las aguas madres."
        )
        if ys_min and any(y > 0 for y in ys_min):
            avisos.append(
                f"Ojo: con el agua mínima a 80 °C ({_fmt(w80)} g) cristalizaría también {_min(_lista(otras))}. "
                "Hace falta algo más de agua."
            )
        cristal = Comp(hidrato, "principal", round(x_opt * (1 + f), 2), "" if hidrato == x_comp.clave else f"de {_n(x_comp)}")
        madres = agua_aux + agua_presente + [Comp(x_comp.clave, "impureza", round(m_x - x_opt, 2))] + otras + resto_solutos
    else:
        relacion = sx[20] / sy[0][20]
        detalle["condicion"] = round(relacion, 2)
        avisos.append(
            f"Funciona si las cantidades lo permiten: con estos datos, la masa de {_min(_n(x_comp))} (como sal anhidra) "
            f"debe ser mayor que {_fmt(relacion, 2)} veces la de {_min(_n(otras[0]))}. Introduce las cantidades para comprobarlo."
        )
        cristal = Comp(hidrato, "principal", None, "" if hidrato == x_comp.clave else f"de {_n(x_comp)}")
        madres = agua_aux + agua_presente + [Comp(x_comp.clave, "impureza")] + otras + resto_solutos
    return Resultado(
        "recristalizacion",
        [Producto(f"Cristales de {SUSTANCIAS[hidrato]['formula']}", fraccion([cristal])),
         Producto("Aguas madres", fraccion(madres))],
        explicacion, coste, avisos=avisos, detalle=detalle,
    )


def disolucion(fr, ctx):
    if any(es_liquido(c) for c in fr):
        raise NoAplicable("La mezcla ya tiene líquido: no hace falta añadir agua.")
    princ = principales(fr)
    solubles = [c for c in princ if solubilidad(c.clave, "agua") == "soluble"]
    insolubles = [c for c in princ if solubilidad(c.clave, "agua") != "soluble"]
    if not solubles:
        raise NoAplicable("Ningún componente es soluble en agua: añadir agua no ayuda a separarlos.")
    if not insolubles:
        raise NoAplicable("Todos los sólidos son solubles: al añadir agua se disolverían juntos (para separarlos haría falta la recristalización).")
    avisos = []
    coste = 1.0
    nombres_fe = {c.clave for c in fr}
    if "hierro" in nombres_fe and nombres_fe & {"sulfato_de_cobre", "sulfato_de_cobre_pentahidratado"}:
        coste += 3.0
        avisos.append("Al añadir agua, el hierro reaccionaría con el sulfato de cobre disuelto: retira antes el hierro con el imán.")
    masa_agua = None
    if all(c.masa is not None for c in solubles):
        total = 0.0
        for c in solubles:
            s = datos_solubilidad(ctx, c.clave)
            if s is None:
                total = None
                break
            total += masa_anhidra(c.clave, c.masa) / s[20] * 100
        if total is not None:
            masa_agua = round(total * 1.2, 0)
            avisos.append(f"Hacen falta al menos unos {_fmt(total, 0)} g de agua a 20 °C; se añade un poco más ({_fmt(masa_agua, 0)} g).")
    return Resultado(
        "disolucion",
        [Producto("Mezcla con agua", fraccion(list(fr) + [Comp("agua", "auxiliar", masa_agua)]))],
        f"El agua disuelve {_min(_lista(solubles))} (sus partículas se hidratan); {_min(_lista(insolubles))} "
        "no se disuelve y queda como sólido, listo para filtrar.",
        coste, avisos=avisos,
    )


def cromatografia(fr, ctx):
    colorantes = [c for c in fr if c.rol == "principal" and es_colorante(c)]
    if len(colorantes) < 2:
        raise NoAplicable("La cromatografía se usa aquí para separar e identificar colorantes; no hay al menos dos.")
    if not any(es_liquido(c) for c in fr):
        raise NoAplicable("Los colorantes deben estar en disolución para aplicar una gota en el papel.")
    est = estructura(fr)
    if len(est.fases) > 1 or [c for c in est.solidos if c.rol == "principal"]:
        raise NoAplicable("Primero hay que obtener una disolución limpia: separa antes los líquidos inmiscibles y los sólidos sin disolver.")
    productos = [Producto(f"{_n(c)} (mancha en el cromatograma)", fraccion([Comp(c.clave, "principal", None, "analitica")]), analitico=True)
                 for c in colorantes]
    resto = [Comp(c.clave, "impureza", c.masa) if c in colorantes else c for c in fr]
    productos.append(Producto("Resto de la disolución", fraccion(resto)))
    return Resultado(
        "cromatografia",
        productos,
        "Se aplica una gota de la disolución en el papel. Cada colorante tiene distinta afinidad por la fase estacionaria "
        "(agua unida a la celulosa) y por la fase móvil, así que avanza a distinta velocidad y aparece como una mancha separada.",
        2.0,
        avisos=["La cromatografía separa e identifica una muestra pequeña: los colorantes no se recuperan en cantidad y el resto de la disolución los sigue conteniendo."],
    )


OPERACIONES = {
    "magnetismo": magnetismo,
    "decantacion": decantacion,
    "filtracion": filtracion,
    "sedimentacion": sedimentacion,
    "disolucion": disolucion,
    "destilacion": destilacion,
    "destilacion_fraccionada": destilacion_fraccionada,
    "evaporacion": evaporacion,
    "cristalizacion": cristalizacion,
    "recristalizacion": recristalizacion,
    "cromatografia": cromatografia,
}
ORDEN_PREFERENCIA = list(OPERACIONES.keys())
AUXILIARES = {"disolucion"}


def aplicar(metodo, fr, ctx):
    """Aplica un método. Lanza NoAplicable si no se puede."""
    if metodo not in OPERACIONES:
        raise NoAplicable("Método desconocido.")
    return OPERACIONES[metodo](fr, ctx)


def evaluar_metodos(sustancias):
    """Compatibilidad con la versión anterior: lista de métodos aplicables.

    Recibe la lista de diccionarios de sustancias (con 'clave') y devuelve
    [{"metodo", "razon", "prioridad"}] ordenados por coste.
    """
    if not sustancias:
        return []
    fr = fraccion([Comp(s["clave"]) for s in sustancias])
    ctx = Contexto(frozenset(OPERACIONES))
    opciones = []
    for metodo in ORDEN_PREFERENCIA:
        try:
            r = aplicar(metodo, fr, ctx)
        except NoAplicable:
            continue
        opciones.append({"metodo": metodo, "razon": r.explicacion, "prioridad": r.coste,
                         "nombre": METODOS[metodo]["nombre"]})
    return sorted(opciones, key=lambda o: o["prioridad"])
