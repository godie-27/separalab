# pruebas/test_cromatografia.py
# Cálculo del Rf con los ejercicios de las fichas y rechazo de datos inválidos.

import unittest

try:
    from pruebas import _ruta  # noqa: F401
except ImportError:
    import _ruta  # noqa: F401

from datos.cromatografia import EJERCICIOS, SIMULACIONES
from logica.cromatografia import ErrorRf, calcular_rf, calcular_varias, comprobar_respuesta

ESPERADOS = {
    "aplicacion1": [0.67, 0.50, 0.17, 0.00],
    "aplicacion2": [0.89, 0.44],
    "lapicero": [0.25, 0.42, 0.67],
    "ficha_g": [0.35, 0.70],
    "variante_g": [0.30, 0.70],
}


class TestRf(unittest.TestCase):

    def test_valores_de_las_fichas(self):
        for e in EJERCICIOS:
            obtenidos = [calcular_rf(m["distancia"], e["frente"])["rf"] for m in e["manchas"]]
            self.assertEqual(obtenidos, ESPERADOS[e["id"]], e["id"])

    def test_pasos_y_coma_decimal(self):
        r = calcular_rf("8,0", "9,0")
        self.assertEqual(r["rf"], 0.89)
        self.assertIn("8,0 cm / 9,0 cm", r["pasos"][1])

    def test_rf_cero_se_interpreta(self):
        self.assertIn("No significa", calcular_rf(0, 12)["interpretacion"])

    def test_frente_cero(self):
        with self.assertRaises(ErrorRf):
            calcular_rf(2, 0)

    def test_mancha_mas_alla_del_frente(self):
        with self.assertRaises(ErrorRf):
            calcular_rf(13, 12)

    def test_negativos_y_no_numericos(self):
        for a, b in ((-1, 5), (1, -5), ("abc", 5), (None, 5), (True, 5), (float("nan"), 5), ("inf", 5)):
            with self.assertRaises(ErrorRf):
                calcular_rf(a, b)

    def test_varias_manchas(self):
        r = calcular_varias([{"nombre": "A", "distancia": 4.2}, {"nombre": "B", "distancia": 8.4}], 12.0)
        self.assertEqual(r["mas_afin_estacionaria"], "A")
        self.assertEqual(r["mas_afin_movil"], "B")
        with self.assertRaises(ErrorRf):
            calcular_varias([], 12)

    def test_comprobar_respuesta_alumno(self):
        self.assertTrue(comprobar_respuesta("0,35", 0.35))
        self.assertTrue(comprobar_respuesta(0.36, 0.35))
        self.assertFalse(comprobar_respuesta(0.5, 0.35))

    def test_simulaciones_en_rango(self):
        for s in SIMULACIONES:
            for m in s["manchas"]:
                self.assertTrue(0 <= m["rf"] <= 1, s["id"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
