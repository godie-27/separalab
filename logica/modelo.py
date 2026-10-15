# logica/modelo.py
# Representación de una mezcla como FRACCIÓN: el contenido de un recipiente.
#
# Una fracción es una tupla ordenada de componentes (Comp). Cada componente
# tiene un rol:
#   - "principal": componente que hay que separar y recuperar.
#   - "impureza":  restos que acompañan a un principal (no cuentan como
#                  componente por separar, pero se declaran).
#   - "auxiliar":  añadido durante el proceso (p. ej., agua para disolver).
# El estado físico de cada componente dentro de la fracción (partículas
# sólidas, líquido, disuelto) NO se guarda: se deduce con estructura().

from typing import NamedTuple, Optional

from datos.sustancias import SUSTANCIAS, miscibilidad, solubilidad


class Comp(NamedTuple):
    clave: str
    rol: str = "principal"
    masa: Optional[float] = None   # gramos (None = cantidad no especificada)
    nota: str = ""                 # "enriquecido", "deshidratado", "analitica", ...


def fraccion(comps):
    """Normaliza una colección de Comp en una fracción (tupla ordenada).

    Une componentes repetidos con el mismo rol sumando sus masas.
    """
    unidos = {}
    for c in comps:
        clave = (c.clave, c.rol)
        if clave in unidos:
            previo = unidos[clave]
            masa = None if previo.masa is None or c.masa is None else previo.masa + c.masa
            nota = previo.nota or c.nota
            unidos[clave] = Comp(c.clave, c.rol, masa, nota)
        else:
            unidos[clave] = c
    # Un principal anula una impureza de la misma sustancia.
    principales = {k for (k, r) in unidos if r == "principal"}
    resultado = [c for (k, r), c in unidos.items() if not (r == "impureza" and k in principales)]
    return tuple(sorted(resultado, key=lambda c: (c.clave, c.rol)))


def _min(texto):
    return texto[:1].lower() + texto[1:] if texto else texto


def principales(fr):
    return [c for c in fr if c.rol == "principal"]


def datos(c):
    return SUSTANCIAS[c.clave]


def pendiente(fr):
    """True si la fracción aún necesita operaciones.

    Hace falta seguir si hay dos o más componentes principales, o si el único
    principal es un sólido que sigue disuelto o mojado en un líquido no principal
    (por ejemplo, la sal en el agua añadida para disolverla).
    """
    princ = principales(fr)
    if len(princ) >= 2:
        return True
    if len(princ) == 1 and not es_liquido(princ[0]):
        return any(es_liquido(c) for c in fr)
    return False


def es_liquido(c):
    return datos(c)["estado"] == "liquido"


def es_colorante(c):
    return datos(c).get("categoria") == "colorante"


def clave_base(clave):
    """Para un hidrato, la sal anhidra; para lo demás, la misma clave."""
    return SUSTANCIAS[clave].get("anhidro", clave)


class Estructura(NamedTuple):
    fases: list          # [{"liquidos": [Comp], "solutos": [Comp], "densidad": float|None}]
    solidos: list        # [Comp] partículas sin disolver
    incertidumbres: list # [str]
    supuestos: list      # [str]


def _agrupar_liquidos(liquidos):
    """Agrupa líquidos en fases según su miscibilidad (unión-búsqueda)."""
    grupos = [[c] for c in liquidos]
    cambiado = True
    while cambiado:
        cambiado = False
        for i in range(len(grupos)):
            for j in range(i + 1, len(grupos)):
                if any(miscibilidad(a.clave, b.clave) is True for a in grupos[i] for b in grupos[j]):
                    grupos[i] = grupos[i] + grupos[j]
                    del grupos[j]
                    cambiado = True
                    break
            if cambiado:
                break
    return grupos


def _densidad_fase(liquidos):
    dens = [(c, datos(c).get("densidad")) for c in liquidos]
    if any(d is None for _, d in dens):
        return None
    if len(dens) == 1:
        return dens[0][1]
    if all(c.masa is not None for c, _ in dens):
        masa = sum(c.masa for c, _ in dens)
        volumen = sum(c.masa / d for c, d in dens)
        return masa / volumen
    # Sin cantidades: se toma el disolvente principal (agua si la hay).
    for c, d in dens:
        if c.clave == "agua":
            return d
    return dens[0][1]


def estructura(fr):
    """Deduce las fases de una fracción: fases líquidas, solutos y sólidos."""
    liquidos = [c for c in fr if es_liquido(c)]
    solidos_todos = [c for c in fr if not es_liquido(c)]
    incertidumbres, supuestos = [], []

    grupos = _agrupar_liquidos(liquidos)
    # Fases sin ningún par inmiscible conocido entre ellas: no se sabe si se mezclan.
    for i in range(len(grupos)):
        for j in range(i + 1, len(grupos)):
            pares = [(a, b) for a in grupos[i] for b in grupos[j]]
            if not any(miscibilidad(a.clave, b.clave) is False for a, b in pares):
                a, b = pares[0]
                incertidumbres.append(
                    f"No hay datos de miscibilidad entre {_min(datos(a)['nombre'])} y "
                    f"{_min(datos(b)['nombre'])}: no se puede saber si forman una o dos fases."
                )
            else:
                desconocidos = [(a, b) for a, b in pares if miscibilidad(a.clave, b.clave) is None]
                for a, b in desconocidos:
                    supuestos.append(
                        f"Se supone que {_min(datos(a)['nombre'])} permanece en su fase y no pasa a la de "
                        f"{_min(datos(b)['nombre'])} (no hay datos de reparto)."
                    )

    fases = [{"liquidos": g, "solutos": [], "densidad": _densidad_fase(g)} for g in grupos]
    solidos = []
    for c in solidos_todos:
        destino = None
        if fases:
            # Preferencia: la fase que contiene agua.
            orden = sorted(range(len(fases)), key=lambda i: 0 if any(l.clave == "agua" for l in fases[i]["liquidos"]) else 1)
            for i in orden:
                if any(solubilidad(c.clave, l.clave) == "soluble" for l in fases[i]["liquidos"]):
                    destino = i
                    break
            if destino is None:
                for fase in fases:
                    for l in fase["liquidos"]:
                        if solubilidad(c.clave, l.clave) is None and SUSTANCIAS[c.clave]["estado"] == "solido":
                            supuestos.append(
                                f"No hay datos de solubilidad de {_min(datos(c)['nombre'])} en "
                                f"{_min(datos(l)['nombre'])}: se supone que no se disuelve."
                            )
        if destino is None:
            solidos.append(c)
        else:
            fases[destino]["solutos"].append(c)
            sup = datos(c).get("supuesto")
            if sup and sup not in supuestos:
                supuestos.append(sup)

    # Con etanol en la fase acuosa y aceite presente, la densidad relativa podría cambiar.
    if len(fases) >= 2:
        for f in fases:
            claves = {l.clave for l in f["liquidos"]}
            if {"agua", "etanol"} <= claves and any(l.masa is None for l in f["liquidos"]):
                supuestos.append(
                    "Se supone que la fase agua-etanol es más densa que el aceite; con mucho etanol podría no serlo."
                )
    return Estructura(fases, solidos, incertidumbres, supuestos)


def describir(fr):
    """Texto breve con los componentes de una fracción."""
    partes = []
    for c in fr:
        nombre = datos(c)["nombre"]
        if c.rol == "impureza":
            nombre = f"restos de {_min(nombre)}"
        elif c.rol == "auxiliar":
            nombre = f"{_min(nombre)} añadida" if c.clave == "agua" else f"{nombre} (auxiliar)"
        partes.append(nombre)
    return ", ".join(partes)


def tipo_mezcla(fr):
    """'homogénea', 'heterogénea' o 'sustancia pura', según las fases presentes."""
    if len(principales(fr)) <= 1:
        return "sustancia pura"
    est = estructura(fr)
    if est.incertidumbres:
        return "no determinada (faltan datos de miscibilidad)"
    n_fases = len(est.fases) + len(est.solidos)
    return "homogénea" if n_fases == 1 else "heterogénea"
