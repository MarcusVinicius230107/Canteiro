"""Cria um usuário. Uso: python criar_usuario.py "Nome" email senha perfil
Perfis: administrador, vendedor, financeiro"""
import sys

from werkzeug.security import generate_password_hash

from app import db

if len(sys.argv) != 5 or sys.argv[4] not in ("administrador", "vendedor", "financeiro"):
    sys.exit(__doc__)

nome, email, senha, perfil = sys.argv[1:]
db.iniciar()
try:
    db.executar(
        "INSERT INTO usuarios (nome, email, senha_hash, perfil) VALUES (%s, %s, %s, %s)",
        (nome, email.lower(), generate_password_hash(senha), perfil), "nenhum")
    print(f"Usuário {email} criado com o perfil {perfil}.")
except Exception as e:
    sys.exit(f"Não foi possível criar o usuário: {e}")
