"""
Script de prueba directo para la Fase 3: Arrays y Propiedades
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

# Código de prueba para Fase 3
codigo = """
// Test de arrays y propiedades
var numeros: IntArray = intArrayOf(1, 2, 3, 4, 5)
var tamano: Int = numeros.size

var mensaje: String = "Hola"
var longitud: Int = mensaje.length

var primero: Int = numeros[0]
numeros[1] = 10

for (i in 0 until numeros.size) {
    var elem: Int = numeros[i]
}

fun obtenerTamano(arr: IntArray): Int {
    return arr.size
}

var tam: Int = obtenerTamano(numeros)

if (numeros.size > 3) {
    println("Array grande")
}
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
    print("✓ ¡FASE 3 IMPLEMENTADA CORRECTAMENTE!")
    print("\nCaracterísticas probadas:")
    print("  ✓ Operador punto para propiedades")
    print("  ✓ Propiedad .size para arrays")
    print("  ✓ Propiedad .length para strings")
    print("  ✓ Acceso a elementos de array con []")
    print("  ✓ Modificación de elementos de array")
    print("  ✓ Uso de propiedades en expresiones")
else:
    print("✗ Hay errores que corregir")
    print("\nERRORES PENDIENTES:")
    for i, error in enumerate(error_manager.errores[:5], 1):
        print(f"  {i}. {error}")
