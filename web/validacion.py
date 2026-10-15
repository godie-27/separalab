# web/validacion.py
# Validación de los datos que llegan desde el navegador. Nunca se confía en
# ellos: tipos, tamaños y valores se comprueban antes de llegar al motor.

from datos.metodos import METODOS, METODOS_SEPARACION
from datos.retos import obtener_reto
from datos.sustancias import SUSTANCIAS

MAX_SUSTANCIAS = 10
MAX_HISTORIAL = 40


class ErrorEntrada(ValueError):
    """Error de datos de entrada; el mensaje se muestra al usuario."""


def cuerpo(request):
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        raise ErrorEntrada("La petición debe ser un objeto JSON.")
    return datos


def sustancias(valor, minimo=1):
    if not isinstance(valor, list):
        raise ErrorEntrada("La selección de sustancias no es válida.")
    if len(valor) > MAX_SUSTANCIAS:
        raise ErrorEntrada(f"Selecciona como máximo {MAX_SUSTANCIAS} sustancias.")
    claves = []
    for v in valor:
        if not isinstance(v, str) or v not in SUSTANCIAS:
            raise ErrorEntrada("Hay una sustancia que no está en el catálogo.")
        if v not in claves:
            claves.append(v)
    if len(claves) < minimo:
        raise ErrorEntrada("Selecciona al menos dos sustancias para formar una mezcla." if minimo >= 2
                           else "Selecciona al menos una sustancia.")
    return claves


def cantidades(valor, claves):
    if valor in (None, {}):
        return None
    if not isinstance(valor, dict):
        raise ErrorEntrada("Las cantidades no son válidas.")
    salida = {}
    for clave, x in valor.items():
        if clave not in claves:
            continue
        if x in (None, ""):
            continue
        if isinstance(x, bool):
            raise ErrorEntrada("Las cantidades deben ser números.")
        try:
            numero = float(str(x).replace(",", "."))
        except ValueError as e:
            raise ErrorEntrada(f"La cantidad de {SUSTANCIAS[clave]['nombre'].lower()} debe ser un número.") from e
        if not 0 < numero <= 10000:
            raise ErrorEntrada(f"La cantidad de {SUSTANCIAS[clave]['nombre'].lower()} debe estar entre 0 y 10 000.")
        salida[clave] = numero
    if salida and len(salida) < len(claves):
        faltan = [SUSTANCIAS[c]["nombre"].lower() for c in claves if c not in salida and not SUSTANCIAS[c].get("categoria")]
        if faltan:
            raise ErrorEntrada("Para usar cantidades, indícalas para todos los componentes (faltan: " + ", ".join(faltan) + ").")
    return salida or None


def permitidos(valor):
    if valor is None:
        return None
    if not isinstance(valor, list) or not all(isinstance(m, str) and m in METODOS_SEPARACION for m in valor):
        raise ErrorEntrada("La lista de métodos permitidos no es válida.")
    if not valor:
        raise ErrorEntrada("Permite al menos un método de separación.")
    return valor


def metodo(valor):
    if not isinstance(valor, str) or valor not in METODOS:
        raise ErrorEntrada("Método desconocido.")
    return valor


def historial(valor):
    if valor is None:
        return []
    if not isinstance(valor, list) or len(valor) > MAX_HISTORIAL:
        raise ErrorEntrada("El historial de la práctica no es válido.")
    salida = []
    for a in valor:
        if not isinstance(a, dict) or not isinstance(a.get("fraccion"), str) or len(a["fraccion"]) > 60:
            raise ErrorEntrada("El historial de la práctica no es válido.")
        salida.append({"fraccion": a["fraccion"], "metodo": metodo(a.get("metodo"))})
    return salida


def entero(valor, minimo, maximo, nombre="valor"):
    if isinstance(valor, bool) or not isinstance(valor, int) or not minimo <= valor <= maximo:
        raise ErrorEntrada(f"El {nombre} no es válido.")
    return valor


def mezcla_practica(datos):
    """Devuelve los parámetros de una práctica: libre o a partir de un reto."""
    m = datos.get("mezcla")
    if not isinstance(m, dict):
        raise ErrorEntrada("Falta la mezcla de la práctica.")
    if m.get("reto") is not None:
        reto = obtener_reto(m.get("reto")) if isinstance(m.get("reto"), str) else None
        if reto is None:
            raise ErrorEntrada("Ese reto no existe.")
        return {
            "sustancias": reto["sustancias"], "cantidades": reto.get("cantidades"),
            "usar_cantidades": reto.get("usar_cantidades", False), "permitidos": reto["permitidos"],
            "solubilidades": reto.get("solubilidades", ()), "recuperar_disolvente": reto.get("recuperar_disolvente", True),
        }
    claves = sustancias(m.get("sustancias"), minimo=2)
    return {
        "sustancias": claves, "cantidades": cantidades(m.get("cantidades"), claves), "usar_cantidades": True,
        "permitidos": permitidos(m.get("permitidos")), "solubilidades": (),
        "recuperar_disolvente": bool(m.get("recuperar_disolvente", True)),
    }
