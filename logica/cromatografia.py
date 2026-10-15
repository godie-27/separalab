# logica/cromatografia.py
# Cálculo y validación del factor de retención (Rf).
#   Rf = distancia recorrida por la mancha / distancia recorrida por el frente
# Ambas distancias se miden desde la MISMA línea de origen. Rf es adimensional
# y, en un cromatograma bien medido, está entre 0 y 1.


class ErrorRf(ValueError):
    pass


def _numero(valor, nombre):
    if isinstance(valor, bool):
        raise ErrorRf(f"La {nombre} debe ser un número.")
    try:
        x = float(str(valor).replace(",", "."))
    except (TypeError, ValueError):
        raise ErrorRf(f"La {nombre} debe ser un número (por ejemplo, 4,2).")
    if x != x or x in (float("inf"), float("-inf")):
        raise ErrorRf(f"La {nombre} debe ser un número finito.")
    return x


def _f(x, dec=2):
    return f"{x:.{dec}f}".replace(".", ",")


def calcular_rf(d_mancha, d_frente):
    """Devuelve el Rf con los pasos del cálculo. Lanza ErrorRf si los datos no son válidos."""
    dm = _numero(d_mancha, "distancia de la mancha")
    df = _numero(d_frente, "distancia del frente del disolvente")
    if df < 0 or dm < 0:
        raise ErrorRf("Las distancias no pueden ser negativas: se miden hacia arriba desde la línea de origen.")
    if df == 0:
        raise ErrorRf("El frente del disolvente no se ha desplazado (distancia 0): no se puede dividir entre cero ni calcular el Rf.")
    if dm > df:
        raise ErrorRf("La mancha no puede haber avanzado más que el frente del disolvente: revisa las medidas "
                      "(ambas se miden desde la línea de origen).")
    rf = dm / df
    if rf == 0:
        interpretacion = ("La mancha no se movió del origen en este ensayo (Rf = 0): interacciona muy fuertemente con la fase "
                          "estacionaria o no es soluble en la fase móvil. No significa que su Rf sea 0 en otras condiciones.")
    elif rf == 1:
        interpretacion = "La mancha avanzó con el frente (Rf = 1): casi no interacciona con la fase estacionaria en estas condiciones."
    elif rf < 0.35:
        interpretacion = "Avanza poco: tiene más afinidad por la fase estacionaria que por la fase móvil."
    elif rf > 0.65:
        interpretacion = "Avanza mucho: tiene más afinidad por la fase móvil que por la fase estacionaria."
    else:
        interpretacion = "Afinidad intermedia por ambas fases."
    return {
        "rf": round(rf, 2),
        "rf_exacto": rf,
        "pasos": [
            "Rf = distancia recorrida por la mancha / distancia recorrida por el frente del disolvente",
            f"Rf = {_f(dm, 1)} cm / {_f(df, 1)} cm",
            f"Rf = {_f(rf, 3)} ≈ {_f(rf)}",
        ],
        "interpretacion": interpretacion,
        "nota": "El Rf no tiene unidades (cm/cm) y depende de las condiciones: papel o placa, disolvente y temperatura.",
    }


def calcular_varias(manchas, d_frente):
    """manchas: [{"nombre", "distancia"}]. Devuelve los Rf y la mancha más/menos retenida."""
    if not isinstance(manchas, list) or not manchas:
        raise ErrorRf("Indica al menos una mancha.")
    if len(manchas) > 12:
        raise ErrorRf("Como máximo 12 manchas.")
    resultados = []
    for i, m in enumerate(manchas, start=1):
        if not isinstance(m, dict):
            raise ErrorRf("Formato de mancha no válido.")
        nombre = str(m.get("nombre") or f"Mancha {i}")[:40]
        r = calcular_rf(m.get("distancia"), d_frente)
        resultados.append({"nombre": nombre, **r})
    mas = max(resultados, key=lambda r: r["rf_exacto"])
    menos = min(resultados, key=lambda r: r["rf_exacto"])
    return {"manchas": resultados, "mas_afin_movil": mas["nombre"], "mas_afin_estacionaria": menos["nombre"]}


def comprobar_respuesta(valor_alumno, rf_correcto, tolerancia=0.02):
    """¿El Rf que calculó el estudiante es correcto (con redondeo)?"""
    v = _numero(valor_alumno, "respuesta")
    return abs(v - rf_correcto) <= tolerancia + 1e-9
