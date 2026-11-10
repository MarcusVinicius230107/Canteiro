const pedido = new URLSearchParams(location.search).get("m");
const m = ["vendas", "estoque", "financeiro"].includes(pedido) ? pedido : "vendas";

(async () => {
  document.body.dataset.titulo = "menu." + m;
  $("titulo-modulo").dataset.i18n = "menu." + m;
  $("texto-modulo").dataset.i18n = "modulo." + m + ".texto";
  if (!(await iniciarPagina())) return;
  const listar = () => $("previstos").replaceChildren(
    ...I18n.t("modulo." + m + ".previsto").split("|").map(t => {
      const li = document.createElement("li");
      li.textContent = t;
      return li;
    }));
  listar();
  document.addEventListener("idioma", listar);
})();
