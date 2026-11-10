const estado = { pagina: 1, busca: "", categoria: "", dados: null };

function card(p) {
  const li = document.createElement("li");
  li.className = "card";
  const h = document.createElement("h2");
  h.textContent = p.nome_popular;
  const info = document.createElement("p");
  info.textContent = `${I18n.t("cat." + p.categoria)} · ${I18n.moeda(p.preco)} · ${I18n.t("plantas.estoque", { n: I18n.numero(p.estoque) })}`;
  const acoes = document.createElement("div");
  acoes.className = "acoes";
  acoes.append(botao("plantas.detalhes", "btn-sec", () => detalhar(p.id)));
  if (pode("administrador", "vendedor")) acoes.append(botao("plantas.editar", "btn-sec", () => { location.href = "cadastro.html?id=" + p.id; }));
  if (pode("administrador")) acoes.append(botao("plantas.excluir", "btn-perigo", () => excluir(p)));
  li.append(h, info, acoes);
  return li;
}

function desenhar() {
  const d = estado.dados;
  $("lista").replaceChildren(...d.itens.map(card));
  $("vazio").hidden = d.itens.length > 0;
  $("pagina").textContent = I18n.t("plantas.pagina", { p: d.pagina, t: d.total_paginas });
  $("anterior").disabled = d.pagina <= 1;
  $("proxima").disabled = d.pagina >= d.total_paginas;
}

async function carregar() {
  const q = new URLSearchParams({ pagina: estado.pagina, por_pagina: 6 });
  if (estado.busca) q.set("busca", estado.busca);
  if (estado.categoria) q.set("categoria", estado.categoria);
  try {
    estado.dados = await api("/api/plantas?" + q);
    desenhar();
  } catch (e) { mostrar($("msg"), textoErro(e), "erro"); }
}

async function detalhar(id) {
  try {
    const p = await api("/api/plantas/" + id);
    const linhas = [
      ["campo.nome_cientifico", p.nome_cientifico || "—"],
      ["campo.categoria", I18n.t("cat." + p.categoria)],
      ["campo.luminosidade", I18n.t("luz." + p.luminosidade)],
      ["campo.preco", I18n.moeda(p.preco)],
      ["campo.estoque", I18n.numero(p.estoque)],
      ["campo.data_entrada", I18n.data(p.data_entrada)],
      ["campo.pet_seguro", I18n.t(p.pet_seguro ? "pet.sim" : "pet.nao")],
      ["campo.observacoes", p.observacoes || "—"],
    ];
    $("detalhe-titulo").textContent = p.nome_popular;
    $("detalhe-lista").replaceChildren(...linhas.flatMap(([chave, valor]) => {
      const dt = document.createElement("dt"), dd = document.createElement("dd");
      dt.textContent = I18n.t(chave);
      dd.textContent = valor;
      return [dt, dd];
    }));
    $("detalhe").showModal();
  } catch (e) { mostrar($("msg"), textoErro(e), "erro"); }
}

async function excluir(p) {
  if (!confirm(I18n.t("plantas.confirmar", { nome: p.nome_popular }))) return;
  try {
    await api("/api/plantas/" + p.id, { metodo: "DELETE" });
    if (estado.dados.itens.length === 1 && estado.pagina > 1) estado.pagina--;
    await carregar();
    mostrar($("msg"), I18n.t("plantas.excluida"), "ok");
  } catch (e) { mostrar($("msg"), textoErro(e), "erro"); }
}

(async () => {
  if (!(await iniciarPagina())) return;
  $("novo").hidden = !pode("administrador", "vendedor");
  const aviso = sessionStorage.getItem("aviso");
  if (aviso) { sessionStorage.removeItem("aviso"); mostrar($("msg"), I18n.t(aviso), "ok"); }

  let espera;
  $("busca").addEventListener("input", () => {
    clearTimeout(espera);
    espera = setTimeout(() => { estado.busca = $("busca").value.trim(); estado.pagina = 1; carregar(); }, 300);
  });
  $("categoria").addEventListener("change", () => { estado.categoria = $("categoria").value; estado.pagina = 1; carregar(); });
  $("anterior").addEventListener("click", () => { estado.pagina--; carregar(); });
  $("proxima").addEventListener("click", () => { estado.pagina++; carregar(); });
  document.addEventListener("idioma", () => estado.dados && desenhar());
  carregar();
})();
