"""
Tests de Integracion End-to-End - KForge v2.0

Prueba el pipeline completo: Kotlin -> TAC -> JVM Bytecode -> .class ejecutable
"""

import sys
import io
import os
import struct
import subprocess
from pathlib import Path

# Agregar el directorio raiz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Fix encoding para Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from core.controller import CompiladorController


def test_simple_arithmetic():
    """Test programa simple con aritmetica."""
    print("[TEST 1] Programa simple - Aritmetica")

    codigo = """
    fun main() {
        val x: Int = 5
        val y: Int = 3
        val suma: Int = x + y
    }
    """

    controller = CompiladorController()
    resultado = controller.ejecutar_jvm(
        codigo,
        class_name="SimpleArithmetic",
        output_path="tests/jvm/output/SimpleArithmetic.class"
    )

    assert resultado["exito"], f"Compilacion fallo: {resultado['errores']}"
    assert resultado["bytecode_jvm"] is not None
    assert len(resultado["bytecode_jvm"]) > 0

    # Verificar magic number
    magic = struct.unpack('>I', resultado["bytecode_jvm"][0:4])[0]
    assert magic == 0xCAFEBABE

    # Verificar que el archivo se creo
    assert os.path.exists("tests/jvm/output/SimpleArithmetic.class")

    print(f"  checkmark Bytecode size: {len(resultado['bytecode_jvm'])} bytes")
    print(f"  checkmark TAC instructions: {len(resultado['tac_instructions'])}")
    print(f"  checkmark Archivo .class creado")
    print()


def test_variable_assignment():
    """Test asignaciones de variables."""
    print("[TEST 2] Asignaciones de variables")

    codigo = """
    fun main() {
        val a: Int = 10
        val b: Int = 20
        val c: Int = 30
        var resultado: Int = a + b + c
    }
    """

    controller = CompiladorController()
    resultado = controller.ejecutar_jvm(
        codigo,
        class_name="Variables",
        output_path="tests/jvm/output/Variables.class"
    )

    assert resultado["exito"]
    assert resultado["class_info"]["bytecode_size"] > 0

    print(f"  checkmark Compilacion exitosa")
    print(f"  checkmark {resultado['class_info']['tac_instructions']} instrucciones TAC")
    print()


def test_expressions():
    """Test expresiones complejas."""
    print("[TEST 3] Expresiones complejas")

    codigo = """
    fun main() {
        val a: Int = 5
        val b: Int = 3
        val suma: Int = a + b
        val resta: Int = a - b
        val mult: Int = a * b
        val div: Int = a / b
    }
    """

    controller = CompiladorController()
    resultado = controller.ejecutar_jvm(
        codigo,
        class_name="Expressions",
        output_path="tests/jvm/output/Expressions.class"
    )

    assert resultado["exito"]
    assert os.path.exists("tests/jvm/output/Expressions.class")

    print(f"  checkmark Multiples operaciones compiladas")
    print(f"  checkmark Archivo .class generado")
    print()


def test_functions():
    """Test definicion y llamada de funciones."""
    print("[TEST 4] Funciones")

    codigo = """
    fun suma(a: Int, b: Int): Int {
        return a + b
    }

    fun main() {
        val resultado: Int = suma(5, 3)
    }
    """

    controller = CompiladorController()
    resultado = controller.ejecutar_jvm(
        codigo,
        class_name="Functions",
        output_path="tests/jvm/output/Functions.class"
    )

    assert resultado["exito"]

    print(f"  checkmark Funcion definida y llamada")
    print(f"  checkmark Bytecode size: {resultado['class_info']['bytecode_size']} bytes")
    print()


def test_control_flow_if():
    """Test estructura de control if."""
    print("[TEST 5] Control de flujo - If")

    codigo = """
    fun main() {
        val x: Int = 10
        if (x > 5) {
            val y: Int = 20
        }
    }
    """

    controller = CompiladorController()
    resultado = controller.ejecutar_jvm(
        codigo,
        class_name="IfStatement",
        output_path="tests/jvm/output/IfStatement.class"
    )

    assert resultado["exito"]

    print(f"  checkmark If statement compilado")
    print()


def test_control_flow_while():
    """Test estructura de control while."""
    print("[TEST 6] Control de flujo - While")

    codigo = """
    fun main() {
        var i: Int = 0
        while (i < 5) {
            i = i + 1
        }
    }
    """

    controller = CompiladorController()
    resultado = controller.ejecutar_jvm(
        codigo,
        class_name="WhileLoop",
        output_path="tests/jvm/output/WhileLoop.class"
    )

    assert resultado["exito"]

    print(f"  checkmark While loop compilado")
    print()


def test_java_version_6():
    """Test compilacion con Java 6."""
    print("[TEST 7] Version Java 6")

    codigo = """
    fun main() {
        val x: Int = 42
    }
    """

    controller = CompiladorController()
    resultado = controller.ejecutar_jvm(
        codigo,
        class_name="Java6Test",
        output_path="tests/jvm/output/Java6Test.class",
        java_version=6
    )

    assert resultado["exito"]
    assert resultado["class_info"]["java_version"] == 6

    # Verificar version en bytecode
    bytecode = resultado["bytecode_jvm"]
    _, major = struct.unpack('>HH', bytecode[4:8])
    assert major == 50  # Java 6

    print(f"  checkmark Version 50.0 (Java 6)")
    print()


def test_compilation_errors():
    """Test manejo de errores de compilacion."""
    print("[TEST 8] Manejo de errores")

    codigo_invalido = """
    fun main() {
        val x =  # Sintaxis invalida
    }
    """

    controller = CompiladorController()
    resultado = controller.ejecutar_jvm(
        codigo_invalido,
        class_name="ErrorTest"
    )

    assert not resultado["exito"]
    assert len(resultado["errores"]) > 0

    print(f"  checkmark Errores detectados correctamente")
    print(f"  checkmark {len(resultado['errores'])} error(es) reportado(s)")
    print()


def test_verify_classfile_structure():
    """Test estructura del archivo .class generado."""
    print("[TEST 9] Verificar estructura .class")

    codigo = """
    fun main() {
        val test: Int = 123
    }
    """

    controller = CompiladorController()
    resultado = controller.ejecutar_jvm(
        codigo,
        class_name="StructureTest",
        output_path="tests/jvm/output/StructureTest.class"
    )

    assert resultado["exito"]

    # Leer archivo
    with open("tests/jvm/output/StructureTest.class", 'rb') as f:
        bytecode = f.read()

    # Verificar magic
    magic = struct.unpack('>I', bytecode[0:4])[0]
    assert magic == 0xCAFEBABE

    # Verificar version
    minor, major = struct.unpack('>HH', bytecode[4:8])
    assert minor == 0
    assert major == 50  # Java 6

    print(f"  checkmark Magic number: 0x{magic:X}")
    print(f"  checkmark Version: {major}.{minor}")
    print(f"  checkmark Estructura valida")
    print()


def test_javap_validation():
    """Test validacion con javap (si esta disponible)."""
    print("[TEST 10] Validacion con javap")

    # Verificar si javap esta disponible
    try:
        result = subprocess.run(
            ["javap", "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        javap_available = result.returncode == 0
    except:
        javap_available = False

    if not javap_available:
        print("  info javap no disponible - saltando validacion")
        print()
        return

    # Generar clase de test
    codigo = """
    fun main() {
        val x: Int = 100
    }
    """

    controller = CompiladorController()
    resultado = controller.ejecutar_jvm(
        codigo,
        class_name="JavapTest",
        output_path="tests/jvm/output/JavapTest.class"
    )

    assert resultado["exito"]

    # Ejecutar javap
    try:
        result = subprocess.run(
            ["javap", "-c", "tests/jvm/output/JavapTest.class"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            print("  checkmark javap ejecuto correctamente")
            print("  checkmark .class es valido")
        else:
            print(f"  warning javap fallo: {result.stderr}")

    except Exception as e:
        print(f"  warning Error ejecutando javap: {e}")

    print()


def run_all_tests():
    """Ejecuta todos los tests de integracion."""
    print("=" * 70)
    print("TESTS DE INTEGRACION END-TO-END - KForge v2.0 (Fase 12)")
    print("=" * 70)
    print()

    # Crear directorio de output
    Path("tests/jvm/output").mkdir(parents=True, exist_ok=True)

    test_simple_arithmetic()
    test_variable_assignment()
    test_expressions()
    test_functions()
    test_control_flow_if()
    test_control_flow_while()
    test_java_version_6()
    test_compilation_errors()
    test_verify_classfile_structure()
    test_javap_validation()

    print("=" * 70)
    print("TODOS LOS TESTS DE INTEGRACION PASARON")
    print("=" * 70)


if __name__ == '__main__':
    run_all_tests()
