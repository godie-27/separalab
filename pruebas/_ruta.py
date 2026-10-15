# Permite ejecutar cada archivo de pruebas directamente (python pruebas/test_x.py).
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)
