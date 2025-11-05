"""
Script de prueba para el compilador KForge.
Permite probar el compilador desde línea de comandos sin interfaz gráfica.
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path para poder importar 'core'
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.controller import CompiladorController


def prueba_basica():
    """Ejecuta una prueba basica del compilador."""
    print("=" * 70)
    print("PRUEBA BASICA DEL COMPILADOR KFORGE")
    print("=" * 70)
    print()

    # Codigo de prueba
    codigo = """
// Prueba basica del compilador
var a: Int = 5
var b: Int = 10

if (a < b) {
    a = a + 1
} else {
    b = b - 1
}

var resultado: Int = a + b
"""

    print("Codigo a compilar:")
    print("-" * 70)
    print(codigo)
    print("-" * 70)
    print()

    # Crear controlador y ejecutar
    controlador = CompiladorController()
    resultado = controlador.ejecutar(codigo)

    # Mostrar resultados
    if resultado["exito"]:
        print("[OK] COMPILACION EXITOSA")
        print()
        print(f"Total de tokens generados: {len(resultado['tokens'])}")
        print()

        print("Resultados del analisis semantico:")
        for item in resultado["semantico"]:
            print(f"  - {item}")
    else:
        print("[ERROR] COMPILACION FALLIDA")
        print()
        print("Errores encontrados:")
        for error in resultado["errores"]:
            print(f"  - {error}")

    print()
    print("=" * 70)


def prueba_desde_archivo(ruta_archivo: str):
    """
    Ejecuta una prueba del compilador desde un archivo.

    Args:
        ruta_archivo: Ruta al archivo con código Kotlin.
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()

        print("=" * 70)
        print(f"COMPILANDO ARCHIVO: {ruta_archivo}")
        print("=" * 70)
        print()

        controlador = CompiladorController()
        resultado = controlador.ejecutar(codigo)

        # Mostrar resumen completo
        print(controlador.obtener_resumen_completo())

    except FileNotFoundError:
        print(f"Error: No se encontro el archivo '{ruta_archivo}'")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")


def mostrar_uso():
    """Muestra informacion de uso del script."""
    print("""
Uso: python test_compilador.py [archivo]

Argumentos:
  archivo    Ruta al archivo .kt o .txt con codigo Kotlin (opcional)

Ejemplos:
  python test_compilador.py                    # Ejecuta prueba basica
  python test_compilador.py tests/ejemplo_kotlin.txt   # Compila un archivo

Si no se proporciona un archivo, se ejecuta una prueba basica predefinida.
    """)


def main():
    """Funcion principal."""
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help', 'help']:
            mostrar_uso()
        else:
            prueba_desde_archivo(sys.argv[1])
    else:
        prueba_basica()


if __name__ == "__main__":
    main()
