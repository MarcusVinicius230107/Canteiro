const estado = { pagina: 1, busca: "", dados: null };
const formatarCpf = (c) => c.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, "$1.$2.$3-$4");

function card(c) {
  const li = document.createElement("li");
  li.className = "card";
  const h = document.createElement("h2");
  h.textContent = c.nome;
  const info = document.createElement("p");
  info.textContent = [formatarCpf(c.cpf), c.email, c.cidade].filter(Boolean).join(" · ");
  const acoes = document.createElement("div");
  acoes.className = "acoes";
  if (pode("administrador", "vendedor")) acoes.append(botao("clientes.editar", "btn-sec", () => { location.href = "cliente.html?id=" + c.id; }));
  if (pode("administrador")) acoes.append(botao("clientes.excluir", "btn-perigo", () => excluir(c)));
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
  try { estado.dados = await api("/api/clientes?" + q); desenhar(); }
  catch (e) { mostrar($("msg"), textoErro(e), "erro"); }
}

async function excluir(c) {
  if (!confirm(I18n.t("clientes.confirmar", { nome: c.nome }))) return;
  try {
    await api("/api/clientes/" + c.id, { metodo: "DELETE" });
    if (estado.dados.itens.length === 1 && estado.pagina > 1) estado.pagina--;
    await carregar();
    mostrar($("msg"), I18n.t("clientes.excluido"), "ok");
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
  $("anterior").addEventListener("click", () => { estado.pagina--; carregar(); });
  $("proxima").addEventListener("click", () => { estado.pagina++; carregar(); });
  document.addEventListener("idioma", () => estado.dados && desenhar());
  carregar();
})();
