# Arquitetura do Canteiro (ERP web)

## Visão geral

```
Navegador (web/: HTML, CSS, JS)  ──HTTP + JSON + JWT──►  API Flask (api/)  ──SQL──►  PostgreSQL
```

O front-end é totalmente separado da API e conversa com ela só por requisições HTTP (`fetch`).

## Organização em camadas (MVC adaptado)

| Camada | Onde fica | Papel |
|--------|-----------|-------|
| Model | `api/app/repositorio*.py` | Acesso ao banco, sempre com consultas parametrizadas |
| Controller | `api/app/rotas_*.py` | Recebe a requisição, valida, aplica permissão e chama o Model |
| View | `web/` | Telas, formulários e tradução (consome a API) |
| Núcleo | `auth.py`, `db.py`, `registro.py`, `validacao.py`, `respostas.py` | Login/JWT, conexão, log, regras de validação e padrão de erro |

## Núcleo e módulos

- **Núcleo:** autenticação, perfis de acesso, log de ações, i18n, layout padrão e tratamento de erros.
- **Módulos implementados por completo:** *Plantas* (produtos) e *Clientes*, com CRUD, busca, paginação e validações.
- **Painel inicial:** indicadores simples (plantas, itens em estoque, estoque baixo, clientes).
- **Módulos previstos (tela inicial + tabelas modeladas):**
  - **Vendas:** `pedidos` e `itens_pedido`, com baixa automática do estoque.
  - **Estoque:** `movimentacoes_estoque` (entradas, saídas e ajustes).
  - **Financeiro:** `contas` a pagar e a receber, ligadas a pedidos e fornecedores.

Para criar um módulo novo: um `repositorio_x.py`, um `rotas_x.py` registrado em `app/__init__.py` e uma página em `web/` com a entrada no menu (`MODULOS` em `web/js/app.js`).

## Perfis e controle de acesso

A API valida o perfil em cada requisição (resposta 403 se não permitido). O menu esconde o que o perfil não pode usar.

| Ação | administrador | vendedor | financeiro |
|------|:---:|:---:|:---:|
| Consultar plantas, clientes e painel | sim | sim | sim |
| Incluir e alterar plantas e clientes | sim | sim | não |
| Excluir plantas e clientes | sim | não | não |
| Consultar o log (`GET /api/logs`) | sim | não | não |
| Menu Vendas e Estoque | sim | sim | não |
| Menu Financeiro | sim | não | sim |

Novos usuários: `python criar_usuario.py "Nome" email senha perfil` (na pasta `api`).

## Log de ações

A tabela `logs` registra **login**, **incluir**, **alterar** e **excluir**, com usuário, entidade, id e data/hora.
Para consultar: `GET /api/logs` (administrador) ou `SELECT * FROM logs ORDER BY id DESC;` no banco.

## Integração com os exercícios anteriores

- **EX1 (responsivo):** o layout do ERP usa os 3 breakpoints; o menu lateral vira hambúrguer em telas pequenas.
- **EX2 (i18n):** todas as telas do ERP têm português e inglês (`web/i18n/`).
- **EX3 (cadastros):** Plantas e Clientes reaproveitam o mesmo padrão de CRUD, validação e paginação.
- **EX4 e EX6 (API e consumo):** o ERP é a API do EX4 consumida pelo front do EX6.
