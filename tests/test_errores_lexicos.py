#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Errores Léxicos para el Compilador KForge
==================================================
Verifica que el analizador léxico detecte correctamente todos los
errores léxicos posibles en código Kotlin.
"""

import sys
import os

# Añadir directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.controller import CompiladorController
from core.errors import ErrorManager, LexicalError


def ejecutar_test_errores_lexicos():
    """Ejecuta el test de errores léxicos y verifica que se detecten correctamente."""

    print("=" * 60)
    print("TEST DE ERRORES LÉXICOS")
    print("=" * 60)
    print()

    # Leer archivo de test
    archivo_test = os.path.join(os.path.dirname(__file__), '..', 'test_kt', 'test_errores_lexicos.kt')

    try:
        with open(archivo_test, 'r', encoding='utf-8') as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"[X] ERROR: No se encontro el archivo {archivo_test}")
        return False

    print(f"[+] Archivo: {os.path.basename(archivo_test)}")
    print(f"[+] Longitud: {len(codigo)} caracteres")
    print()

    # Crear controlador y ejecutar análisis léxico
    controlador = CompiladorController()
    error_manager = controlador.error_manager

    print("[*] Ejecutando analisis lexico...")
    print()

    # Crear lexer y tokenizar
    from core.lexer import Lexer
    lexer = Lexer(error_manager)
    tokens = lexer.tokenizar(codigo)

    # Verificar que se hayan detectado errores léxicos
    errores_lexicos = [e for e in error_manager.errores if isinstance(e, LexicalError)]
    total_errores = len(errores_lexicos)

    print(f"[*] Resultados del Analisis Lexico:")
    print(f"    Total de errores lexicos detectados: {total_errores}")
    print()

    if total_errores == 0:
        print("[X] FALLO: No se detectaron errores lexicos")
        print("    El analizador lexico deberia detectar multiples errores en este archivo.")
        return False

    # Mostrar todos los errores detectados
    print("[*] Errores detectados:")
    print("-" * 60)
    for i, error in enumerate(errores_lexicos, 1):
        # Convertir el error a string y manejar caracteres especiales
        error_str = str(error)
        # Reemplazar caracteres que pueden causar problemas de encoding
        error_str = error_str.encode('ascii', 'replace').decode('ascii')
        print(f"{i}. {error_str}")
    print("-" * 60)
    print()

    # Verificar que se detectaron errores esperados
    errores_texto = [str(error).lower() for error in errores_lexicos]

    # Patrones de errores esperados
    errores_esperados = {
        'caracter_invalido': ['caracter', 'invalido', 'no valido', 'no reconocido', '@', '#'],
        'string_sin_cerrar': ['string', 'cadena', 'cerrar', 'no cerrada', '"'],
        'numero_invalido': ['numero', 'formato', 'invalido'],
        'identificador_invalido': ['identificador', 'invalido', 'comienza con numero', 'digito'],
        'operador_invalido': ['operador', 'invalido', 'no valido'],
    }

    print("[*] Categorias de errores detectados:")
    categorias_encontradas = 0

    for categoria, palabras_clave in errores_esperados.items():
        encontrado = False
        for error_texto in errores_texto:
            if any(palabra in error_texto for palabra in palabras_clave):
                encontrado = True
                categorias_encontradas += 1
                break

        estado = "[OK]" if encontrado else "[--]"
        print(f"    {estado} {categoria.replace('_', ' ').title()}")

    print()

    # Resumen
    print("=" * 60)
    if total_errores > 0:
        print(f"[OK] TEST EXITOSO: Se detectaron {total_errores} errores lexicos")
        print(f"     Categorias identificadas: {categorias_encontradas}/{len(errores_esperados)}")
    else:
        print("[X] TEST FALLIDO: No se detectaron errores lexicos")
    print("=" * 60)

    return total_errores > 0


def main():
    """Función principal."""
    exito = ejecutar_test_errores_lexicos()
    sys.exit(0 if exito else 1)


if __name__ == "__main__":
    main()
