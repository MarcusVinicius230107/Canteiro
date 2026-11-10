"""Camada de dados (Model): todo acesso ao banco de plantas passa por aqui."""
from . import db

COLUNAS = (
    "id, nome_popular, nome_cientifico, categoria, luminosidade, "
    "preco, estoque, data_entrada, pet_seguro, observacoes"
)


def _para_dict(linha):
    if linha is None:
        return None
    linha = dict(linha)
    linha["preco"] = float(linha["preco"])
    linha["data_entrada"] = linha["data_entrada"].isoformat()
    return linha


def listar(busca, categoria, pagina, por_pagina):
    # Só fragmentos fixos entram no SQL; todo valor do usuário vai em parâmetros (%s).
    filtros, params = [], []
    if busca:
        filtros.append("(nome_popular ILIKE %s OR nome_cientifico ILIKE %s)")
        params += [f"%{busca}%", f"%{busca}%"]
    if categoria:
        filtros.append("categoria = %s")
        params.append(categoria)
    onde = ("WHERE " + " AND ".join(filtros)) if filtros else ""

    total = db.executar(f"SELECT COUNT(*) AS n FROM plantas {onde}", params, "um")["n"]
    linhas = db.executar(
        f"SELECT {COLUNAS} FROM plantas {onde} "
        "ORDER BY nome_popular, id LIMIT %s OFFSET %s",
        params + [por_pagina, (pagina - 1) * por_pagina],
    )
    return [_para_dict(l) for l in linhas], total


def buscar(planta_id):
    return _para_dict(
        db.executar(f"SELECT {COLUNAS} FROM plantas WHERE id = %s", (planta_id,), "um")
    )


def criar(d):
    return _para_dict(db.executar(
        """INSERT INTO plantas (nome_popular, nome_cientifico, categoria, luminosidade,
                                preco, estoque, data_entrada, pet_seguro, observacoes)
           VALUES (%(nome_popular)s, %(nome_cientifico)s, %(categoria)s, %(luminosidade)s,
                   %(preco)s, %(estoque)s, %(data_entrada)s, %(pet_seguro)s, %(observacoes)s)
           RETURNING """ + COLUNAS,
        d, "um",
    ))


def atualizar(planta_id, d):
    return _para_dict(db.executar(
        """UPDATE plantas SET nome_popular = %(nome_popular)s,
               nome_cientifico = %(nome_cientifico)s, categoria = %(categoria)s,
               luminosidade = %(luminosidade)s, preco = %(preco)s, estoque = %(estoque)s,
               data_entrada = %(data_entrada)s, pet_seguro = %(pet_seguro)s,
               observacoes = %(observacoes)s
           WHERE id = %(id)s RETURNING """ + COLUNAS,
        {**d, "id": planta_id}, "um",
    ))


def excluir(planta_id):
    return db.executar("DELETE FROM plantas WHERE id = %s", (planta_id,), "nenhum") > 0
