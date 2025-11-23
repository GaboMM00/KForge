"""
Test de UI con sentencias globales para verificar que se muestre el código generado.
"""

from core.controller import CompiladorController

codigo = """var n: Int = 0
while (n < 10) {
    if (n == 5) {
        break
    }
    n = n + 1
}"""

print("Compilando codigo con sentencias globales...")
controller = CompiladorController()
resultado = controller.ejecutar_semantico(codigo)

print(f"\nExito: {resultado['exito']}")
print(f"codigo_intermedio presente: {bool(resultado.get('codigo_intermedio'))}")
print(f"bytecode presente: {bool(resultado.get('bytecode'))}")

if resultado.get('codigo_intermedio'):
    print(f"\nLongitud TAC: {len(resultado['codigo_intermedio'])} caracteres")
    print(f"Primeras 100 caracteres del TAC: {resultado['codigo_intermedio'][:100]}")

if resultado.get('bytecode'):
    print(f"\nLongitud Bytecode: {len(resultado['bytecode'])} caracteres")
    print(f"Primeras 100 caracteres del Bytecode: {resultado['bytecode'][:100]}")

print("\n\nLa UI deberia mostrar:")
print("  1. TAC en la pestana 'Codigo' (boton 'Ver TAC')")
print("  2. Bytecode en la pestana 'Codigo' (boton 'Ver Bytecode')")
print("  3. Boton 'Guardar Codigo' funcional")
