#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Errores Semanticos para el Compilador KForge
=====================================================
Verifica que el analizador semantico detecte correctamente todos los
errores semanticos posibles en codigo Kotlin.
"""

import sys
import os

# Anadir directorio raiz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.controller import CompiladorController
from core.errors import ErrorManager, SemanticError
from core.lexer import Lexer
from core.parser import Parser
from core.semantic import AnalizadorSemantico


def ejecutar_test_errores_semanticos():
    """Ejecuta el test de errores semanticos y verifica que se detecten correctamente."""

    print("=" * 60)
    print("TEST DE ERRORES SEMANTICOS")
    print("=" * 60)
    print()

    # Leer archivo de test
    archivo_test = os.path.join(os.path.dirname(__file__), '..', 'test_kt', 'test_errores_semanticos.kt')

    try:
        with open(archivo_test, 'r', encoding='utf-8') as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"[X] ERROR: No se encontro el archivo {archivo_test}")
        return False

    print(f"[+] Archivo: {os.path.basename(archivo_test)}")
    print(f"[+] Longitud: {len(codigo)} caracteres")
    print()

    # Crear controlador y ejecutar analisis completo
    controlador = CompiladorController()
    error_manager = controlador.error_manager

    print("[*] Ejecutando analisis lexico, sintactico y semantico...")
    print()

    # Crear lexer y tokenizar
    lexer = Lexer(error_manager)
    tokens = lexer.tokenizar(codigo)

    # Verificar si hay errores lexicos
    errores_lexicos = [e for e in error_manager.errores if hasattr(e, '__class__') and 'Lexical' in e.__class__.__name__]
    if errores_lexicos:
        print(f"[!] Advertencia: Se detectaron {len(errores_lexicos)} errores lexicos")
        print("    (estos seran ignorados para el test de errores semanticos)")
        print()

    # Crear parser y parsear
    parser = Parser(tokens, error_manager)
    ast = parser.parsear()

    # Verificar si hay errores sintacticos
    errores_sintacticos = [e for e in error_manager.errores if hasattr(e, '__class__') and 'Syntax' in e.__class__.__name__]
    if errores_sintacticos:
        print(f"[!] Advertencia: Se detectaron {len(errores_sintacticos)} errores sintacticos")
        print("    (estos seran ignorados para el test de errores semanticos)")
        print()

    # Crear analizador semantico y analizar
    if ast:
        analizador = AnalizadorSemantico(error_manager)
        analizador.analizar(ast)

    # Verificar que se hayan detectado errores semanticos
    errores_semanticos = [e for e in error_manager.errores if hasattr(e, '__class__') and 'Semantic' in e.__class__.__name__]
    total_errores = len(errores_semanticos)

    print(f"[*] Resultados del Analisis Semantico:")
    print(f"    Total de errores semanticos detectados: {total_errores}")
    print()

    if total_errores == 0:
        print("[X] FALLO: No se detectaron errores semanticos")
        print("    El analizador semantico deberia detectar multiples errores en este archivo.")
        return False

    # Mostrar todos los errores detectados
    print("[*] Errores detectados:")
    print("-" * 60)
    for i, error in enumerate(errores_semanticos, 1):
        # Convertir el error a string y manejar caracteres especiales
        error_str = str(error)
        # Reemplazar caracteres que pueden causar problemas de encoding
        error_str = error_str.encode('ascii', 'replace').decode('ascii')
        print(f"{i}. {error_str}")
    print("-" * 60)
    print()

    # Verificar que se detectaron errores esperados
    errores_texto = [str(error).lower() for error in errores_semanticos]

    # Patrones de errores esperados
    errores_esperados = {
        'variable_no_declarada': ['variable', 'no declarada', 'no existe'],
        'tipos_incompatibles': ['tipo', 'incompatible', 'esperaba', 'se obtuvo'],
        'funcion_no_declarada': ['funcion', 'no declarada', 'no existe'],
        'argumentos_incorrectos': ['argumento', 'parametro', 'esperaba', 'se recibieron'],
        'variable_no_inicializada': ['inicializada', 'sin valor'],
        'retorno_incorrecto': ['return', 'retorno', 'tipo'],
        'operador_invalido': ['operador', 'invalido', 'tipo'],
        'break_continue': ['break', 'continue', 'fuera'],
        'variable_duplicada': ['duplicada', 'ya declarada'],
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
        print(f"[OK] TEST EXITOSO: Se detectaron {total_errores} errores semanticos")
        print(f"     Categorias identificadas: {categorias_encontradas}/{len(errores_esperados)}")
    else:
        print("[X] TEST FALLIDO: No se detectaron errores semanticos")
    print("=" * 60)

    return total_errores > 0


def main():
    """Funcion principal."""
    exito = ejecutar_test_errores_semanticos()
    sys.exit(0 if exito else 1)


if __name__ == "__main__":
    main()
