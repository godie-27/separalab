/* SEPARALAB · página «Retos». */
"use strict";
(() => {
  const { h, api, aviso, vaciar, fmt } = SL;
  const RETOS = SL.leerJSON("datos-retos");
  const SUST = Object.fromEntries(SL.leerJSON("datos-sustancias").map(s => [s.clave, s]));
  const lista = document.getElementById("lista-retos");
  const zona = document.getElementById("reto");
  const pestanas = [...document.querySelectorAll(".pestanas button")];
  let nivel = "";
  let actual = null;

  const NOMBRE_METODO = {
    magnetismo: "magnetismo", decantacion: "decantación", filtracion: "filtración", sedimentacion: "sedimentación",
    destilacion: "destilación simple", destilacion_fraccionada: "destilación fraccionada", evaporacion: "evaporación",
    cristalizacion: "cristalización", recristalizacion: "recristalización", cromatografia: "cromatografía",
  };

  function pintarLista() {
    vaciar(lista);
    RETOS.filter(r => !nivel || r.nivel === nivel).forEach(r => {
      lista.append(h("button", { type: "button", "aria-current": String(actual === r.id),
        onclick: () => abrir(r.id) }, h("span", { clase: "nivel " + r.nivel, texto: r.nivel_nombre }), " ", h("b", { texto: r.titulo })));
    });
  }

  pestanas.forEach(b => b.addEventListener("click", () => {
    nivel = b.dataset.nivel;
    pestanas.forEach(x => x.setAttribute("aria-selected", String(x === b)));
    pintarLista();
  }));

  document.getElementById("boton-aleatorio").addEventListener("click", () => {
    const candidatos = RETOS.filter(r => (!nivel || r.nivel === nivel) && r.id !== actual);
    const pool = candidatos.length ? candidatos : RETOS.filter(r => !nivel || r.nivel === nivel);
    if (pool.length) abrir(pool[Math.floor(Math.random() * pool.length)].id);
  });

  function abrir(id) {
    const r = RETOS.find(x => x.id === id);
    if (!r) return;
    actual = id;
    history.replaceState(null, "", "?reto=" + id);
    pintarLista();
    vaciar(zona);
    const ficha = h("article", { clase: "hoja" });
    ficha.append(h("p", {}, h("span", { clase: "nivel " + r.nivel, texto: r.nivel_nombre }), " ", h("span", { clase: "atenuado pequeno", texto: "Fuente: " + r.fuente })),
      h("h2", { texto: r.titulo }), h("p", { texto: r.enunciado }));
    const chips = h("p", {}, h("b", { texto: "Componentes: " }), r.sustancias.map(k => {
      const cant = r.cantidades && r.cantidades[k];
      const unidad = SUST[k].estado === "liquido" ? "mL" : "g";
      const chip = h("span", { clase: "chip" }, h("i"), SUST[k].nombre + (cant ? ` · ${fmt(cant, cant % 1 ? 1 : 0)} ${unidad}` : ""));
      chip.firstChild.style.background = SL.color(k);
      return chip;
    }));
    ficha.append(chips, h("p", {}, h("b", { texto: "Métodos permitidos: " }), r.permitidos.map(m => NOMBRE_METODO[m]).join(", ") + "."));
    if (!r.recuperar_disolvente) ficha.append(aviso("info", null, "En este reto no hace falta recuperar el agua."));
    if (r.tabla_solubilidad.length) {
      const t = h("table", { clase: "dato-tabla" }, h("thead", {}, h("tr", {}, ["Sustancia", "Solubilidad a 20 °C", "a 80 °C", "Unidad"].map(x => h("th", { texto: x })))),
        h("tbody", {}, r.tabla_solubilidad.map(d => h("tr", {}, h("td", { texto: d.sal }), h("td", { clase: "num", texto: fmt(d.s20) }), h("td", { clase: "num", texto: fmt(d.s80) }), h("td", { texto: d.unidad })))));
      ficha.append(h("h3", { texto: "Datos del enunciado" }), h("div", { style: "overflow-x:auto" }, t));
    }
    if (r.cantidades && !r.usar_cantidades) {
      ficha.append(aviso("info", null, "Este reto se corrige de forma cualitativa, como pide el enunciado. El reto «¿Cristaliza solo el sulfato de cobre?» comprueba las cantidades."));
    }
    const pistas = h("div", { "aria-live": "polite" });
    let nivelPista = 0;
    const botonPista = h("button", { clase: "boton discreto", type: "button", texto: `Pista general (${r.num_pistas})`, disabled: !r.num_pistas, onclick: async () => {
      nivelPista += 1;
      try {
        const p = await api(`/api/retos/${r.id}/pista`, { nivel: nivelPista });
        pistas.append(aviso("info", `Pista ${Math.min(nivelPista, p.total)} de ${p.total}`, p.texto));
        if (nivelPista >= p.total) botonPista.disabled = true;
      } catch (e) { pistas.append(aviso("error", null, e.message)); }
    } });
    const practica = h("div", { style: "margin-top:14px" });
    const botonEmpezar = h("button", { clase: "boton", type: "button", texto: "Resolver este reto", onclick: () => {
      botonEmpezar.disabled = true;
      SL.Practica(practica, { reto: r.id }, {
        solucion: () => api(`/api/retos/${r.id}/solucion`),
        alReiniciar: () => abrir(r.id),
      });
    } });
    ficha.append(h("div", { clase: "botones", style: "margin-top:12px" }, botonEmpezar, botonPista,
      h("button", { clase: "boton discreto", type: "button", texto: "Ver la solución", onclick: async ev => {
        ev.currentTarget.disabled = true;
        try { SL.renderPlan(practica, await api(`/api/retos/${r.id}/solucion`), { titulo: "Solución propuesta" }); }
        catch (e) { practica.append(aviso("error", null, e.message)); }
      } })), pistas);
    r.preguntas.forEach((p, i) => {
      const caja = h("div", { clase: "pregunta" }, h("h3", { texto: "Pregunta de razonamiento" + (r.preguntas.length > 1 ? " " + (i + 1) : "") }), h("p", { texto: p.pregunta }));
      const opciones = h("div", { clase: "opciones" });
      const res = h("div", { "aria-live": "polite" });
      p.opciones.forEach((o, j) => opciones.append(h("button", { clase: "opcion", type: "button", texto: o, onclick: async () => {
        try {
          const c = await api(`/api/retos/${r.id}/pregunta`, { indice: i, opcion: j });
          vaciar(res).append(aviso(c.correcta ? "bien" : "error", c.correcta ? "¡Correcto!" : "Respuesta correcta: " + c.respuesta, c.explicacion));
          [...opciones.children].forEach((b, k) => { b.disabled = true; if (k === j) b.setAttribute("aria-pressed", "true"); });
        } catch (e) { vaciar(res).append(aviso("error", null, e.message)); }
      } })));
      caja.append(opciones, res);
      ficha.append(caja);
    });
    zona.append(ficha, practica);
  }

  pintarLista();
  const inicial = new URLSearchParams(location.search).get("reto");
  if (inicial) abrir(inicial);
})();
