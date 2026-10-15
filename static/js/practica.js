/* SEPARALAB · página «Practicar». */
"use strict";
(() => {
  const { aviso, vaciar } = SL;
  const form = document.getElementById("form-practica");
  const config = document.getElementById("configuracion");
  const zona = document.getElementById("practica");
  const error = document.getElementById("error-practica");
  document.querySelectorAll("[data-muestra]").forEach(el => { el.style.background = SL.color(el.dataset.muestra); });

  function reiniciar() {
    zona.classList.add("oculto");
    config.classList.remove("oculto");
    vaciar(zona);
    config.scrollIntoView({ behavior: "smooth" });
  }

  form.addEventListener("submit", async ev => {
    ev.preventDefault();
    vaciar(error);
    const sustancias = [...form.querySelectorAll('input[name="sustancia"]:checked')].map(c => c.value);
    const permitidos = [...form.querySelectorAll('input[name="permitido"]:checked')].map(c => c.value);
    if (sustancias.length < 2) { error.append(aviso("error", null, "Elige al menos dos sustancias.")); return; }
    if (!permitidos.length) { error.append(aviso("error", null, "Permite al menos un método.")); return; }
    const mezcla = { sustancias, permitidos };
    try {
      await SL.api("/api/practica/estado", { mezcla, historial: [] });
    } catch (e) { error.append(aviso("error", "No se puede practicar con esta mezcla", e.message)); return; }
    config.classList.add("oculto");
    zona.classList.remove("oculto");
    SL.Practica(zona, mezcla, { alReiniciar: reiniciar });
  });
})();
