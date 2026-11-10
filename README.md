# Canteiro — ERP web para viveiro de plantas

Projeto da disciplina (Fatec Americana) que evolui exercício por exercício até a estrutura de um ERP web.
O tema é um viveiro: plantas, clientes, vendas, estoque e financeiro.

## Declaração de uso de IA

Projeto feito com IA em algumas partes, corrigido com interação humana

## Estrutura

```
canteiro/
├── api/                      # back-end (Python + Flask + PostgreSQL)
│   ├── app/                  # auth, rotas_*, repositorio*, validacao, registro (log), db
│   ├── schema.sql            # criação de todas as tabelas
│   ├── dados_exemplo.sql     # dados de exemplo (opcional)
│   ├── criar_usuario.py      # cria usuários com perfil
│   ├── testes/               # testes automatizados
│   └── run.py
├── web/                      # front-end (HTML, CSS e JS puros), separado da API
│   ├── *.html, css/, js/     # páginas, layout responsivo, scripts
│   └── i18n/                 # pt-BR.json e en.json
└── docs/                     # api.md, arquitetura.md, diagrama-er.md
```

## Como rodar

Requisitos: Python 3 e um PostgreSQL (local ou na nuvem, como o Neon).

**1. API** (terminal na pasta `api`):
```bash
python -m venv venv
venv\Scripts\activate          # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```
Defina a conexão e o segredo do token e inicie (exemplo no PowerShell; cmd usa `set VAR=valor`, Linux/Mac usa `export VAR="valor"`):
```powershell
$env:DATABASE_URL="postgresql://usuario:senha@host:5432/banco?sslmode=require"
$env:JWT_SECRET="uma-frase-longa-e-secreta-com-mais-de-32-caracteres"
python run.py
```
As tabelas são criadas sozinhas. API em `http://localhost:5000`.

**2. Front-end** (**outro** terminal, na pasta `web`):
```bash
python -m http.server 3000
```
Acesse **http://localhost:3000**. Não abra os arquivos direto no navegador: as traduções são carregadas por requisição.
Se a API estiver em outro endereço, mude `API_URL` em `web/js/config.js`.

**3. Usuários.** O primeiro acesso usa `admin@canteiro.local` / `canteiro123` (mude com `ADMIN_SENHA` antes da primeira execução). Para criar outros perfis (na pasta `api`, com a mesma `DATABASE_URL`):
```bash
python criar_usuario.py "Vera" vendedor@canteiro.local senha123 vendedor
python criar_usuario.py "Fábio" financeiro@canteiro.local senha123 financeiro
```

**Testes** (use um banco de teste, pois eles apagam plantas e clientes): `python -m unittest discover -s testes -t . -v`

Variáveis: `DATABASE_URL`, `JWT_SECRET`, `ADMIN_SENHA`, `CORS_ORIGENS` (padrão `*`).

## Perfis de acesso

Veja a tabela completa em `docs/arquitetura.md`. Resumo: **administrador** faz tudo; **vendedor** consulta, inclui e altera; **financeiro** só consulta (e vê o módulo Financeiro).

## Andamento por exercício

| Exercício | Situação |
|-----------|----------|
| EX1 Web responsiva | Feito: 4 páginas + ERP, HTML semântico, 3 breakpoints, grid/flexbox, menu hambúrguer, unidades relativas |
| EX2 i18n web | Feito: pt-BR e inglês, seletor com escolha salva, datas/números/moeda e mensagens traduzidos |
| EX3 Cadastro | Feito: Plantas e Clientes (CRUD, validação no cliente e no servidor, busca, paginação, SQL parametrizado) |
| EX4 API | Feito: verbos e status HTTP, JSON padronizado, JWT, CORS, documentação (`docs/api.md`) |
| EX5, EX7 Mobile | A fazer |
| EX6 Web + API | Feito: front separado, token, login/expiração, carregamento, listar/detalhar/incluir/alterar/excluir |
| EX8 Calculadora | Projeto à parte |
| EX9 ERP | Estrutura pronta: arquitetura, diagrama ER e SQL, login com perfis, layout com menu lateral e painel, 2 cadastros completos, log de ações. Vendas, Estoque e Financeiro têm navegação, tela inicial e tabelas modeladas |

## Versionamento (Git)

```bash
git init
git add .
git commit -m "Canteiro: API, web e ERP (EX1 a EX4, EX6 e EX9)"
```
