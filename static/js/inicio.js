/* SEPARALAB · demostración de la portada: una mezcla real resuelta por el motor. */
"use strict";
(async () => {
  const caja = document.getElementById("demo-portada");
  if (!caja) return;
  try {
    const plan = await SL.api("/api/resolver", { sustancias: ["agua", "aceite", "arena", "cloruro_de_sodio"] });
    caja.append(SL.figuraVaso(plan.vaso_inicial, "Mezcla", null, { grande: true }),
      SL.h("span", { clase: "operador", "aria-hidden": "true", texto: "→" }),
      SL.h("div", { clase: "separados" }, plan.recuperados.map(r => SL.figuraVaso(r.vaso, r.principal.nombre, null))));
  } catch (e) {
    caja.append(SL.h("p", { clase: "atenuado", texto: "No se pudo cargar la demostración." }));
  }
})();
