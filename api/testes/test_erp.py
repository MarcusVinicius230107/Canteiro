import os
import unittest

from werkzeug.security import generate_password_hash

from app import create_app, db, preparar_banco

CLIENTE = {"nome": "Maria Souza", "email": "maria@exemplo.com", "cpf": "529.982.247-25",
           "telefone": "(19) 99999-0000", "cidade": "Americana"}
PLANTA = {"nome_popular": "Jiboia", "categoria": "interior", "luminosidade": "sombra",
          "preco": 29.9, "estoque": 3}


class TestERP(unittest.TestCase):
    @classmethod
    def _cab(cls, email, senha):
        r = cls.c.post("/api/auth/login", json={"email": email, "senha": senha})
        return {"Authorization": "Bearer " + r.json["token"]}

    @classmethod
    def setUpClass(cls):
        preparar_banco()
        for nome, email, perfil in (("Vera", "vendedor@teste.local", "vendedor"),
                                    ("Fábio", "financeiro@teste.local", "financeiro")):
            db.executar("INSERT INTO usuarios (nome, email, senha_hash, perfil) VALUES (%s,%s,%s,%s) "
                        "ON CONFLICT (email) DO NOTHING",
                        (nome, email, generate_password_hash("senha123"), perfil), "nenhum")
        cls.c = create_app().test_client()
        cls.adm = cls._cab("admin@canteiro.local", os.environ.get("ADMIN_SENHA", "canteiro123"))
        cls.vend = cls._cab("vendedor@teste.local", "senha123")
        cls.fin = cls._cab("financeiro@teste.local", "senha123")

    def setUp(self):
        db.executar("DELETE FROM clientes", resultado="nenhum")
        db.executar("DELETE FROM plantas", resultado="nenhum")

    def test_cliente_crud(self):
        r = self.c.post("/api/clientes", json=CLIENTE, headers=self.adm)
        self.assertEqual((r.status_code, r.json["cpf"]), (201, "52998224725"))
        cid = r.json["id"]
        r = self.c.put(f"/api/clientes/{cid}", json={**CLIENTE, "cidade": "Campinas"}, headers=self.adm)
        self.assertEqual(r.json["cidade"], "Campinas")
        self.assertEqual(self.c.get("/api/clientes?busca=maria", headers=self.adm).json["total"], 1)
        self.assertEqual(self.c.get("/api/clientes?busca=52998", headers=self.adm).json["total"], 1)
        self.assertEqual(self.c.delete(f"/api/clientes/{cid}", headers=self.adm).status_code, 204)
        self.assertEqual(self.c.delete(f"/api/clientes/{cid}", headers=self.adm).status_code, 404)

    def test_validacao_cliente(self):
        r = self.c.post("/api/clientes", json={**CLIENTE, "cpf": "111.111.111-11", "email": "x"}, headers=self.adm)
        self.assertEqual(r.status_code, 400)
        self.assertIn("cpf", r.json["erro"]["detalhes"])
        self.assertIn("email", r.json["erro"]["detalhes"])

    def test_duplicado(self):
        self.c.post("/api/clientes", json=CLIENTE, headers=self.adm)
        r = self.c.post("/api/clientes", json=CLIENTE, headers=self.adm)
        self.assertEqual((r.status_code, r.json["erro"]["codigo"]), (409, "duplicado"))

    def test_perfis(self):
        r = self.c.post("/api/clientes", json=CLIENTE, headers=self.vend)
        self.assertEqual(r.status_code, 201)
        r2 = self.c.delete(f"/api/clientes/{r.json['id']}", headers=self.vend)
        self.assertEqual((r2.status_code, r2.json["erro"]["codigo"]), (403, "sem_permissao"))
        self.assertEqual(self.c.post("/api/clientes", json=CLIENTE, headers=self.fin).status_code, 403)
        self.assertEqual(self.c.post("/api/plantas", json=PLANTA, headers=self.fin).status_code, 403)
        self.assertEqual(self.c.get("/api/clientes", headers=self.fin).status_code, 200)
        self.assertEqual(self.c.post("/api/plantas", json=PLANTA, headers=self.vend).status_code, 201)
        self.assertEqual(self.c.get("/api/logs", headers=self.vend).status_code, 403)

    def test_painel(self):
        self.c.post("/api/clientes", json=CLIENTE, headers=self.adm)
        self.c.post("/api/plantas", json=PLANTA, headers=self.adm)
        r = self.c.get("/api/painel", headers=self.fin)
        self.assertEqual(r.json, {"plantas": 1, "estoque": 3, "estoque_baixo": 1, "clientes": 1})

    def test_log_de_acoes(self):
        r = self.c.post("/api/clientes", json=CLIENTE, headers=self.adm)
        self.c.delete(f"/api/clientes/{r.json['id']}", headers=self.adm)
        itens = self.c.get("/api/logs", headers=self.adm).json["itens"]
        acoes = {i["acao"] for i in itens}
        self.assertTrue({"login", "incluir", "excluir"} <= acoes)
        self.assertEqual(itens[0]["usuario"], "admin@canteiro.local")


if __name__ == "__main__":
    unittest.main()
