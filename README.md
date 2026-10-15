# SEPARALAB

Laboratorio digital para aprender a **separar mezclas** (4.º y 5.º de secundaria): resuelve mezclas paso a paso, permite practicar con corrección razonada, propone retos comprobados e incluye un módulo de **cromatografía**.

## Módulos

| Página | Qué hace |
|---|---|
| **Resolver** (`/resolver`) | Elige sustancias (y, si quieres, cantidades y métodos permitidos). Muestra el tipo de mezcla, las fases, las reacciones posibles y la secuencia completa. En cada paso indica método, propiedad, por qué funciona, por qué va en ese punto, montaje, material, procedimiento, qué se recupera y qué queda, avisos de pureza o pérdidas y alternativas. Si algo no se puede separar, explica qué falta. |
| **Practicar** (`/practica`) | El estudiante resuelve su propia mezcla: tipo de mezcla, fracción, método, predicción, material y orden del procedimiento. Se acepta cualquier secuencia químicamente coherente, con puntuación y pistas. |
| **Retos** (`/retos`) | 17 ejercicios validados (básico, intermedio, avanzado y desafío), incluidas las fichas de clase C, D y G, con pistas progresivas y preguntas de razonamiento. |
| **Cromatografía** (`/cromatografia`) | Teoría (papel y capa fina), calculadora de Rf con pasos y validación, los ejercicios de las fichas, identificación con patrones, preguntas y una simulación. |
| **Laboratorio** (`/laboratorio`) | Montaje dibujado de cada método, material con la función de cada pieza, procedimiento, precauciones y limitaciones. |
| **Videos** (`/videos`) | Videos verificados (Universitat de Barcelona y Royal Society of Chemistry) con qué observar en cada uno. |

## Cómo funciona el motor químico

- La mezcla se representa como **fracciones**: el contenido de un recipiente. De cada fracción se deducen sus **fases**: líquidos agrupados por miscibilidad, lo disuelto en cada uno y los sólidos sin disolver.
- Cada método (`logica/reglas.py`) es una **operación** con una condición, que si no se cumple devuelve un motivo explicado, y un **efecto**: las fracciones que produce, lo que se pierde, avisos y un coste.
- El **planificador** (`logica/planificador.py`) busca la secuencia de menor coste. El coste suma el del método y penalizaciones por pérdidas, baja pureza, alteraciones por calor o reacciones. Así elige entre alternativas y explica por qué.
- Con **cantidades**, la recristalización se comprueba numéricamente: agua de hidratación del CuSO₄·5H₂O, intervalo de agua en el que la cristalización es selectiva y rendimiento.
- Se avisa de las **reacciones químicas** (Fe + Cu²⁺, Fe + S al calentar) y de los límites reales: azeótropo etanol-agua, partículas coloidales, hidratos que se deshidratan, o que la cromatografía es analítica.
- Lo que no se sabe no se inventa: miscibilidad desconocida, dos sólidos insolubles sin método o datos de solubilidad ausentes aparecen como «sin resolver», con el motivo.

## Estructura

```
app.py                  Aplicación Flask (create_app): seguridad, errores, arranque
web/rutas.py            Páginas y API JSON (sin química)
web/validacion.py       Validación de todo lo que llega del navegador
datos/                  Catálogo: sustancias, métodos, materiales, reacciones, retos, cromatografía, videos
logica/modelo.py        Fracciones, fases y estructura física
logica/reglas.py        Operaciones (métodos de separación)
logica/planificador.py  Búsqueda de la secuencia, explicación de pasos, diagnóstico
logica/practica.py      Evaluación del modo práctica
logica/retos.py         Selección y corrección de retos
logica/cromatografia.py Cálculo y validación de Rf
interfaz/interfaz.py    Versión de consola (main.py)
templates/              Páginas HTML; montajes/ e iconos SVG propios
static/                 CSS y JavaScript (sin librerías externas)
pruebas/                73 pruebas automáticas
```

## Ejecutar en tu computadora

Requisitos: Python 3.10 o superior.

**Windows:** doble clic en `iniciar_web.bat` y abre http://127.0.0.1:5000

**Cualquier sistema:**

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    ·    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Versión de consola: `python main.py`

## Pruebas automáticas

```bash
python -m unittest discover -s pruebas -t .
```

Comprueban los casos de las fichas (secuencias, fracciones, avisos y cálculos), las 247 combinaciones del catálogo original, los retos, el modo práctica, el cálculo de Rf, las rutas web y la validación de entradas.

## Publicar en Internet (Render, plan gratuito)

1. Crea una cuenta en GitHub y sube esta carpeta a un repositorio nuevo. **No subas `.venv/`**; el `.gitignore` ya lo excluye.
2. Crea una cuenta en https://render.com e inicia sesión con GitHub.
3. Elige **New → Blueprint**, selecciona el repositorio y confirma. Render lee `render.yaml`: instala `requirements.txt` y arranca con `gunicorn app:app`.
4. Al terminar, Render te da un enlace público `https://separalab-xxxx.onrender.com`.

Ten en cuenta que en el plan gratuito el servicio se duerme tras 15 minutos sin visitas, y la siguiente visita tarda alrededor de un minuto en cargar.

Después de publicar, comprueba:

- Que las siete páginas abren.
- Que «Resolver» con agua, aceite, arena y sal muestra tres pasos.
- Que un reto se puede completar.
- Que la calculadora de Rf responde.

La aplicación no usa base de datos, cuentas ni claves: no hay nada secreto que configurar.

## Ampliar SEPARALAB

- **Nueva sustancia:** añade una entrada en `datos/sustancias.py` (estado, densidad, solubilidad en cada líquido, magnetismo…). Añade la miscibilidad en `MISCIBILIDAD` si es líquida y su color en `static/js/comun.js`.
- **Nuevo reto:** añádelo en `datos/retos.py`. `pruebas/test_retos.py` comprueba automáticamente que tiene solución.
- **Nuevo video:** añádelo en `datos/recursos.py` con su fuente y licencia, después de comprobar el enlace.
- **Nuevo ejercicio de cromatografía:** añádelo en `datos/cromatografia.py`.

## Datos y fuentes

- Los datos de solubilidad de NaCl y CuSO₄ y los ejercicios proceden de las fichas de clase. Cada reto usa los datos de su propio enunciado.
- Las densidades y los puntos de ebullición son valores de referencia aproximados (20 °C, 1 atm).
- Los Rf de las fichas son datos de esos ejercicios en sus condiciones, no constantes universales. Los valores marcados como ilustrativos son inventados con fines didácticos.
- Los dibujos son originales. Los videos se enlazan en su web original, respetando sus licencias.
