"""
Test para verificar que main() puede omitir el tipo de retorno
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from core.lexer import Lexer
from core.parser import Parser
from core.semantic import AnalizadorSemantico
from core.errors import ErrorManager

# Test 1: main() sin tipo de retorno
codigo1 = """
fun main() {
    var x: Int = 5
    println("Hola")
}
"""

# Test 2: otra función SIN tipo de retorno (debe fallar)
codigo2 = """
fun suma(a: Int, b: Int) {
    return a + b
}
"""

# Test 3: main() con tipo explícito (debe seguir funcionando)
codigo3 = """
fun main(): Unit {
    var x: Int = 5
}
"""

print("=" * 60)
print("Test 1: main() sin tipo de retorno")
print("=" * 60)

error_manager = ErrorManager()
lexer = Lexer(error_manager)
tokens = lexer.tokenizar(codigo1)
parser = Parser(tokens, error_manager)
ast = parser.parsear()

if error_manager.tiene_errores():
    print("✗ FALLO - No debería tener errores")
    for e in error_manager.errores:
        print(f"  {e}")
else:
    print("✓ ÉXITO - main() sin tipo de retorno funciona")

print("\n" + "=" * 60)
print("Test 2: función 'suma' sin tipo de retorno (debe fallar)")
print("=" * 60)

error_manager2 = ErrorManager()
lexer2 = Lexer(error_manager2)
tokens2 = lexer2.tokenizar(codigo2)
parser2 = Parser(tokens2, error_manager2)
ast2 = parser2.parsear()

if error_manager2.tiene_errores():
    print("✓ ÉXITO - Correctamente rechaza función sin tipo de retorno")
    print(f"  Error esperado: {error_manager2.errores[0]}")
else:
    print("✗ FALLO - Debería requerir tipo de retorno para funciones no-main")

print("\n" + "=" * 60)
print("Test 3: main() con tipo explícito Unit")
print("=" * 60)

error_manager3 = ErrorManager()
lexer3 = Lexer(error_manager3)
tokens3 = lexer3.tokenizar(codigo3)
parser3 = Parser(tokens3, error_manager3)
ast3 = parser3.parsear()

if error_manager3.tiene_errores():
    print("✗ FALLO - main(): Unit debería funcionar")
    for e in error_manager3.errores:
        print(f"  {e}")
else:
    print("✓ ÉXITO - main(): Unit sigue funcionando")

print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)

if (not error_manager.tiene_errores() and
    error_manager2.tiene_errores() and
    not error_manager3.tiene_errores()):
    print("✓ ¡Todos los tests pasaron!")
    print("  - main() sin tipo: OK")
    print("  - otras funciones requieren tipo: OK")
    print("  - main(): Unit sigue funcionando: OK")
else:
    print("✗ Algunos tests fallaron")
