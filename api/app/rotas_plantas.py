"""Controller: recebe a requisição, valida e chama o repositório."""
from flask import Blueprint, jsonify, request

from . import registro, repositorio, validacao
from .auth import exige_login, exige_perfil
from .respostas import erro

bp = Blueprint("plantas", __name__, url_prefix="/api/plantas")


def _numero_da_url(nome, padrao, minimo, maximo):
    try:
        valor = int(request.args.get(nome, padrao))
    except ValueError:
        valor = padrao
    return max(minimo, min(maximo, valor))


def _corpo_json():
    dados = request.get_json(silent=True)
    return dados if isinstance(dados, dict) else None


@bp.get("")
@exige_login
def listar():
    pagina = _numero_da_url("pagina", 1, 1, 1_000_000)
    por_pagina = _numero_da_url("por_pagina", 10, 1, 100)
    busca = (request.args.get("busca") or "").strip()
    categoria = request.args.get("categoria") or None
    if categoria and categoria not in validacao.CATEGORIAS:
        return erro(400, "parametro_invalido", "Categoria inválida.")

    itens, total = repositorio.listar(busca, categoria, pagina, por_pagina)
    return jsonify(
        itens=itens, pagina=pagina, por_pagina=por_pagina, total=total,
        total_paginas=max(1, -(-total // por_pagina)),
    )


@bp.get("/<int:planta_id>")
@exige_login
def detalhar(planta_id):
    planta = repositorio.buscar(planta_id)
    if planta is None:
        return erro(404, "nao_encontrado", "Planta não encontrada.")
    return jsonify(planta)


@bp.post("")
@exige_perfil("administrador", "vendedor")
def criar():
    dados = _corpo_json()
    if dados is None:
        return erro(400, "corpo_invalido", "Envie um objeto JSON no corpo da requisição.")
    limpo, erros = validacao.validar_planta(dados)
    if erros:
        return erro(400, "validacao", "Dados inválidos.", erros)
    planta = repositorio.criar(limpo)
    registro.registrar("incluir", "planta", planta["id"])
    return jsonify(planta), 201


@bp.put("/<int:planta_id>")
@exige_perfil("administrador", "vendedor")
def atualizar(planta_id):
    dados = _corpo_json()
    if dados is None:
        return erro(400, "corpo_invalido", "Envie um objeto JSON no corpo da requisição.")
    limpo, erros = validacao.validar_planta(dados)
    if erros:
        return erro(400, "validacao", "Dados inválidos.", erros)
    planta = repositorio.atualizar(planta_id, limpo)
    if planta is None:
        return erro(404, "nao_encontrado", "Planta não encontrada.")
    registro.registrar("alterar", "planta", planta_id)
    return jsonify(planta)


@bp.delete("/<int:planta_id>")
@exige_perfil("administrador")
def excluir(planta_id):
    if not repositorio.excluir(planta_id):
        return erro(404, "nao_encontrado", "Planta não encontrada.")
    registro.registrar("excluir", "planta", planta_id)
    return "", 204
