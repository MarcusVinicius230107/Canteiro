const CAMPOS = ["nome", "email", "cpf", "telefone", "cidade"];
const id = new URLSearchParams(location.search).get("id");

function cpfValido(cpf) {
  cpf = cpf.replace(/\D/g, "");
  if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) return false;
  for (const n of [9, 10]) {
    let soma = 0;
    for (let i = 0; i < n; i++) soma += Number(cpf[i]) * (n + 1 - i);
    if (Number(cpf[n]) !== (soma * 10 % 11) % 10) return false;
  }
  return true;
}

function validar(d) {
  const e = {};
  if (d.nome.length < 2 || d.nome.length > 100) e.nome = "val.nome";
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email)) e.email = "val.email";
  if (!cpfValido(d.cpf)) e.cpf = "val.cpf";
  const tel = d.telefone.replace(/\D/g, "");
  if (tel && ![10, 11].includes(tel.length)) e.telefone = "val.telefone";
  return e;
}

function mostrarErros(erros) {
  for (const c of CAMPOS) {
    $("erro-" + c).textContent = erros[c] ? I18n.t(erros[c]) : "";
    $(c).setAttribute("aria-invalid", erros[c] ? "true" : "false");
  }
}

(async () => {
  if (!pode("administrador", "vendedor")) { location.href = "clientes.html"; return; }
  $("titulo-pagina").dataset.i18n = id ? "cliente.titulo_editar" : "cliente.titulo_novo";
  if (!(await iniciarPagina())) return;

  if (id) {
    try {
      const c = await api("/api/clientes/" + id);
      for (const k of CAMPOS) $(k).value = c[k] ?? "";
    } catch (e) { mostrar($("msg"), textoErro(e), "erro"); }
  }

  $("form").addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const d = Object.fromEntries(CAMPOS.map(c => [c, $(c).value.trim()]));
    const erros = validar(d);
    mostrarErros(erros);
    if (Object.keys(erros).length) { mostrar($("msg"), I18n.t("erro.validacao"), "erro"); return; }
    try {
      await api(id ? "/api/clientes/" + id : "/api/clientes", { metodo: id ? "PUT" : "POST", corpo: d });
      sessionStorage.setItem("aviso", "cliente.salvo");
      location.href = "clientes.html";
    } catch (e) {
      mostrarErros(Object.fromEntries(Object.keys(e.detalhes).map(k => [k, "erro.validacao"])));
      mostrar($("msg"), textoErro(e), "erro");
    }
  });
})();
