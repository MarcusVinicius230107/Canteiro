"""Controller dos clientes. Leitura: qualquer perfil. Escrever: administrador e vendedor. Excluir: administrador."""
from flask import Blueprint, jsonify, request

from . import registro, repositorio_clientes as repo, validacao
from .auth import exige_login, exige_perfil
from .respostas import erro
from .rotas_plantas import _corpo_json, _numero_da_url

bp = Blueprint("clientes", __name__, url_prefix="/api/clientes")


def _nao_encontrado():
    return erro(404, "nao_encontrado", "Cliente não encontrado.")


@bp.get("")
@exige_login
def listar():
    pagina = _numero_da_url("pagina", 1, 1, 1_000_000)
    por_pagina = _numero_da_url("por_pagina", 10, 1, 100)
    itens, total = repo.listar((request.args.get("busca") or "").strip(), pagina, por_pagina)
    return jsonify(itens=itens, pagina=pagina, por_pagina=por_pagina, total=total,
                   total_paginas=max(1, -(-total // por_pagina)))


@bp.get("/<int:cliente_id>")
@exige_login
def detalhar(cliente_id):
    cliente = repo.buscar(cliente_id)
    return jsonify(cliente) if cliente else _nao_encontrado()


@bp.post("")
@exige_perfil("administrador", "vendedor")
def criar():
    dados = _corpo_json()
    if dados is None:
        return erro(400, "corpo_invalido", "Envie um objeto JSON no corpo da requisição.")
    limpo, erros = validacao.validar_cliente(dados)
    if erros:
        return erro(400, "validacao", "Dados inválidos.", erros)
    cliente = repo.criar(limpo)
    registro.registrar("incluir", "cliente", cliente["id"])
    return jsonify(cliente), 201


@bp.put("/<int:cliente_id>")
@exige_perfil("administrador", "vendedor")
def atualizar(cliente_id):
    dados = _corpo_json()
    if dados is None:
        return erro(400, "corpo_invalido", "Envie um objeto JSON no corpo da requisição.")
    limpo, erros = validacao.validar_cliente(dados)
    if erros:
        return erro(400, "validacao", "Dados inválidos.", erros)
    cliente = repo.atualizar(cliente_id, limpo)
    if cliente is None:
        return _nao_encontrado()
    registro.registrar("alterar", "cliente", cliente_id)
    return jsonify(cliente)


@bp.delete("/<int:cliente_id>")
@exige_perfil("administrador")
def excluir(cliente_id):
    if not repo.excluir(cliente_id):
        return _nao_encontrado()
    registro.registrar("excluir", "cliente", cliente_id)
    return "", 204
