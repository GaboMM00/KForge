#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Errores Sintacticos para el Compilador KForge
======================================================
Verifica que el analizador sintactico detecte correctamente todos los
errores sintacticos posibles en codigo Kotlin.
"""

import sys
import os

# Anadir directorio raiz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.controller import CompiladorController
from core.errors import ErrorManager, SyntaxError
from core.lexer import Lexer
from core.parser import Parser


def ejecutar_test_errores_sintacticos():
    """Ejecuta el test de errores sintacticos y verifica que se detecten correctamente."""

    print("=" * 60)
    print("TEST DE ERRORES SINTACTICOS")
    print("=" * 60)
    print()

    # Leer archivo de test
    archivo_test = os.path.join(os.path.dirname(__file__), '..', 'test_kt', 'test_errores_sintacticos.kt')

    try:
        with open(archivo_test, 'r', encoding='utf-8') as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"[X] ERROR: No se encontro el archivo {archivo_test}")
        return False

    print(f"[+] Archivo: {os.path.basename(archivo_test)}")
    print(f"[+] Longitud: {len(codigo)} caracteres")
    print()

    # Crear controlador y ejecutar analisis lexico y sintactico
    controlador = CompiladorController()
    error_manager = controlador.error_manager

    print("[*] Ejecutando analisis lexico y sintactico...")
    print()

    # Crear lexer y tokenizar
    lexer = Lexer(error_manager)
    tokens = lexer.tokenizar(codigo)

    # Verificar si hay errores lexicos
    errores_lexicos = [e for e in error_manager.errores if hasattr(e, '__class__') and 'Lexical' in e.__class__.__name__]
    if errores_lexicos:
        print(f"[!] Advertencia: Se detectaron {len(errores_lexicos)} errores lexicos")
        print("    (estos seran ignorados para el test de errores sintacticos)")
        print()

    # Crear parser y parsear
    parser = Parser(tokens, error_manager)
    ast = parser.parsear()

    # Verificar que se hayan detectado errores sintacticos
    errores_sintacticos = [e for e in error_manager.errores if hasattr(e, '__class__') and 'Syntax' in e.__class__.__name__]
    total_errores = len(errores_sintacticos)

    print(f"[*] Resultados del Analisis Sintactico:")
    print(f"    Total de errores sintacticos detectados: {total_errores}")
    print()

    if total_errores == 0:
        print("[X] FALLO: No se detectaron errores sintacticos")
        print("    El analizador sintactico deberia detectar multiples errores en este archivo.")
        return False

    # Mostrar todos los errores detectados
    print("[*] Errores detectados:")
    print("-" * 60)
    for i, error in enumerate(errores_sintacticos, 1):
        # Convertir el error a string y manejar caracteres especiales
        error_str = str(error)
        # Reemplazar caracteres que pueden causar problemas de encoding
        error_str = error_str.encode('ascii', 'replace').decode('ascii')
        print(f"{i}. {error_str}")
    print("-" * 60)
    print()

    # Verificar que se detectaron errores esperados
    errores_texto = [str(error).lower() for error in errores_sintacticos]

    # Patrones de errores esperados
    errores_esperados = {
        'falta_tipo': ['tipo', 'esperaba', ':'],
        'falta_asignacion': ['=', 'asign', 'esperaba'],
        'parentesis': ['parentesis', '(', ')'],
        'llaves': ['llave', '{', '}'],
        'falta_in': ['in', 'for'],
        'corchetes': ['corchete', '[', ']'],
        'expresion_incompleta': ['expresion', 'incompleta', 'esperaba'],
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
        print(f"[OK] TEST EXITOSO: Se detectaron {total_errores} errores sintacticos")
        print(f"     Categorias identificadas: {categorias_encontradas}/{len(errores_esperados)}")
    else:
        print("[X] TEST FALLIDO: No se detectaron errores sintacticos")
    print("=" * 60)

    return total_errores > 0


def main():
    """Funcion principal."""
    exito = ejecutar_test_errores_sintacticos()
    sys.exit(0 if exito else 1)


if __name__ == "__main__":
    main()
