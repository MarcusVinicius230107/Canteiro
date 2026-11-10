###Trabalho feito por Marcus Vinícius Silva Thomaz & Murilo Fonseca Michelani###

# Canteiro — ERP web para viveiro de plantas

O tema é um viveiro: plantas, clientes, vendas, estoque e financeiro.

## Declaração de uso de IA

Este projeto foi desenvolvido com o auxílio da ferramenta de IA **Claude (Anthropic)**.

**Partes geradas ou escritas com IA:**
- A estrutura do projeto e o código da API (Python/Flask): rotas, validações, autenticação JWT, perfis de acesso e log de ações.
- O esquema do banco de dados (SQL) e os dados de exemplo.
- O front-end (HTML, CSS e JavaScript): páginas, layout responsivo e internacionalização (português e inglês).
- Os testes automatizados e a documentação (`docs/`), incluindo o diagrama do banco.

**O que nós fizemos:**
- Configurar o banco de dados PostgreSQL no Neon e conectei a API a ele.
- Executar e testei o sistema, incluindo login, cadastros, perfis e idiomas.
- Criar os usuários dos perfis e cadastrei dados de teste.
- Publicar o projeto no GitHub.
- Correção de Erros eventuais na aplicação

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


## Versionamento (Git)

```bash
git init
git add .
git commit -m "Canteiro: API, web e ERP (EX1 a EX4, EX6 e EX9)"
```
