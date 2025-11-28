"""
Script de prueba directo para la Fase 2: Funciones y Llamadas
"""
import sys
import io
from pathlib import Path

# Agregar el directorio raíz al path para poder importar 'core'
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from core.lexer import Lexer
from core.parser import Parser
from core.semantic import AnalizadorSemantico
from core.errors import ErrorManager

# Código de prueba para Fase 2
codigo = """
// Test de funciones
fun suma(a: Int, b: Int): Int {
    return a + b
}

fun resta(x: Int, y: Int): Int {
    return x - y
}

var resultado1: Int = suma(5, 3)
var resultado2: Int = resta(10, 4)

// Test de funciones built-in
var arr: IntArray = intArrayOf(1, 2, 3)
println("Resultado:")
println(resultado1)
"""

# Crear gestor de errores
error_manager = ErrorManager()

# ============================================================
# ANÁLISIS LÉXICO
# ============================================================
print("=" * 60)
print("ANÁLISIS LÉXICO")
print("=" * 60)
lexer = Lexer(error_manager)
tokens = lexer.tokenizar(codigo)
print(f"Tokens generados: {len(tokens)}")

if error_manager.tiene_errores():
    print("\nERRORES LÉXICOS:")
    for error in error_manager.errores:
        print(f"  - {error}")
else:
    print("✓ Sin errores léxicos")

# ============================================================
# ANÁLISIS SINTÁCTICO
# ============================================================
print("\n" + "=" * 60)
print("ANÁLISIS SINTÁCTICO")
print("=" * 60)
parser = Parser(tokens, error_manager)
ast = parser.parsear()

errores_sintacticos = [e for e in error_manager.errores if "Sintáctico" in str(e)]
if errores_sintacticos:
    print("\nERRORES SINTÁCTICOS:")
    for error in errores_sintacticos:
        print(f"  - {error}")
else:
    print("✓ Sin errores sintácticos")

if ast:
    print("\nAST generado correctamente")
    print(f"Tipo de nodo raíz: {ast.tipo.name}")
    print(f"Número de hijos: {len(ast.hijos)}")

# ============================================================
# ANÁLISIS SEMÁNTICO
# ============================================================
print("\n" + "=" * 60)
print("ANÁLISIS SEMÁNTICO")
print("=" * 60)
analizador_semantico = AnalizadorSemantico(error_manager)
resultados = analizador_semantico.analizar(ast)

errores_semanticos = [e for e in error_manager.errores if "Semántico" in str(e)]
if errores_semanticos:
    print("\nERRORES SEMÁNTICOS:")
    for error in errores_semanticos:
        print(f"  - {error}")
else:
    print("✓ Sin errores semánticos")

if resultados:
    print("\nResultados del análisis semántico:")
    for item in resultados[:10]:  # Mostrar solo los primeros 10
        print(f"  {item}")

# ============================================================
# RESUMEN
# ============================================================
print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)
print(f"Total de errores: {len(error_manager.errores)}")
if not error_manager.tiene_errores():
    print("✓ ¡FASE 2 IMPLEMENTADA CORRECTAMENTE!")
    print("\nCaracterísticas probadas:")
    print("  ✓ Declaración de funciones con parámetros")
    print("  ✓ Tipos de retorno")
    print("  ✓ Llamadas a funciones")
    print("  ✓ Funciones built-in (intArrayOf, println)")
    print("  ✓ Return statement")
else:
    print("✗ Hay errores que corregir")
    print("\nERRORES PENDIENTES:")
    for i, error in enumerate(error_manager.errores[:5], 1):
        print(f"  {i}. {error}")
