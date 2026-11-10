from flask import jsonify


def erro(status, codigo, mensagem, detalhes=None):
    """Formato único de erro: {"erro": {"codigo", "mensagem", "detalhes"?}}"""
    corpo = {"erro": {"codigo": codigo, "mensagem": mensagem}}
    if detalhes:
        corpo["erro"]["detalhes"] = detalhes
    return jsonify(corpo), status
