# datos/retos.py
# Banco de retos validados. Cada reto se comprueba con el motor químico en
# pruebas/test_retos.py: si un reto deja de tener solución, la prueba falla.
#
# Campos:
#   usar_cantidades: si el motor razona con las masas (True) o solo
#                    cualitativamente, como pide el enunciado (False).
#   solubilidades:   datos propios del ejercicio ((clave, s20, s80, unidad, fuente), ...).
#   parcial_esperado: True si, con los datos del enunciado, la separación no
#                    puede completarse (es parte de lo que el estudiante debe descubrir).

TABLA_D = (
    ("cloruro_de_sodio", 36.0, 39.0, "g/100 g de agua", "Ficha de clase (Ejemplo D)"),
    ("sulfato_de_cobre", 20.0, 55.0, "g/100 g de agua", "Ficha de clase (Ejemplo D)"),
)
TABLA_G = (
    ("cloruro_de_sodio", 36.0, 38.4, "g/100 mL de agua", "Ficha de clase (Ejemplo G)"),
    ("sulfato_de_cobre", 20.7, 57.4, "g/100 mL de agua", "Ficha de clase (Ejemplo G)"),
)

RETOS = [
    # ------------------------------------------------------------------ básico
    {
        "id": "b1", "nivel": "basico", "titulo": "Arena en el agua",
        "enunciado": "Tienes un vaso con agua y arena. Separa y recupera ambos componentes.",
        "sustancias": ["agua", "arena"], "permitidos": ["filtracion", "sedimentacion", "evaporacion", "destilacion"],
        "pistas": ["¿La arena se disuelve en agua?", "Un sólido insoluble puede quedar retenido en un papel con poros."],
        "fuente": "Apuntes de clase (tabla de métodos)",
    },
    {
        "id": "b2", "nivel": "basico", "titulo": "Tiza y agua",
        "enunciado": "Se ha mezclado carbonato de calcio (tiza en polvo) con agua. Recupera el sólido y el agua.",
        "sustancias": ["agua", "carbonato_de_calcio"], "permitidos": ["filtracion", "sedimentacion", "evaporacion", "destilacion", "cristalizacion"],
        "pistas": ["¿Todos los compuestos iónicos se disuelven en agua?", "El CaCO₃ es prácticamente insoluble."],
        "fuente": "Apuntes de clase (tabla de métodos)",
    },
    {
        "id": "b3", "nivel": "basico", "titulo": "Hierro y azufre",
        "enunciado": "Una mezcla de polvo de hierro y polvo de azufre. Sepáralos sin cambiar su naturaleza química.",
        "sustancias": ["hierro", "azufre"], "permitidos": ["magnetismo", "filtracion", "evaporacion", "destilacion"],
        "pistas": ["En una mezcla, cada componente conserva sus propiedades.", "Uno de los dos es atraído por un imán."],
        "preguntas": [{
            "pregunta": "Si se calienta la mezcla y se forma sulfuro de hierro(II), FeS, ¿se puede separar el hierro con un imán?",
            "opciones": ["Sí, porque el FeS contiene hierro", "No, porque el FeS es un compuesto con propiedades nuevas y no es magnético",
                         "Solo si se tritura primero"],
            "correcta": 1,
            "explicacion": "El FeS es una sustancia pura nueva: no conserva el magnetismo del hierro ni el olor del azufre. Un compuesto solo se descompone por métodos químicos.",
        }],
        "fuente": "Apuntes de clase (métodos de separación)",
    },
    {
        "id": "b4", "nivel": "basico", "titulo": "Agua y aceite",
        "enunciado": "Separa el agua del aceite vegetal de una mezcla.",
        "sustancias": ["agua", "aceite"], "permitidos": ["decantacion", "filtracion", "destilacion", "evaporacion"],
        "pistas": ["¿Se mezclan el agua y el aceite?", "Fíjate en cuál es menos denso."],
        "fuente": "Apuntes de clase (tabla de métodos)",
    },
    {
        "id": "b5", "nivel": "basico", "titulo": "Recuperar la sal",
        "enunciado": "Tienes agua con sal disuelta. Solo te interesa recuperar la sal sólida.",
        "sustancias": ["agua", "cloruro_de_sodio"], "permitidos": ["filtracion", "evaporacion", "cristalizacion", "decantacion"],
        "recuperar_disolvente": False,
        "pistas": ["¿Puede un papel de filtro retener algo que está disuelto?", "El agua es volátil y la sal no."],
        "fuente": "Apuntes de clase (tabla de métodos)",
    },
    # ------------------------------------------------------------------ intermedio
    {
        "id": "i1", "nivel": "intermedio", "titulo": "Arena y sal",
        "enunciado": "Una mezcla seca de arena y sal. Recupera ambos sólidos.",
        "sustancias": ["arena", "cloruro_de_sodio"], "permitidos": ["filtracion", "evaporacion", "cristalizacion", "magnetismo", "decantacion"],
        "pistas": ["Ninguno de los métodos separa directamente dos sólidos secos como estos.", "Puedes añadir agua: ¿qué se disuelve y qué no?"],
        "fuente": "SEPARALAB",
    },
    {
        "id": "i2", "nivel": "intermedio", "titulo": "Alcohol, agua y arcilla",
        "enunciado": "Describe cómo separar los componentes de una mezcla de alcohol, agua y arcilla. La arcilla es insoluble en agua; el agua y el alcohol son miscibles por sus enlaces de hidrógeno.",
        "sustancias": ["etanol", "agua", "arcilla"], "permitidos": ["filtracion", "decantacion", "destilacion", "destilacion_fraccionada", "evaporacion"],
        "pistas": ["Primero retira lo que no está disuelto.", "Los dos líquidos son miscibles: ¿qué propiedad los diferencia?"],
        "fuente": "Ficha de examen (pregunta 1a)",
    },
    {
        "id": "i3", "nivel": "intermedio", "titulo": "Hierro, arena y agua",
        "enunciado": "Un recipiente contiene agua, arena y limaduras de hierro. Recupera los tres componentes.",
        "sustancias": ["agua", "arena", "hierro"], "permitidos": ["magnetismo", "filtracion", "destilacion", "evaporacion", "decantacion"],
        "pistas": ["Hay dos sólidos insolubles: uno de ellos tiene una propiedad especial.", "El agua puede recuperarse si no se pierde por evaporación."],
        "fuente": "SEPARALAB",
    },
    {
        "id": "i4", "nivel": "intermedio", "titulo": "Agua, aceite y arena",
        "enunciado": "Separa una mezcla de agua, aceite vegetal y arena.",
        "sustancias": ["agua", "aceite", "arena"], "permitidos": ["decantacion", "filtracion", "destilacion", "evaporacion"],
        "pistas": ["Hay dos líquidos que no se mezclan.", "¿Qué conviene hacer antes de filtrar?"],
        "fuente": "SEPARALAB",
    },
    {
        "id": "i5", "nivel": "intermedio", "titulo": "Sal en alcohol",
        "enunciado": "Se ha echado sal en etanol. Recupera ambos.",
        "sustancias": ["etanol", "cloruro_de_sodio"], "permitidos": ["filtracion", "evaporacion", "destilacion", "cristalizacion"],
        "pistas": ["¿La sal se disuelve igual en etanol que en agua?", "Las sustancias iónicas son más solubles en agua que en otros disolventes."],
        "fuente": "SEPARALAB (basado en los apuntes de solvatación)",
    },
    # ------------------------------------------------------------------ avanzado
    {
        "id": "a1", "nivel": "avanzado", "titulo": "Seis componentes (ficha C)",
        "enunciado": (
            "Una mezcla heterogénea contiene 20 g de limaduras de hierro, 40 g de arena (SiO₂), 30 g de NaCl, "
            "25 g de CuSO₄·5H₂O, 150 mL de agua y 50 mL de aceite vegetal. Recupera cada componente usando únicamente "
            "magnetismo, decantación, filtración, destilación simple, evaporación y recristalización. "
            "Considera que la solubilidad del CuSO₄·5H₂O disminuye mucho al enfriar y la del NaCl cambia muy poco."
        ),
        "sustancias": ["hierro", "arena", "cloruro_de_sodio", "sulfato_de_cobre_pentahidratado", "agua", "aceite"],
        "cantidades": {"hierro": 20, "arena": 40, "cloruro_de_sodio": 30, "sulfato_de_cobre_pentahidratado": 25, "agua": 150, "aceite": 50},
        "usar_cantidades": False,
        "permitidos": ["magnetismo", "decantacion", "filtracion", "destilacion", "evaporacion", "recristalizacion"],
        "pistas": ["Empieza por lo que se separa sin alterar nada.", "Con dos líquidos en capas, filtrar es incómodo.",
                   "Para recuperar el agua no basta con evaporar.", "Las dos sales se separan por su distinta solubilidad con la temperatura."],
        "preguntas": [{
            "pregunta": "¿Por qué el magnetismo debe aplicarse antes de la filtración?",
            "opciones": ["Porque el imán no funciona en seco",
                         "Porque al filtrar, el hierro quedaría retenido junto con la arena en el papel; además, en contacto con la disolución de CuSO₄ puede reaccionar",
                         "Porque el hierro se disuelve en el agua"],
            "correcta": 1,
            "explicacion": "El hierro es insoluble: al filtrar quedaría mezclado con la arena. Retirarlo antes también evita que reaccione con el Cu²⁺ disuelto (Fe + Cu²⁺ → Fe²⁺ + Cu).",
        }],
        "fuente": "Ficha de clase (pregunta 2)",
    },
    {
        "id": "a2", "nivel": "avanzado", "titulo": "Arena, agua, aceite y dos sales (ficha D)",
        "enunciado": (
            "Una mezcla contiene arena, agua, aceite vegetal, NaCl y CuSO₄. Usa decantación, filtración, destilación simple, "
            "evaporación y recristalización. La arena es insoluble; el aceite es inmiscible con el agua y menos denso; "
            "el CuSO₄ forma cristales al enfriar una disolución caliente."
        ),
        "sustancias": ["arena", "agua", "aceite", "cloruro_de_sodio", "sulfato_de_cobre"],
        "permitidos": ["decantacion", "filtracion", "destilacion", "evaporacion", "recristalizacion"],
        "solubilidades": TABLA_D,
        "pistas": ["Empieza por los líquidos que forman capas.", "Mira cuánto cambia la solubilidad de cada sal entre 20 y 80 °C."],
        "fuente": "Ficha de clase (pregunta 9)",
    },
    {
        "id": "a3", "nivel": "avanzado", "titulo": "Agua, alcohol y sal",
        "enunciado": "Recupera el agua, el etanol y la sal de una disolución que contiene los tres.",
        "sustancias": ["agua", "etanol", "cloruro_de_sodio"], "permitidos": ["filtracion", "destilacion", "destilacion_fraccionada", "evaporacion", "cristalizacion"],
        "pistas": ["Los dos líquidos son miscibles y tienen distinto punto de ebullición.", "La sal no es volátil."],
        "fuente": "SEPARALAB",
    },
    {
        "id": "a4", "nivel": "avanzado", "titulo": "Mezcla con colorantes (variante de la ficha G)",
        "enunciado": (
            "Una mezcla contiene arena, agua, aceite vegetal, sulfato de cobre(II), etanol y dos colorantes orgánicos. "
            "Recupera, en la medida de lo posible, los componentes usando decantación, filtración, destilación simple, "
            "evaporación, recristalización y cromatografía. Tras las primeras separaciones se obtiene una solución acuosa "
            "con el sulfato de cobre y los dos colorantes."
        ),
        "sustancias": ["arena", "agua", "aceite", "sulfato_de_cobre", "etanol", "colorante_a", "colorante_b"],
        "permitidos": ["decantacion", "filtracion", "destilacion", "evaporacion", "recristalizacion", "cromatografia"],
        "pistas": ["Primero los líquidos inmiscibles, después los sólidos.", "Los colorantes se separan e identifican en el papel."],
        "fuente": "Ficha de clase (pregunta 4)",
    },
    # ------------------------------------------------------------------ desafío
    {
        "id": "d1", "nivel": "desafio", "titulo": "Seis componentes y dos colorantes (ficha G)",
        "enunciado": (
            "Una mezcla contiene 50,0 g de arena, 100 mL de agua, 40 mL de aceite vegetal, 15,0 g de NaCl, 20,0 g de CuSO₄, "
            "30 mL de etanol y dos colorantes orgánicos, A y B. Sepáralos en la medida de lo posible con sedimentación, "
            "decantación, filtración, destilación simple, evaporación, recristalización y cromatografía de papel. "
            "Usa la tabla de solubilidades del enunciado."
        ),
        "sustancias": ["arena", "agua", "aceite", "cloruro_de_sodio", "sulfato_de_cobre", "etanol", "colorante_a", "colorante_b"],
        "cantidades": {"arena": 50, "agua": 100, "aceite": 40, "cloruro_de_sodio": 15, "sulfato_de_cobre": 20, "etanol": 30},
        "usar_cantidades": True,
        "solubilidades": TABLA_G,
        "permitidos": ["sedimentacion", "decantacion", "filtracion", "destilacion", "evaporacion", "recristalizacion", "cromatografia"],
        "pistas": ["El etanol y el agua se separan por destilación, pero no del todo.", "Comprueba con la tabla cuánta agua hace falta para que solo cristalice el CuSO₄.",
                   "La cromatografía no recupera gramos de colorante."],
        "preguntas": [{
            "pregunta": "En el cromatograma, el frente del disolvente recorre 12,0 cm, el colorante A 4,2 cm y el B 8,4 cm. ¿Cuál tiene más afinidad por la fase estacionaria?",
            "opciones": ["A (Rf = 0,35)", "B (Rf = 0,70)", "Ambos igual"],
            "correcta": 0,
            "explicacion": "Rf(A) = 4,2/12,0 = 0,35 y Rf(B) = 8,4/12,0 = 0,70. A avanza menos: interacciona más con la fase estacionaria.",
        }],
        "fuente": "Ficha de clase (pregunta 2)",
    },
    {
        "id": "d2", "nivel": "desafio", "titulo": "¿Cristaliza solo el sulfato de cobre? (ficha C con números)",
        "enunciado": (
            "Retoma la ficha C (30 g de NaCl y 25 g de CuSO₄·5H₂O tras la destilación). Con los datos de solubilidad de la "
            "ficha G, comprueba si al disolver las sales en la mínima agua caliente y enfriar a 20 °C cristaliza solo el sulfato de cobre."
        ),
        "sustancias": ["cloruro_de_sodio", "sulfato_de_cobre_pentahidratado"],
        "cantidades": {"cloruro_de_sodio": 30, "sulfato_de_cobre_pentahidratado": 25},
        "usar_cantidades": True,
        "solubilidades": TABLA_G,
        "permitidos": ["recristalizacion", "evaporacion", "cristalizacion", "filtracion"],
        "parcial_esperado": True,
        "pistas": ["25 g de CuSO₄·5H₂O contienen solo 15,98 g de CuSO₄.", "Calcula el agua mínima para disolver los 30 g de NaCl a 80 °C y cuánto NaCl admite esa agua a 20 °C."],
        "preguntas": [{
            "pregunta": "Con la mínima agua a 80 °C (78,1 g), ¿qué cristaliza al enfriar a 20 °C?",
            "opciones": ["Solo CuSO₄·5H₂O", "Sobre todo NaCl (unos 1,9 g) y nada de CuSO₄·5H₂O", "Nada"],
            "correcta": 1,
            "explicacion": ("A 20 °C, 78,1 g de agua disuelven 28,1 g de NaCl (quedan 1,9 g sin disolver) y 16,2 g de CuSO₄, "
                            "más que los 15,98 g presentes. El razonamiento cualitativo es correcto, pero con estas masas la "
                            "separación no es limpia."),
        }],
        "fuente": "SEPARALAB, a partir de las fichas C y G",
    },
    {
        "id": "d3", "nivel": "desafio", "titulo": "Sólidos secos que reaccionan con agua",
        "enunciado": "Una mezcla seca de limaduras de hierro, arena y sulfato de cobre(II) anhidro. Recupera los tres sin que ocurra ninguna reacción química.",
        "sustancias": ["hierro", "arena", "sulfato_de_cobre"],
        "permitidos": ["magnetismo", "filtracion", "evaporacion", "cristalizacion", "destilacion"],
        "pistas": ["¿Qué pasaría si añades agua con el hierro presente?", "Fe + Cu²⁺ → Fe²⁺ + Cu"],
        "fuente": "SEPARALAB",
    },
]

NIVELES = {
    "basico": "Básico",
    "intermedio": "Intermedio",
    "avanzado": "Avanzado",
    "desafio": "Desafío",
}


def obtener_reto(id_reto):
    return next((r for r in RETOS if r["id"] == id_reto), None)
