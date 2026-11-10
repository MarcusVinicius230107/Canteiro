import datetime
import os
import unittest

import jwt

from app import auth, create_app, db, preparar_banco

VALIDA = {
    "nome_popular": "Samambaia", "nome_cientifico": "Nephrolepis exaltata",
    "categoria": "interior", "luminosidade": "meia_sombra", "preco": 39.9,
    "estoque": 12, "data_entrada": "2026-11-01", "pet_seguro": True,
    "observacoes": "Gosta de umidade",
}


class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        preparar_banco()
        cls.c = create_app().test_client()
        r = cls.c.post("/api/auth/login", json={
            "email": "admin@canteiro.local",
            "senha": os.environ.get("ADMIN_SENHA", "canteiro123")})
        cls.h = {"Authorization": "Bearer " + r.json["token"]}

    def setUp(self):
        db.executar("DELETE FROM plantas", resultado="nenhum")

    def test_login_invalido(self):
        r = self.c.post("/api/auth/login", json={"email": "x@x.com", "senha": "errada"})
        self.assertEqual(r.status_code, 401)
        self.assertEqual(r.json["erro"]["codigo"], "credenciais_invalidas")

    def test_exige_token(self):
        self.assertEqual(self.c.get("/api/plantas").status_code, 401)
        r = self.c.get("/api/plantas", headers={"Authorization": "Bearer lixo"})
        self.assertEqual(r.json["erro"]["codigo"], "token_invalido")

    def test_token_expirado(self):
        passado = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1)
        token = jwt.encode({"sub": "1", "exp": passado}, auth.segredo(), algorithm="HS256")
        r = self.c.get("/api/plantas", headers={"Authorization": "Bearer " + token})
        self.assertEqual(r.json["erro"]["codigo"], "token_expirado")

    def test_crud_completo(self):
        r = self.c.post("/api/plantas", json=VALIDA, headers=self.h)
        self.assertEqual(r.status_code, 201)
        pid = r.json["id"]
        self.assertEqual(r.json["data_entrada"], "2026-11-01")
        self.assertEqual(self.c.get(f"/api/plantas/{pid}", headers=self.h).status_code, 200)
        r = self.c.put(f"/api/plantas/{pid}", json={**VALIDA, "estoque": 3}, headers=self.h)
        self.assertEqual((r.status_code, r.json["estoque"]), (200, 3))
        self.assertEqual(self.c.delete(f"/api/plantas/{pid}", headers=self.h).status_code, 204)
        self.assertEqual(self.c.get(f"/api/plantas/{pid}", headers=self.h).status_code, 404)
        self.assertEqual(self.c.delete(f"/api/plantas/{pid}", headers=self.h).status_code, 404)

    def test_validacao(self):
        r = self.c.post("/api/plantas", json={"preco": -5, "estoque": "x"}, headers=self.h)
        self.assertEqual(r.status_code, 400)
        detalhes = r.json["erro"]["detalhes"]
        for campo in ("nome_popular", "categoria", "luminosidade", "preco", "estoque"):
            self.assertIn(campo, detalhes)
        r = self.c.post("/api/plantas", data="não é json", headers=self.h)
        self.assertEqual(r.json["erro"]["codigo"], "corpo_invalido")

    def test_busca_e_paginacao(self):
        for nome in ("Samambaia", "Jiboia", "Sálvia"):
            self.c.post("/api/plantas", json={**VALIDA, "nome_popular": nome}, headers=self.h)
        r = self.c.get("/api/plantas?por_pagina=2", headers=self.h)
        self.assertEqual((r.json["total"], r.json["total_paginas"], len(r.json["itens"])), (3, 2, 2))
        r = self.c.get("/api/plantas?busca=jibo", headers=self.h)
        self.assertEqual([i["nome_popular"] for i in r.json["itens"]], ["Jiboia"])
        r = self.c.get("/api/plantas?categoria=jardim", headers=self.h)
        self.assertEqual(r.json["total"], 0)

    def test_sql_injection_nao_funciona(self):
        r = self.c.get("/api/plantas?busca=' OR '1'='1", headers=self.h)
        self.assertEqual((r.status_code, r.json["total"]), (200, 0))

    def test_erros_em_json_e_cors(self):
        r = self.c.get("/api/nao-existe")
        self.assertEqual((r.status_code, r.json["erro"]["codigo"]), (404, "not_found"))
        r = self.c.options("/api/plantas", headers={
            "Origin": "http://localhost:3000", "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization"})
        self.assertIn("Access-Control-Allow-Origin", r.headers)


if __name__ == "__main__":
    unittest.main()
