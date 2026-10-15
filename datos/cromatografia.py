# datos/cromatografia.py
# Ejercicios de cromatografía de las fichas de clase y preajustes de la
# simulación. Los Rf de las fichas son datos de esos ejercicios (no constantes
# universales). Los marcados como "ilustrativo" son inventados con fines
# didácticos y así se indica en la interfaz.

EJERCICIOS = [
    {
        "id": "aplicacion1",
        "titulo": "Ejemplo de aplicación 1 · cromatografía en capa fina",
        "tecnica": "TLC",
        "condiciones": "Fase estacionaria: sílice (polar). Fase móvil: disolvente hidrocarbonado (apolar).",
        "frente": 12.0,
        "manchas": [
            {"nombre": "Mancha roja", "distancia": 8.0, "color": "#e5484d"},
            {"nombre": "Mancha verde", "distancia": 6.0, "color": "#30a46c"},
            {"nombre": "Mancha azul", "distancia": 2.0, "color": "#3e63dd"},
            {"nombre": "Mancha negra", "distancia": 0.0, "color": "#1c2024"},
        ],
        "pide": ["Mancha roja", "Mancha azul"],
        "pregunta": {
            "texto": "La fase estacionaria es sílice y el disolvente es un hidrocarburo. Entre la mancha roja y la azul, ¿cuál corresponde al componente más polar?",
            "opciones": ["La roja", "La azul"],
            "correcta": 1,
            "explicacion": ("La sílice es polar (grupos –OH) y el hidrocarburo es apolar. El componente más polar interacciona más con la "
                            "sílice y avanza menos: la azul (Rf 0,17) frente a la roja (Rf 0,67). La negra no se movió en este ensayo (Rf 0). "
                            "La polaridad es una guía, no la única causa: también influyen el tamaño y los enlaces de hidrógeno."),
        },
        "fuente": "Ficha de clase · Ejemplo de aplicación 1",
    },
    {
        "id": "aplicacion2",
        "titulo": "Ejemplo de aplicación 2 · cromatografía en papel",
        "tecnica": "papel",
        "condiciones": "Papel de cromatografía. Disolvente: butan-1-ol, propanona y agua.",
        "frente": 9.0,
        "manchas": [
            {"nombre": "Mancha 1", "distancia": 8.0, "color": "#8e4ec6"},
            {"nombre": "Mancha 2", "distancia": 4.0, "color": "#f76b15"},
        ],
        "pide": ["Mancha 1", "Mancha 2"],
        "pregunta": {
            "texto": "¿Qué mancha corresponde a la sustancia con más afinidad por la fase móvil?",
            "opciones": ["Mancha 1", "Mancha 2"],
            "correcta": 0,
            "explicacion": "La mancha 1 (Rf 0,89) avanza casi con el frente: se disuelve mejor en la fase móvil que en el agua unida al papel.",
        },
        "fuente": "Ficha de clase · Ejemplo de aplicación 2",
    },
    {
        "id": "lapicero",
        "titulo": "Tinta de un lapicero",
        "tecnica": "papel",
        "condiciones": "Papel de filtro. Fase móvil: etanol.",
        "frente": 12.0,
        "manchas": [
            {"nombre": "Color 1", "distancia": 3.0, "color": "#3e63dd"},
            {"nombre": "Color 2", "distancia": 5.0, "color": "#8e4ec6"},
            {"nombre": "Color 3", "distancia": 8.0, "color": "#e54666"},
        ],
        "pide": ["Color 1", "Color 2", "Color 3"],
        "nota_terminologia": "La ficha llama a este valor «coeficiente de reparto»; en los apuntes es el factor de retención o retardo, Rf.",
        "fuente": "Ficha de examen (pregunta 1b)",
    },
    {
        "id": "ficha_g",
        "titulo": "Colorantes A y B (ficha G)",
        "tecnica": "papel",
        "condiciones": "Papel cromatográfico con un disolvente adecuado (no especificado en la ficha).",
        "frente": 12.0,
        "manchas": [
            {"nombre": "Colorante A", "distancia": 4.2, "color": "#12a594"},
            {"nombre": "Colorante B", "distancia": 8.4, "color": "#d6409f"},
        ],
        "pide": ["Colorante A", "Colorante B"],
        "pregunta": {
            "texto": "¿Cuál de los dos colorantes presenta mayor afinidad por la fase estacionaria?",
            "opciones": ["Colorante A", "Colorante B"],
            "correcta": 0,
            "explicacion": "A tiene el Rf menor (0,35 frente a 0,70): avanza menos porque interacciona más con la fase estacionaria.",
        },
        "nota_terminologia": "La ficha llama a este valor «coeficiente de reparto»; en los apuntes es el factor de retención o retardo, Rf.",
        "fuente": "Ficha de clase (pregunta 2b)",
    },
    {
        "id": "variante_g",
        "titulo": "Colorantes A y B (variante de la ficha G)",
        "tecnica": "papel",
        "condiciones": "Papel cromatográfico.",
        "frente": 12.0,
        "manchas": [
            {"nombre": "Colorante A", "distancia": 3.6, "color": "#12a594"},
            {"nombre": "Colorante B", "distancia": 8.4, "color": "#d6409f"},
        ],
        "pide": ["Colorante A", "Colorante B"],
        "pregunta": {
            "texto": "A partir de los valores de Rf, ¿qué colorante tiene mayor afinidad por la fase estacionaria?",
            "opciones": ["Colorante A", "Colorante B"],
            "correcta": 0,
            "explicacion": "Rf(A) = 0,30 y Rf(B) = 0,70: A queda más cerca del origen, retenido por la fase estacionaria.",
        },
        "fuente": "Ficha de clase (pregunta 4)",
    },
]

PREGUNTAS_CONCEPTUALES = [
    {
        "id": "naftaleno",
        "texto": ("Una mezcla de naftaleno (C₁₀H₈) y naftol (C₁₀H₈O) se analiza por TLC con sílice polar como fase estacionaria "
                  "y hexano apolar como fase móvil. ¿Qué sustancia avanzará más?"),
        "opciones": ["El naftaleno", "El naftol", "Las dos igual"],
        "correcta": 0,
        "explicacion": ("El naftol tiene un grupo –OH que forma enlaces de hidrógeno con la sílice, así que queda más retenido. "
                        "El naftaleno, apolar, se disuelve mejor en el hexano y avanza más: tendrá el Rf mayor. "
                        "Para calcular su Rf hacen falta las distancias medidas en el cromatograma."),
        "fuente": "Ficha de clase (pregunta 10, sin el diagrama)",
    },
    {
        "id": "lapiz",
        "texto": "¿Por qué la línea de origen se traza con lápiz y no con bolígrafo?",
        "opciones": ["Porque se ve mejor", "Porque el grafito no se disuelve en el disolvente; la tinta del bolígrafo se separaría también",
                     "Porque el lápiz absorbe el disolvente"],
        "correcta": 1,
        "explicacion": "La tinta del bolígrafo contiene colorantes que también se separarían y estropearían el cromatograma.",
        "fuente": "SEPARALAB",
    },
    {
        "id": "tapa",
        "texto": "¿Para qué se tapa la cámara de cromatografía?",
        "opciones": ["Para que no entre luz", "Para que el aire se sature de vapor de disolvente y este no se evapore del papel",
                     "Para calentar el disolvente"],
        "correcta": 1,
        "explicacion": "Según los apuntes, la tapa satura la atmósfera de la cámara con vapor del disolvente y evita su pérdida por evaporación.",
        "fuente": "Apuntes de clase",
    },
    {
        "id": "nivel",
        "texto": "¿Qué ocurre si el nivel del disolvente queda por encima de la línea de origen?",
        "opciones": ["Nada", "La muestra se disuelve en el disolvente de la cámara en lugar de ascender por el papel",
                     "El Rf se duplica"],
        "correcta": 1,
        "explicacion": "La mancha se lava hacia el disolvente del fondo y no se forma un cromatograma.",
        "fuente": "SEPARALAB",
    },
]

IDENTIFICACION = {
    "titulo": "Identificar los colorantes de una muestra (ejercicio ilustrativo)",
    "ilustrativo": True,
    "condiciones": "Mismo papel, mismo disolvente y misma cámara para todas las muestras.",
    "frente": 10.0,
    "patrones": [
        {"nombre": "Patrón amarillo", "distancia": 8.5, "color": "#ffc53d"},
        {"nombre": "Patrón azul", "distancia": 5.0, "color": "#3e63dd"},
        {"nombre": "Patrón rojo", "distancia": 2.5, "color": "#e5484d"},
    ],
    "muestra": [
        {"distancia": 8.5, "color": "#ffc53d"},
        {"distancia": 2.5, "color": "#e5484d"},
    ],
    "correctos": ["Patrón amarillo", "Patrón rojo"],
    "explicacion": ("Las manchas de la muestra están a la misma altura que los patrones amarillo y rojo en la MISMA placa y con el mismo "
                    "disolvente: coinciden sus Rf (0,85 y 0,25). Comparar Rf solo es válido si las condiciones son idénticas."),
}

# Simulación: preajustes con los Rf de los ejercicios de clase.
SIMULACIONES = [
    {"id": e["id"], "titulo": e["titulo"], "tecnica": e["tecnica"], "condiciones": e["condiciones"],
     "manchas": [{"nombre": m["nombre"], "rf": round(m["distancia"] / e["frente"], 3), "color": m["color"]} for m in e["manchas"]],
     "ilustrativo": False, "fuente": e["fuente"]}
    for e in EJERCICIOS
] + [
    {
        "id": "rotulador",
        "titulo": "Tinta negra de rotulador soluble en agua (ilustrativo)",
        "tecnica": "papel",
        "condiciones": "Papel de filtro y agua como fase móvil.",
        "manchas": [
            {"nombre": "Componente amarillo", "rf": 0.85, "color": "#ffc53d"},
            {"nombre": "Componente rosa", "rf": 0.6, "color": "#e54666"},
            {"nombre": "Componente azul", "rf": 0.3, "color": "#3e63dd"},
        ],
        "ilustrativo": True,
        "fuente": "Valores inventados para la simulación: cada tinta da resultados distintos.",
    },
]
