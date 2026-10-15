/* SEPARALAB · módulo de cromatografía: dibujo de cromatogramas, calculadora,
   ejercicios de las fichas, identificación, preguntas y simulación. */
"use strict";
(() => {
  const { h, s, api, aviso, vaciar, fmt } = SL;
  const EJ = SL.leerJSON("datos-ejercicios");
  const PREG = SL.leerJSON("datos-preguntas");
  const IDENT = SL.leerJSON("datos-ident");
  const SIM = SL.leerJSON("datos-sim");

  /* ------------------------------------------------------------ dibujo de un cromatograma
     carriles: [{manchas: [{distancia, color, nombre}], etiqueta}]  (distancias en cm) */
  function cromatograma({ frente, carriles, tecnica = "papel", medidas = true, frenteVisible = null, etiqueta = "Cromatograma" }) {
    const n = carriles.length;
    const anchoTira = Math.max(70, 46 * n);
    const W = anchoTira + 174, H = 320, x0 = 84, origen = 278, arriba = 26;
    const escala = (origen - arriba - 14) / (frente || 1);
    const fv = frenteVisible === null ? frente : frenteVisible;
    const svg = s("svg", { viewBox: `0 0 ${W} ${H}`, class: "croma" + (n > 1 ? " croma-ancho" : ""), role: "img", "aria-label": etiqueta });
    svg.append(s("rect", { x: x0, y: arriba - 10, width: anchoTira, height: origen - arriba + 36, rx: tecnica === "TLC" ? 3 : 1,
      fill: tecnica === "TLC" ? "#eef1f4" : "#ffffff", stroke: "#14243b", "stroke-width": 1.6 }));
    // zona mojada por el disolvente
    const yFrente = origen - fv * escala;
    svg.append(s("rect", { x: x0 + 1, y: yFrente, width: anchoTira - 2, height: origen - yFrente + 25, fill: "#ede6fb", opacity: .7 }));
    svg.append(s("line", { x1: x0, x2: x0 + anchoTira, y1: origen, y2: origen, stroke: "#14243b", "stroke-width": 1.3 }));
    svg.append(s("text", { x: x0 - 6, y: origen + 4, "text-anchor": "end", "font-size": 11, fill: "#4a5b70", texto: "origen" }));
    if (fv > 0) {
      svg.append(s("line", { x1: x0, x2: x0 + anchoTira, y1: yFrente, y2: yFrente, stroke: "#1d64c8", "stroke-width": 1.5, "stroke-dasharray": "5 3" }));
      svg.append(s("text", { x: x0 - 6, y: yFrente + 4, "text-anchor": "end", "font-size": 11, fill: "#1d64c8", texto: "frente" }));
    }
    if (medidas && fv > 0) {
      const xm = x0 - 70;
      svg.append(s("line", { x1: xm, x2: xm, y1: origen, y2: yFrente, stroke: "#1d64c8", "stroke-width": 1.2 }));
      svg.append(s("text", { x: xm - 4, y: (origen + yFrente) / 2, "text-anchor": "middle", "font-size": 11, fill: "#1d64c8",
        transform: `rotate(-90 ${xm - 4} ${(origen + yFrente) / 2})`, texto: fmt(frente, 1) + " cm" }));
    }
    carriles.forEach((carril, i) => {
      const cx = x0 + anchoTira * (i + .5) / n;
      svg.append(s("circle", { cx, cy: origen, r: 2, fill: "#14243b" }));
      if (carril.etiqueta) svg.append(s("text", { x: cx, y: origen + 22, "text-anchor": "middle", "font-size": 10.5, fill: "#4a5b70", texto: carril.etiqueta }));
      carril.manchas.forEach((m, k) => {
        const d = Math.min(m.distancia, fv);
        const cy = origen - d * escala;
        const r = 6 + Math.min(d, 10) * .25;
        svg.append(s("ellipse", { cx, cy, rx: r, ry: r * .8, fill: m.color || "#6b7b8f", opacity: .9, stroke: "#14243b", "stroke-width": .5 }));
        if (medidas && n === 1) {
          const xr = x0 + anchoTira + 10 + k * 7;
          svg.append(s("line", { x1: xr, x2: xr, y1: origen, y2: cy, stroke: m.color || "#6b7b8f", "stroke-width": 1.4 }));
          svg.append(s("line", { x1: cx + r, x2: xr, y1: cy, y2: cy, stroke: "#9aa8b6", "stroke-width": .8, "stroke-dasharray": "2 2" }));
          svg.append(s("text", { x: x0 + anchoTira + 44, y: cy + 4, "font-size": 11, fill: "#14243b", texto: `${fmt(m.distancia, 1)} cm` }));
        }
      });
    });
    return svg;
  }

  /* ------------------------------------------------------------ calculadora */
  const filas = document.getElementById("rf-filas");
  const COLORES = ["#e5484d", "#3e63dd", "#30a46c", "#f76b15", "#8e4ec6", "#12a594"];
  function anadirFila(nombre = "", distancia = "") {
    const i = filas.children.length;
    if (i >= 8) return;
    const fila = h("div", { clase: "calc-fila" },
      h("input", { type: "text", "aria-label": `Nombre de la mancha ${i + 1}`, value: nombre || `Mancha ${i + 1}` }),
      h("input", { type: "text", inputmode: "decimal", "aria-label": `Distancia de la mancha ${i + 1} en cm`, value: distancia }),
      h("button", { clase: "boton discreto", type: "button", "aria-label": "Quitar mancha", texto: "×", onclick: () => { fila.remove(); } }));
    filas.append(fila);
  }
  anadirFila("Mancha 1", "4,2");
  anadirFila("Mancha 2", "8,4");
  document.getElementById("rf-anadir").addEventListener("click", () => anadirFila());
  document.getElementById("form-rf").addEventListener("submit", async ev => {
    ev.preventDefault();
    const res = vaciar(document.getElementById("rf-resultado"));
    const dibujo = vaciar(document.getElementById("rf-dibujo"));
    const frente = document.getElementById("rf-frente").value;
    const manchas = [...filas.children].map(f => ({ nombre: f.children[0].value, distancia: f.children[1].value }));
    try {
      const r = await api("/api/rf", { frente, manchas });
      r.manchas.forEach(m => res.append(h("div", { clase: "pasos-calculo" },
        h("div", {}, h("b", { texto: m.nombre })), ...m.pasos.map(p => h("div", { texto: p })),
        h("div", { clase: "pequeno atenuado", texto: m.interpretacion }))));
      res.append(aviso("info", null, `Más afinidad por la fase estacionaria: ${r.mas_afin_estacionaria}. Más afinidad por la fase móvil: ${r.mas_afin_movil}.`,
        "El Rf no tiene unidades y depende de las condiciones del experimento."));
      const f = parseFloat(String(frente).replace(",", "."));
      dibujo.append(cromatograma({ frente: f, carriles: [{ manchas: r.manchas.map((m, i) => ({ distancia: m.rf_exacto * f, color: COLORES[i % COLORES.length] })) }],
        etiqueta: "Cromatograma con las distancias introducidas" }));
    } catch (e) { res.append(aviso("error", "Revisa los datos", e.message)); }
  });

  /* ------------------------------------------------------------ preguntas de opción múltiple */
  function preguntaOpciones(p) {
    const caja = h("div", { clase: "pregunta" }, h("p", {}, h("b", { texto: p.texto })));
    const opciones = h("div", { clase: "opciones" });
    const res = h("div", { "aria-live": "polite" });
    p.opciones.forEach((o, j) => opciones.append(h("button", { clase: "opcion", type: "button", texto: o, onclick: () => {
      const ok = j === p.correcta;
      vaciar(res).append(aviso(ok ? "bien" : "error", ok ? "¡Correcto!" : "Respuesta correcta: " + p.opciones[p.correcta], p.explicacion));
      [...opciones.children].forEach((b, k) => { b.disabled = true; if (k === j) b.setAttribute("aria-pressed", "true"); });
    } })));
    caja.append(opciones, res);
    return caja;
  }

  /* ------------------------------------------------------------ ejercicios de las fichas */
  const zonaEj = document.getElementById("ejercicios");
  EJ.forEach(e => {
    const art = h("article", { clase: "ejercicio-croma", style: "padding:16px 0;border-top:1px solid #d6e0e8" });
    art.append(h("div", {}, cromatograma({ frente: e.frente, tecnica: e.tecnica, carriles: [{ manchas: e.manchas }], etiqueta: e.titulo })));
    const der = h("div", {}, h("h3", { texto: e.titulo }), h("p", { clase: "atenuado", texto: e.condiciones }),
      h("p", { texto: `Frente del disolvente: ${fmt(e.frente, 1)} cm desde el origen.` }));
    e.pide.forEach(nombre => {
      const input = h("input", { type: "text", inputmode: "decimal", "aria-label": `Rf de ${nombre}`, placeholder: "Rf" });
      const res = h("p", { clase: "resultado-mini", "aria-live": "polite" });
      der.append(h("div", { clase: "respuesta-rf" }, h("span", { texto: nombre }), input,
        h("button", { clase: "boton secundario", type: "button", texto: "Comprobar", onclick: async () => {
          try {
            const r = await api("/api/rf/comprobar", { ejercicio: e.id, mancha: nombre, respuesta: input.value });
            vaciar(res).append(r.correcta ? "✔ Correcto. " : "✘ No es correcto. ", r.solucion.pasos.slice(1).join(" → "));
            res.style.color = r.correcta ? "#1b7a4c" : "#b3392a";
          } catch (err) { vaciar(res).append(err.message); res.style.color = "#b3392a"; }
        } })), res);
    });
    if (e.pregunta) der.append(preguntaOpciones(e.pregunta));
    if (e.nota_terminologia) der.append(h("p", { clase: "pequeno atenuado", texto: e.nota_terminologia }));
    der.append(h("p", { clase: "pequeno atenuado", texto: "Fuente: " + e.fuente }));
    art.append(der);
    zonaEj.append(art);
  });

  /* ------------------------------------------------------------ identificación */
  document.getElementById("ident-dibujo").append(cromatograma({
    frente: IDENT.frente, medidas: false, etiqueta: "Placa con patrones y muestra problema",
    carriles: [...IDENT.patrones.map(p => ({ manchas: [p], etiqueta: p.nombre.replace("Patrón ", "") })), { manchas: IDENT.muestra, etiqueta: "muestra" }],
  }));
  const identOpc = document.getElementById("ident-opciones");
  IDENT.patrones.forEach(p => identOpc.append(h("label", { clase: "casilla" }, h("input", { type: "checkbox", value: p.nombre }), h("span", { texto: p.nombre }))));
  document.getElementById("ident-comprobar").addEventListener("click", () => {
    const elegidos = [...identOpc.querySelectorAll("input:checked")].map(i => i.value).sort();
    const ok = JSON.stringify(elegidos) === JSON.stringify([...IDENT.correctos].sort());
    vaciar(document.getElementById("ident-resultado")).append(aviso(ok ? "bien" : "error", ok ? "¡Correcto!" : "Revisa la altura de cada mancha", IDENT.explicacion));
  });

  /* ------------------------------------------------------------ preguntas conceptuales */
  const zonaPreg = document.getElementById("conceptuales");
  PREG.forEach(p => zonaPreg.append(preguntaOpciones(p)));

  /* ------------------------------------------------------------ simulación */
  const sel = document.getElementById("sim-preset");
  const rango = document.getElementById("sim-tiempo");
  const dibujoSim = document.getElementById("sim-dibujo");
  const datosSim = document.getElementById("sim-datos");
  const FRENTE_SIM = 10;
  SIM.forEach((p, i) => sel.append(h("option", { value: String(i), texto: p.titulo })));
  let animacion = null;

  function pintarSim() {
    const p = SIM[Number(sel.value)];
    const t = Number(rango.value) / 100;
    const fv = FRENTE_SIM * t;
    vaciar(dibujoSim).append(cromatograma({
      frente: FRENTE_SIM, frenteVisible: fv, tecnica: p.tecnica, medidas: false, etiqueta: "Simulación: " + p.titulo,
      carriles: [{ manchas: p.manchas.map(m => ({ distancia: m.rf * fv, color: m.color })) }],
    }));
    document.getElementById("sim-condiciones").textContent = p.condiciones + (p.ilustrativo ? " Valores ilustrativos." : "");
    vaciar(datosSim);
    if (t >= .999) {
      datosSim.append(h("table", { clase: "dato-tabla" }, h("thead", {}, h("tr", {}, h("th", { texto: "Componente" }), h("th", { clase: "num", texto: "Rf" }))),
        h("tbody", {}, p.manchas.map(m => h("tr", {}, h("td", { texto: m.nombre }), h("td", { clase: "num", texto: fmt(m.rf, 2) }))))),
      h("p", { clase: "pequeno atenuado", texto: (p.ilustrativo ? "" : "Rf de la ficha en esas condiciones. ") + p.fuente }));
    } else {
      datosSim.append(h("p", { clase: "pequeno atenuado", texto: `Frente: ${fmt(fv, 1)} cm. Cada mancha ha recorrido siempre la misma fracción del frente.` }));
    }
  }
  function parar() { if (animacion) cancelAnimationFrame(animacion); animacion = null; document.getElementById("sim-play").textContent = "Iniciar"; }
  document.getElementById("sim-play").addEventListener("click", () => {
    if (animacion) return parar();
    if (Number(rango.value) >= 100) rango.value = 0;
    document.getElementById("sim-play").textContent = "Pausa";
    let previo = null;
    const paso = ts => {
      if (previo !== null) rango.value = Math.min(100, Number(rango.value) + (ts - previo) / 60);
      previo = ts;
      pintarSim();
      if (Number(rango.value) >= 100) return parar();
      animacion = requestAnimationFrame(paso);
    };
    animacion = requestAnimationFrame(paso);
  });
  document.getElementById("sim-reset").addEventListener("click", () => { parar(); rango.value = 0; pintarSim(); });
  rango.addEventListener("input", () => { parar(); pintarSim(); });
  sel.addEventListener("change", () => { parar(); rango.value = 0; pintarSim(); });
  pintarSim();
})();
