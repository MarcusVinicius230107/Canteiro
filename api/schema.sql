CREATE TABLE IF NOT EXISTS usuarios (
    id         SERIAL PRIMARY KEY,
    nome       VARCHAR(100) NOT NULL,
    email      VARCHAR(150) NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    perfil     VARCHAR(20) NOT NULL DEFAULT 'vendedor'
               CHECK (perfil IN ('administrador', 'vendedor', 'financeiro')),
    criado_em  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS plantas (
    id              SERIAL PRIMARY KEY,
    nome_popular    VARCHAR(100) NOT NULL,
    nome_cientifico VARCHAR(150),
    categoria       VARCHAR(20) NOT NULL
                    CHECK (categoria IN ('interior', 'jardim', 'suculenta', 'frutifera', 'aromatica')),
    luminosidade    VARCHAR(12) NOT NULL
                    CHECK (luminosidade IN ('sombra', 'meia_sombra', 'sol_pleno')),
    preco           NUMERIC(10,2) NOT NULL CHECK (preco >= 0),
    estoque         INTEGER NOT NULL DEFAULT 0 CHECK (estoque >= 0),
    data_entrada    DATE NOT NULL DEFAULT CURRENT_DATE,
    pet_seguro      BOOLEAN NOT NULL DEFAULT FALSE,
    observacoes     VARCHAR(500),
    criada_em       TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_plantas_nome ON plantas (nome_popular);

-- ===== Cadastros =====
CREATE TABLE IF NOT EXISTS clientes (
    id            SERIAL PRIMARY KEY,
    nome          VARCHAR(100) NOT NULL,
    email         VARCHAR(150) NOT NULL UNIQUE,
    cpf           CHAR(11) NOT NULL UNIQUE,
    telefone      VARCHAR(20),
    cidade        VARCHAR(80),
    data_cadastro DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS fornecedores (
    id       SERIAL PRIMARY KEY,
    nome     VARCHAR(100) NOT NULL,
    cnpj     CHAR(14) UNIQUE,
    email    VARCHAR(150),
    telefone VARCHAR(20)
);

-- ===== Vendas =====
CREATE TABLE IF NOT EXISTS pedidos (
    id         SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id),
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    data       TIMESTAMP NOT NULL DEFAULT NOW(),
    status     VARCHAR(12) NOT NULL DEFAULT 'aberto'
               CHECK (status IN ('aberto', 'pago', 'cancelado')),
    total      NUMERIC(12,2) NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS itens_pedido (
    id             SERIAL PRIMARY KEY,
    pedido_id      INTEGER NOT NULL REFERENCES pedidos(id) ON DELETE CASCADE,
    planta_id      INTEGER NOT NULL REFERENCES plantas(id),
    quantidade     INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario NUMERIC(10,2) NOT NULL CHECK (preco_unitario >= 0)
);

-- ===== Estoque =====
CREATE TABLE IF NOT EXISTS movimentacoes_estoque (
    id        SERIAL PRIMARY KEY,
    planta_id INTEGER NOT NULL REFERENCES plantas(id),
    tipo      VARCHAR(10) NOT NULL CHECK (tipo IN ('entrada', 'saida', 'ajuste')),
    quantidade INTEGER NOT NULL,
    motivo    VARCHAR(120),
    pedido_id INTEGER REFERENCES pedidos(id),
    criada_em TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ===== Financeiro =====
CREATE TABLE IF NOT EXISTS contas (
    id            SERIAL PRIMARY KEY,
    tipo          VARCHAR(8) NOT NULL CHECK (tipo IN ('pagar', 'receber')),
    descricao     VARCHAR(150) NOT NULL,
    valor         NUMERIC(12,2) NOT NULL CHECK (valor >= 0),
    vencimento    DATE NOT NULL,
    status        VARCHAR(10) NOT NULL DEFAULT 'aberta'
                  CHECK (status IN ('aberta', 'paga', 'cancelada')),
    pedido_id     INTEGER REFERENCES pedidos(id),
    fornecedor_id INTEGER REFERENCES fornecedores(id)
);

-- ===== Auditoria =====
CREATE TABLE IF NOT EXISTS logs (
    id         SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    acao       VARCHAR(30) NOT NULL,
    entidade   VARCHAR(30),
    entidade_id INTEGER,
    criado_em  TIMESTAMP NOT NULL DEFAULT NOW()
);
