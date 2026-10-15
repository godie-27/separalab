/* SEPARALAB · página «Resolver una mezcla». */
"use strict";

(() => {
  const { h, api, aviso, vaciar } = SL;
  const form = document.getElementById("form-mezcla");
  const resultado = document.getElementById("resultado");
  const errorForm = document.getElementById("error-form");
  const camposCantidades = document.getElementById("campos-cantidades");
  const casillas = [...form.querySelectorAll('input[name="sustancia"]')];
  const valores = {};

  document.querySelectorAll("[data-muestra]").forEach(el => { el.style.background = SL.color(el.dataset.muestra); });

  function seleccionadas() { return casillas.filter(c => c.checked); }

  function pintarCantidades() {
    const sel = seleccionadas();
    vaciar(camposCantidades);
    if (!sel.length) { camposCantidades.append(h("p", { clase: "pequeno atenuado", texto: "Primero elige las sustancias." })); return; }
    sel.forEach(c => {
      const id = "cant-" + c.value;
      const unidad = c.dataset.estado === "liquido" ? "mL" : "g";
      const input = h("input", { type: "number", id, min: "0", step: "any", inputmode: "decimal", value: valores[c.value] ?? "",
        oninput: e => { valores[c.value] = e.target.value; } });
      camposCantidades.append(h("div", { clase: "campo-linea" }, h("label", { for: id, texto: c.dataset.nombre }), input, h("span", { texto: unidad })));
    });
    camposCantidades.append(h("p", { clase: "pequeno atenuado", texto: "Deja todo vacío para un análisis cualitativo. Los colorantes no necesitan cantidad." }));
  }
  casillas.forEach(c => c.addEventListener("change", pintarCantidades));

  document.getElementById("boton-limpiar").addEventListener("click", () => {
    casillas.forEach(c => { c.checked = false; });
    Object.keys(valores).forEach(k => delete valores[k]);
    pintarCantidades();
    vaciar(errorForm);
  });

  function leerCantidades(claves) {
    const salida = {};
    claves.forEach(k => { if (valores[k] !== undefined && String(valores[k]).trim() !== "") salida[k] = String(valores[k]).trim(); });
    return Object.keys(salida).length ? salida : null;
  }

  async function resolver(cuerpo, boton) {
    vaciar(errorForm);
    boton.disabled = true;
    const textoAnterior = boton.textContent;
    boton.textContent = "Analizando…";
    try {
      const plan = await api("/api/resolver", cuerpo);
      SL.renderPlan(resultado, plan);
      if (window.matchMedia("(max-width: 960px)").matches) resultado.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (e) {
      errorForm.append(aviso("error", "No se pudo resolver", e.message));
    } finally {
      boton.disabled = false;
      boton.textContent = textoAnterior;
    }
  }

  form.addEventListener("submit", ev => {
    ev.preventDefault();
    const claves = seleccionadas().map(c => c.value);
    if (!claves.length) { vaciar(errorForm).append(aviso("error", null, "Elige al menos una sustancia.")); return; }
    const permitidos = [...form.querySelectorAll('input[name="permitido"]:checked')].map(c => c.value);
    if (!permitidos.length) { vaciar(errorForm).append(aviso("error", null, "Permite al menos un método de separación.")); return; }
    resolver({
      sustancias: claves,
      cantidades: leerCantidades(claves),
      permitidos,
      recuperar_disolvente: document.getElementById("recuperar").checked,
    }, document.getElementById("boton-resolver"));
  });

  // Enlace directo: /resolver?m=agua,aceite,arena
  const param = new URLSearchParams(location.search).get("m");
  if (param) {
    param.split(",").forEach(k => { const c = casillas.find(x => x.value === k); if (c) c.checked = true; });
    pintarCantidades();
    if (seleccionadas().length) form.requestSubmit();
  }
})();
