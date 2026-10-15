# datos/reacciones.py
# Interacciones químicas entre componentes. Una separación física no puede
# deshacer una reacción: el motor las avisa y las declara como supuesto.

REACCIONES = [
    {
        "reactivos": [{"hierro"}, {"sulfato_de_cobre", "sulfato_de_cobre_pentahidratado"}],
        "condicion": "agua",
        "ecuacion": "Fe(s) + Cu²⁺(aq) → Fe²⁺(aq) + Cu(s)",
        "explicacion": (
            "El hierro desplaza al cobre de su disolución: las limaduras se recubren de cobre rojizo y parte del "
            "hierro se disuelve. Es un cambio químico. El modelo, como los enunciados escolares, supone que el "
            "hierro se retira antes de que reaccione apreciablemente; por eso conviene separarlo primero."
        ),
        "consejo": "Retirar el hierro con el imán antes de añadir agua o en cuanto la mezcla tenga agua.",
    },
    {
        "reactivos": [{"hierro"}, {"azufre"}],
        "condicion": "calor",
        "ecuacion": "Fe(s) + S(s) → FeS(s)  (al calentar)",
        "explicacion": (
            "Al calentarlos juntos forman sulfuro de hierro(II), un compuesto con propiedades nuevas: ya no es "
            "magnético ni huele a azufre, y no se puede separar con un imán."
        ),
        "consejo": "Separar con el imán sin calentar la mezcla.",
    },
]


def reacciones_posibles(claves, hay_agua):
    """Devuelve las reacciones cuyos reactivos están presentes.

    Cada resultado incluye 'activa': True si la condición se cumple ya (hay agua),
    o False si solo ocurriría al cambiar las condiciones (añadir agua, calentar).
    """
    presentes = set(claves)
    encontradas = []
    for reaccion in REACCIONES:
        if all(presentes & grupo for grupo in reaccion["reactivos"]):
            activa = reaccion["condicion"] == "agua" and hay_agua
            encontradas.append({**reaccion, "activa": activa})
    return encontradas
