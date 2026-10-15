# pruebas/test_retos.py
# Cada reto del banco debe tener una solución defendible con sus datos.

import unittest

try:
    from pruebas import _ruta  # noqa: F401
except ImportError:
    import _ruta  # noqa: F401

from datos.retos import NIVELES, RETOS
from datos.sustancias import SUSTANCIAS
from logica.retos import corregir_pregunta, solucion


class TestRetos(unittest.TestCase):

    def test_datos_validos(self):
        ids = [r["id"] for r in RETOS]
        self.assertEqual(len(ids), len(set(ids)))
        for reto in RETOS:
            self.assertIn(reto["nivel"], NIVELES)
            for clave in reto["sustancias"]:
                self.assertIn(clave, SUSTANCIAS, reto["id"])
            for p in reto.get("preguntas", []):
                self.assertLess(p["correcta"], len(p["opciones"]))

    def test_cada_nivel_tiene_retos(self):
        for nivel in NIVELES:
            self.assertGreaterEqual(sum(r["nivel"] == nivel for r in RETOS), 3, nivel)

    def test_todos_resolubles(self):
        for reto in RETOS:
            r = solucion(reto)
            if reto.get("parcial_esperado"):
                self.assertFalse(r["completo"], reto["id"])
            else:
                self.assertTrue(r["completo"], (reto["id"], r["sin_resolver"]))
                for p in r["pasos"]:
                    self.assertTrue(p["metodo"] in reto["permitidos"] or p["auxiliar"], (reto["id"], p["metodo"]))

    def test_reto_sal_no_filtra(self):
        reto = next(r for r in RETOS if r["id"] == "b5")
        self.assertNotIn("filtracion", [p["metodo"] for p in solucion(reto)["pasos"]])

    def test_correccion_de_preguntas(self):
        reto = next(r for r in RETOS if r["id"] == "d1")
        self.assertTrue(corregir_pregunta(reto, 0, 0)["correcta"])
        self.assertFalse(corregir_pregunta(reto, 0, 1)["correcta"])
        self.assertIsNone(corregir_pregunta(reto, 5, 0))


if __name__ == "__main__":
    unittest.main(verbosity=2)
