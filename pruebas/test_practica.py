# pruebas/test_practica.py
# El modo práctica acepta todas las secuencias válidas y explica los errores.

import unittest

try:
    from pruebas import _ruta  # noqa: F401
except ImportError:
    import _ruta  # noqa: F401

from logica import practica


class TestPractica(unittest.TestCase):

    def preparar(self, claves, permitidos=None):
        return practica.preparar(claves, None, permitidos)

    def test_dos_primeros_pasos_validos(self):
        fr, ctx = self.preparar(["agua", "arena", "hierro"])
        a = practica.evaluar(fr, ctx, [], "1", "magnetismo")
        b = practica.evaluar(fr, ctx, [], "1", "filtracion")
        self.assertEqual(a["estado"], "optima")
        self.assertIn(b["estado"], ("optima", "valida"))

    def test_filtrar_disolucion_no_aplicable(self):
        fr, ctx = self.preparar(["agua", "cloruro_de_sodio"])
        r = practica.evaluar(fr, ctx, [], "1", "filtracion")
        self.assertEqual(r["estado"], "no_aplicable")
        self.assertIn("atraviesa el papel", r["mensaje"])
        self.assertFalse(r["aceptada"])

    def test_evaporar_pierde_agua_desaconsejada(self):
        fr, ctx = self.preparar(["agua", "cloruro_de_sodio"])
        r = practica.evaluar(fr, ctx, [], "1", "evaporacion")
        self.assertEqual(r["estado"], "desaconsejada")
        self.assertIn("destilación", r["mensaje"])

    def test_filtrar_con_aceite_valida_pero_peor(self):
        fr, ctx = self.preparar(["agua", "aceite", "arena"])
        self.assertEqual(practica.evaluar(fr, ctx, [], "1", "filtracion")["estado"], "valida")

    def test_historial_y_estado(self):
        fr, ctx = self.preparar(["agua", "aceite", "arena"])
        h = [{"fraccion": "1", "metodo": "decantacion"}]
        e = practica.estado(fr, ctx, h)
        self.assertEqual([p["id"] for p in e["pendientes"]], ["1.2"])
        h.append({"fraccion": "1.2", "metodo": "filtracion"})
        e = practica.estado(fr, ctx, h)
        self.assertTrue(e["completo"])
        self.assertEqual(len(e["recuperados"]), 3)

    def test_historial_invalido(self):
        fr, ctx = self.preparar(["agua", "cloruro_de_sodio"])
        with self.assertRaises(practica.ErrorPractica):
            practica.estado(fr, ctx, [{"fraccion": "1", "metodo": "filtracion"}])
        with self.assertRaises(practica.ErrorPractica):
            practica.estado(fr, ctx, [{"fraccion": "9", "metodo": "destilacion"}])

    def test_prediccion(self):
        fr, ctx = self.preparar(["agua", "arena"])
        r = practica.evaluar(fr, ctx, [], "1", "filtracion", prediccion=["arena"])
        self.assertFalse(r["prediccion"]["correcta"])
        self.assertEqual(r["prediccion"]["faltan"], ["agua"])

    def test_pistas_progresivas(self):
        fr, ctx = self.preparar(["agua", "aceite"])
        textos = [practica.pista(fr, ctx, [], "1", n)["texto"] for n in (1, 2, 3)]
        self.assertNotIn("Decantación", textos[0])
        self.assertIn("Decantación", textos[2])

    def test_materiales_y_procedimiento(self):
        opciones = {o["clave"] for o in practica.opciones_materiales("filtracion", semilla=1)}
        self.assertTrue({"embudo", "papel_filtro"} <= opciones)
        self.assertTrue(practica.corregir_materiales("magnetismo", ["iman", "vaso_precipitados", "espatula", "vidrio_reloj"])["correcta"])
        r = practica.corregir_materiales("magnetismo", ["iman", "bureta"])
        self.assertEqual([m["clave"] for m in r["sobran"]], ["bureta"])
        self.assertTrue(practica.corregir_procedimiento("decantacion", [0, 1, 2, 3, 4])["correcta"])
        self.assertFalse(practica.corregir_procedimiento("decantacion", [1, 0, 2, 3, 4])["correcta"])
        with self.assertRaises(practica.ErrorPractica):
            practica.corregir_procedimiento("decantacion", [0, 0, 1])


if __name__ == "__main__":
    unittest.main(verbosity=2)


class TestRetosEnPractica(unittest.TestCase):
    """Cada reto se puede terminar en el modo práctica eligiendo siempre una opción óptima."""

    def test_todos_los_retos_se_completan(self):
        from datos.retos import RETOS
        for reto in RETOS:
            fr, ctx = practica.preparar(reto["sustancias"], reto.get("cantidades"), reto["permitidos"],
                                        reto.get("solubilidades", ()), reto.get("usar_cantidades", False),
                                        reto.get("recuperar_disolvente", True))
            historial = []
            for _ in range(20):
                e = practica.estado(fr, ctx, historial)
                if e["completo"] or e["terminado"]:
                    break
                fraccion = next(p for p in e["pendientes"] if not p["sin_salida"])
                elegido = None
                for m in e["metodos"]:
                    if practica.evaluar(fr, ctx, historial, fraccion["id"], m["clave"])["estado"] == "optima":
                        elegido = m["clave"]
                        break
                self.assertIsNotNone(elegido, (reto["id"], fraccion["texto"]))
                historial.append({"fraccion": fraccion["id"], "metodo": elegido})
            e = practica.estado(fr, ctx, historial)
            self.assertEqual(e["completo"], not reto.get("parcial_esperado", False), (reto["id"], e["pendientes"]))
