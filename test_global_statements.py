"""
Test para verificar generación de TAC/Bytecode con sentencias globales.
"""

from core.controller import CompiladorController


def test_global_statements():
    """Prueba código sin funciones (sentencias globales)."""

    codigo = """var n: Int = 0
while (n < 10) {
    if (n == 5) {
        break
    }
    n = n + 1
}"""

    print("=" * 80)
    print("TEST: SENTENCIAS GLOBALES (sin funciones)")
    print("=" * 80)
    print("\nCodigo:")
    print(codigo)
    print("\n" + "=" * 80)

    controller = CompiladorController()
    resultado = controller.ejecutar_semantico(codigo)

    print(f"\nExito: {resultado['exito']}")
    print(f"Errores: {len(resultado['errores'])}")

    if resultado['errores']:
        print("\nErrores encontrados:")
        for error in resultado['errores']:
            print(f"  - {error}")

    if resultado.get("codigo_intermedio"):
        print("\n[OK] TAC GENERADO:")
        print(resultado["codigo_intermedio"])
    else:
        print("\n[FAIL] No se genero codigo TAC")

    if resultado.get("bytecode"):
        print("\n[OK] BYTECODE GENERADO:")
        print(resultado["bytecode"])
    else:
        print("\n[FAIL] No se genero bytecode")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    test_global_statements()
