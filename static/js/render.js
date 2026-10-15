/* SEPARALAB · dibujo de la solución completa (resolver, práctica y retos). */
"use strict";

(() => {
  const { h, aviso, vaso, figuraVaso, montaje, icono, fmt } = SL;

  const TXT_SOLUBILIDAD = { soluble: "soluble", poco_soluble: "muy poco soluble", insoluble: "insoluble" };

  function lista(items, ordenada) {
    return h(ordenada ? "ol" : "ul", {}, items.map(t => h("li", { texto: t })));
  }

  function textoFases(analisis) {
    return analisis.fases.map(f => f.tipo === "liquida"
      ? "fase líquida: " + f.liquidos.join(" + ").toLowerCase() + (f.disueltos.length ? " (con " + f.disueltos.join(", ").toLowerCase() + " disuelto)" : "")
      : "sólido: " + f.componente.toLowerCase()).join(" · ");
  }

  function tablaComponentes(componentes) {
    const tabla = h("table", { clase: "dato-tabla" });
    tabla.append(h("thead", {}, h("tr", {}, ["Componente", "Tipo", "Estado", "En agua", "Densidad (g/mL)", "Ebullición (°C)", "Magnético"].map(t => h("th", { texto: t })))));
    const cuerpo = h("tbody");
    componentes.forEach(c => {
      cuerpo.append(h("tr", {},
        h("td", {}, h("b", { texto: c.nombre }), c.formula ? " (" + c.formula + ")" : ""),
        h("td", { texto: c.tipo }),
        h("td", { texto: c.estado === "liquido" ? "líquido" : "sólido" }),
        h("td", { texto: c.estado === "liquido" ? "—" : (TXT_SOLUBILIDAD[c.solubilidad_agua] || "sin dato") }),
        h("td", { clase: "num", texto: c.densidad ? fmt(c.densidad, 2) + " aprox." : "—" }),
        h("td", { clase: "num", texto: c.punto_ebullicion ? fmt(c.punto_ebullicion, 1) : "—" }),
        h("td", { texto: c.magnetico ? "sí" : "no" })));
    });
    tabla.append(cuerpo);
    return h("div", { style: "overflow-x:auto" }, tabla);
  }

  function tablaSolubilidad(datos) {
    const t = h("table", { clase: "dato-tabla" });
    t.append(h("thead", {}, h("tr", {}, ["Sal", "20 °C", "80 °C", "Unidad", "Fuente"].map(x => h("th", { texto: x })))));
    t.append(h("tbody", {}, datos.map(d => h("tr", {},
      h("td", { texto: d.sal }), h("td", { clase: "num", texto: fmt(d.s20) }), h("td", { clase: "num", texto: fmt(d.s80) }),
      h("td", { texto: d.unidad }), h("td", { texto: d.fuente })))));
    return h("div", { style: "overflow-x:auto" }, t);
  }

  function materiales(lista) {
    return h("div", { clase: "materiales" }, lista.map(m =>
      h("div", { clase: "material", title: m.funcion }, icono("i-" + m.icono), h("span", { texto: m.nombre }))));
  }

  function paso(p, abierto) {
    const det = h("details", { clase: "paso" + (p.auxiliar ? " auxiliar" : "") });
    if (abierto) det.open = true;
    det.append(h("summary", {},
      h("span", { clase: "num", texto: String(p.numero) }),
      h("div", {}, h("h3", { texto: p.nombre }), h("p", { texto: `Sobre: ${p.entrada.nombre.toLowerCase()} · aprovecha: ${p.propiedad.toLowerCase()}` })),
      h("span", { clase: "flecha", "aria-hidden": "true", texto: "▸" })));
    const cuerpo = h("div", { clase: "paso-cuerpo" });

    const trans = h("div", { clase: "transformacion" },
      figuraVaso(p.entrada.vaso, p.entrada.texto, null),
      h("span", { clase: "operador", "aria-hidden": "true", texto: "→" }),
      h("div", { clase: "productos-vasos" }, p.productos.map(x => figuraVaso(x.vaso, `${x.nombre}: ${x.texto}`, x.estado))));
    cuerpo.append(trans);
    if (p.perdidos && p.perdidos.length) {
      cuerpo.append(aviso("atencion", null, "No se recupera: " + p.perdidos.map(c => c.nombre.toLowerCase()).join(", ") + " (pasa al aire)."));
    }

    const izq = h("div", { clase: "bloque" },
      h("h4", { texto: "Por qué funciona" }), h("p", { texto: p.explicacion }),
      h("h4", { texto: "Fundamento" }), h("p", { texto: p.fundamento }),
      h("h4", { texto: "Por qué en este punto" }), h("p", { texto: p.por_que_aqui }));
    if (p.detalle && p.detalle.datos) {
      izq.append(h("h4", { texto: "Datos de solubilidad usados" }), tablaSolubilidad(p.detalle.datos));
    }
    if (p.avisos.length) {
      izq.append(h("h4", { texto: "Avisos, pureza y pérdidas" }), ...p.avisos.map(a => aviso("atencion", null, a)));
    }
    if (p.alternativas.length) {
      izq.append(h("h4", { texto: "Otras opciones consideradas" }),
        h("ul", { clase: "alternativas" }, p.alternativas.map(a => h("li", {}, h("b", { texto: a.nombre + ": " }), a.motivo))));
    }
    const der = h("div", { clase: "bloque" });
    const dibujo = montaje(p.montaje);
    if (dibujo) der.append(h("h4", { texto: "Montaje" }), h("div", { clase: "montaje" }, dibujo));
    der.append(h("h4", { texto: "Materiales" }), materiales(p.materiales),
      h("h4", { texto: "Procedimiento" }), lista(p.procedimiento, true));
    if (p.precauciones.length) der.append(h("h4", { texto: "Precauciones" }), lista(p.precauciones));
    if (p.limitaciones.length) der.append(h("h4", { texto: "Limitaciones" }), lista(p.limitaciones));
    cuerpo.append(h("div", { clase: "bloques" }, izq, der));
    det.append(cuerpo);
    return det;
  }

  function finales(plan) {
    const caja = h("section", { clase: "hoja", style: "margin-top:18px" }, h("h2", { texto: "Resultado final" }));
    if (plan.recuperados.length) {
      caja.append(h("h3", { texto: "Componentes separados" }),
        h("div", { clase: "final-lista" }, plan.recuperados.map(r => {
          let pie = r.principal.nombre;
          if (r.principal.nota === "enriquecido") pie += " (enriquecido, no puro)";
          if (r.principal.nota === "alterado por el calor") pie += " (alterado por el calor)";
          if (r.impurezas.length) pie += " · con restos de " + r.impurezas.map(i => i.nombre.toLowerCase()).join(", ");
          if (r.principal.masa) pie += ` · ≈ ${fmt(r.principal.masa, 1)} g`;
          return figuraVaso(r.vaso, pie, "recuperado");
        })));
    }
    if (plan.analiticos.length) {
      caja.append(aviso("info", "Separados solo en el cromatograma",
        plan.analiticos.map(a => a.componentes.map(c => c.nombre).join(", ")).join(" · ") +
        ". La cromatografía los separa e identifica, pero no los recupera en cantidad."));
    }
    if (plan.perdidos.length) {
      caja.append(aviso("atencion", "No se recupera", plan.perdidos.map(p => p.nombre).join(", ") + ": se evapora durante el proceso."));
    }
    plan.sin_resolver.forEach(f => {
      caja.append(aviso("error", "Fracción sin separar: " + f.texto, ...f.motivos));
    });
    return caja;
  }

  function renderPlan(contenedor, plan, opciones = {}) {
    SL.vaciar(contenedor);
    const a = plan.analisis;
    const cabeza = h("section", { clase: "hoja" });
    const resumen = h("div", { clase: "resumen" }, figuraVaso(plan.vaso_inicial, "Mezcla inicial", null, { grande: true }));
    const texto = h("div", { clase: "texto" },
      h("h2", { texto: opciones.titulo || "Cómo separar esta mezcla" }),
      h("p", {}, h("b", { texto: "Tipo de mezcla: " }), a.tipo + (a.num_fases ? ` (${a.num_fases} fase${a.num_fases > 1 ? "s" : ""})` : "") + "."),
      a.fases.length ? h("p", { clase: "atenuado", texto: textoFases(a) }) : null,
      h("p", { texto: plan.resumen }));
    if (plan.pasos.length) {
      texto.append(h("ol", { clase: "ruta", "aria-label": "Secuencia de métodos" },
        plan.pasos.map(p => h("li", { clase: p.auxiliar ? "aux" : "", texto: p.nombre.split(" (")[0] }))));
    }
    resumen.append(texto);
    cabeza.append(resumen);
    if (a.nota_sustancia_pura) cabeza.append(aviso("info", "Sustancia pura", a.nota_sustancia_pura));
    a.reacciones.forEach(r => cabeza.append(aviso(r.activa ? "error" : "atencion",
      (r.activa ? "Reacción química posible: " : "Cuidado: ") + r.ecuacion, r.explicacion, r.consejo)));
    a.incertidumbres.forEach(t => cabeza.append(aviso("error", "Falta información", t)));
    if (a.supuestos.length) cabeza.append(aviso("info", "Supuestos del modelo", h("ul", {}, a.supuestos.map(t => h("li", { texto: t })))));
    const det = h("details", { clase: "plegable" }, h("summary", { texto: "Propiedades de los componentes" }), tablaComponentes(a.componentes));
    cabeza.append(det);
    contenedor.append(cabeza);
    plan.pasos.forEach((p, i) => contenedor.append(paso(p, i === 0)));
    if (plan.pasos.length || plan.sin_resolver.length) contenedor.append(finales(plan));
  }

  SL.renderPlan = renderPlan;
  SL.renderMateriales = materiales;
})();
