/* SEPARALAB · utilidades comunes (sin dependencias externas).
   Todo el texto se inserta con textContent: nunca se interpreta como HTML. */
"use strict";

const SL = (() => {
  const NS = "http://www.w3.org/2000/svg";

  /* ------------------------------------------------------------ DOM */
  function h(etiqueta, atributos, ...hijos) {
    const el = document.createElement(etiqueta);
    for (const [k, v] of Object.entries(atributos || {})) {
      if (v === null || v === undefined || v === false) continue;
      if (k === "clase") el.className = v;
      else if (k === "texto") el.textContent = v;
      else if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
      else el.setAttribute(k, v === true ? "" : v);
    }
    for (const hijo of hijos.flat()) {
      if (hijo === null || hijo === undefined || hijo === false) continue;
      el.append(hijo instanceof Node ? hijo : document.createTextNode(String(hijo)));
    }
    return el;
  }

  function s(etiqueta, atributos, ...hijos) {
    const el = document.createElementNS(NS, etiqueta);
    for (const [k, v] of Object.entries(atributos || {})) {
      if (v === null || v === undefined) continue;
      if (k === "texto") el.textContent = v;
      else el.setAttribute(k, v);
    }
    for (const hijo of hijos.flat()) if (hijo) el.append(hijo);
    return el;
  }

  function icono(id, clase) {
    const svg = s("svg", { "aria-hidden": "true", class: clase || "" });
    svg.append(s("use", { href: "#" + id }));
    return svg;
  }

  function vaciar(el) { while (el.firstChild) el.removeChild(el.firstChild); return el; }

  function aviso(tipo, titulo, ...texto) {
    return h("div", { clase: "aviso " + tipo, role: tipo === "error" ? "alert" : null },
      titulo ? h("strong", { texto: titulo }) : null,
      ...texto.filter(Boolean).map(t => (t instanceof Node ? t : h("p", { texto: t }))));
  }

  function fmt(n, dec = 1) {
    return Number(n).toFixed(dec).replace(".", ",");
  }

  /* ------------------------------------------------------------ API */
  async function api(url, cuerpo) {
    let respuesta;
    try {
      respuesta = await fetch(url, cuerpo === undefined ? {} : {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(cuerpo),
      });
    } catch (e) {
      throw new Error("No se pudo conectar con SEPARALAB. Comprueba tu conexión e inténtalo de nuevo.");
    }
    let datos = null;
    try { datos = await respuesta.json(); } catch (e) { /* respuesta no JSON */ }
    if (!respuesta.ok) {
      throw new Error((datos && datos.error) || `El servidor respondió con un error (${respuesta.status}).`);
    }
    if (datos === null) throw new Error("La respuesta del servidor no es válida.");
    return datos;
  }

  /* ------------------------------------------------------------ colores de las sustancias */
  const COLOR = {
    agua: "#a9d4f5", etanol: "#d9cdf5", aceite: "#f2c94c",
    arena: "#d8b98a", hierro: "#4b5563", azufre: "#f2d22e", sulfuro_de_hierro: "#3b3631",
    cloruro_de_sodio: "#ffffff", sulfato_de_cobre: "#eef2f5", sulfato_de_cobre_pentahidratado: "#2f80ed",
    arcilla: "#a7754a", carbonato_de_calcio: "#f7f7f2", oxido_de_hierro: "#a0451f", sacarosa: "#ffffff",
    colorante_a: "#12a594", colorante_b: "#d6409f",
  };
  const TINTE = {
    sulfato_de_cobre: "#5b9ff0", sulfato_de_cobre_pentahidratado: "#5b9ff0",
    colorante_a: "#2bb3a3", colorante_b: "#e06ab4",
  };
  const color = clave => COLOR[clave] || "#c2cbd4";

  function mezclarColores(a, b, t) {
    const pa = parseInt(a.slice(1), 16), pb = parseInt(b.slice(1), 16);
    const c = [16, 8, 0].map(sh => Math.round(((pa >> sh) & 255) * (1 - t) + ((pb >> sh) & 255) * t));
    return "#" + c.map(x => x.toString(16).padStart(2, "0")).join("");
  }

  /* ------------------------------------------------------------ vaso: dibujo de una fracción */
  function vaso(datos, opciones = {}) {
    const fases = (datos && datos.fases) || [];
    const solidos = (datos && datos.solidos) || [];
    const svg = s("svg", { viewBox: "0 0 100 120", class: "vaso" + (opciones.grande ? " grande" : ""), role: "img",
      "aria-label": opciones.etiqueta || "Vaso con la fracción" });
    const idClip = "clip-" + Math.random().toString(36).slice(2, 9);
    svg.append(s("defs", {}, s("clipPath", { id: idClip }, s("path", { d: "M23 14v86a8 8 0 0 0 8 8h38a8 8 0 0 0 8-8V14z" }))));
    const g = s("g", { "clip-path": `url(#${idClip})` });
    svg.append(g);
    const fondo = 108;
    const alturaLiquido = fases.length ? 64 : 0;
    let y = fondo - alturaLiquido;
    const alto = fases.length ? alturaLiquido / fases.length : 0;
    fases.forEach((fase, i) => {
      let c = fase.liquidos.includes("agua") ? COLOR.agua : color(fase.liquidos[0]);
      if (fase.liquidos.length > 1 && !fase.liquidos.includes("agua")) c = mezclarColores(c, color(fase.liquidos[1]), .4);
      if (fase.liquidos.includes("etanol") && fase.liquidos.includes("agua")) c = mezclarColores(c, COLOR.etanol, .45);
      const tintes = fase.solutos.filter(x => TINTE[x]).map(x => TINTE[x]);
      tintes.forEach(t => { c = mezclarColores(c, t, .55); });
      g.append(s("rect", { x: 20, y: y, width: 60, height: alto + 1, fill: c }));
      if (i > 0) g.append(s("line", { x1: 20, x2: 80, y1: y, y2: y, stroke: "#14243b", "stroke-width": .8, "stroke-dasharray": "3 2" }));
      const incoloros = fase.solutos.filter(x => !TINTE[x]);
      incoloros.forEach((x, k) => {
        for (let j = 0; j < 5; j++) {
          g.append(s("rect", { x: 30 + ((j * 11 + k * 5) % 40), y: y + 5 + ((j * 7 + k * 9) % Math.max(alto - 10, 4)),
            width: 2.2, height: 2.2, fill: "#ffffff", stroke: "#6b7b8f", "stroke-width": .4, opacity: .85 }));
        }
      });
      y += alto;
    });
    // Sólidos: sedimento en el fondo (o montón si no hay líquido)
    const filas = fases.length ? 1 : 3;
    solidos.forEach((clave, k) => {
      const c = color(clave);
      for (let fila = 0; fila < filas; fila++) {
        for (let j = 0; j < 7; j++) {
          const cx = 28 + j * 7.4 + ((fila + k) % 2) * 3.4;
          const cy = fondo - 3 - (k * filas + fila) * 5;
          if (cy < 40) continue;
          g.append(s("circle", { cx, cy, r: 2.6, fill: c, stroke: "#14243b", "stroke-width": .4 }));
        }
      }
    });
    // Vidrio
    svg.append(s("path", { d: "M18 12h64M23 12v88a8 8 0 0 0 8 8h38a8 8 0 0 0 8-8V12", fill: "none", stroke: "#14243b", "stroke-width": 2.2, "stroke-linecap": "round" }));
    svg.append(s("path", { d: "M70 30h7M70 46h7M70 62h7", stroke: "#14243b", "stroke-width": 1 }));
    if (datos && datos.incierto) svg.append(s("text", { x: 50, y: 60, "text-anchor": "middle", "font-size": 30, fill: "#b3392a", texto: "?" }));
    return svg;
  }

  function figuraVaso(datos, pie, estado, opciones = {}) {
    const fig = h("figure", { clase: "vaso-figura" });
    fig.append(vaso(datos, { ...opciones, etiqueta: pie }));
    const cap = h("figcaption", {}, h("span", { texto: pie }));
    if (estado) {
      const textos = { recuperado: "recuperado", sigue: "sigue mezclado", analitico: "solo en el cromatograma", auxiliar: "auxiliar" };
      cap.append(h("br"), h("span", { clase: "etiqueta-estado " + estado, texto: textos[estado] || estado }));
    }
    fig.append(cap);
    return fig;
  }

  function montaje(nombre) {
    const t = document.getElementById("montaje-" + nombre);
    return t ? t.content.cloneNode(true) : null;
  }

  function leerJSON(id) {
    const el = document.getElementById(id);
    return el ? JSON.parse(el.textContent) : null;
  }

  /* ------------------------------------------------------------ menú en móvil */
  document.addEventListener("DOMContentLoaded", () => {
    const boton = document.querySelector(".boton-menu");
    const menu = document.getElementById("menu-principal");
    if (boton && menu) {
      boton.addEventListener("click", () => {
        const abierto = menu.classList.toggle("abierto");
        boton.setAttribute("aria-expanded", String(abierto));
      });
    }
  });

  return { h, s, icono, vaciar, aviso, fmt, api, vaso, figuraVaso, montaje, color, leerJSON };
})();
