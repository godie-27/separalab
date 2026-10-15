# app.py
# Punto de entrada de la aplicación web SEPARALAB (Flask).
#   Local:      python app.py   →  http://127.0.0.1:5000
#   Producción: gunicorn app:app

import os

from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import HTTPException

from logica.practica import ErrorPractica
from web.rutas import bp
from web.validacion import ErrorEntrada


def _es_api():
    return request.path.startswith("/api/")


def create_app():
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 64 * 1024  # 64 KB: de sobra para cualquier petición válida
    app.config["JSON_SORT_KEYS"] = False
    app.json.ensure_ascii = False
    app.json.sort_keys = False
    app.register_blueprint(bp)

    @app.after_request
    def cabeceras_seguridad(respuesta):
        respuesta.headers["X-Content-Type-Options"] = "nosniff"
        respuesta.headers["X-Frame-Options"] = "SAMEORIGIN"
        respuesta.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        respuesta.headers["Content-Security-Policy"] = (
            "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; script-src 'self'; connect-src 'self'; "
            "frame-ancestors 'self'; base-uri 'self'; form-action 'self'"
        )
        return respuesta

    @app.errorhandler(ErrorEntrada)
    @app.errorhandler(ErrorPractica)
    def error_entrada(e):
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(HTTPException)
    def error_http(e):
        mensajes = {404: "No se encontró lo que buscas.", 405: "Método no permitido.",
                    413: "La petición es demasiado grande.", 400: "La petición no es válida."}
        mensaje = mensajes.get(e.code, "Ha ocurrido un error.")
        if _es_api():
            return jsonify({"error": mensaje}), e.code
        return render_template("error.html", codigo=e.code, mensaje=mensaje), e.code

    @app.errorhandler(Exception)
    def error_interno(e):
        app.logger.exception("Error no controlado")
        mensaje = "Ha ocurrido un error inesperado. Inténtalo de nuevo con otra combinación."
        if _es_api():
            return jsonify({"error": mensaje}), 500
        return render_template("error.html", codigo=500, mensaje=mensaje), 500

    return app


app = create_app()

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    print("\n🧪 SEPARALAB")
    print(f"Abre en tu navegador: http://127.0.0.1:{puerto}")
    print("Para detener la página, vuelve a esta ventana y presiona Ctrl+C.\n")
    app.run(host="127.0.0.1", port=puerto, debug=False)
