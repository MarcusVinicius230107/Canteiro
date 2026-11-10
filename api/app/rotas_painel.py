from flask import Blueprint, jsonify, request

from . import db
from .auth import exige_login, exige_perfil

bp = Blueprint("painel", __name__, url_prefix="/api")


@bp.get("/painel")
@exige_login
def painel():
    r = db.executar(
        """SELECT (SELECT COUNT(*) FROM plantas) AS plantas,
                  (SELECT COALESCE(SUM(estoque), 0) FROM plantas) AS estoque,
                  (SELECT COUNT(*) FROM plantas WHERE estoque <= 5) AS estoque_baixo,
                  (SELECT COUNT(*) FROM clientes) AS clientes""",
        resultado="um",
    )
    return jsonify({k: int(v) for k, v in r.items()})


@bp.get("/logs")
@exige_perfil("administrador")
def logs():
    try:
        limite = max(1, min(200, int(request.args.get("limite", 50))))
    except ValueError:
        limite = 50
    linhas = db.executar(
        """SELECT l.id, l.acao, l.entidade, l.entidade_id, l.criado_em, u.email AS usuario
             FROM logs l LEFT JOIN usuarios u ON u.id = l.usuario_id
            ORDER BY l.id DESC LIMIT %s""", (limite,))
    for l in linhas:
        l["criado_em"] = l["criado_em"].isoformat(timespec="seconds")
    return jsonify(itens=linhas)
