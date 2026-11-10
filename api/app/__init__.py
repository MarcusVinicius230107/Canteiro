import os

import psycopg2.errors
from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from . import auth, db, rotas_clientes, rotas_painel, rotas_plantas
from .respostas import erro


def create_app():
    app = Flask(__name__)
    app.json.ensure_ascii = False  # acentos legíveis no JSON
    CORS(app, resources={r"/api/*": {"origins": os.environ.get("CORS_ORIGENS", "*")}})

    app.register_blueprint(auth.bp)
    app.register_blueprint(rotas_plantas.bp)
    app.register_blueprint(rotas_clientes.bp)
    app.register_blueprint(rotas_painel.bp)

    @app.get("/api/saude")
    def saude():
        return jsonify(status="ok")

    @app.errorhandler(HTTPException)
    def erro_http(e):
        return erro(e.code, e.name.lower().replace(" ", "_"), e.description)

    @app.errorhandler(psycopg2.errors.UniqueViolation)
    def erro_duplicado(e):
        return erro(409, "duplicado", "Já existe um registro com esse e-mail ou CPF.")

    @app.errorhandler(Exception)
    def erro_interno(e):
        app.logger.exception(e)
        return erro(500, "erro_interno", "Erro interno do servidor.")

    return app


def preparar_banco():
    db.iniciar()
    auth.garantir_admin()
