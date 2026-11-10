# Documentação da API — Canteiro

Base: `http://localhost:5000` · Formato: JSON · Autenticação: JWT (`Authorization: Bearer <token>`)

## Formato de erro (todas as rotas)

```json
{ "erro": { "codigo": "validacao", "mensagem": "Dados inválidos.", "detalhes": { "preco": "Informe um número maior ou igual a zero." } } }
```

| Status | Quando |
|--------|--------|
| 200 | Consulta ou alteração feita |
| 201 | Registro criado |
| 204 | Registro excluído (sem corpo) |
| 400 | Dados inválidos (`validacao`, `corpo_invalido`, `parametro_invalido`) |
| 401 | Sem token, token inválido/expirado ou login incorreto |
| 404 | Registro ou rota não encontrada |
| 500 | Erro interno (`erro_interno`) |

## Endpoints

| Método | Rota | Auth | Descrição |
|--------|------|------|-----------|
| GET | `/api/saude` | não | Verifica se a API está no ar |
| POST | `/api/auth/login` | não | Devolve o token JWT (validade de 2 h) |
| GET | `/api/plantas` | sim | Lista com `busca`, `categoria`, `pagina`, `por_pagina` |
| GET | `/api/plantas/{id}` | sim | Detalhe de uma planta |
| POST | `/api/plantas` | sim | Cria uma planta |
| PUT | `/api/plantas/{id}` | sim | Altera uma planta (envie todos os campos) |
| DELETE | `/api/plantas/{id}` | sim | Exclui uma planta |

## Campos da planta

| Campo | Tipo | Regra |
|-------|------|-------|
| `nome_popular` | texto | obrigatório, 2 a 100 caracteres |
| `nome_cientifico` | texto | opcional, até 150 |
| `categoria` | seleção | `interior`, `jardim`, `suculenta`, `frutifera`, `aromatica` |
| `luminosidade` | seleção | `sombra`, `meia_sombra`, `sol_pleno` |
| `preco` | número | maior ou igual a 0 |
| `estoque` | inteiro | maior ou igual a 0 |
| `data_entrada` | data | `AAAA-MM-DD` (padrão: hoje) |
| `pet_seguro` | booleano | `true` ou `false` |
| `observacoes` | texto | opcional, até 500 |

## Exemplos (use `curl.exe` no PowerShell do Windows)

**Login**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@canteiro.local","senha":"canteiro123"}'
```
Resposta `200`:
```json
{ "token": "eyJ...", "tipo": "Bearer", "expira_em": 7200,
  "usuario": { "id": 1, "nome": "Administrador", "email": "admin@canteiro.local", "perfil": "administrador" } }
```

**Criar planta**
```bash
curl -X POST http://localhost:5000/api/plantas \
  -H "Authorization: Bearer SEU_TOKEN" -H "Content-Type: application/json" \
  -d '{"nome_popular":"Lavanda","categoria":"aromatica","luminosidade":"sol_pleno","preco":22,"estoque":15,"pet_seguro":true}'
```
Resposta `201`:
```json
{ "id": 1, "nome_popular": "Lavanda", "nome_cientifico": null, "categoria": "aromatica",
  "luminosidade": "sol_pleno", "preco": 22.0, "estoque": 15,
  "data_entrada": "2026-11-08", "pet_seguro": true, "observacoes": null }
```

**Listar com busca e paginação**
```bash
curl "http://localhost:5000/api/plantas?busca=lav&categoria=aromatica&pagina=1&por_pagina=5" \
  -H "Authorization: Bearer SEU_TOKEN"
```
Resposta `200`:
```json
{ "itens": [ { "id": 1, "nome_popular": "Lavanda", "...": "..." } ],
  "pagina": 1, "por_pagina": 5, "total": 1, "total_paginas": 1 }
```

**Erro de validação** (`400`)
```json
{ "erro": { "codigo": "validacao", "mensagem": "Dados inválidos.",
            "detalhes": { "nome_popular": "Informe de 2 a 100 caracteres.", "categoria": "Valor inválido. Use: interior, jardim, suculenta, frutifera, aromatica." } } }
```

---

# Etapa ERP: clientes, painel, log e perfis

Novos códigos de erro: `403 sem_permissao` (perfil sem acesso) e `409 duplicado` (e-mail ou CPF já cadastrado).

| Método | Rota | Perfis | Descrição |
|--------|------|--------|-----------|
| GET | `/api/clientes` | todos | Lista com `busca` (nome, e-mail ou CPF), `pagina`, `por_pagina` |
| GET | `/api/clientes/{id}` | todos | Detalhe |
| POST | `/api/clientes` | administrador, vendedor | Cria |
| PUT | `/api/clientes/{id}` | administrador, vendedor | Altera (envie todos os campos) |
| DELETE | `/api/clientes/{id}` | administrador | Exclui |
| GET | `/api/painel` | todos | Indicadores: `plantas`, `estoque`, `estoque_baixo`, `clientes` |
| GET | `/api/logs?limite=50` | administrador | Últimas ações registradas |

Em **plantas**, `POST` e `PUT` agora exigem administrador ou vendedor, e `DELETE` exige administrador.

Campos do cliente: `nome` (2 a 100), `email` (formato válido), `cpf` (11 dígitos com dígito verificador, aceita pontuação), `telefone` (opcional, 10 ou 11 dígitos), `cidade` (opcional, até 80).

```bash
curl -X POST http://localhost:5000/api/clientes \
  -H "Authorization: Bearer SEU_TOKEN" -H "Content-Type: application/json" \
  -d '{"nome":"Maria Souza","email":"maria@exemplo.com","cpf":"529.982.247-25","cidade":"Americana"}'
```
Resposta `201`:
```json
{ "id": 1, "nome": "Maria Souza", "email": "maria@exemplo.com", "cpf": "52998224725",
  "telefone": null, "cidade": "Americana", "data_cadastro": "2026-11-09" }
```
