const $ = (id) => document.getElementById(id);

const Sessao = {
  token: () => localStorage.getItem("token"),
  usuario: () => JSON.parse(localStorage.getItem("usuario") || "{}"),
  sair() { localStorage.removeItem("token"); localStorage.removeItem("usuario"); location.href = "login.html"; },
};
const pode = (...perfis) => perfis.includes(Sessao.usuario().perfil);

class ErroApi extends Error {
  constructor(codigo, mensagem, detalhes) {
    super(mensagem || codigo);
    this.codigo = codigo;
    this.detalhes = detalhes || {};
  }
}

let pendentes = 0;
function barra(ligar) {
  pendentes += ligar ? 1 : -1;
  $("barra").hidden = pendentes <= 0;
}

// Todas as chamadas à API passam por aqui: token, indicador de carregamento e erros.
async function api(caminho, { metodo = "GET", corpo, auth = true } = {}) {
  barra(true);
  try {
    const cab = { "Content-Type": "application/json" };
    if (auth) cab.Authorization = "Bearer " + Sessao.token();
    let resp;
    try {
      resp = await fetch(CONFIG.API_URL + caminho, { method: metodo, headers: cab, body: corpo && JSON.stringify(corpo) });
    } catch { throw new ErroApi("rede"); }
    if (resp.status === 204) return null;
    const dados = await resp.json().catch(() => ({}));
    if (!resp.ok) {
      const e = dados.erro || {};
      if (resp.status === 401 && auth) { // token expirado ou inválido
        localStorage.removeItem("token");
        localStorage.removeItem("usuario");
        location.href = "login.html?expirou=1";
      }
      throw new ErroApi(e.codigo || "erro_interno", e.mensagem, e.detalhes);
    }
    return dados;
  } finally { barra(false); }
}

function textoErro(e) {
  const chave = "erro." + e.codigo;
  return I18n.existe(chave) ? I18n.t(chave) : I18n.t("erro.erro_interno");
}

function mostrar(el, texto, tipo = "") {
  el.textContent = texto;
  el.className = "msg " + tipo;
}

function botao(chave, classe, aoClicar) {
  const b = document.createElement("button");
  b.type = "button";
  b.className = "btn " + classe;
  b.textContent = I18n.t(chave);
  b.addEventListener("click", aoClicar);
  return b;
}

// Módulos do ERP e os perfis que enxergam cada um no menu.
const TODOS = ["administrador", "vendedor", "financeiro"];
const MODULOS = [
  { grupo: "menu.cadastros", itens: [
    { href: "plantas.html", chave: "menu.plantas", perfis: TODOS },
    { href: "clientes.html", chave: "menu.clientes", perfis: TODOS },
  ] },
  { grupo: "menu.operacoes", itens: [
    { href: "modulo.html?m=vendas", chave: "menu.vendas", perfis: ["administrador", "vendedor"] },
    { href: "modulo.html?m=estoque", chave: "menu.estoque", perfis: ["administrador", "vendedor"] },
    { href: "modulo.html?m=financeiro", chave: "menu.financeiro", perfis: ["administrador", "financeiro"] },
  ] },
];

function montarShell() {
  const perfil = Sessao.usuario().perfil;
  const links = MODULOS.map(g => {
    const itens = g.itens.filter(i => i.perfis.includes(perfil));
    return itens.length
      ? `<h3 data-i18n="${g.grupo}"></h3>` + itens.map(i => `<a href="${i.href}" data-i18n="${i.chave}"></a>`).join("")
      : "";
  }).join("");
  document.body.insertAdjacentHTML("afterbegin", `
    <header class="topo"><div class="topo-in">
      <a class="marca" href="index.html">Canteiro</a>
      <button id="menu-btn" type="button" aria-expanded="false" aria-controls="menu" data-i18n-aria="menu.abrir">&#9776;</button>
      <div class="topo-dir">
        <span id="usuario" class="usuario"></span>
        <select id="idioma" aria-label="Idioma / Language"><option value="pt-BR">Português</option><option value="en">English</option></select>
        <button id="sair" type="button" class="link" data-i18n="menu.sair"></button>
      </div>
    </div></header>
    <div class="corpo"><nav id="menu" aria-label="Menu"><a href="index.html" data-i18n="menu.painel"></a>${links}</nav></div>`);
  document.querySelector(".corpo").append(document.querySelector("main"));
}

function atualizarUsuario() {
  const u = Sessao.usuario();
  $("usuario").textContent = `${u.nome} (${I18n.t("perfil." + u.perfil)})`;
}

async function iniciarPagina({ publica = false } = {}) {
  document.body.insertAdjacentHTML("afterbegin", '<div id="barra" hidden></div>');
  if (!publica && (!Sessao.token() || !Sessao.usuario().perfil)) { location.href = "login.html"; return false; }
  if (!publica) montarShell();
  await I18n.iniciar();
  if (publica) return true;

  atualizarUsuario();
  document.addEventListener("idioma", atualizarUsuario);
  $("menu-btn").addEventListener("click", () => {
    $("menu-btn").setAttribute("aria-expanded", $("menu").classList.toggle("aberto"));
  });
  $("sair").addEventListener("click", Sessao.sair);
  const atual = (location.pathname.split("/").pop() || "index.html") + location.search;
  document.querySelectorAll("#menu a").forEach(a => {
    if (a.getAttribute("href") === atual) a.setAttribute("aria-current", "page");
  });
  return true;
}
