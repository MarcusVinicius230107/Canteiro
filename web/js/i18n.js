const I18n = {
  idioma: localStorage.getItem("idioma") || (navigator.language.startsWith("en") ? "en" : "pt-BR"),
  dic: {},
  async carregar() { this.dic = await (await fetch(`i18n/${this.idioma}.json`)).json(); },
  existe(chave) { return chave in this.dic; },
  t(chave, vars = {}) {
    let s = this.dic[chave] ?? chave;
    for (const k in vars) s = s.replace(`{${k}}`, vars[k]);
    return s;
  },
  moeda(v) { return new Intl.NumberFormat(this.idioma, { style: "currency", currency: "BRL" }).format(v); },
  numero(v) { return new Intl.NumberFormat(this.idioma).format(v); },
  data(iso) {
    const [a, m, d] = iso.split("-").map(Number);
    return new Intl.DateTimeFormat(this.idioma).format(new Date(a, m - 1, d));
  },
  aplicar() {
    document.documentElement.lang = this.idioma;
    document.querySelectorAll("[data-i18n]").forEach(e => e.textContent = this.t(e.dataset.i18n));
    document.querySelectorAll("[data-i18n-ph]").forEach(e => e.placeholder = this.t(e.dataset.i18nPh));
    document.querySelectorAll("[data-i18n-aria]").forEach(e => e.setAttribute("aria-label", this.t(e.dataset.i18nAria)));
    document.title = this.t(document.body.dataset.titulo) + " · Canteiro";
  },
  async iniciar() {
    await this.carregar();
    this.aplicar();
    const sel = document.getElementById("idioma");
    if (!sel) return;
    sel.value = this.idioma;
    sel.addEventListener("change", async () => {
      this.idioma = sel.value;
      localStorage.setItem("idioma", this.idioma);
      await this.carregar();
      this.aplicar();
      document.dispatchEvent(new Event("idioma"));
    });
  },
};
