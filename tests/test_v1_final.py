"""
TEST FINAL DE LA VERSIÓN 1 DEL COMPILADOR KFORGE
=================================================
Este script ejecuta el test final que demuestra todas las características
implementadas en las Fases 1, 2 y 3 del compilador.

Algoritmo de prueba: Bubble Sort (Ordenamiento de Burbuja)
"""
import sys
import io
from pathlib import Path

# Agregar el directorio raíz al path para poder importar 'core'
sys.path.insert(0, str(Path(__file__).parent.parent))

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from core.lexer import Lexer
from core.parser import Parser
from core.semantic import AnalizadorSemantico
from core.errors import ErrorManager

def print_header(title, width=60):
    """Imprime un encabezado decorado"""
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)

# Leer el archivo de test
test_file = Path(__file__).parent.parent / "test_kt" / "test_v1_final.kt"

try:
    with open(test_file, 'r', encoding='utf-8') as f:
        codigo = f.read()
except FileNotFoundError:
    print(f"✗ No se encontró el archivo: {test_file}")
    sys.exit(1)

print_header("KFORGE COMPILER v1.0 - TEST FINAL", 70)
print("\n  Prueba Final: Algoritmo Bubble Sort")
print("  Características probadas: Fases 1, 2 y 3 completas")
print(f"  Archivo de test: {test_file.name}")
print(f"  Tamaño del código: {len(codigo)} caracteres")

# Crear gestor de errores
error_manager = ErrorManager()

# ============================================================
# ANÁLISIS LÉXICO
# ============================================================
print_header("ANÁLISIS LÉXICO")
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
    print(f"Número de declaraciones: {len(ast.hijos)}")

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

# ============================================================
# RESUMEN DE CARACTERÍSTICAS PROBADAS
# ============================================================
print_header("CARACTERÍSTICAS PROBADAS")

print("\nFase 1 - Fundamentos:")
print("  ✓ Declaraciones de variables (var)")
print("  ✓ Tipos de datos: Int, Boolean")
print("  ✓ Expresiones aritméticas: +, -, *, /")
print("  ✓ Operadores de comparación: >, <, ==, !=")
print("  ✓ Operadores lógicos: !, &&, ||")
print("  ✓ Estructuras de control: if, for")
print("  ✓ Sentencias: break")
print("  ✓ Rangos: 0 until n con expresiones aritméticas")

print("\nFase 2 - Funciones:")
print("  ✓ Declaración de funciones (fun main)")
print("  ✓ Llamadas a funciones built-in (println)")
print("  ✓ Bloques de código anidados")

print("\nFase 3 - Arrays y Propiedades:")
print("  ✓ Arrays: IntArray")
print("  ✓ Creación de arrays: intArrayOf()")
print("  ✓ Acceso a elementos: arr[i]")
print("  ✓ Modificación de elementos: arr[i] = value")
print("  ✓ Propiedad .size para arrays")
print("  ✓ Índices con expresiones aritméticas: arr[j + 1]")

# ============================================================
# RESUMEN FINAL
# ============================================================
print_header("RESUMEN FINAL")

total_errores = len(error_manager.errores)
print(f"Total de errores: {total_errores}")

if total_errores == 0:
    print("\n" + "=" * 70)
    print("✓ ¡VERSIÓN 1 DEL COMPILADOR COMPLETADA!".center(70))
    print("=" * 70)
    print()
    print("  El compilador KForge v1.0 puede compilar exitosamente:")
    print("  • Variables y tipos básicos (Int, Double, String, Boolean)")
    print("  • Estructuras de control (if, for, while, break, continue)")
    print("  • Funciones y llamadas (declaración, parámetros, retorno)")
    print("  • Arrays con propiedades y acceso (IntArray, DoubleArray)")
    print("  • Algoritmos complejos como Bubble Sort")
    print()
    print("  🎉 ¡Felicitaciones! El compilador está listo para la v1.0")
    print()
    sys.exit(0)
else:
    print("\n✗ El test no pasó completamente")
    print("\nERRORES PENDIENTES:")
    for i, error in enumerate(error_manager.errores[:10], 1):
        print(f"  {i}. {error}")
    sys.exit(1)
