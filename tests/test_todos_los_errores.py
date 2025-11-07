#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Completo de Errores para el Compilador KForge
===================================================
Ejecuta todos los tests de errores del compilador:
- Errores lexicos
- Errores sintacticos
- Errores semanticos
"""

import sys
import os
import subprocess

# Anadir directorio raiz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def ejecutar_test(nombre_test, script_path):
    """
    Ejecuta un test individual y retorna el resultado.

    Args:
        nombre_test: Nombre descriptivo del test
        script_path: Ruta al script de test

    Returns:
        True si el test fue exitoso, False en caso contrario
    """
    print()
    print("=" * 70)
    print(f"EJECUTANDO: {nombre_test}")
    print("=" * 70)
    print()

    try:
        # Ejecutar el test
        resultado = subprocess.run(
            [sys.executable, script_path],
            capture_output=False,
            text=True,
            cwd=os.path.dirname(script_path)
        )

        exito = resultado.returncode == 0

        if exito:
            print()
            print(f"[OK] {nombre_test} completado exitosamente")
        else:
            print()
            print(f"[X] {nombre_test} fallo")

        return exito

    except Exception as e:
        print(f"[X] Error al ejecutar {nombre_test}: {e}")
        return False


def main():
    """Funcion principal que ejecuta todos los tests de errores."""

    print("=" * 70)
    print(" " * 15 + "TEST COMPLETO DE ERRORES - KFORGE")
    print("=" * 70)
    print()
    print("Este script ejecuta todos los tests de deteccion de errores:")
    print("  1. Test de Errores Lexicos")
    print("  2. Test de Errores Sintacticos")
    print("  3. Test de Errores Semanticos")
    print()

    # Directorio de tests
    tests_dir = os.path.dirname(__file__)

    # Tests a ejecutar
    tests = [
        ("Test de Errores Lexicos", os.path.join(tests_dir, "test_errores_lexicos.py")),
        ("Test de Errores Sintacticos", os.path.join(tests_dir, "test_errores_sintacticos.py")),
        ("Test de Errores Semanticos", os.path.join(tests_dir, "test_errores_semanticos.py")),
    ]

    # Ejecutar todos los tests
    resultados = []
    for nombre, script in tests:
        exito = ejecutar_test(nombre, script)
        resultados.append((nombre, exito))

    # Resumen final
    print()
    print("=" * 70)
    print(" " * 25 + "RESUMEN FINAL")
    print("=" * 70)
    print()

    tests_exitosos = 0
    tests_fallidos = 0

    for nombre, exito in resultados:
        estado = "[OK]" if exito else "[X]"
        print(f"{estado} {nombre}")
        if exito:
            tests_exitosos += 1
        else:
            tests_fallidos += 1

    print()
    print("-" * 70)
    print(f"Total de tests: {len(resultados)}")
    print(f"Tests exitosos: {tests_exitosos}")
    print(f"Tests fallidos: {tests_fallidos}")
    print("-" * 70)
    print()

    if tests_fallidos == 0:
        print("[OK] TODOS LOS TESTS DE ERRORES PASARON EXITOSAMENTE!")
        print()
        print("El compilador KForge detecta correctamente:")
        print("  - Errores lexicos (caracteres invalidos, strings sin cerrar, etc.)")
        print("  - Errores sintacticos (falta de parentesis, llaves, tipos, etc.)")
        print("  - Errores semanticos (tipos incompatibles, variables no declaradas, etc.)")
        return 0
    else:
        print(f"[X] {tests_fallidos} test(s) fallaron")
        print("    Revisa los errores anteriores para mas detalles")
        return 1


if __name__ == "__main__":
    resultado = main()
    sys.exit(resultado)
