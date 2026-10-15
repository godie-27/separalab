# datos/materiales.py
# Material y equipo de laboratorio. "icono" es el nombre del dibujo SVG propio
# en templates/iconos/ (todos los dibujos son originales de SEPARALAB).

MATERIALES = {
    "iman": {"nombre": "Imán", "funcion": "Atrae los sólidos ferromagnéticos, como el hierro.", "icono": "iman"},
    "vaso_precipitados": {"nombre": "Vaso de precipitados", "funcion": "Contener, mezclar y calentar líquidos.", "icono": "vaso"},
    "espatula": {"nombre": "Espátula", "funcion": "Tomar y trasladar sólidos.", "icono": "espatula"},
    "vidrio_reloj": {"nombre": "Vidrio de reloj", "funcion": "Recoger y secar pequeñas cantidades de sólido.", "icono": "vidrio_reloj"},
    "embudo_decantacion": {"nombre": "Embudo de decantación (pera)", "funcion": "Separar líquidos inmiscibles abriendo la llave para vaciar la fase inferior.", "icono": "pera"},
    "soporte_universal": {"nombre": "Soporte universal con aro o pinzas", "funcion": "Sujetar el material en posición.", "icono": "soporte"},
    "embudo": {"nombre": "Embudo de vidrio", "funcion": "Sostener el papel de filtro y dirigir el líquido.", "icono": "embudo"},
    "papel_filtro": {"nombre": "Papel de filtro", "funcion": "Retener las partículas sólidas; deja pasar el líquido y lo disuelto.", "icono": "papel_filtro"},
    "varilla": {"nombre": "Varilla de vidrio", "funcion": "Agitar y guiar el líquido al verterlo.", "icono": "varilla"},
    "matraz_erlenmeyer": {"nombre": "Matraz Erlenmeyer", "funcion": "Recoger el filtrado o el destilado.", "icono": "erlenmeyer"},
    "capsula": {"nombre": "Cápsula de porcelana", "funcion": "Evaporar el disolvente de una disolución.", "icono": "capsula"},
    "tripode_rejilla": {"nombre": "Trípode y rejilla", "funcion": "Sostener el recipiente sobre la fuente de calor.", "icono": "tripode"},
    "mechero": {"nombre": "Mechero Bunsen", "funcion": "Fuente de calor con llama (no usar con líquidos inflamables).", "icono": "mechero"},
    "placa_calefactora": {"nombre": "Placa o manta calefactora", "funcion": "Calentar sin llama abierta.", "icono": "placa"},
    "matraz_destilacion": {"nombre": "Matraz de destilación (balón)", "funcion": "Contener la mezcla que se calienta.", "icono": "balon"},
    "termometro": {"nombre": "Termómetro", "funcion": "Medir la temperatura del vapor a la altura de la salida lateral.", "icono": "termometro"},
    "refrigerante": {"nombre": "Refrigerante (condensador)", "funcion": "Enfriar el vapor con agua que circula a contracorriente para condensarlo.", "icono": "refrigerante"},
    "columna_fraccionamiento": {"nombre": "Columna de fraccionamiento", "funcion": "Ofrece mucha superficie para condensaciones y vaporizaciones sucesivas.", "icono": "columna"},
    "piedras_ebullicion": {"nombre": "Piedras de ebullición", "funcion": "Evitan la ebullición brusca.", "icono": "piedras"},
    "cristalizador": {"nombre": "Cristalizador", "funcion": "Recipiente ancho donde se enfría la disolución y crecen los cristales.", "icono": "cristalizador"},
    "bano_hielo": {"nombre": "Baño de agua fría o hielo", "funcion": "Enfriar la disolución para disminuir la solubilidad.", "icono": "bano"},
    "papel_cromatografia": {"nombre": "Papel de cromatografía", "funcion": "Fase estacionaria (agua unida a la celulosa).", "icono": "papel_croma"},
    "placa_tlc": {"nombre": "Placa de capa fina (sílice)", "funcion": "Fase estacionaria polar para TLC.", "icono": "placa_tlc"},
    "camara_cromatografia": {"nombre": "Cámara con tapa", "funcion": "Satura el aire con vapor del disolvente y evita que se evapore.", "icono": "camara"},
    "capilar": {"nombre": "Capilar o micropipeta", "funcion": "Aplicar una gota pequeña de muestra en la línea de origen.", "icono": "capilar"},
    "lapiz_regla": {"nombre": "Lápiz y regla", "funcion": "Trazar la línea de origen (el lápiz no se disuelve) y medir distancias.", "icono": "regla"},
    "probeta": {"nombre": "Probeta", "funcion": "Medir volúmenes de líquido.", "icono": "probeta"},
    "balanza": {"nombre": "Balanza", "funcion": "Medir masas.", "icono": "balanza"},
    # Distractores frecuentes (material que no corresponde a separaciones)
    "pipeta_aforada": {"nombre": "Pipeta aforada", "funcion": "Medir con precisión un volumen fijo.", "icono": "pipeta"},
    "bureta": {"nombre": "Bureta", "funcion": "Añadir volúmenes variables en una titulación.", "icono": "bureta"},
    "mortero": {"nombre": "Mortero", "funcion": "Triturar sólidos.", "icono": "mortero"},
}


def nombre_material(clave):
    return MATERIALES.get(clave, {}).get("nombre", clave)
