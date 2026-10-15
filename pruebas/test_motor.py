# pruebas/test_motor.py
# Casos de referencia de las fichas de clase y casos límite del motor.
# Comprueban la SECUENCIA, las FRACCIONES y los AVISOS, no solo que aparezca un método.

import unittest

try:
    from pruebas import _ruta  # noqa: F401
except ImportError:
    import _ruta  # noqa: F401

from datos.retos import TABLA_D, TABLA_G
from logica.planificador import resolver_mezcla

C = ["hierro", "arena", "cloruro_de_sodio", "sulfato_de_cobre_pentahidratado", "agua", "aceite"]
C_METODOS = ["magnetismo", "decantacion", "filtracion", "destilacion", "evaporacion", "recristalizacion"]
C_CANT = {"hierro": 20, "arena": 40, "cloruro_de_sodio": 30, "sulfato_de_cobre_pentahidratado": 25, "agua": 150, "aceite": 50}
G = ["arena", "agua", "aceite", "cloruro_de_sodio", "sulfato_de_cobre", "etanol", "colorante_a", "colorante_b"]
G_CANT = {"arena": 50, "agua": 100, "aceite": 40, "cloruro_de_sodio": 15, "sulfato_de_cobre": 20, "etanol": 30}
G_METODOS = ["sedimentacion", "decantacion", "filtracion", "destilacion", "evaporacion", "recristalizacion", "cromatografia"]


def metodos(r):
    return [p["metodo"] for p in r["pasos"]]


def recuperados(r):
    return {x["principal"]["clave"] for x in r["recuperados"]}


def avisos(r):
    return " ".join(a for p in r["pasos"] for a in p["avisos"])


class TestCasosBasicos(unittest.TestCase):

    def test_filtracion_solido_insoluble(self):
        for solido in ("arena", "carbonato_de_calcio"):
            r = resolver_mezcla(["agua", solido])
            self.assertEqual(metodos(r), ["filtracion"])
            self.assertEqual(recuperados(r), {"agua", solido})

    def test_liquidos_inmiscibles(self):
        r = resolver_mezcla(["agua", "aceite"])
        self.assertEqual(metodos(r), ["decantacion"])
        superior = r["pasos"][0]["productos"][0]
        self.assertEqual(superior["componentes"][0]["clave"], "aceite")

    def test_hierro_y_azufre_magnetismo(self):
        r = resolver_mezcla(["hierro", "azufre"])
        self.assertEqual(metodos(r), ["magnetismo"])
        self.assertTrue(any("FeS" in x["ecuacion"] for x in r["analisis"]["reacciones"]))

    def test_fes_es_sustancia_pura(self):
        r = resolver_mezcla(["sulfuro_de_hierro"])
        self.assertEqual(r["pasos"], [])
        self.assertIn("compuesto", r["analisis"]["nota_sustancia_pura"])

    def test_fes_no_es_magnetico(self):
        r = resolver_mezcla(["sulfuro_de_hierro", "arena"])
        self.assertNotIn("magnetismo", metodos(r))
        self.assertTrue(r["sin_resolver"])

    def test_sal_disuelta_no_se_filtra(self):
        r = resolver_mezcla(["agua", "cloruro_de_sodio"])
        self.assertNotIn("filtracion", metodos(r))
        self.assertEqual(metodos(r), ["destilacion"])  # recupera también el agua

    def test_sal_sin_recuperar_agua_evapora(self):
        r = resolver_mezcla(["agua", "cloruro_de_sodio"], recuperar_disolvente=False)
        self.assertEqual(metodos(r), ["evaporacion"])
        self.assertEqual([p["clave"] for p in r["perdidos"]], ["agua"])

    def test_disolucion_arena_y_sal_secas(self):
        r = resolver_mezcla(["arena", "cloruro_de_sodio"])
        self.assertEqual(metodos(r), ["disolucion", "filtracion", "evaporacion"])
        self.assertEqual(recuperados(r), {"arena", "cloruro_de_sodio"})

    def test_sal_en_etanol_se_filtra(self):
        r = resolver_mezcla(["etanol", "cloruro_de_sodio"])
        self.assertEqual(metodos(r), ["filtracion"])

    def test_etanol_agua_fraccionada_y_azeotropo(self):
        r = resolver_mezcla(["etanol", "agua"])
        self.assertEqual(metodos(r), ["destilacion_fraccionada"])
        self.assertIn("azeótropo", avisos(r))
        etanol = next(x for x in r["recuperados"] if x["principal"]["clave"] == "etanol")
        self.assertTrue(etanol["impurezas"], "el etanol debe salir con restos de agua")

    def test_etanol_agua_solo_simple(self):
        r = resolver_mezcla(["etanol", "agua"], permitidos=["destilacion", "filtracion"])
        self.assertEqual(metodos(r), ["destilacion"])
        destilado = r["pasos"][0]["productos"][0]["componentes"]
        etanol = next(c for c in destilado if c["clave"] == "etanol")
        self.assertEqual(etanol["nota"], "enriquecido")

    def test_alcohol_agua_arcilla(self):
        r = resolver_mezcla(["etanol", "agua", "arcilla"])
        self.assertEqual(metodos(r)[0], "filtracion")
        self.assertIn("arcilla", avisos(r).lower())


class TestCasosLimite(unittest.TestCase):

    def test_miscibilidad_desconocida(self):
        r = resolver_mezcla(["aceite", "etanol"])
        self.assertFalse(r["completo"])
        self.assertIn("miscibilidad", r["sin_resolver"][0]["motivos"][0])

    def test_dos_solidos_insolubles(self):
        r = resolver_mezcla(["arena", "arcilla", "agua"])
        self.assertFalse(r["completo"])
        self.assertEqual({c["clave"] for c in r["sin_resolver"][0]["componentes"]}, {"arena", "arcilla"})

    def test_reaccion_hierro_cobre(self):
        r = resolver_mezcla(["agua", "hierro", "sulfato_de_cobre"])
        self.assertTrue(any(x["activa"] for x in r["analisis"]["reacciones"]))
        self.assertEqual(metodos(r)[0], "magnetismo")

    def test_hierro_antes_de_disolver(self):
        r = resolver_mezcla(["hierro", "arena", "sulfato_de_cobre"])
        self.assertEqual(metodos(r)[0], "magnetismo")
        self.assertLess(metodos(r).index("magnetismo"), metodos(r).index("disolucion"))

    def test_sulfato_de_cobre_se_cristaliza(self):
        r = resolver_mezcla(["agua", "sulfato_de_cobre"])
        self.assertEqual(metodos(r), ["cristalizacion"])
        self.assertIn("sulfato_de_cobre_pentahidratado", recuperados(r))

    def test_metodo_no_permitido_se_explica(self):
        r = resolver_mezcla(["agua", "aceite"], permitidos=["filtracion"])
        self.assertFalse(r["completo"])
        self.assertTrue(any("no está entre los métodos permitidos" in m for m in r["sin_resolver"][0]["motivos"]))

    def test_estado_coherente(self):
        """Cada componente inicial acaba recuperado, perdido, analizado o sin resolver; nada desaparece."""
        for claves in (C, G, ["agua", "arena", "hierro", "aceite"]):
            r = resolver_mezcla(claves)
            finales = set()
            finales |= recuperados(r)
            finales |= {p["clave"] for p in r["perdidos"]}
            finales |= {c["clave"] for x in r["analiticos"] for c in x["componentes"]}
            finales |= {c["clave"] for x in r["sin_resolver"] for c in x["componentes"] if c["rol"] == "principal"}
            finales = {"sulfato_de_cobre" if k == "sulfato_de_cobre_pentahidratado" else k for k in finales}
            iniciales = {"sulfato_de_cobre" if k == "sulfato_de_cobre_pentahidratado" else k for k in claves}
            self.assertEqual(finales, iniciales, claves)


class TestFichas(unittest.TestCase):

    def test_ejemplo_c_secuencia_de_la_ficha(self):
        r = resolver_mezcla(C, permitidos=C_METODOS)
        self.assertEqual(metodos(r), ["magnetismo", "decantacion", "filtracion", "destilacion", "recristalizacion", "evaporacion"])
        self.assertTrue(r["completo"])
        destilacion = r["pasos"][3]
        self.assertEqual(destilacion["productos"][0]["componentes"][0]["clave"], "agua")
        self.assertEqual({c["clave"] for c in destilacion["productos"][1]["componentes"]},
                         {"cloruro_de_sodio", "sulfato_de_cobre_pentahidratado"})

    def test_ejemplo_c_con_cantidades_no_separa_limpio(self):
        r = resolver_mezcla(C, C_CANT, C_METODOS)
        self.assertFalse(r["completo"])
        motivo = " ".join(r["sin_resolver"][0]["motivos"])
        self.assertIn("78,1", motivo)
        self.assertIn("1,88", motivo)

    def test_ejemplo_c_con_tabla_d_tampoco(self):
        r = resolver_mezcla(C, C_CANT, C_METODOS, solubilidades=TABLA_D)
        self.assertFalse(r["completo"])
        self.assertIn("76,9", " ".join(r["sin_resolver"][0]["motivos"]))

    def test_ejemplo_d_cualitativo_con_condicion(self):
        r = resolver_mezcla(["arena", "agua", "aceite", "cloruro_de_sodio", "sulfato_de_cobre"],
                            permitidos=["decantacion", "filtracion", "destilacion", "evaporacion", "recristalizacion"],
                            solubilidades=TABLA_D)
        self.assertEqual(metodos(r), ["decantacion", "filtracion", "destilacion", "recristalizacion", "evaporacion"])
        recrist = r["pasos"][3]
        self.assertAlmostEqual(recrist["detalle"]["condicion"], 0.56, places=2)

    def test_ejemplo_g_cuantitativo(self):
        r = resolver_mezcla(G, G_CANT, G_METODOS, solubilidades=TABLA_G)
        self.assertTrue(r["completo"])
        self.assertIn("cromatografia", metodos(r))
        recrist = next(p for p in r["pasos"] if p["metodo"] == "recristalizacion")
        self.assertEqual(recrist["detalle"]["ventana"][1], 96.6)
        self.assertAlmostEqual(recrist["detalle"]["ventana"][0], 48.1, delta=0.15)
        self.assertEqual(recrist["detalle"]["rendimiento"], 57)
        self.assertEqual({c["clave"] for x in r["analiticos"] for c in x["componentes"]}, {"colorante_a", "colorante_b"})
        # El etanol sale enriquecido (solo se permite la destilación simple).
        etanol = next(x for x in r["recuperados"] if x["principal"]["clave"] == "etanol")
        self.assertEqual(etanol["principal"]["nota"], "enriquecido")

    def test_ejemplo_g_sin_cromatografia_queda_parcial(self):
        permitidos = [m for m in G_METODOS if m != "cromatografia"]
        r = resolver_mezcla(G, G_CANT, permitidos, solubilidades=TABLA_G)
        self.assertFalse(r["completo"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
