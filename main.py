"""
KForge - Compilador Kotlin
Punto de entrada principal de la aplicación.
"""

import sys
import os

# Agregar el directorio actual al path para importaciones
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.interfaz import ejecutar_interfaz


def main():
    """
    Función principal que inicia la aplicación.
    """
    try:
        ejecutar_interfaz()
    except KeyboardInterrupt:
        print("\nAplicación cerrada por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
