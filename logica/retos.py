# logica/retos.py
# Selección y preparación de retos. Los retos solo salen de datos/retos.py
# (casos validados), nunca de combinaciones al azar.

import random

from datos.retos import NIVELES, RETOS, obtener_reto
from datos.sustancias import SUSTANCIAS
from logica.planificador import resolver_mezcla


def resumen(reto):
    """Datos que ve el estudiante (sin la solución)."""
    tabla = [{"sal": SUSTANCIAS[k]["nombre"], "s20": s20, "s80": s80, "unidad": u, "fuente": f}
             for (k, s20, s80, u, f) in reto.get("solubilidades", ())]
    return {
        "id": reto["id"], "nivel": reto["nivel"], "nivel_nombre": NIVELES[reto["nivel"]], "titulo": reto["titulo"],
        "enunciado": reto["enunciado"], "sustancias": reto["sustancias"], "cantidades": reto.get("cantidades"),
        "usar_cantidades": reto.get("usar_cantidades", False), "permitidos": reto["permitidos"],
        "recuperar_disolvente": reto.get("recuperar_disolvente", True),
        "tabla_solubilidad": tabla, "num_pistas": len(reto.get("pistas", [])),
        "preguntas": [{"pregunta": p["pregunta"], "opciones": p["opciones"]} for p in reto.get("preguntas", [])],
        "fuente": reto.get("fuente", ""),
    }


def aleatorio(nivel=None, excluir=None):
    candidatos = [r for r in RETOS if (nivel is None or r["nivel"] == nivel) and r["id"] != excluir]
    if not candidatos:
        candidatos = [r for r in RETOS if nivel is None or r["nivel"] == nivel]
    return random.choice(candidatos) if candidatos else None


def solucion(reto):
    return resolver_mezcla(
        reto["sustancias"],
        reto.get("cantidades") if reto.get("usar_cantidades") else None,
        reto["permitidos"],
        reto.get("recuperar_disolvente", True),
        reto.get("solubilidades", ()),
    )


def pista(reto, nivel):
    pistas = reto.get("pistas", [])
    if not pistas:
        return None
    return pistas[min(max(nivel, 1), len(pistas)) - 1]


def corregir_pregunta(reto, indice, opcion):
    preguntas = reto.get("preguntas", [])
    if not 0 <= indice < len(preguntas):
        return None
    p = preguntas[indice]
    return {"correcta": opcion == p["correcta"], "respuesta": p["opciones"][p["correcta"]], "explicacion": p["explicacion"]}


__all__ = ["RETOS", "NIVELES", "obtener_reto", "resumen", "aleatorio", "solucion", "pista", "corregir_pregunta"]
