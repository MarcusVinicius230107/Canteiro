let dados = null;

function saudar() { $("ola").textContent = I18n.t("painel.ola", { nome: Sessao.usuario().nome }); }

function desenhar() {
  const linhas = [["painel.plantas", dados.plantas], ["painel.estoque", dados.estoque],
                  ["painel.baixo", dados.estoque_baixo], ["painel.clientes", dados.clientes]];
  $("indicadores").replaceChildren(...linhas.map(([chave, valor]) => {
    const li = document.createElement("li");
    li.className = "card indicador";
    const rotulo = document.createElement("span");
    rotulo.textContent = I18n.t(chave);
    const numero = document.createElement("strong");
    numero.textContent = I18n.numero(valor);
    li.append(rotulo, numero);
    return li;
  }));
}

(async () => {
  if (!(await iniciarPagina())) return;
  saudar();
  document.addEventListener("idioma", () => { saudar(); if (dados) desenhar(); });
  try { dados = await api("/api/painel"); desenhar(); }
  catch (e) { mostrar($("msg"), textoErro(e), "erro"); }
})();
