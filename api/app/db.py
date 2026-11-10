import os

import psycopg2
from psycopg2.extras import RealDictCursor


def _url():
    return os.environ.get(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/canteiro"
    )


def executar(sql, params=None, resultado="todos"):
    """Executa SQL parametrizado. resultado: todos | um | nenhum (devolve linhas afetadas)."""
    conn = psycopg2.connect(_url(), cursor_factory=RealDictCursor)
    try:
        with conn:  # commit ou rollback automático
            with conn.cursor() as cur:
                cur.execute(sql, params)
                if resultado == "todos":
                    return cur.fetchall()
                if resultado == "um":
                    return cur.fetchone()
                return cur.rowcount
    finally:
        conn.close()


def iniciar():
    """Cria as tabelas, se ainda não existirem."""
    caminho = os.path.join(os.path.dirname(__file__), "..", "schema.sql")
    with open(caminho, encoding="utf-8") as f:
        executar(f.read(), resultado="nenhum")
