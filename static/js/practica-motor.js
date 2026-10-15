/* SEPARALAB · motor de la práctica interactiva (lo usan «Practicar» y «Retos»).
   El estado vive en el navegador (historial de decisiones aceptadas); el
   servidor lo reconstruye y evalúa cada decisión con el mismo motor químico. */
"use strict";

(() => {
  const { h, api, aviso, vaciar, figuraVaso, icono } = SL;

  const PUNTOS = { optima: 10, valida: 6, desaconsejada: 2, fallo: -2, pista: -1, materiales: 3, orden: 3, prediccion: 2, tipo: 2 };
  const NOMBRE_ESTADO = { optima: "Elección óptima", valida: "Válida, pero no la mejor", desaconsejada: "Posible, pero empeora el resultado",
    no_aplicable: "No se puede aplicar", no_permitido: "Método no permitido" };

  function Practica(raiz, mezcla, opciones = {}) {
    const est = {
      historial: [], puntos: 0, registro: [], fallosPaso: 0, pistaNivel: 0,
      fraccion: null, metodo: null, estado: null, tipoRespondido: false, totalInicial: 0,
    };
    vaciar(raiz);
    const marcador = h("div", { clase: "hoja marcador", role: "status" });
    const zona = h("div", { clase: "hoja", style: "margin-top:14px" });
    const zonaRegistro = h("div", { clase: "hoja", style: "margin-top:14px" });
    raiz.append(marcador, zona, zonaRegistro);

    const cuerpo = extra => ({ mezcla, historial: est.historial, ...extra });

    function sumar(n) { est.puntos = Math.max(0, est.puntos + n); }

    function pintarMarcador() {
      vaciar(marcador);
      const e = est.estado;
      const hechos = e ? e.recuperados.length + e.analiticos.length : 0;
      const pendientes = e ? e.pendientes.reduce((n, p) => n + p.componentes.filter(c => c.rol === "principal").length, 0) : 0;
      const total = Math.max(hechos + pendientes, 1);
      const barra = h("div", { clase: "barra", role: "progressbar", "aria-valuemin": "0", "aria-valuemax": String(total), "aria-valuenow": String(hechos), "aria-label": "Componentes separados" }, h("i"));
      barra.firstChild.style.width = (100 * hechos / total) + "%";
      marcador.append(
        h("div", {}, h("span", { clase: "puntos", texto: est.puntos + " pts" })),
        barra,
        h("span", { clase: "atenuado", texto: `${hechos} de ${total} componentes separados · ${est.historial.length} decisiones` }));
    }

    function pintarRegistro() {
      vaciar(zonaRegistro);
      zonaRegistro.append(h("h3", { texto: "Tu procedimiento" }));
      if (!est.registro.length) { zonaRegistro.append(h("p", { clase: "atenuado", texto: "Aquí aparecerá cada decisión con su evaluación." })); return; }
      zonaRegistro.append(h("ol", { clase: "registro" }, est.registro.map(r =>
        h("li", { clase: r.estado }, h("b", { texto: r.metodo }), ` sobre ${r.fraccion.toLowerCase()} — ${NOMBRE_ESTADO[r.estado]}` + (r.intentos > 1 ? ` (al intento ${r.intentos})` : "")))));
    }

    async function cargar() {
      try {
        est.estado = await api("/api/practica/estado", cuerpo());
      } catch (e) {
        vaciar(zona).append(aviso("error", "No se pudo cargar la práctica", e.message));
        return;
      }
      if (!est.totalInicial) est.totalInicial = est.estado.pendientes.reduce((n, p) => n + p.componentes.length, 0);
      pintarMarcador();
      pintarRegistro();
      if (!est.tipoRespondido && est.historial.length === 0 && est.estado.pendientes.length) return preguntaTipo();
      if (est.estado.completo || est.estado.terminado) return final();
      tablero();
    }

    /* ---------------------------------------------- 1. ¿qué tipo de mezcla es? */
    function preguntaTipo() {
      const f = est.estado.pendientes[0];
      vaciar(zona);
      zona.append(h("h2", { texto: "Analiza la mezcla" }),
        h("div", { clase: "resumen" }, figuraVaso(f.vaso, f.texto, null, { grande: true }),
          h("div", { clase: "texto" },
            h("p", { texto: "Antes de separar, observa: ¿cuántas fases distingues? ¿Qué está disuelto y qué no?" }),
            h("p", {}, h("b", { texto: "¿Qué tipo de mezcla es?" })))));
      const opciones = h("div", { clase: "botones" });
      const resp = h("div", { "aria-live": "polite" });
      ["homogénea", "heterogénea"].forEach(t => opciones.append(h("button", { clase: "boton secundario", type: "button", texto: t[0].toUpperCase() + t.slice(1),
        onclick: () => {
          const correcto = f.tipo;
          const ok = correcto.startsWith(t);
          vaciar(resp);
          if (correcto.startsWith("no determinada")) {
            resp.append(aviso("atencion", "No se puede decidir", "Faltan datos de miscibilidad entre algunos líquidos: no se sabe si forman una o dos fases."));
          } else if (ok) {
            sumar(PUNTOS.tipo);
            resp.append(aviso("bien", "¡Correcto!", t === "heterogénea"
              ? "Se distinguen varias fases (capas o partículas visibles): sus componentes conservan sus propiedades y no están uniformemente repartidos."
              : "Tiene una sola fase con la misma composición en todo su volumen: lo disuelto no se ve."));
          } else {
            resp.append(aviso("error", "No exactamente", `Es ${correcto}. ` + (correcto === "heterogénea"
              ? "Hay más de una fase: un sólido sin disolver o dos líquidos que no se mezclan."
              : "Todo está disuelto o mezclado en una sola fase uniforme.")));
          }
          est.tipoRespondido = true;
          pintarMarcador();
          [...opciones.children].forEach(b => { b.disabled = true; });
          resp.append(h("button", { clase: "boton", type: "button", texto: "Empezar a separar", onclick: tablero }));
        } })));
      zona.append(opciones, resp);
    }

    /* ---------------------------------------------- 2. elegir fracción, método y predicción */
    function tablero() {
      est.metodo = null;
      est.fallosPaso = 0;
      est.pistaNivel = 0;
      const pend = est.estado.pendientes.filter(p => !p.sin_salida);
      if (!pend.some(p => p.id === est.fraccion)) est.fraccion = pend.length ? pend[0].id : null;
      vaciar(zona);
      zona.append(h("h2", { texto: "¿Qué haces ahora?" }));
      const cajaFr = h("div", { clase: "fracciones" });
      est.estado.pendientes.forEach(p => {
        const boton = h("button", { clase: "fraccion", type: "button", "aria-pressed": String(p.id === est.fraccion), disabled: p.sin_salida,
          onclick: () => { est.fraccion = p.id; tablero(); } },
          SL.vaso(p.vaso, { etiqueta: p.texto }),
          h("span", {}, h("b", { texto: p.nombre }), p.texto, p.sin_salida ? h("em", { texto: " · no se puede separar más" }) : null));
        cajaFr.append(boton);
      });
      zona.append(h("h3", { texto: "1. Elige la fracción" }), cajaFr);

      const fr = est.estado.pendientes.find(p => p.id === est.fraccion);
      if (!fr) return final();
      const cajaM = h("div", { clase: "metodos-opciones" });
      est.estado.metodos.forEach(m => {
        cajaM.append(h("button", { clase: "opcion", type: "button", "aria-pressed": "false",
          onclick: ev => { est.metodo = m.clave; [...cajaM.children].forEach(b => b.setAttribute("aria-pressed", String(b === ev.currentTarget))); comprobar.disabled = false; } },
          h("b", { texto: m.nombre }), h("small", { texto: m.propiedad })));
      });
      zona.append(h("h3", { texto: "2. Elige el método" }), cajaM);

      const principales = fr.componentes.filter(c => c.rol === "principal");
      const pred = h("div", {});
      principales.forEach(c => pred.append(h("label", { clase: "casilla" }, h("input", { type: "checkbox", name: "prediccion", value: c.clave }), h("span", { texto: c.nombre }))));
      zona.append(h("h3", { texto: "3. ¿Qué componentes quedarán separados después de este paso?" }),
        h("p", { clase: "pequeno atenuado", texto: "Marca los que crees que salen ya aislados (déjalo vacío si ninguno)." }), pred);

      const salida = h("div", { "aria-live": "polite" });
      const comprobar = h("button", { clase: "boton", type: "button", texto: "Comprobar", disabled: true, onclick: () => evaluar(salida, comprobar) });
      const botonPista = h("button", { clase: "boton discreto", type: "button", texto: "Pedir una pista (−1)", onclick: () => pedirPista(salida) });
      zona.append(h("div", { clase: "botones", style: "margin-top:14px" }, comprobar, botonPista), salida);
    }

    async function pedirPista(salida) {
      est.pistaNivel = Math.min(est.pistaNivel + 1, 3);
      try {
        const r = await api("/api/practica/pista", cuerpo({ fraccion: est.fraccion, nivel: est.pistaNivel }));
        sumar(PUNTOS.pista);
        pintarMarcador();
        salida.prepend(aviso("info", `Pista ${est.pistaNivel} de 3`, r.texto));
      } catch (e) { salida.prepend(aviso("error", null, e.message)); }
    }

    async function evaluar(salida, boton) {
      const prediccion = [...zona.querySelectorAll('input[name="prediccion"]:checked')].map(i => i.value);
      boton.disabled = true;
      let r;
      try {
        r = await api("/api/practica/evaluar", cuerpo({ fraccion: est.fraccion, metodo: est.metodo, prediccion }));
      } catch (e) {
        salida.prepend(aviso("error", null, e.message));
        boton.disabled = false;
        return;
      }
      vaciar(salida);
      if (!r.aceptada) {
        est.fallosPaso += 1;
        sumar(PUNTOS.fallo);
        pintarMarcador();
        salida.append(aviso("error", `${NOMBRE_ESTADO[r.estado]}: ${r.nombre}`, r.mensaje, r.consejo,
          est.fallosPaso >= 2 ? "Si te atascas, pide una pista." : null));
        boton.disabled = false;
        return;
      }
      const base = { optima: PUNTOS.optima, valida: PUNTOS.valida, desaconsejada: PUNTOS.desaconsejada }[r.estado];
      sumar(est.fallosPaso === 0 ? base : Math.ceil(base / 2));
      const tipo = r.estado === "optima" ? "bien" : r.estado === "valida" ? "atencion" : "error";
      const textosPred = [];
      if (r.prediccion) {
        if (r.prediccion.correcta) { sumar(PUNTOS.prediccion); textosPred.push("Tu predicción de lo que se separa es correcta."); }
        else {
          const nombres = claves => claves.map(k => (zona.querySelector(`input[value="${k}"]`)?.nextSibling?.textContent || k).toLowerCase()).join(", ");
          textosPred.push("Predicción: " + [r.prediccion.faltan.length ? "también queda separado " + nombres(r.prediccion.faltan) : "",
            r.prediccion.sobran.length ? "todavía no se separa " + nombres(r.prediccion.sobran) : ""].filter(Boolean).join("; ") + ".");
        }
      }
      pintarMarcador();
      salida.append(aviso(tipo, `${NOMBRE_ESTADO[r.estado]}: ${r.nombre}`, r.mensaje, r.explicacion, ...textosPred),
        h("div", { clase: "productos-vasos", style: "margin:10px 0" }, r.productos.map(p => figuraVaso(p.vaso, `${p.nombre}: ${p.texto}`, p.estado))));
      (r.avisos || []).slice(r.estado === "optima" ? 0 : 1).forEach(a => salida.append(aviso("atencion", null, a)));
      const fr = est.estado.pendientes.find(p => p.id === est.fraccion);
      est.registro.push({ metodo: r.nombre, fraccion: fr.nombre, estado: r.estado, intentos: est.fallosPaso + 1 });
      pintarRegistro();
      const decision = { fraccion: est.fraccion, metodo: est.metodo };
      [...zona.querySelectorAll("button.opcion, button.fraccion, input")].forEach(b => { b.disabled = true; });
      materialesYPasos(salida, decision);
    }

    /* ---------------------------------------------- 3. materiales y orden del procedimiento */
    async function materialesYPasos(salida, decision) {
      const etapa = h("div", { clase: "etapa" });
      salida.append(etapa);
      let opcionesMat, pasos;
      try {
        [opcionesMat, pasos] = await Promise.all([
          api("/api/practica/materiales", { metodo: decision.metodo }),
          api("/api/practica/procedimiento", { metodo: decision.metodo }),
        ]);
      } catch (e) { etapa.append(aviso("error", null, e.message)); return continuar(decision, etapa); }

      const elegidos = new Set();
      const rejilla = h("div", { clase: "metodos-opciones" });
      opcionesMat.opciones.forEach(m => rejilla.append(h("button", { clase: "opcion material-opcion", type: "button", "aria-pressed": "false",
        onclick: ev => { elegidos.has(m.clave) ? elegidos.delete(m.clave) : elegidos.add(m.clave); ev.currentTarget.setAttribute("aria-pressed", String(elegidos.has(m.clave))); } },
        icono("i-" + m.icono), h("span", { texto: m.nombre }))));
      const resMat = h("div", { "aria-live": "polite" });
      const botonMat = h("button", { clase: "boton secundario", type: "button", texto: "Comprobar materiales", onclick: async () => {
        try {
          const r = await api("/api/practica/materiales", { metodo: decision.metodo, seleccion: [...elegidos] });
          vaciar(resMat);
          if (r.correcta) { sumar(PUNTOS.materiales); resMat.append(aviso("bien", "Material correcto", `Has elegido las ${r.total} piezas necesarias.`)); }
          else {
            resMat.append(aviso("atencion", `${r.aciertos} de ${r.total} piezas correctas`,
              r.faltan.length ? h("p", {}, h("b", { texto: "Falta: " }), r.faltan.map(m => `${m.nombre} (${m.funcion.toLowerCase().replace(/\.$/, "")})`).join("; ")) : null,
              r.sobran.length ? h("p", {}, h("b", { texto: "No hace falta: " }), r.sobran.map(m => m.nombre).join(", ")) : null));
          }
          botonMat.disabled = true;
          [...rejilla.children].forEach(b => { b.disabled = true; });
          pintarMarcador();
        } catch (e) { resMat.append(aviso("error", null, e.message)); }
      } });
      etapa.append(h("h3", {}, h("span", { clase: "n", texto: "4." }), "Elige el material"), rejilla, h("div", { clase: "botones", style: "margin-top:8px" }, botonMat), resMat);

      let orden = pasos.pasos.slice();
      const listaPasos = h("ol", { clase: "ordenar" });
      const pintarPasos = (marcas) => {
        vaciar(listaPasos);
        orden.forEach((p, i) => listaPasos.append(h("li", { clase: marcas ? (marcas[i] ? "bien" : "mal") : "" },
          h("b", { texto: String(i + 1) }), h("span", { texto: p.texto }),
          h("span", { clase: "mover" },
            h("button", { type: "button", "aria-label": "Subir", texto: "↑", disabled: i === 0 || !!marcas, onclick: () => { [orden[i - 1], orden[i]] = [orden[i], orden[i - 1]]; pintarPasos(); } }),
            h("button", { type: "button", "aria-label": "Bajar", texto: "↓", disabled: i === orden.length - 1 || !!marcas, onclick: () => { [orden[i + 1], orden[i]] = [orden[i], orden[i + 1]]; pintarPasos(); } })))));
      };
      pintarPasos();
      const resOrden = h("div", { "aria-live": "polite" });
      const botonOrden = h("button", { clase: "boton secundario", type: "button", texto: "Comprobar el orden", onclick: async () => {
        try {
          const r = await api("/api/practica/procedimiento", { metodo: decision.metodo, orden: orden.map(p => p.id) });
          pintarPasos(orden.map((p, i) => p.id === i));
          vaciar(resOrden);
          if (r.correcta) { sumar(PUNTOS.orden); resOrden.append(aviso("bien", "Orden correcto", "Cada paso prepara el siguiente.")); }
          else resOrden.append(aviso("atencion", `${r.posiciones_correctas} de ${r.total} pasos en su sitio`, h("ol", {}, r.orden_correcto.map(t => h("li", { texto: t })))));
          botonOrden.disabled = true;
          pintarMarcador();
        } catch (e) { resOrden.append(aviso("error", null, e.message)); }
      } });
      etapa.append(h("h3", {}, h("span", { clase: "n", texto: "5." }), "Ordena el procedimiento"), listaPasos,
        h("div", { clase: "botones", style: "margin-top:8px" }, botonOrden), resOrden);
      continuar(decision, etapa);
    }

    function continuar(decision, etapa) {
      etapa.append(h("div", { clase: "botones", style: "margin-top:16px" },
        h("button", { clase: "boton", type: "button", texto: "Aplicar y continuar", onclick: () => {
          est.historial.push(decision);
          est.fraccion = null;
          cargar();
          raiz.scrollIntoView({ behavior: "smooth", block: "start" });
        } })));
    }

    /* ---------------------------------------------- 4. final */
    function final() {
      const e = est.estado;
      vaciar(zona);
      zona.append(h("h2", { texto: e.completo ? "¡Mezcla separada!" : "Fin de la práctica" }),
        h("p", { texto: `Puntuación: ${est.puntos} puntos en ${est.historial.length} decisiones.` }));
      if (e.recuperados.length) {
        zona.append(h("h3", { texto: "Has recuperado" }),
          h("div", { clase: "final-lista" }, e.recuperados.map(r => figuraVaso(r.vaso, `${r.nombre}: ${r.texto}`, "recuperado"))));
      }
      if (e.analiticos.length) zona.append(aviso("info", "Separados en el cromatograma", e.analiticos.map(a => a.componentes.map(c => c.nombre).join(", ")).join(" · ")));
      if (e.perdidos.length) zona.append(aviso("atencion", "No recuperaste", e.perdidos.map(p => p.nombre).join(", ") + ": se evaporó."));
      e.pendientes.forEach(p => zona.append(aviso("error", "Sin separar: " + p.texto, ...(p.motivos || []))));
      const solucion = h("div", { style: "margin-top:14px" });
      zona.append(h("div", { clase: "botones" },
        h("button", { clase: "boton secundario", type: "button", texto: "Ver la solución de SEPARALAB", onclick: async ev => {
          ev.currentTarget.disabled = true;
          try {
            const plan = opciones.solucion ? await opciones.solucion() : await api("/api/resolver", {
              sustancias: mezcla.sustancias, cantidades: mezcla.cantidades || null, permitidos: mezcla.permitidos || null,
              recuperar_disolvente: mezcla.recuperar_disolvente !== false });
            SL.renderPlan(solucion, plan, { titulo: "Solución propuesta" });
          } catch (err) { solucion.append(aviso("error", null, err.message)); }
        } }),
        opciones.alReiniciar ? h("button", { clase: "boton discreto", type: "button", texto: "Empezar de nuevo", onclick: opciones.alReiniciar }) : null), solucion);
      if (opciones.alTerminar) opciones.alTerminar(est);
    }

    cargar();
    return est;
  }

  SL.Practica = Practica;
})();
