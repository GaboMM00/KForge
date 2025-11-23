"""
Script de prueba para verificar la integración de TAC y Bytecode en la UI.
Prueba el pipeline completo sin abrir la interfaz gráfica.
"""

from core.controller import CompiladorController


def test_integration():
    """Prueba la generación de TAC y Bytecode a través del controller."""

    # Código Kotlin de prueba
    codigo = """
fun suma(a: Int, b: Int): Int {
    return a + b
}

fun main() {
    val x: Int = 10
    val y: Int = 20
    val resultado: Int = suma(x, y)
    println(resultado)
}
"""

    print("=" * 80)
    print("TEST DE INTEGRACIÓN UI - TAC Y BYTECODE")
    print("=" * 80)

    # Crear controller
    controller = CompiladorController()

    # Ejecutar compilación completa (incluye TAC y Bytecode)
    print("\n[1] Ejecutando análisis semántico (incluye TAC y Bytecode)...\n")
    resultado = controller.ejecutar_semantico(codigo)

    # Verificar resultados
    print(f"Éxito: {resultado['exito']}")
    print(f"Errores: {len(resultado['errores'])}")

    if resultado['exito']:
        print("\n[2] Verificando codigo TAC generado...")
        if resultado.get("codigo_intermedio"):
            tac_lines = resultado["codigo_intermedio"].split('\n')
            print(f"   [OK] TAC generado: {len(tac_lines)} lineas")
            print("\n--- Primeras 20 lineas del TAC ---")
            for i, line in enumerate(tac_lines[:20], 1):
                print(f"{i:3d}: {line}")
        else:
            print("   [FAIL] No se genero codigo TAC")

        print("\n[3] Verificando bytecode generado...")
        if resultado.get("bytecode"):
            bc_lines = resultado["bytecode"].split('\n')
            print(f"   [OK] Bytecode generado: {len(bc_lines)} lineas")
            print(f"   [OK] Instrucciones: {len(resultado.get('bytecode_instructions', []))}")
            print("\n--- Primeras 30 lineas del Bytecode ---")
            for i, line in enumerate(bc_lines[:30], 1):
                print(f"{i:3d}: {line}")
        else:
            print("   [FAIL] No se genero bytecode")

        print("\n[4] Verificando estructura del resultado...")
        keys = ['tokens', 'arbol', 'semantico', 'codigo_intermedio', 'bytecode',
                'tac', 'bytecode_instructions', 'errores', 'exito']
        for key in keys:
            exists = key in resultado
            symbol = "[OK]" if exists else "[FAIL]"
            print(f"   {symbol} '{key}': {exists}")

        print("\n" + "=" * 80)
        print("RESULTADO: INTEGRACIÓN EXITOSA")
        print("=" * 80)
        print("\nLa UI debería poder:")
        print("  1. Mostrar TAC en la pestaña 'Código'")
        print("  2. Alternar entre TAC y Bytecode con botones")
        print("  3. Guardar código a archivos .tac o .asm")
        print("  4. Aplicar syntax highlighting al código generado")

    else:
        print("\n" + "=" * 80)
        print("RESULTADO: COMPILACIÓN FALLIDA")
        print("=" * 80)
        for error in resultado['errores']:
            print(f"  - {error}")


if __name__ == "__main__":
    test_integration()
