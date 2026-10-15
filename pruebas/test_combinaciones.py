# pruebas/test_combinaciones.py
# Recorre todas las combinaciones de las 8 sustancias del proyecto original
# (247) y comprueba que el motor nunca da por separado lo que sigue mezclado.

import itertools
import unittest

try:
    from pruebas import _ruta  # noqa: F401
except ImportError:
    import _ruta  # noqa: F401

from logica.planificador import resolver_mezcla

ORIGINALES = ["agua", "aceite", "etanol", "arena", "hierro", "cloruro_de_sodio", "sulfato_de_cobre", "arcilla"]


class TestCombinaciones(unittest.TestCase):

    def test_ninguna_separacion_falsa(self):
        total = 0
        for r_ in range(2, len(ORIGINALES) + 1):
            for combo in itertools.combinations(ORIGINALES, r_):
                total += 1
                r = resolver_mezcla(list(combo))
                for x in r["recuperados"]:
                    principales = [c for c in x["componentes"] if c["rol"] == "principal"]
                    self.assertEqual(len(principales), 1, (combo, x))
                    self.assertFalse(principales[0]["estado"] == "solido"
                                     and any(c["estado"] == "liquido" for c in x["componentes"]),
                                     f"{combo}: sólido 'recuperado' aún disuelto: {x}")
                for p in r["pasos"]:
                    self.assertTrue(p["productos"], combo)
                self.assertEqual(r["completo"], not r["sin_resolver"], combo)
        self.assertEqual(total, 247)

    def test_recuperacion_de_sales_juntas_no_es_completa(self):
        r = resolver_mezcla(["agua", "cloruro_de_sodio", "sulfato_de_cobre"], permitidos=["destilacion", "evaporacion", "filtracion"])
        self.assertFalse(r["completo"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
