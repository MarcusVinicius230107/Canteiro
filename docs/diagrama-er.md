# Diagrama entidade-relacionamento

Pode ser visualizado no GitHub (renderiza Mermaid) ou colando o código em https://mermaid.live para exportar como imagem.
O script completo está em `api/schema.sql`.

```mermaid
erDiagram
    USUARIOS ||--o{ PEDIDOS : registra
    USUARIOS ||--o{ LOGS : gera
    CLIENTES ||--o{ PEDIDOS : faz
    PEDIDOS ||--|{ ITENS_PEDIDO : contem
    PLANTAS ||--o{ ITENS_PEDIDO : "vendida em"
    PLANTAS ||--o{ MOVIMENTACOES_ESTOQUE : movimenta
    PEDIDOS ||--o{ MOVIMENTACOES_ESTOQUE : "baixa estoque"
    PEDIDOS ||--o{ CONTAS : gera
    FORNECEDORES ||--o{ CONTAS : recebe

    USUARIOS {
        int id PK
        string nome
        string email UK
        string senha_hash
        string perfil "administrador, vendedor ou financeiro"
    }
    CLIENTES {
        int id PK
        string nome
        string email UK
        string cpf UK
        string telefone
        string cidade
        date data_cadastro
    }
    FORNECEDORES {
        int id PK
        string nome
        string cnpj UK
        string email
        string telefone
    }
    PLANTAS {
        int id PK
        string nome_popular
        string nome_cientifico
        string categoria
        string luminosidade
        decimal preco
        int estoque
        date data_entrada
        boolean pet_seguro
        string observacoes
    }
    PEDIDOS {
        int id PK
        int cliente_id FK
        int usuario_id FK
        datetime data
        string status "aberto, pago ou cancelado"
        decimal total
    }
    ITENS_PEDIDO {
        int id PK
        int pedido_id FK
        int planta_id FK
        int quantidade
        decimal preco_unitario
    }
    MOVIMENTACOES_ESTOQUE {
        int id PK
        int planta_id FK
        int pedido_id FK
        string tipo "entrada, saida ou ajuste"
        int quantidade
        string motivo
    }
    CONTAS {
        int id PK
        int pedido_id FK
        int fornecedor_id FK
        string tipo "pagar ou receber"
        string descricao
        decimal valor
        date vencimento
        string status "aberta, paga ou cancelada"
    }
    LOGS {
        int id PK
        int usuario_id FK
        string acao
        string entidade
        int entidade_id
        datetime criado_em
    }
```
