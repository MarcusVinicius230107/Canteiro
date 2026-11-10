"""Camada de dados (Model) dos clientes."""
from . import db

COLUNAS = "id, nome, email, cpf, telefone, cidade, data_cadastro"


def _para_dict(linha):
    if linha is None:
        return None
    linha = dict(linha)
    linha["data_cadastro"] = linha["data_cadastro"].isoformat()
    return linha


def listar(busca, pagina, por_pagina):
    onde, params = "", []
    if busca:
        onde = "WHERE nome ILIKE %s OR email ILIKE %s OR cpf LIKE %s"
        params = [f"%{busca}%", f"%{busca}%", f"%{busca}%"]
    total = db.executar(f"SELECT COUNT(*) AS n FROM clientes {onde}", params, "um")["n"]
    linhas = db.executar(
        f"SELECT {COLUNAS} FROM clientes {onde} ORDER BY nome, id LIMIT %s OFFSET %s",
        params + [por_pagina, (pagina - 1) * por_pagina],
    )
    return [_para_dict(l) for l in linhas], total


def buscar(cliente_id):
    return _para_dict(db.executar(
        f"SELECT {COLUNAS} FROM clientes WHERE id = %s", (cliente_id,), "um"))


def criar(d):
    return _para_dict(db.executar(
        """INSERT INTO clientes (nome, email, cpf, telefone, cidade)
           VALUES (%(nome)s, %(email)s, %(cpf)s, %(telefone)s, %(cidade)s)
           RETURNING """ + COLUNAS, d, "um"))


def atualizar(cliente_id, d):
    return _para_dict(db.executar(
        """UPDATE clientes SET nome = %(nome)s, email = %(email)s, cpf = %(cpf)s,
               telefone = %(telefone)s, cidade = %(cidade)s
           WHERE id = %(id)s RETURNING """ + COLUNAS,
        {**d, "id": cliente_id}, "um"))


def excluir(cliente_id):
    return db.executar("DELETE FROM clientes WHERE id = %s", (cliente_id,), "nenhum") > 0
