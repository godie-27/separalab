# interfaz/interfaz.py
# Versión de consola de SEPARALAB. Usa el mismo motor que la web.

from datos.sustancias import ORDEN_CATALOGO, SUSTANCIAS
from logica.planificador import resolver_mezcla


def mostrar_menu():
    print("\n" + "=" * 56)
    print("       🧪 SEPARALAB · SEPARADOR DE MEZCLAS")
    print("=" * 56)
    print("\nSustancias disponibles:\n")
    for i, clave in enumerate(ORDEN_CATALOGO, start=1):
        print(f"{i:2d}. {SUSTANCIAS[clave]['nombre']}")
    print("\n 0. Analizar mezcla")


def seleccionar_sustancias():
    seleccionadas = []
    while True:
        mostrar_menu()
        entrada = input("\nElige el número de una sustancia (0 para continuar): ").strip()
        if entrada == "0":
            break
        if not entrada.isdigit() or not 1 <= int(entrada) <= len(ORDEN_CATALOGO):
            print("Introduce un número de la lista.")
            continue
        clave = ORDEN_CATALOGO[int(entrada) - 1]
        if clave in seleccionadas:
            print("Esa sustancia ya fue seleccionada.")
            continue
        seleccionadas.append(clave)
        print(f"\nAñadida: {SUSTANCIAS[clave]['nombre']}")
    return seleccionadas


def mostrar_lista(titulo, elementos):
    print(f"\n{titulo}")
    for elemento in elementos or ["Ninguno"]:
        print(f"- {elemento}")


def mostrar_procedimiento(claves):
    resultado = resolver_mezcla(claves)
    analisis = resultado["analisis"]
    print("\n" + "=" * 56)
    print("       RESULTADO DEL ANÁLISIS")
    print("=" * 56)
    print(f"\nTipo de mezcla: {analisis['tipo']}")
    if analisis["nota_sustancia_pura"]:
        print(analisis["nota_sustancia_pura"])
    for reaccion in analisis["reacciones"]:
        print(f"\n⚠ Reacción posible: {reaccion['ecuacion']}\n  {reaccion['explicacion']}")
    for paso in resultado["pasos"]:
        print("\n" + "-" * 56)
        print(f"PASO {paso['numero']}: {paso['nombre']}  (sobre: {paso['entrada']['nombre']})")
        print("-" * 56)
        print(f"Propiedad: {paso['propiedad']}")
        print(f"Por qué funciona: {paso['explicacion']}")
        print(f"Por qué aquí: {paso['por_que_aqui']}")
        mostrar_lista("Materiales:", [m["nombre"] for m in paso["materiales"]])
        print("\nProcedimiento:")
        for i, instruccion in enumerate(paso["procedimiento"], start=1):
            print(f"{i}. {instruccion}")
        mostrar_lista("Fracciones obtenidas:", [f"{p['nombre']}: {p['texto']} [{p['estado']}]" for p in paso["productos"]])
        if paso["avisos"]:
            mostrar_lista("Avisos:", paso["avisos"])
    for fraccion in resultado["sin_resolver"]:
        print(f"\nSin resolver: {fraccion['texto']}")
        for motivo in fraccion["motivos"]:
            print(f"  · {motivo}")
    print("\n" + resultado["resumen"])
    print("\n" + "=" * 56)


def iniciar_interfaz():
    claves = seleccionar_sustancias()
    if claves:
        mostrar_procedimiento(claves)
    else:
        print("\nNo seleccionaste ninguna sustancia.")
