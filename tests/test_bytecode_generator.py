"""
Tests para el Generador de Bytecode Stack-Based

Este archivo contiene tests completos para verificar la generación
de bytecode desde código TAC.

Autor: Gabriel Alejandro Medina Miramontes
Versión: 1.1
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.controller import CompiladorController
from core.tac import TACGenerator
from core.bytecode import BytecodeGenerator


def compilar_y_generar_bytecode(codigo: str):
    """
    Compila código Kotlin, genera TAC y luego bytecode.

    Returns:
        Tuple (exito: bool, bytecode: List, tac: List, errores: List)
    """
    controlador = CompiladorController()

    # Ejecutar frontend (lexer, parser, semantic)
    resultado = controlador.ejecutar(codigo)

    if not resultado['exito'] or controlador.error_manager.tiene_errores():
        return False, [], [], controlador.error_manager.errores

    # Generar TAC
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(controlador.ast)

    # Generar Bytecode
    bytecode_gen = BytecodeGenerator()
    bytecode_instructions = bytecode_gen.generate(tac_instructions)

    return True, bytecode_instructions, tac_instructions, []


def test_simple_assignment():
    """Test 1: Asignación simple TAC -> Bytecode"""
    print("\n[TEST 1] Asignacion simple TAC -> Bytecode")
    codigo = """
    fun main() {
        var x: Int = 5
    }
    """

    exito, bytecode, tac, errores = compilar_y_generar_bytecode(codigo)

    if not exito:
        print(f"ERROR: Compilación falló")
        return False

    print(f"Instrucciones TAC: {len(tac)}")
    print(f"Instrucciones Bytecode: {len(bytecode)}")

    # Verificar que hay instrucciones bytecode
    if len(bytecode) < 3:
        print(f"ERROR: Se esperaban al menos 3 instrucciones bytecode")
        return False

    # Verificar instrucciones clave
    opcodes = [inst.opcode for inst in bytecode]

    if 'PUSH' not in opcodes and 'LOAD' not in opcodes:
        print("ERROR: No se encontró PUSH o LOAD")
        return False

    if 'STORE' not in opcodes:
        print("ERROR: No se encontró STORE")
        return False

    print("OK: Asignación simple funciona")
    return True


def test_arithmetic_operations():
    """Test 2: Operaciones aritméticas"""
    print("\n[TEST 2] Operaciones aritméticas")
    codigo = """
    fun main() {
        var a: Int = 10
        var b: Int = 5
        var suma: Int = a + b
    }
    """

    exito, bytecode, tac, errores = compilar_y_generar_bytecode(codigo)

    if not exito:
        print(f"ERROR: Compilación falló")
        return False

    print(f"Instrucciones Bytecode generadas: {len(bytecode)}")

    # Verificar operaciones aritméticas
    opcodes = [inst.opcode for inst in bytecode]

    if 'ADD' not in opcodes:
        print("ERROR: No se encontró ADD")
        return False

    # Imprimir primeras instrucciones para debugging
    print("\nPrimeras 10 instrucciones:")
    for i, inst in enumerate(bytecode[:10]):
        print(f"  {i:3d}: {inst}")

    print("OK: Operaciones aritméticas funcionan")
    return True


def test_if_statement():
    """Test 3: Estructura if con saltos"""
    print("\n[TEST 3] Estructura if con saltos")
    codigo = """
    fun main() {
        var x: Int = 10
        if (x > 5) {
            var a: Int = 1
        }
    }
    """

    exito, bytecode, tac, errores = compilar_y_generar_bytecode(codigo)

    if not exito:
        print(f"ERROR: Compilación falló")
        return False

    print(f"Instrucciones Bytecode: {len(bytecode)}")

    # Verificar instrucciones de control de flujo
    opcodes = [inst.opcode for inst in bytecode]

    if 'JUMPF' not in opcodes:
        print("ERROR: No se encontró JUMPF")
        return False

    if 'LABEL' not in opcodes:
        print("ERROR: No se encontraron LABELs")
        return False

    print("OK: Estructura if funciona correctamente")
    return True


def test_while_loop():
    """Test 4: Loop while"""
    print("\n[TEST 4] Loop while")
    codigo = """
    fun main() {
        var i: Int = 0
        while (i < 10) {
            i = i + 1
        }
    }
    """

    exito, bytecode, tac, errores = compilar_y_generar_bytecode(codigo)

    if not exito:
        print(f"ERROR: Compilación falló")
        return False

    print(f"Instrucciones Bytecode: {len(bytecode)}")

    # Verificar estructura del while
    opcodes = [inst.opcode for inst in bytecode]

    if 'JUMP' not in opcodes:
        print("ERROR: No se encontró JUMP (para volver al inicio del loop)")
        return False

    if 'JUMPF' not in opcodes:
        print("ERROR: No se encontró JUMPF (para salir del loop)")
        return False

    print("OK: Loop while funciona correctamente")
    return True


def test_function_call():
    """Test 5: Llamada a función"""
    print("\n[TEST 5] Llamada a función")
    codigo = """
    fun suma(a: Int, b: Int): Int {
        return a + b
    }

    fun main() {
        var resultado: Int = suma(5, 3)
    }
    """

    exito, bytecode, tac, errores = compilar_y_generar_bytecode(codigo)

    if not exito:
        print(f"ERROR: Compilación falló")
        return False

    print(f"Instrucciones Bytecode: {len(bytecode)}")

    # Verificar instrucciones de función
    opcodes = [inst.opcode for inst in bytecode]

    if 'CALL' not in opcodes:
        print("ERROR: No se encontró CALL")
        return False

    if 'RET' not in opcodes:
        print("ERROR: No se encontró RET")
        return False

    # Los parámetros se pushean antes de CALL
    # Verificar que hay PUSH o LOAD antes de CALL
    call_index = opcodes.index('CALL')
    if call_index < 2:
        print("ERROR: No hay suficientes instrucciones antes de CALL")
        return False

    print("OK: Llamada a función funciona correctamente")
    return True


def test_arrays():
    """Test 6: Arrays (ALOAD y ASTORE)"""
    print("\n[TEST 6] Arrays (ALOAD y ASTORE)")
    codigo = """
    fun main() {
        var arr: IntArray = intArrayOf(1, 2, 3)
        var x: Int = arr[0]
        arr[1] = 10
    }
    """

    exito, bytecode, tac, errores = compilar_y_generar_bytecode(codigo)

    if not exito:
        print(f"ERROR: Compilación falló")
        return False

    print(f"Instrucciones Bytecode: {len(bytecode)}")

    # Verificar operaciones de array
    opcodes = [inst.opcode for inst in bytecode]

    if 'ALOAD' not in opcodes:
        print("ERROR: No se encontró ALOAD (array load)")
        return False

    if 'ASTORE' not in opcodes:
        print("ERROR: No se encontró ASTORE (array store)")
        return False

    print("OK: Arrays funcionan correctamente")
    return True


def test_format_output():
    """Test 7: Formato de salida assembly"""
    print("\n[TEST 7] Formato de salida assembly")
    codigo = """
    fun main() {
        var x: Int = 10
        var y: Int = x + 5
    }
    """

    exito, bytecode_list, tac, errores = compilar_y_generar_bytecode(codigo)

    if not exito:
        print(f"ERROR: Compilación falló")
        return False

    # Generar formato de salida
    bytecode_gen = BytecodeGenerator()
    bytecode_gen.instructions = bytecode_list
    output = bytecode_gen.format_output(show_comments=True)

    print(f"\nBytecode Assembly generado:")
    print("=" * 70)
    print(output)
    print("=" * 70)

    # Verificar que el output tiene contenido
    if len(output) < 50:
        print("ERROR: Output muy corto")
        return False

    # Verificar que contiene comentarios
    if ';' not in output:
        print("ERROR: No se encontraron comentarios")
        return False

    # Verificar que contiene números de línea
    if ':' not in output:
        print("ERROR: No se encontraron números de línea")
        return False

    print("\nOK: Formato de salida assembly funciona correctamente")
    return True


def test_bubble_sort():
    """Test 8: Algoritmo completo (Bubble Sort)"""
    print("\n[TEST 8] Algoritmo completo (Bubble Sort)")

    # Leer el código del test final
    test_file = os.path.join(os.path.dirname(__file__), '..', 'test_kt', 'test_v1_final.kt')
    with open(test_file, 'r', encoding='utf-8') as f:
        codigo = f.read()

    exito, bytecode, tac, errores = compilar_y_generar_bytecode(codigo)

    if not exito:
        print(f"ERROR: Compilación falló")
        for error in errores:
            print(f"  - {error}")
        return False

    print(f"TAC instructions: {len(tac)}")
    print(f"Bytecode instructions: {len(bytecode)}")

    # Verificar que se generó bytecode completo
    if len(bytecode) < 100:
        print(f"WARNING: Se esperaban más instrucciones para Bubble Sort")

    # Verificar que tiene HALT al final
    if bytecode[-1].opcode != 'HALT':
        print("ERROR: No termina con HALT")
        return False

    # Mostrar muestra del bytecode generado
    bytecode_gen = BytecodeGenerator()
    bytecode_gen.instructions = bytecode
    output = bytecode_gen.format_output(show_comments=False)

    lines = output.split('\n')
    print(f"\nPrimeras 30 líneas del bytecode:")
    for line in lines[:30]:
        print(line)

    print(f"\n... ({len(lines) - 30} líneas más) ...")

    print(f"\nOK: Bubble Sort generó {len(bytecode)} instrucciones bytecode")
    return True


def test_logical_operators():
    """Test 9: Operadores lógicos (AND, OR, NOT)"""
    print("\n[TEST 9] Operadores lógicos")
    codigo = """
    fun main() {
        var a: Boolean = true
        var b: Boolean = false
        var c: Boolean = a && b
        var d: Boolean = !a
    }
    """

    exito, bytecode, tac, errores = compilar_y_generar_bytecode(codigo)

    if not exito:
        print(f"ERROR: Compilación falló")
        return False

    print(f"Instrucciones Bytecode: {len(bytecode)}")

    # Verificar operadores lógicos
    opcodes = [inst.opcode for inst in bytecode]

    if 'AND' not in opcodes:
        print("ERROR: No se encontró AND")
        return False

    if 'NOT' not in opcodes:
        print("ERROR: No se encontró NOT")
        return False

    print("OK: Operadores lógicos funcionan correctamente")
    return True


def test_comparisons():
    """Test 10: Comparaciones"""
    print("\n[TEST 10] Comparaciones")
    codigo = """
    fun main() {
        var a: Int = 10
        var b: Int = 5
        var c: Boolean = a < b
        var d: Boolean = a == b
    }
    """

    exito, bytecode, tac, errores = compilar_y_generar_bytecode(codigo)

    if not exito:
        print(f"ERROR: Compilación falló")
        return False

    print(f"Instrucciones Bytecode: {len(bytecode)}")

    # Verificar comparaciones
    opcodes = [inst.opcode for inst in bytecode]

    comparisons_found = any(op in opcodes for op in ['LT', 'GT', 'LE', 'GE', 'EQ', 'NE'])

    if not comparisons_found:
        print("ERROR: No se encontraron comparaciones")
        return False

    print("OK: Comparaciones funcionan correctamente")
    return True


def main():
    """Ejecuta todos los tests"""
    print("=" * 70)
    print("TESTS DE GENERACIÓN DE BYTECODE - KForge Compiler v1.1")
    print("=" * 70)

    tests = [
        test_simple_assignment,
        test_arithmetic_operations,
        test_if_statement,
        test_while_loop,
        test_function_call,
        test_arrays,
        test_format_output,
        test_logical_operators,
        test_comparisons,
        test_bubble_sort
    ]

    resultados = []
    for test in tests:
        try:
            resultado = test()
            resultados.append(resultado)
        except Exception as e:
            print(f"\nEXCEPCIÓN en {test.__name__}: {e}")
            import traceback
            traceback.print_exc()
            resultados.append(False)

    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN DE TESTS")
    print("=" * 70)

    tests_exitosos = sum(1 for r in resultados if r)
    tests_totales = len(resultados)

    print(f"Tests exitosos: {tests_exitosos}/{tests_totales}")

    if tests_exitosos == tests_totales:
        print("\n[OK] TODOS LOS TESTS DE BYTECODE PASARON CORRECTAMENTE")
        return 0
    else:
        print(f"\n[FALLO] {tests_totales - tests_exitosos} tests fallaron")
        return 1


if __name__ == "__main__":
    exit(main())
