import datetime
import os
from functools import wraps

import jwt
from flask import Blueprint, g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, registro
from .respostas import erro

bp = Blueprint("auth", __name__, url_prefix="/api/auth")
VALIDADE_HORAS = 2


def segredo():
    return os.environ.get("JWT_SECRET", "dev-troque-este-segredo-antes-de-publicar-0123")


def garantir_admin():
    """Na primeira execução, cria o usuário administrador inicial."""
    n = db.executar("SELECT COUNT(*) AS n FROM usuarios", resultado="um")["n"]
    if n == 0:
        senha = os.environ.get("ADMIN_SENHA", "canteiro123")
        db.executar(
            "INSERT INTO usuarios (nome, email, senha_hash, perfil) "
            "VALUES (%s, %s, %s, 'administrador')",
            ("Administrador", "admin@canteiro.local", generate_password_hash(senha)),
            "nenhum",
        )


@bp.post("/login")
def login():
    d = request.get_json(silent=True) or {}
    email = (d.get("email") or "").strip().lower()
    senha = d.get("senha") or ""
    u = db.executar(
        "SELECT id, nome, email, senha_hash, perfil FROM usuarios WHERE email = %s",
        (email,), "um",
    )
    if not u or not check_password_hash(u["senha_hash"], senha):
        return erro(401, "credenciais_invalidas", "E-mail ou senha incorretos.")

    agora = datetime.datetime.now(datetime.timezone.utc)
    token = jwt.encode(
        {"sub": str(u["id"]), "perfil": u["perfil"], "iat": agora,
         "exp": agora + datetime.timedelta(hours=VALIDADE_HORAS)},
        segredo(), algorithm="HS256",
    )
    registro.registrar("login", "usuario", u["id"], usuario_id=u["id"])
    return jsonify(
        token=token, tipo="Bearer", expira_em=VALIDADE_HORAS * 3600,
        usuario={"id": u["id"], "nome": u["nome"], "email": u["email"], "perfil": u["perfil"]},
    )


def exige_login(f):
    @wraps(f)
    def interno(*args, **kwargs):
        cabecalho = request.headers.get("Authorization", "")
        if not cabecalho.startswith("Bearer "):
            return erro(401, "nao_autenticado",
                        "Envie o token no cabeçalho Authorization: Bearer <token>.")
        try:
            g.usuario = jwt.decode(cabecalho[7:], segredo(), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return erro(401, "token_expirado", "Token expirado. Faça login novamente.")
        except jwt.InvalidTokenError:
            return erro(401, "token_invalido", "Token inválido.")
        return f(*args, **kwargs)
    return interno


def exige_perfil(*perfis):
    """Exige login e que o perfil do usuário esteja na lista (senão, 403)."""
    def decorador(f):
        @exige_login
        @wraps(f)
        def interno(*args, **kwargs):
            if g.usuario.get("perfil") not in perfis:
                return erro(403, "sem_permissao", "Você não tem permissão para esta ação.")
            return f(*args, **kwargs)
        return interno
    return decorador
