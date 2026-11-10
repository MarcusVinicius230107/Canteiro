from flask import g, has_request_context

from . import db


def registrar(acao, entidade=None, entidade_id=None, usuario_id=None):
    """Grava no log de ações (login, incluir, alterar, excluir)."""
    if usuario_id is None and has_request_context() and "usuario" in g:
        usuario_id = int(g.usuario["sub"])
    db.executar(
        "INSERT INTO logs (usuario_id, acao, entidade, entidade_id) VALUES (%s, %s, %s, %s)",
        (usuario_id, acao, entidade, entidade_id), "nenhum",
    )
