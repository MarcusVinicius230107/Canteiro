import math
from datetime import date

CATEGORIAS = ("interior", "jardim", "suculenta", "frutifera", "aromatica")
LUMINOSIDADES = ("sombra", "meia_sombra", "sol_pleno")


def _texto_opcional(valor, maximo, campo, erros):
    texto = (valor or "").strip() or None
    if texto and len(texto) > maximo:
        erros[campo] = f"Use no máximo {maximo} caracteres."
    return texto


def validar_planta(d):
    """Devolve (dados_limpos, erros). Se erros estiver vazio, os dados são válidos."""
    erros, limpo = {}, {}

    nome = (d.get("nome_popular") or "").strip()
    if not 2 <= len(nome) <= 100:
        erros["nome_popular"] = "Informe de 2 a 100 caracteres."
    limpo["nome_popular"] = nome

    limpo["nome_cientifico"] = _texto_opcional(
        d.get("nome_cientifico"), 150, "nome_cientifico", erros
    )

    for campo, opcoes in (("categoria", CATEGORIAS), ("luminosidade", LUMINOSIDADES)):
        valor = d.get(campo)
        if valor not in opcoes:
            erros[campo] = "Valor inválido. Use: " + ", ".join(opcoes) + "."
        limpo[campo] = valor

    try:
        preco = float(d.get("preco"))
        if preco < 0 or not math.isfinite(preco):
            raise ValueError
        limpo["preco"] = round(preco, 2)
    except (TypeError, ValueError):
        erros["preco"] = "Informe um número maior ou igual a zero."

    try:
        estoque = int(d.get("estoque", 0))
        if estoque < 0:
            raise ValueError
        limpo["estoque"] = estoque
    except (TypeError, ValueError):
        erros["estoque"] = "Informe um número inteiro maior ou igual a zero."

    try:
        limpo["data_entrada"] = date.fromisoformat(
            str(d.get("data_entrada") or date.today().isoformat())
        )
    except ValueError:
        erros["data_entrada"] = "Use o formato AAAA-MM-DD."

    pet = d.get("pet_seguro", False)
    if not isinstance(pet, bool):
        erros["pet_seguro"] = "Use true ou false."
    limpo["pet_seguro"] = pet

    limpo["observacoes"] = _texto_opcional(d.get("observacoes"), 500, "observacoes", erros)
    return limpo, erros


# ---------- clientes ----------
import re


def cpf_valido(cpf):
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for n in (9, 10):
        soma = sum(int(cpf[i]) * (n + 1 - i) for i in range(n))
        if int(cpf[n]) != (soma * 10 % 11) % 10:
            return False
    return True


def validar_cliente(d):
    erros, limpo = {}, {}
    nome = (d.get("nome") or "").strip()
    if not 2 <= len(nome) <= 100:
        erros["nome"] = "Informe de 2 a 100 caracteres."
    limpo["nome"] = nome

    email = (d.get("email") or "").strip().lower()
    if len(email) > 150 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        erros["email"] = "E-mail inválido."
    limpo["email"] = email

    cpf = re.sub(r"\D", "", str(d.get("cpf") or ""))
    if not cpf_valido(cpf):
        erros["cpf"] = "CPF inválido."
    limpo["cpf"] = cpf

    telefone = re.sub(r"\D", "", str(d.get("telefone") or ""))
    if telefone and len(telefone) not in (10, 11):
        erros["telefone"] = "Informe DDD + número (10 ou 11 dígitos)."
    limpo["telefone"] = telefone or None

    limpo["cidade"] = _texto_opcional(d.get("cidade"), 80, "cidade", erros)
    return limpo, erros
