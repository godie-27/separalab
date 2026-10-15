# pruebas/test_api.py
# Rutas web y API: respuestas correctas, validación de entradas y errores comprensibles.

import unittest

try:
    from pruebas import _ruta  # noqa: F401
except ImportError:
    import _ruta  # noqa: F401

from app import create_app


class TestPaginas(unittest.TestCase):

    def setUp(self):
        self.c = create_app().test_client()

    def test_paginas_principales(self):
        for ruta in ("/", "/resolver", "/practica", "/retos", "/cromatografia", "/laboratorio", "/videos"):
            r = self.c.get(ruta)
            self.assertEqual(r.status_code, 200, ruta)
            self.assertIn(b"SEPARALAB", r.data)

    def test_archivos_estaticos(self):
        for ruta in ("/static/css/separalab.css", "/static/js/comun.js", "/static/js/render.js",
                     "/static/js/practica-motor.js", "/static/img/logo.svg"):
            r = self.c.get(ruta)
            self.assertEqual(r.status_code, 200, ruta)
            r.close()

    def test_404_html_y_json(self):
        self.assertEqual(self.c.get("/no-existe").status_code, 404)
        r = self.c.get("/api/no-existe")
        self.assertEqual(r.status_code, 404)
        self.assertIn("error", r.get_json())

    def test_cabeceras_de_seguridad(self):
        r = self.c.get("/")
        self.assertEqual(r.headers["X-Content-Type-Options"], "nosniff")
        self.assertIn("script-src 'self'", r.headers["Content-Security-Policy"])


class TestApiResolver(unittest.TestCase):

    def setUp(self):
        self.c = create_app().test_client()

    def post(self, url, datos):
        return self.c.post(url, json=datos)

    def test_resolver_ok(self):
        r = self.post("/api/resolver", {"sustancias": ["agua", "arena"]})
        self.assertEqual(r.status_code, 200)
        self.assertEqual([p["metodo"] for p in r.get_json()["pasos"]], ["filtracion"])

    def test_ruta_antigua_compatible(self):
        r = self.post("/api/analizar", {"sustancias": ["agua", "aceite"]})
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.get_json()["pasos"])

    def test_entradas_malformadas(self):
        casos = [
            {"sustancias": [{"a": 1}, "agua"]},       # el error 500 de la versión anterior
            {"sustancias": "agua"},
            {"sustancias": ["agua", "plutonio"]},
            {"sustancias": []},
            {"sustancias": ["agua", "arena"], "cantidades": {"agua": "mucha"}},
            {"sustancias": ["agua", "arena"], "cantidades": {"agua": -5, "arena": 3}},
            {"sustancias": ["agua", "arena"], "cantidades": {"agua": 100}},
            {"sustancias": ["agua", "arena"], "permitidos": ["teletransporte"]},
            {"sustancias": ["agua", "arena"], "permitidos": []},
            {"sustancias": ["agua", "arena"], "recuperar_disolvente": "si"},
            {"sustancias": ["agua"] * 3 + ["arena", "aceite", "etanol", "hierro", "azufre", "arcilla", "sacarosa", "carbonato_de_calcio", "oxido_de_hierro"]},
        ]
        for datos in casos:
            r = self.post("/api/resolver", datos)
            self.assertEqual(r.status_code, 400, datos)
            self.assertIn("error", r.get_json())
        r = self.c.post("/api/resolver", data="esto no es json", content_type="application/json")
        self.assertEqual(r.status_code, 400)
        self.assertIn("error", r.get_json())

    def test_peticion_demasiado_grande(self):
        r = self.c.post("/api/resolver", data="x" * 100_000, content_type="application/json")
        self.assertEqual(r.status_code, 413)

    def test_cantidades_con_coma(self):
        r = self.post("/api/resolver", {"sustancias": ["agua", "arena"], "cantidades": {"agua": "100,5", "arena": "20"}})
        self.assertEqual(r.status_code, 200)


class TestApiPracticaRetosRf(unittest.TestCase):

    def setUp(self):
        self.c = create_app().test_client()

    def test_flujo_de_practica(self):
        mezcla = {"sustancias": ["agua", "aceite"]}
        e = self.c.post("/api/practica/estado", json={"mezcla": mezcla, "historial": []}).get_json()
        self.assertEqual(e["pendientes"][0]["id"], "1")
        ev = self.c.post("/api/practica/evaluar", json={"mezcla": mezcla, "historial": [], "fraccion": "1", "metodo": "decantacion"}).get_json()
        self.assertEqual(ev["estado"], "optima")
        e = self.c.post("/api/practica/estado", json={"mezcla": mezcla, "historial": [{"fraccion": "1", "metodo": "decantacion"}]}).get_json()
        self.assertTrue(e["completo"])

    def test_practica_historial_invalido(self):
        r = self.c.post("/api/practica/estado", json={"mezcla": {"sustancias": ["agua", "aceite"]}, "historial": [{"fraccion": "1", "metodo": "filtracion"}]})
        self.assertEqual(r.status_code, 400)
        r = self.c.post("/api/practica/estado", json={"mezcla": {"reto": "zz"}})
        self.assertEqual(r.status_code, 400)

    def test_practica_desde_reto(self):
        r = self.c.post("/api/practica/estado", json={"mezcla": {"reto": "a1"}, "historial": []})
        self.assertEqual(r.status_code, 200)
        self.assertNotIn("cromatografia", [m["clave"] for m in r.get_json()["metodos"]])

    def test_materiales_y_procedimiento(self):
        r = self.c.post("/api/practica/materiales", json={"metodo": "filtracion"}).get_json()
        self.assertTrue(r["opciones"])
        r = self.c.post("/api/practica/materiales", json={"metodo": "filtracion", "seleccion": ["no_existe"]})
        self.assertEqual(r.status_code, 400)
        r = self.c.post("/api/practica/procedimiento", json={"metodo": "magnetismo"}).get_json()
        self.assertEqual(len(r["pasos"]), 4)

    def test_retos(self):
        r = self.c.get("/api/retos/aleatorio?nivel=basico").get_json()
        self.assertEqual(r["nivel"], "basico")
        self.assertNotIn("pistas", r)
        self.assertEqual(self.c.get("/api/retos/aleatorio?nivel=imposible").status_code, 400)
        self.assertEqual(self.c.get("/api/retos/zz").status_code, 404)
        p = self.c.post("/api/retos/b1/pista", json={"nivel": 1}).get_json()
        self.assertTrue(p["texto"])
        q = self.c.post("/api/retos/d1/pregunta", json={"indice": 0, "opcion": 0}).get_json()
        self.assertTrue(q["correcta"])
        self.assertTrue(self.c.get("/api/retos/d1/solucion").get_json()["completo"])

    def test_rf(self):
        r = self.c.post("/api/rf", json={"distancia": "4,2", "frente": "12"}).get_json()
        self.assertEqual(r["rf"], 0.35)
        r = self.c.post("/api/rf", json={"distancia": 5, "frente": 0})
        self.assertEqual(r.status_code, 400)
        self.assertIn("frente", r.get_json()["error"])
        r = self.c.post("/api/rf/comprobar", json={"ejercicio": "aplicacion2", "mancha": "Mancha 1", "respuesta": "0,89"}).get_json()
        self.assertTrue(r["correcta"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
