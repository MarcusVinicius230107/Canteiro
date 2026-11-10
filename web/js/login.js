(async () => {
  await iniciarPagina({ publica: true });
  if (new URLSearchParams(location.search).has("expirou")) mostrar($("msg"), I18n.t("login.expirou"), "erro");
  $("form").addEventListener("submit", async (ev) => {
    ev.preventDefault();
    try {
      const r = await api("/api/auth/login", { metodo: "POST", auth: false, corpo: { email: $("email").value, senha: $("senha").value } });
      localStorage.setItem("token", r.token);
      localStorage.setItem("usuario", JSON.stringify(r.usuario));
      location.href = "index.html";
    } catch (e) { mostrar($("msg"), textoErro(e), "erro"); }
  });
})();
