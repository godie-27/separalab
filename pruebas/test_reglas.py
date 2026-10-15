# pruebas/test_reglas.py
# Pruebas originales del proyecto, adaptadas al nuevo motor (la función
# evaluar_metodos se conserva por compatibilidad).

import unittest

try:
    from pruebas import _ruta  # noqa: F401
except ImportError:
    import _ruta  # noqa: F401

from datos.sustancias import SUSTANCIAS
from logica.reglas import evaluar_metodos


def crear_mezcla(*claves):
    """Crea una mezcla de prueba sin modificar el catálogo original."""
    return [dict(SUSTANCIAS[c], clave=c) for c in claves]


def obtener_metodos(mezcla):
    return [opcion["metodo"] for opcion in evaluar_metodos(mezcla)]


class TestReglasSeparacion(unittest.TestCase):

    def test_hierro_y_arena_recomienda_magnetismo(self):
        metodos = obtener_metodos(crear_mezcla("hierro", "arena"))
        self.assertEqual(metodos[0], "magnetismo")

    def test_agua_y_arena_recomienda_filtracion(self):
        metodos = obtener_metodos(crear_mezcla("agua", "arena"))
        self.assertIn("filtracion", metodos)
        self.assertNotIn("magnetismo", metodos)

    def test_agua_y_etanol_recomienda_destilacion(self):
        metodos = obtener_metodos(crear_mezcla("agua", "etanol"))
        self.assertIn("destilacion", metodos)
        self.assertNotIn("decantacion", metodos)

    def test_agua_y_aceite_recomienda_decantacion(self):
        self.assertEqual(obtener_metodos(crear_mezcla("agua", "aceite"))[0], "decantacion")

    def test_agua_aceite_y_arena(self):
        metodos = obtener_metodos(crear_mezcla("agua", "aceite", "arena"))
        self.assertIn("decantacion", metodos)
        self.assertIn("filtracion", metodos)

    def test_sal_disuelta_no_se_filtra(self):
        self.assertNotIn("filtracion", obtener_metodos(crear_mezcla("agua", "cloruro_de_sodio")))

    def test_mezcla_vacia_no_produce_metodos(self):
        self.assertEqual(evaluar_metodos([]), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
