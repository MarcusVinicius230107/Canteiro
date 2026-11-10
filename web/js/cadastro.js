const CAMPOS = ["nome_popular", "nome_cientifico", "categoria", "luminosidade", "preco", "estoque", "data_entrada", "pet_seguro", "observacoes"];
const id = new URLSearchParams(location.search).get("id");

function ler() {
  return {
    nome_popular: $("nome_popular").value.trim(),
    nome_cientifico: $("nome_cientifico").value.trim(),
    categoria: $("categoria").value,
    luminosidade: $("luminosidade").value,
    preco: $("preco").value,
    estoque: $("estoque").value,
    data_entrada: $("data_entrada").value,
    pet_seguro: $("pet_seguro").checked,
    observacoes: $("observacoes").value.trim(),
  };
}

function validar(d) {
  const e = {};
  if (d.nome_popular.length < 2 || d.nome_popular.length > 100) e.nome_popular = "val.nome";
  if (!d.categoria) e.categoria = "val.selecione";
  if (!d.luminosidade) e.luminosidade = "val.selecione";
  if (d.preco === "" || isNaN(d.preco) || Number(d.preco) < 0) e.preco = "val.preco";
  if (!/^\d+$/.test(d.estoque)) e.estoque = "val.estoque";
  if (!d.data_entrada) e.data_entrada = "val.data";
  if (d.observacoes.length > 500) e.observacoes = "val.obs";
  return e;
}

function mostrarErros(erros) {
  for (const c of CAMPOS) {
    if (!$("erro-" + c)) continue;
    $("erro-" + c).textContent = erros[c] ? I18n.t(erros[c]) : "";
    $(c).setAttribute("aria-invalid", erros[c] ? "true" : "false");
  }
}

function preencher(p) {
  for (const c of CAMPOS) {
    if (c === "pet_seguro") $(c).checked = p[c];
    else $(c).value = p[c] ?? "";
  }
}

(async () => {
  if (!pode("administrador", "vendedor")) { location.href = "plantas.html"; return; }
  $("titulo-pagina").dataset.i18n = id ? "cadastro.titulo_editar" : "cadastro.titulo_novo";
  if (!(await iniciarPagina())) return;

  if (id) {
    try { preencher(await api("/api/plantas/" + id)); }
    catch (e) { mostrar($("msg"), textoErro(e), "erro"); }
  } else {
    $("data_entrada").value = new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 10);
  }

  $("form").addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const d = ler();
    const erros = validar(d);
    mostrarErros(erros);
    if (Object.keys(erros).length) { mostrar($("msg"), I18n.t("erro.validacao"), "erro"); return; }
    try {
      const corpo = { ...d, preco: Number(d.preco), estoque: Number(d.estoque) };
      await api(id ? "/api/plantas/" + id : "/api/plantas", { metodo: id ? "PUT" : "POST", corpo });
      sessionStorage.setItem("aviso", "cadastro.salvo");
      location.href = "plantas.html";
    } catch (e) {
      mostrarErros(Object.fromEntries(Object.keys(e.detalhes).map(k => [k, "erro.validacao"])));
      mostrar($("msg"), textoErro(e), "erro");
    }
  });
})();
