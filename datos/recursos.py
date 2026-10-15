# datos/recursos.py
# Videos educativos verificados (octubre de 2026). Se enlazan en su página
# original, sin copiarlos ni modificarlos, respetando su licencia.
# Para añadir uno: copiar un bloque, comprobar que la URL funciona y rellenar
# "licencia" y "fuente". Si no hay un video fiable, el método queda sin video
# y la interfaz lo indica (no se inventan enlaces).

VIDEOS = [
    {
        "metodo": "filtracion",
        "titulo": "Procedimiento para filtrar por gravedad",
        "fuente": "Universitat de Barcelona · Dipòsit Digital (Seco, M. et al., 2009)",
        "idioma": "Español",
        "licencia": "CC BY-NC-ND 3.0 ES",
        "url": "https://diposit.ub.edu/dspace/handle/2445/6781",
        "observar": "Cómo se coloca el papel en el embudo, el uso de la varilla para verter y que el líquido nunca supera el borde del papel.",
    },
    {
        "metodo": "filtracion",
        "titulo": "Cómo hacer un filtro de pliegues",
        "fuente": "Universitat de Barcelona · Dipòsit Digital (Seco, M. et al., 2009)",
        "idioma": "Español",
        "licencia": "CC BY-NC-ND 3.0 ES",
        "url": "https://diposit.ub.edu/dspace/handle/2445/6741",
        "observar": "Los pliegues aumentan la superficie del papel y aceleran la filtración.",
    },
    {
        "metodo": "decantacion",
        "titulo": "Procedimiento para realizar una extracción líquido-líquido (embudo de decantación)",
        "fuente": "Universitat de Barcelona · Dipòsit Digital (Seco, M. et al., 2009)",
        "idioma": "Español",
        "licencia": "CC BY-NC-ND 3.0 ES",
        "url": "https://diposit.ub.edu/dspace/handle/2445/6761",
        "observar": "Las dos capas inmiscibles, cómo se quita el tapón antes de abrir la llave y cómo se recoge la fase inferior.",
    },
    {
        "metodo": "destilacion",
        "titulo": "Simple distillation · practical videos 14–16",
        "fuente": "Royal Society of Chemistry (Education)",
        "idioma": "Inglés",
        "licencia": "© Royal Society of Chemistry (ver en su web)",
        "url": "https://edu.rsc.org/practical/simple-distillation-practical-videos-14-16-students/4012011.article",
        "observar": "Se obtiene agua pura a partir de una disolución coloreada: el colorante no es volátil y queda en el matraz.",
    },
    {
        "metodo": "cristalizacion",
        "titulo": "Preparing a salt · practical videos 14–16 (cristales de sulfato de cobre)",
        "fuente": "Royal Society of Chemistry (Education)",
        "idioma": "Inglés",
        "licencia": "© Royal Society of Chemistry (ver en su web)",
        "url": "https://edu.rsc.org/resources/preparing-a-salt-practical-videos-14-16-students/4011982.article",
        "observar": "Fíjate en la parte final: la disolución se concentra, se deja enfriar y aparecen cristales azules de CuSO₄·5H₂O. (La primera parte es una reacción química para preparar la sal.)",
    },
    {
        "metodo": "cromatografia",
        "titulo": "Investigate the separation of inks using paper chromatography",
        "fuente": "Royal Society of Chemistry (Education)",
        "idioma": "Inglés",
        "licencia": "© Royal Society of Chemistry (ver en su web)",
        "url": "https://edu.rsc.org/resources/paper-chromatography-practical-videos-14-16-students/4011446.article",
        "observar": "La línea de origen a lápiz, el disolvente por debajo de ella y, al final, cómo se calcula el Rf.",
    },
    {
        "metodo": "cromatografia",
        "titulo": "Cómo identificar compuestos por cromatografía en capa fina",
        "fuente": "Universitat de Barcelona · Dipòsit Digital (Seco, M. et al., 2009)",
        "idioma": "Español",
        "licencia": "CC BY-NC-ND 3.0 ES",
        "url": "https://diposit.ub.edu/dspace/handle/2445/6721",
        "observar": "Cómo se aplican las muestras y los patrones en la misma placa para comparar sus Rf.",
    },
]


def videos_de(metodo):
    return [v for v in VIDEOS if v["metodo"] == metodo]
