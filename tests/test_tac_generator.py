"""
Tests para el Generador de Código de Tres Direcciones (TAC)

Este archivo contiene tests completos para verificar la generación
de código TAC desde el AST.

Autor: Gabriel Alejandro Medina Miramontes
Versión: 1.1
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.controller import CompiladorController
from core.tac import TACGenerator


def compilar_y_generar_tac(codigo: str):
    """
    Compila código Kotlin y genera TAC.

    Returns:
        Tuple (exito: bool, instrucciones_tac: List, errores: List)
    """
    controlador = CompiladorController()

    # Ejecutar frontend (lexer, parser, semantic)
    resultado = controlador.ejecutar(codigo)

    if not resultado['exito'] or controlador.error_manager.tiene_errores():
        return False, [], controlador.error_manager.errores

    # Generar TAC
    tac_gen = TACGenerator()
    instrucciones = tac_gen.generate(controlador.ast)

    return True, instrucciones, []


def test_simple_assignment():
    """Test 1: Asignación simple"""
    print("\n[TEST 1] Asignación simple")
    codigo = """
    fun main() {
        var x: Int = 5
    }
    """

    exito, tac, errores = compilar_y_generar_tac(codigo)

    if not exito:
        print(f"ERROR: Compilación falló con {len(errores)} errores")
        for error in errores:
            print(f"  - {error}")
        return False

    print(f"Instrucciones TAC generadas: {len(tac)}")
    for inst in tac:
        print(f"  {inst}")

    # Verificar que hay al menos 3 instrucciones (LABEL func_main, ASSIGN, RETURN)
    if len(tac) < 3:
        print(f"ERROR: Se esperaban al menos 3 instrucciones, se obtuvieron {len(tac)}")
        return False

    # Verificar que hay un ASSIGN
    tiene_assign = any(inst.op == 'ASSIGN' and inst.result == 'x' for inst in tac)
    if not tiene_assign:
        print("ERROR: No se encontró instrucción ASSIGN para x")
        return False

    print("OK: Asignación simple funciona correctamente")
    return True


def test_arithmetic_operations():
    """Test 2: Operaciones aritméticas"""
    print("\n[TEST 2] Operaciones aritméticas")
    codigo = """
    fun main() {
        var a: Int = 10
        var b: Int = 5
        var suma: Int = a + b
        var resta: Int = a - b
        var mult: Int = a * b
        var div: Int = a / b
        var mod: Int = a % b
    }
    """

    exito, tac, errores = compilar_y_generar_tac(codigo)

    if not exito:
        print(f"ERROR: Compilación falló")
        return False

    print(f"Instrucciones TAC generadas: {len(tac)}")
    for inst in tac:
        print(f"  {inst}")

    # Verificar operaciones
    operaciones = ['ADD', 'SUB', 'MUL', 'DIV', 'MOD']
    for op in operaciones:
        tiene_op = any(inst.op == op for inst in tac)
        if not tiene_op:
            print(f"ERROR: No se encontró operación {op}")
            return False

    print("OK: Operaciones aritméticas funcionan correctamente")
    return True


def test_comparisons():
    """Test 3: Comparaciones"""
    print("\n[TEST 3] Comparaciones")
    codigo = """
    fun main() {
        var a: Int = 10
        var b: Int = 5
        var c1: Boolean = a < b
        var c2: Boolean = a > b
        var c3: Boolean = a <= b
        var c4: Boolean = a >= b
        var c5: Boolean = a == b
        var c6: Boolean = a != b
    }
    """

    exito, tac, errores = compilar_y_generar_tac(codigo)

    if not exito:
        print(f"ERROR: Compilación falló")
        return False

    print(f"Instrucciones TAC generadas: {len(tac)}")

    # Verificar comparaciones
    comparaciones = ['LT', 'GT', 'LE', 'GE', 'EQ', 'NE']
    for comp in comparaciones:
        tiene_comp = any(inst.op == comp for inst in tac)
        if not tiene_comp:
            print(f"ERROR: No se encontró comparación {comp}")
            return False

    print("OK: Comparaciones funcionan correctamente")
    return True


def test_logical_operators():
    """Test 4: Operadores lógicos"""
    print("\n[TEST 4] Operadores lógicos")
    codigo = """
    fun main() {
        var a: Boolean = true
        var b: Boolean = false
        var c1: Boolean = a && b
        var c2: Boolean = a || b
        var c3: Boolean = !a
    }
    """

    exito, tac, errores = compilar_y_generar_tac(codigo)

    if not exito:
        print(f"ERROR: Compilación falló")
        return False

    print(f"Instrucciones TAC generadas: {len(tac)}")

    # Verificar operadores lógicos
    tiene_and = any(inst.op == 'AND' for inst in tac)
    tiene_or = any(inst.op == 'OR' for inst in tac)
    tiene_not = any(inst.op == 'NOT' for inst in tac)

    if not (tiene_and and tiene_or and tiene_not):
        print(f"ERROR: Faltan operadores lógicos (AND={tiene_and}, OR={tiene_or}, NOT={tiene_not})")
        return False

    print("OK: Operadores lógicos funcionan correctamente")
    return True


def test_if_statement():
    """Test 5: Estructura if/else"""
    print("\n[TEST 5] Estructura if/else")
    codigo = """
    fun main() {
        var x: Int = 10
        if (x > 5) {
            var a: Int = 1
        } else {
            var b: Int = 2
        }
    }
    """

    exito, tac, errores = compilar_y_generar_tac(codigo)

    if not exito:
        print(f"ERROR: Compilación falló")
        return False

    print(f"Instrucciones TAC generadas: {len(tac)}")
    for inst in tac:
        print(f"  {inst}")

    # Verificar IF_FALSE, GOTO y LABELs
    tiene_if_false = any(inst.op == 'IF_FALSE' for inst in tac)
    tiene_goto = any(inst.op == 'GOTO' for inst in tac)
    num_labels = sum(1 for inst in tac if inst.op == 'LABEL' and inst.label and inst.label.startswith('L'))

    if not tiene_if_false:
        print("ERROR: No se encontró IF_FALSE")
        return False

    if not tiene_goto:
        print("ERROR: No se encontró GOTO")
        return False

    if num_labels < 2:
        print(f"ERROR: Se esperaban al menos 2 etiquetas, se encontraron {num_labels}")
        return False

    print("OK: Estructura if/else funciona correctamente")
    return True


def test_while_loop():
    """Test 6: Loop while"""
    print("\n[TEST 6] Loop while")
    codigo = """
    fun main() {
        var i: Int = 0
        while (i < 10) {
            i = i + 1
        }
    }
    """

    exito, tac, errores = compilar_y_generar_tac(codigo)

    if not exito:
        print(f"ERROR: Compilación falló")
        return False

    print(f"Instrucciones TAC generadas: {len(tac)}")
    for inst in tac:
        print(f"  {inst}")

    # Verificar estructura del while
    tiene_if_false = any(inst.op == 'IF_FALSE' for inst in tac)
    tiene_goto = any(inst.op == 'GOTO' for inst in tac)
    num_labels = sum(1 for inst in tac if inst.op == 'LABEL' and inst.label and inst.label.startswith('L'))

    if not tiene_if_false or not tiene_goto:
        print("ERROR: Estructura de while incorrecta")
        return False

    if num_labels < 2:
        print(f"ERROR: Se esperaban al menos 2 etiquetas para while")
        return False

    print("OK: Loop while funciona correctamente")
    return True


def test_for_loop():
    """Test 7: Loop for"""
    print("\n[TEST 7] Loop for")
    codigo = """
    fun main() {
        for (i in 0..10) {
            var x: Int = i
        }
    }
    """

    exito, tac, errores = compilar_y_generar_tac(codigo)

    if not exito:
        print(f"ERROR: Compilación falló")
        return False

    print(f"Instrucciones TAC generadas: {len(tac)}")
    for inst in tac:
        print(f"  {inst}")

    # Verificar estructura del for
    tiene_le = any(inst.op == 'LE' for inst in tac)  # Comparación i <= 10
    tiene_add = any(inst.op == 'ADD' for inst in tac)  # Incremento i + 1

    if not tiene_le:
        print("ERROR: No se encontró comparación LE en for")
        return False

    if not tiene_add:
        print("ERROR: No se encontró incremento en for")
        return False

    print("OK: Loop for funciona correctamente")
    return True


def test_function_with_return():
    """Test 8: Función con return"""
    print("\n[TEST 8] Función con return")
    codigo = """
    fun suma(a: Int, b: Int): Int {
        return a + b
    }

    fun main() {
        var resultado: Int = suma(5, 3)
    }
    """

    exito, tac, errores = compilar_y_generar_tac(codigo)

    if not exito:
        print(f"ERROR: Compilación falló")
        return False

    print(f"Instrucciones TAC generadas: {len(tac)}")
    for inst in tac:
        print(f"  {inst}")

    # Verificar RETURN con valor
    tiene_return_valor = any(inst.op == 'RETURN' and inst.arg1 is not None for inst in tac)

    if not tiene_return_valor:
        print("ERROR: No se encontró RETURN con valor")
        return False

    print("OK: Función con return funciona correctamente")
    return True


def test_function_call():
    """Test 9: Llamada a función"""
    print("\n[TEST 9] Llamada a función")
    codigo = """
    fun suma(a: Int, b: Int): Int {
        return a + b
    }

    fun main() {
        var resultado: Int = suma(5, 3)
    }
    """

    exito, tac, errores = compilar_y_generar_tac(codigo)

    if not exito:
        print(f"ERROR: Compilación falló")
        return False

    print(f"Instrucciones TAC generadas: {len(tac)}")

    # Verificar PARAM y CALL
    num_params = sum(1 for inst in tac if inst.op == 'PARAM')
    tiene_call = any(inst.op == 'CALL' and inst.arg1 == 'suma' for inst in tac)

    if num_params < 2:
        print(f"ERROR: Se esperaban 2 PARAMs, se encontraron {num_params}")
        return False

    if not tiene_call:
        print("ERROR: No se encontró CALL a suma")
        return False

    print("OK: Llamada a función funciona correctamente")
    return True


def test_arrays():
    """Test 10: Arrays"""
    print("\n[TEST 10] Arrays")
    codigo = """
    fun main() {
        var arr: IntArray = intArrayOf(1, 2, 3)
        var x: Int = arr[0]
        arr[1] = 10
    }
    """

    exito, tac, errores = compilar_y_generar_tac(codigo)

    if not exito:
        print(f"ERROR: Compilación falló")
        return False

    print(f"Instrucciones TAC generadas: {len(tac)}")
    for inst in tac:
        print(f"  {inst}")

    # Verificar ARRAY_LOAD y ARRAY_STORE
    tiene_load = any(inst.op == 'ARRAY_LOAD' for inst in tac)
    tiene_store = any(inst.op == 'ARRAY_STORE' for inst in tac)

    if not tiene_load:
        print("ERROR: No se encontró ARRAY_LOAD")
        return False

    if not tiene_store:
        print("ERROR: No se encontró ARRAY_STORE")
        return False

    print("OK: Arrays funcionan correctamente")
    return True


def test_bubble_sort():
    """Test 11: Algoritmo completo (Bubble Sort)"""
    print("\n[TEST 11] Algoritmo completo (Bubble Sort)")

    # Leer el código del test final
    test_file = os.path.join(os.path.dirname(__file__), '..', 'test_kt', 'test_v1_final.kt')
    with open(test_file, 'r', encoding='utf-8') as f:
        codigo = f.read()

    exito, tac, errores = compilar_y_generar_tac(codigo)

    if not exito:
        print(f"ERROR: Compilación falló")
        for error in errores:
            print(f"  - {error}")
        return False

    print(f"Instrucciones TAC generadas: {len(tac)}")
    print("\nPrimeras 20 instrucciones:")
    for i, inst in enumerate(tac[:20]):
        print(f"  {i:3d}: {inst}")

    if len(tac) > 20:
        print(f"\n... ({len(tac) - 20} instrucciones más) ...")

    # Verificar que se generó código TAC completo
    if len(tac) < 30:
        print(f"ERROR: Se esperaban al menos 30 instrucciones para Bubble Sort")
        return False

    print(f"\nOK: Bubble Sort generó {len(tac)} instrucciones TAC correctamente")
    return True


def main():
    """Ejecuta todos los tests"""
    print("=" * 70)
    print("TESTS DE GENERACIÓN DE CÓDIGO TAC - KForge Compiler v1.1")
    print("=" * 70)

    tests = [
        test_simple_assignment,
        test_arithmetic_operations,
        test_comparisons,
        test_logical_operators,
        test_if_statement,
        test_while_loop,
        test_for_loop,
        test_function_with_return,
        test_function_call,
        test_arrays,
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
        print("\n[OK] TODOS LOS TESTS DE TAC PASARON CORRECTAMENTE")
        return 0
    else:
        print(f"\n[FALLO] {tests_totales - tests_exitosos} tests fallaron")
        return 1


if __name__ == "__main__":
    exit(main())
