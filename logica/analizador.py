# logica/analizador.py
# Fachada compatible con la versión anterior del proyecto. La lógica real está
# en logica/planificador.py y logica/reglas.py.

from datos.metodos import obtener_metodo
from logica.reglas import evaluar_metodos


def describir_mezcla(sustancias):
    """Nombres de las sustancias de la mezcla, separados por comas."""
    if not sustancias:
        return "No quedan sustancias en la mezcla."
    return ", ".join(s["nombre"] for s in sustancias)


def analizar_mezcla(sustancias):
    """Métodos aplicables a la mezcla, ordenados del más al menos adecuado."""
    procedimiento = []
    for resultado in evaluar_metodos(sustancias):
        metodo = obtener_metodo(resultado["metodo"])
        procedimiento.append({
            "metodo": resultado["metodo"],
            "nombre": metodo["nombre"],
            "propiedad": metodo["propiedad"],
            "descripcion": metodo["descripcion"],
            "resultado": metodo.get("descripcion", ""),
            "razon": resultado["razon"],
            "prioridad": resultado["prioridad"],
        })
    return procedimiento
