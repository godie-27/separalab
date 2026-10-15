# datos/sustancias.py
# Catálogo de sustancias y propiedades físicas de SEPARALAB.
#
# Criterios:
# - Los valores numéricos generales (densidad, punto de ebullición) son valores
#   de referencia aproximados, a 20 °C y 1 atm, como los que aparecen en los
#   libros de texto. Se marcan como "aprox." en la interfaz.
# - Los datos de solubilidad de NaCl y CuSO4 proceden de las fichas de clase
#   (Ejemplo G, g/100 mL de agua) y coinciden con los del proyecto original.
#   Cada ejercicio puede sustituirlos por sus propios datos.
# - "solubilidad" indica el comportamiento cualitativo en cada líquido:
#   "soluble", "poco_soluble", "insoluble" o None (dato desconocido).
# - "tipo" distingue elemento, compuesto o material (mezcla natural que el
#   modelo trata como un único componente, p. ej. la arena o el aceite).

SUSTANCIAS = {
    # ------------------------------------------------------------- líquidos
    "agua": {
        "nombre": "Agua",
        "formula": "H₂O",
        "simbolo": "H₂O",
        "tipo": "compuesto",
        "estado": "liquido",
        "magnetico": False,
        "densidad": 1.00,
        "punto_ebullicion": 100.0,
        "volatil": True,
        "polaridad": "polar",
        "solubilidad": {},
        "descripcion": "Disolvente polar; disuelve muchos sólidos iónicos por interacciones ion-dipolo (hidratación).",
        "peligros": [],
    },
    "etanol": {
        "nombre": "Etanol (alcohol)",
        "formula": "C₂H₅OH",
        "simbolo": "EtOH",
        "tipo": "compuesto",
        "estado": "liquido",
        "magnetico": False,
        "densidad": 0.79,
        "punto_ebullicion": 78.4,
        "volatil": True,
        "polaridad": "polar",
        "solubilidad": {},
        "descripcion": "Líquido polar, miscible con el agua porque ambos forman enlaces de hidrógeno.",
        "peligros": ["Inflamable: calentar sin llama abierta (manta o placa calefactora)."],
    },
    "aceite": {
        "nombre": "Aceite vegetal",
        "formula": None,
        "simbolo": "Aceite",
        "tipo": "material",
        "estado": "liquido",
        "magnetico": False,
        "densidad": 0.92,
        "punto_ebullicion": None,
        "volatil": False,
        "polaridad": "apolar",
        "solubilidad": {},
        "descripcion": "Mezcla de triglicéridos, poco polar; inmiscible con el agua y menos densa que ella.",
        "peligros": [],
    },
    # ------------------------------------------------------------- sólidos
    "arena": {
        "nombre": "Arena",
        "formula": "SiO₂",
        "simbolo": "SiO₂",
        "tipo": "material",
        "estado": "solido",
        "magnetico": False,
        "densidad": 2.65,
        "particula": "gruesa",
        "solubilidad": {"agua": "insoluble", "etanol": "insoluble", "aceite": "insoluble"},
        "descripcion": "Formada principalmente por dióxido de silicio (sólido covalente en red); insoluble en agua.",
        "peligros": [],
    },
    "hierro": {
        "nombre": "Hierro (limaduras)",
        "formula": "Fe",
        "simbolo": "Fe",
        "tipo": "elemento",
        "estado": "solido",
        "magnetico": True,
        "densidad": 7.87,
        "particula": "gruesa",
        "solubilidad": {"agua": "insoluble", "etanol": "insoluble", "aceite": "insoluble"},
        "descripcion": "Metal ferromagnético: un imán lo atrae. Insoluble en agua (con el tiempo se oxida).",
        "peligros": [],
    },
    "azufre": {
        "nombre": "Azufre (polvo)",
        "formula": "S",
        "simbolo": "S",
        "tipo": "elemento",
        "estado": "solido",
        "magnetico": False,
        "densidad": 2.07,
        "particula": "fina",
        "solubilidad": {"agua": "insoluble", "etanol": "poco_soluble", "aceite": None},
        "descripcion": "No metal amarillo, no magnético e insoluble en agua.",
        "peligros": ["No calentar mezclado con hierro: reaccionan y forman sulfuro de hierro(II)."],
    },
    "sulfuro_de_hierro": {
        "nombre": "Sulfuro de hierro(II)",
        "formula": "FeS",
        "simbolo": "FeS",
        "tipo": "compuesto",
        "estado": "solido",
        "magnetico": False,
        "densidad": 4.84,
        "particula": "fina",
        "solubilidad": {"agua": "insoluble", "etanol": "insoluble", "aceite": "insoluble"},
        "descripcion": (
            "Compuesto formado al calentar hierro y azufre. Según los apuntes, no es magnético "
            "y no huele a azufre: no conserva las propiedades de sus elementos."
        ),
        "peligros": [],
    },
    "cloruro_de_sodio": {
        "nombre": "Cloruro de sodio (sal)",
        "formula": "NaCl",
        "simbolo": "NaCl",
        "tipo": "compuesto",
        "estado": "solido",
        "magnetico": False,
        "densidad": 2.16,
        "particula": "gruesa",
        "solubilidad": {"agua": "soluble", "etanol": "poco_soluble", "aceite": "insoluble"},
        "solubilidad_agua": {
            "unidad": "g/100 mL de agua",
            20: 36.0,
            80: 38.4,
            "fuente": "Ficha de clase (Ejemplo G)",
        },
        "descripcion": "Sólido iónico; en agua sus iones se hidratan (interacción ion-dipolo). Su solubilidad casi no cambia con la temperatura.",
        "peligros": [],
    },
    "sulfato_de_cobre": {
        "nombre": "Sulfato de cobre(II) anhidro",
        "formula": "CuSO₄",
        "simbolo": "CuSO₄",
        "tipo": "compuesto",
        "estado": "solido",
        "magnetico": False,
        "densidad": 3.60,
        "particula": "fina",
        "masa_molar": 159.61,
        "cristaliza_como": "sulfato_de_cobre_pentahidratado",
        "se_altera_al_calentar": (
            "Si la disolución se evapora a sequedad con calor fuerte, el sólido queda parcialmente deshidratado "
            "(mezcla de azul y blanco); para obtener cristales azules de CuSO₄·5H₂O conviene cristalizar."
        ),
        "solubilidad": {"agua": "soluble", "etanol": "poco_soluble", "aceite": "insoluble"},
        "solubilidad_agua": {
            "unidad": "g/100 mL de agua (como CuSO₄ anhidro)",
            20: 20.7,
            80: 57.4,
            "fuente": "Ficha de clase (Ejemplo G)",
        },
        "descripcion": (
            "Polvo blanco. Al disolverse forma iones Cu²⁺ hidratados (disolución azul). "
            "Al cristalizar desde agua se obtiene CuSO₄·5H₂O azul, no la forma anhidra."
        ),
        "peligros": ["Nocivo si se ingiere e irritante: usar guantes y gafas."],
    },
    "sulfato_de_cobre_pentahidratado": {
        "nombre": "Sulfato de cobre(II) pentahidratado",
        "formula": "CuSO₄·5H₂O",
        "simbolo": "CuSO₄·5H₂O",
        "tipo": "compuesto",
        "estado": "solido",
        "magnetico": False,
        "densidad": 2.29,
        "particula": "gruesa",
        "masa_molar": 249.69,
        "anhidro": "sulfato_de_cobre",
        "cristaliza_como": "sulfato_de_cobre_pentahidratado",
        "se_altera_al_calentar": (
            "Al calentarlo hasta sequedad pierde su agua de hidratación y pasa de azul a blanco "
            "(CuSO₄ anhidro): ya no se recupera como pentahidrato."
        ),
        "solubilidad": {"agua": "soluble", "etanol": "poco_soluble", "aceite": "insoluble"},
        "descripcion": "Cristales azules. Cada 25,0 g contienen 15,98 g de CuSO₄ y 9,02 g de agua de hidratación.",
        "peligros": ["Nocivo si se ingiere e irritante: usar guantes y gafas."],
    },
    "arcilla": {
        "nombre": "Arcilla",
        "formula": None,
        "simbolo": "Arcilla",
        "tipo": "material",
        "estado": "solido",
        "magnetico": False,
        "densidad": 2.5,
        "particula": "muy_fina",
        "solubilidad": {"agua": "insoluble", "etanol": "insoluble", "aceite": "insoluble"},
        "descripcion": (
            "Mezcla de aluminosilicatos hidratados (no tiene una fórmula única). Insoluble, "
            "pero sus partículas son tan finas que forman una suspensión turbia."
        ),
        "peligros": [],
    },
    "carbonato_de_calcio": {
        "nombre": "Carbonato de calcio (tiza)",
        "formula": "CaCO₃",
        "simbolo": "CaCO₃",
        "tipo": "compuesto",
        "estado": "solido",
        "magnetico": False,
        "densidad": 2.71,
        "particula": "fina",
        "solubilidad": {"agua": "insoluble", "etanol": "insoluble", "aceite": "insoluble"},
        "descripcion": (
            "Sólido iónico prácticamente insoluble en agua (se disuelve del orden de miligramos por litro): "
            "no todos los compuestos iónicos son solubles."
        ),
        "peligros": ["Reacciona con los ácidos y libera CO₂: eso sería un cambio químico, no una separación."],
    },
    "oxido_de_hierro": {
        "nombre": "Óxido de hierro(III) hidratado (herrumbre)",
        "formula": "Fe₂O₃·nH₂O",
        "simbolo": "Fe₂O₃·nH₂O",
        "tipo": "compuesto",
        "estado": "solido",
        "magnetico": False,
        "densidad": None,
        "particula": "fina",
        "solubilidad": {"agua": "insoluble", "etanol": "insoluble", "aceite": "insoluble"},
        "descripcion": "Contiene hierro, pero no es hierro metálico: un imán no lo separa como a las limaduras.",
        "peligros": [],
    },
    "sacarosa": {
        "nombre": "Sacarosa (azúcar)",
        "formula": "C₁₂H₂₂O₁₁",
        "simbolo": "C₁₂H₂₂O₁₁",
        "tipo": "compuesto",
        "estado": "solido",
        "magnetico": False,
        "densidad": 1.59,
        "particula": "gruesa",
        "solubilidad": {"agua": "soluble", "etanol": "poco_soluble", "aceite": "insoluble"},
        "se_altera_al_calentar": "Si se calienta a sequedad se carameliza y se descompone: conviene cristalizarla, no evaporar a sequedad.",
        "descripcion": "Compuesto molecular muy soluble en agua: se disuelve por enlaces de hidrógeno, sin formar iones.",
        "peligros": [],
    },
    "colorante_a": {
        "nombre": "Colorante orgánico A",
        "formula": None,
        "simbolo": "Col. A",
        "tipo": "compuesto",
        "estado": "solido",
        "categoria": "colorante",
        "magnetico": False,
        "densidad": None,
        "particula": "fina",
        "solubilidad": {"agua": "soluble", "etanol": "soluble", "aceite": "insoluble"},
        "supuesto": "Se supone soluble en la fase acuosa, como en la variante del Ejemplo G de las fichas.",
        "descripcion": "Colorante presente en pequeña cantidad; se separa e identifica por cromatografía.",
        "peligros": [],
    },
    "colorante_b": {
        "nombre": "Colorante orgánico B",
        "formula": None,
        "simbolo": "Col. B",
        "tipo": "compuesto",
        "estado": "solido",
        "categoria": "colorante",
        "magnetico": False,
        "densidad": None,
        "particula": "fina",
        "solubilidad": {"agua": "soluble", "etanol": "soluble", "aceite": "insoluble"},
        "supuesto": "Se supone soluble en la fase acuosa, como en la variante del Ejemplo G de las fichas.",
        "descripcion": "Colorante presente en pequeña cantidad; se separa e identifica por cromatografía.",
        "peligros": [],
    },
}

# Miscibilidad entre pares de líquidos: True, False o ausente (desconocido).
MISCIBILIDAD = {
    frozenset({"agua", "etanol"}): True,
    frozenset({"agua", "aceite"}): False,
    # aceite + etanol: depende del aceite y de la temperatura; no se registra.
}

# Pares de líquidos que forman azeótropo (límite de la destilación).
AZEOTROPOS = {
    frozenset({"agua", "etanol"}): "El etanol y el agua forman un azeótropo (≈ 95,6 % de etanol en masa): ninguna destilación da etanol puro.",
}

ORDEN_CATALOGO = list(SUSTANCIAS.keys())


def obtener_sustancia(clave):
    """Devuelve los datos de una sustancia por su clave."""
    return SUSTANCIAS.get(clave)


def listar_sustancias():
    """Devuelve las claves de las sustancias disponibles."""
    return list(SUSTANCIAS.keys())


def miscibilidad(clave_a, clave_b):
    """True (miscibles), False (inmiscibles) o None (dato desconocido)."""
    if clave_a == clave_b:
        return True
    return MISCIBILIDAD.get(frozenset({clave_a, clave_b}))


def son_miscibles(sustancia_a, sustancia_b):
    """Compatibilidad con la versión anterior: recibe diccionarios con 'clave'."""
    return miscibilidad(sustancia_a.get("clave"), sustancia_b.get("clave"))


def solubilidad(clave_solido, clave_liquido):
    """'soluble', 'poco_soluble', 'insoluble' o None."""
    datos = SUSTANCIAS.get(clave_solido, {})
    return datos.get("solubilidad", {}).get(clave_liquido)


def nombre(clave):
    return SUSTANCIAS.get(clave, {}).get("nombre", clave)


def masa_anhidra(clave, masa):
    """Convierte la masa de un hidrato en masa de sal anhidra (si procede)."""
    datos = SUSTANCIAS[clave]
    anhidro = datos.get("anhidro")
    if not anhidro or masa is None:
        return masa
    return masa * SUSTANCIAS[anhidro]["masa_molar"] / datos["masa_molar"]


def agua_por_gramo_anhidro(clave_anhidro):
    """g de agua de hidratación que acompañan a 1 g de sal anhidra al cristalizar."""
    hidrato = SUSTANCIAS[clave_anhidro].get("cristaliza_como")
    if not hidrato or hidrato == clave_anhidro:
        return 0.0
    m_h = SUSTANCIAS[hidrato]["masa_molar"]
    m_a = SUSTANCIAS[clave_anhidro]["masa_molar"]
    return (m_h - m_a) / m_a
