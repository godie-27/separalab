# datos/metodos.py
# Métodos de separación: fundamento, materiales, procedimiento, precauciones y
# limitaciones. La lógica que decide cuándo se aplican está en logica/reglas.py.

METODOS = {
    "magnetismo": {
        "nombre": "Separación magnética (imantación)",
        "propiedad": "Magnetismo",
        "descripcion": "Un imán atrae el sólido ferromagnético y lo retira de la mezcla.",
        "fundamento": (
            "En una mezcla cada componente conserva sus propiedades características. El hierro metálico "
            "es ferromagnético y el imán lo atrae; los demás componentes no responden al imán y se quedan."
        ),
        "cuando": "Hay un sólido magnético (hierro metálico) mezclado con materiales no magnéticos.",
        "materiales": ["iman", "vaso_precipitados", "espatula", "vidrio_reloj"],
        "procedimiento": [
            "Cubrir el imán con papel o una bolsa fina para poder soltar después el hierro.",
            "Pasar el imán cerca de la mezcla, removiéndola, hasta que no se atraiga más sólido.",
            "Retirar el imán sobre un vidrio de reloj y quitar el papel para soltar el hierro.",
            "Repetir hasta que el imán ya no atraiga partículas.",
        ],
        "precauciones": ["Envolver el imán: las limaduras pegadas directamente cuestan de despegar."],
        "limitaciones": [
            "Solo funciona con hierro metálico (también níquel o cobalto); los compuestos de hierro como el FeS o la herrumbre no se comportan igual.",
            "Pueden quedar partículas no magnéticas atrapadas entre las limaduras.",
        ],
        "observar": "Cómo las limaduras se orientan y se pegan al imán mientras la arena o el azufre quedan en el recipiente.",
        "montaje": "magnetismo",
    },
    "decantacion": {
        "nombre": "Decantación con embudo de separación",
        "propiedad": "Inmiscibilidad y diferencia de densidad",
        "descripcion": "Dos líquidos que no se mezclan forman capas; se abre la llave para retirar la capa inferior.",
        "fundamento": (
            "Las moléculas polares del agua se atraen entre sí más que con las del aceite (poco polar), "
            "por eso no se mezclan y forman dos fases. La fase menos densa queda arriba."
        ),
        "cuando": "Hay dos líquidos inmiscibles (por ejemplo, agua y aceite).",
        "materiales": ["embudo_decantacion", "soporte_universal", "vaso_precipitados", "matraz_erlenmeyer"],
        "procedimiento": [
            "Colocar el embudo de separación en el aro del soporte con la llave cerrada.",
            "Verter la mezcla y dejar reposar hasta que se vean dos capas nítidas.",
            "Quitar el tapón y abrir la llave para recoger la capa inferior en un vaso.",
            "Cerrar la llave justo cuando la interfase llega a ella.",
            "Verter la capa superior por la boca del embudo a otro recipiente.",
        ],
        "precauciones": ["Quitar el tapón antes de abrir la llave para que el líquido salga sin vacío."],
        "limitaciones": [
            "En la interfase siempre se pierde o se mezcla un poco de líquido.",
            "Las sustancias disueltas se reparten entre las fases según su solubilidad en cada una.",
        ],
        "observar": "La interfase entre las dos capas y el momento de cerrar la llave.",
        "montaje": "decantacion",
    },
    "filtracion": {
        "nombre": "Filtración",
        "propiedad": "Solubilidad y tamaño de partícula",
        "descripcion": "El papel de filtro retiene el sólido insoluble y deja pasar el líquido con lo que lleva disuelto.",
        "fundamento": (
            "Los poros del papel son mayores que las moléculas y los iones disueltos, pero menores que "
            "las partículas del sólido insoluble. Lo disuelto atraviesa el filtro: por eso la filtración "
            "no separa una sal de su disolución."
        ),
        "cuando": "Hay un sólido insoluble en un líquido.",
        "materiales": ["embudo", "papel_filtro", "soporte_universal", "vaso_precipitados", "varilla", "matraz_erlenmeyer"],
        "procedimiento": [
            "Doblar el papel de filtro en cono y colocarlo en el embudo; humedecerlo para que se adhiera.",
            "Colocar el embudo en el soporte con un recipiente limpio debajo.",
            "Verter la mezcla poco a poco ayudándose de la varilla de vidrio, sin superar el borde del papel.",
            "Lavar el residuo con un poco de líquido limpio para arrastrar lo disuelto.",
            "Dejar secar el residuo sobre el papel o en un vidrio de reloj.",
        ],
        "precauciones": ["No rellenar el embudo por encima del borde del papel."],
        "limitaciones": [
            "Las partículas muy finas (arcilla) pueden atravesar el papel o taparlo; conviene dejar sedimentar antes.",
            "El residuo queda húmedo y con restos de lo disuelto si no se lava.",
        ],
        "observar": "El filtrado sale transparente mientras el sólido se queda en el papel.",
        "montaje": "filtracion",
    },
    "sedimentacion": {
        "nombre": "Sedimentación y decantación del líquido",
        "propiedad": "Densidad (el sólido es más denso que el líquido)",
        "descripcion": "Se deja reposar para que el sólido se deposite y se vierte con cuidado el líquido de encima.",
        "fundamento": "La gravedad lleva al fondo las partículas más densas que el líquido.",
        "cuando": "Hay un sólido insoluble y denso en un líquido y basta una separación aproximada.",
        "materiales": ["vaso_precipitados", "varilla"],
        "procedimiento": [
            "Dejar la mezcla en reposo hasta que el sólido se deposite en el fondo.",
            "Inclinar el vaso y verter lentamente el líquido, ayudándose de la varilla, sin remover el sedimento.",
        ],
        "precauciones": [],
        "limitaciones": ["Menos completa que la filtración: el líquido arrastra partículas finas y el sedimento queda mojado."],
        "observar": "Cómo se aclara el líquido a medida que el sólido se deposita.",
        "montaje": "sedimentacion",
    },
    "destilacion": {
        "nombre": "Destilación simple",
        "propiedad": "Diferencia de punto de ebullición (volatilidad)",
        "descripcion": "Se calienta la mezcla; el componente más volátil se evapora, se condensa en el refrigerante y se recoge.",
        "fundamento": (
            "Al calentar aumenta la energía cinética media de las partículas. Las del componente más volátil "
            "(fuerzas intermoleculares más débiles) pasan antes al vapor; en el refrigerante pierden energía y "
            "se condensan. Los sólidos disueltos no son volátiles y quedan en el matraz."
        ),
        "cuando": "Recuperar un disolvente de una disolución, o separar líquidos miscibles con puntos de ebullición muy distintos.",
        "materiales": ["matraz_destilacion", "termometro", "refrigerante", "soporte_universal", "placa_calefactora", "piedras_ebullicion", "matraz_erlenmeyer"],
        "procedimiento": [
            "Llenar el matraz hasta la mitad como máximo y añadir piedras de ebullición.",
            "Colocar el termómetro con el bulbo a la altura de la salida lateral.",
            "Conectar el refrigerante: el agua entra por abajo y sale por arriba.",
            "Calentar suavemente y recoger el destilado mientras la temperatura se mantiene estable.",
            "Detener el calentamiento antes de que el matraz quede seco y dejar enfriar antes de desmontar.",
        ],
        "precauciones": [
            "Nunca calentar un sistema cerrado.",
            "No destilar hasta sequedad.",
            "Con líquidos inflamables (etanol), calentar con placa o manta, sin llama.",
        ],
        "limitaciones": [
            "Con líquidos miscibles de puntos de ebullición cercanos solo se obtiene un destilado enriquecido.",
            "Si el residuo se seca del todo, algunas sales cambian (los hidratos pierden agua).",
        ],
        "observar": "El termómetro se estabiliza mientras destila un componente y las gotas que caen del refrigerante.",
        "montaje": "destilacion",
    },
    "destilacion_fraccionada": {
        "nombre": "Destilación fraccionada",
        "propiedad": "Diferencia de punto de ebullición",
        "descripcion": "Como la simple, pero con una columna que permite muchas condensaciones y vaporizaciones sucesivas.",
        "fundamento": (
            "En cada tramo de la columna el vapor se condensa y se vuelve a evaporar, enriqueciéndose cada vez "
            "en el componente más volátil. Equivale a muchas destilaciones simples seguidas."
        ),
        "cuando": "Líquidos miscibles con puntos de ebullición cercanos (etanol y agua, petróleo).",
        "materiales": ["matraz_destilacion", "columna_fraccionamiento", "termometro", "refrigerante", "soporte_universal", "placa_calefactora", "piedras_ebullicion", "matraz_erlenmeyer"],
        "procedimiento": [
            "Montar la columna de fraccionamiento entre el matraz y la cabeza de destilación.",
            "Calentar lentamente para que el vapor ascienda poco a poco por la columna.",
            "Recoger una fracción mientras la temperatura se mantiene constante.",
            "Cambiar de recipiente cuando la temperatura empiece a subir.",
        ],
        "precauciones": ["Etanol inflamable: calentar sin llama abierta."],
        "limitaciones": ["El etanol y el agua forman un azeótropo (≈ 95,6 % de etanol en masa): no se obtiene etanol puro."],
        "observar": "Cómo la temperatura sube en escalones y se recogen fracciones distintas.",
        "montaje": "destilacion_fraccionada",
    },
    "evaporacion": {
        "nombre": "Evaporación",
        "propiedad": "Volatilidad del disolvente",
        "descripcion": "Se calienta la disolución hasta que el disolvente pasa al aire y queda el sólido.",
        "fundamento": (
            "El disolvente es volátil y el soluto no. Al calentar, las partículas del disolvente escapan "
            "como vapor; las del soluto quedan en la cápsula."
        ),
        "cuando": "Recuperar un sólido disuelto cuando no interesa recuperar el disolvente.",
        "materiales": ["capsula", "tripode_rejilla", "mechero", "varilla"],
        "procedimiento": [
            "Verter la disolución en una cápsula de porcelana.",
            "Calentar suavemente removiendo con la varilla.",
            "Retirar el calor cuando quede poco líquido y dejar que el calor residual termine la evaporación.",
            "Dejar enfriar y recoger el sólido.",
        ],
        "precauciones": ["Calentar al final con suavidad para evitar salpicaduras."],
        "limitaciones": [
            "El disolvente se pierde.",
            "Si hay varios solutos, quedan todos juntos.",
            "Las sustancias sensibles al calor (hidratos, azúcar) se alteran.",
        ],
        "observar": "Cómo aparece el sólido en los bordes de la cápsula cuando el líquido disminuye.",
        "montaje": "evaporacion",
    },
    "cristalizacion": {
        "nombre": "Cristalización",
        "propiedad": "Solubilidad (y su cambio con la temperatura)",
        "descripcion": "Se concentra la disolución y se deja enfriar o evaporar lentamente para que el soluto forme cristales.",
        "fundamento": (
            "Una disolución saturada no admite más soluto. Al quitar disolvente o enfriar, la solubilidad "
            "disminuye y las partículas del soluto se ordenan formando cristales."
        ),
        "cuando": "Obtener un sólido disuelto en forma de cristales, sobre todo si se altera al calentarlo a sequedad.",
        "materiales": ["vaso_precipitados", "placa_calefactora", "cristalizador", "embudo", "papel_filtro", "varilla"],
        "procedimiento": [
            "Calentar la disolución para evaporar parte del disolvente hasta que esté casi saturada.",
            "Verterla en un cristalizador y dejarla enfriar lentamente, tapada.",
            "Separar los cristales por filtración.",
            "Secar los cristales entre papeles de filtro, sin calentar.",
        ],
        "precauciones": [],
        "limitaciones": ["Parte del soluto queda disuelto en el líquido sobrante (aguas madres)."],
        "observar": "La formación de cristales con formas regulares a medida que la disolución se enfría.",
        "montaje": "cristalizacion",
    },
    "recristalizacion": {
        "nombre": "Recristalización (cristalización fraccionada)",
        "propiedad": "Distinta variación de la solubilidad con la temperatura",
        "descripcion": "Se disuelven las sales en agua caliente y al enfriar cristaliza sobre todo la que más cambia de solubilidad.",
        "fundamento": (
            "Cada sal tiene su propia curva de solubilidad. Si al enfriar la disolución la cantidad de una sal "
            "supera su solubilidad a la temperatura baja y la de la otra no, cristaliza solo la primera."
        ),
        "cuando": "Hay dos o más sales solubles cuyas solubilidades cambian de forma distinta con la temperatura.",
        "materiales": ["vaso_precipitados", "placa_calefactora", "termometro", "bano_hielo", "embudo", "papel_filtro", "varilla"],
        "procedimiento": [
            "Añadir agua caliente (unos 80 °C) a la mezcla de sales, la justa para disolverlas.",
            "Dejar enfriar lentamente hasta unos 20 °C.",
            "Filtrar los cristales formados.",
            "Conservar el filtrado (aguas madres), que contiene la otra sal.",
        ],
        "precauciones": ["Manipular el vaso caliente con pinzas."],
        "limitaciones": [
            "Funciona solo si las cantidades lo permiten: hay que comprobarlo con los datos de solubilidad.",
            "Las aguas madres siguen saturadas de la sal que cristaliza.",
        ],
        "observar": "Qué sal cristaliza al enfriar y el color de las aguas madres.",
        "montaje": "cristalizacion",
    },
    "disolucion": {
        "nombre": "Disolución en agua (operación auxiliar)",
        "propiedad": "Solubilidad",
        "descripcion": "Se añade agua para disolver los componentes solubles y poder separarlos de los insolubles.",
        "fundamento": (
            "El agua es polar: rodea a los iones o moléculas del soluto y los separa de su sólido (solvatación; "
            "con agua se llama hidratación). Los sólidos insolubles no interaccionan lo suficiente y quedan como partículas."
        ),
        "cuando": "Una mezcla de sólidos secos contiene al menos un sólido soluble en agua.",
        "materiales": ["vaso_precipitados", "probeta", "varilla"],
        "procedimiento": [
            "Añadir agua a la mezcla sólida en un vaso de precipitados.",
            "Agitar con la varilla hasta que no se disuelva más sólido.",
        ],
        "precauciones": [],
        "limitaciones": ["No separa nada por sí sola: prepara la mezcla para filtrar después."],
        "observar": "Cómo desaparecen los cristales del sólido soluble mientras el insoluble sigue visible.",
        "montaje": "disolucion",
    },
    "cromatografia": {
        "nombre": "Cromatografía en papel",
        "propiedad": "Diferente afinidad por la fase estacionaria y la fase móvil",
        "descripcion": "Los componentes de una mancha avanzan a distinta velocidad arrastrados por el disolvente.",
        "fundamento": (
            "El agua unida a la celulosa del papel es la fase estacionaria y el disolvente que asciende es la fase "
            "móvil. Cada componente se reparte entre ambas según sus fuerzas intermoleculares: el que tiene más "
            "afinidad por la fase móvil avanza más (Rf mayor)."
        ),
        "cuando": "Separar e identificar los componentes de una mezcla de colorantes o pigmentos.",
        "materiales": ["papel_cromatografia", "camara_cromatografia", "capilar", "lapiz_regla"],
        "procedimiento": [
            "Trazar con lápiz la línea de origen a 1–2 cm del borde inferior.",
            "Aplicar una gota pequeña de la muestra sobre la línea y dejar secar.",
            "Colocar el papel en la cámara con el disolvente por debajo de la línea de origen y tapar.",
            "Retirar el papel antes de que el disolvente llegue al borde y marcar el frente con lápiz.",
            "Medir la distancia de cada mancha y del frente desde la línea de origen y calcular Rf.",
        ],
        "precauciones": ["La línea de origen debe quedar por encima del nivel del disolvente."],
        "limitaciones": [
            "Es una técnica analítica: separa e identifica cantidades muy pequeñas, no recupera gramos.",
            "El Rf depende de las condiciones (papel, disolvente, temperatura).",
        ],
        "observar": "Cómo la mancha inicial se divide en varias que suben a distinta altura.",
        "montaje": "cromatografia",
    },
}

# Métodos que el estudiante puede elegir (la disolución es auxiliar y siempre está permitida).
METODOS_SEPARACION = [
    "magnetismo", "decantacion", "filtracion", "sedimentacion", "destilacion",
    "destilacion_fraccionada", "evaporacion", "cristalizacion", "recristalizacion", "cromatografia",
]
METODOS_AUXILIARES = ["disolucion"]


def obtener_metodo(clave):
    """Devuelve la información de un método."""
    return METODOS.get(clave)


def listar_metodos():
    """Devuelve las claves de todos los métodos disponibles."""
    return list(METODOS.keys())
