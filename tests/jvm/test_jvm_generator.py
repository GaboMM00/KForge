"""
Tests para JVM Generator.
Verifica la conversion de TAC a bytecode JVM.
"""

import sys
import io
from pathlib import Path

# Agregar el directorio raiz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Fix encoding para Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from core.tac import TACInstruction
from core.jvm.jvm_generator import JVMGenerator, LocalVariableManager, StackDepthTracker
from core.jvm.constant_pool import ConstantPool
from core.jvm.instructions import JVMOpcode
from core.utils import TipoDato


def test_local_variable_manager():
    """Test gestion de variables locales."""
    print("[TEST 1] Local Variable Manager")

    # Metodo estatico
    lvm = LocalVariableManager(is_static=True)
    assert lvm.next_slot == 0, "Metodo estatico debe empezar en slot 0"

    # Asignar variables
    slot_a = lvm.get_or_allocate("a", TipoDato.INT)
    assert slot_a == 0, f"Primera variable debe ser slot 0, fue {slot_a}"

    slot_b = lvm.get_or_allocate("b", TipoDato.INT)
    assert slot_b == 1, f"Segunda variable debe ser slot 1, fue {slot_b}"

    # Reutilizar variable
    slot_a2 = lvm.get_or_allocate("a", TipoDato.INT)
    assert slot_a2 == slot_a, "Debe reutilizar slot de variable existente"

    # Variable double ocupa 2 slots
    slot_d = lvm.get_or_allocate("d", TipoDato.DOUBLE)
    assert slot_d == 2, f"Double debe ser slot 2, fue {slot_d}"

    max_locals = lvm.get_max_locals()
    assert max_locals == 4, f"max_locals debe ser 4 (0,1,2,3), fue {max_locals}"

    print("  ✓ Variables asignadas correctamente")
    print(f"  ✓ max_locals: {max_locals}")
    print()


def test_stack_depth_tracker():
    """Test rastreo de profundidad del stack."""
    print("[TEST 2] Stack Depth Tracker")

    tracker = StackDepthTracker()

    # Push
    tracker.push()
    assert tracker.current_depth == 1
    assert tracker.max_depth == 1

    tracker.push()
    assert tracker.current_depth == 2
    assert tracker.max_depth == 2

    # Pop
    tracker.pop()
    assert tracker.current_depth == 1
    assert tracker.max_depth == 2  # max no cambia

    tracker.push(3)
    assert tracker.current_depth == 4
    assert tracker.max_depth == 4

    tracker.pop(4)
    assert tracker.current_depth == 0

    print("  ✓ Stack depth rastreado correctamente")
    print(f"  ✓ max_stack: {tracker.get_max_stack()}")
    print()


def test_simple_assignment():
    """Test asignacion simple: x = 5"""
    print("[TEST 3] Asignacion simple")

    cp = ConstantPool()
    generator = JVMGenerator(cp)

    # TAC: x = 5
    tac = [
        TACInstruction('ASSIGN', "5", None, "x")
    ]

    bytecode, max_stack, max_locals = generator.generate(tac)

    # Verificar que genero bytecode
    assert len(bytecode) > 0, "Debe generar bytecode"
    assert max_stack > 0, "max_stack debe ser > 0"
    assert max_locals > 0, "max_locals debe ser > 0"

    print(f"  ✓ Bytecode generado: {len(bytecode)} bytes")
    print(f"  ✓ max_stack: {max_stack}")
    print(f"  ✓ max_locals: {max_locals}")
    print(f"  ✓ Bytecode hex: {bytecode.hex()}")
    print()


def test_arithmetic_operations():
    """Test operaciones aritmeticas."""
    print("[TEST 4] Operaciones aritmeticas")

    cp = ConstantPool()
    generator = JVMGenerator(cp)

    # TAC: result = 10 + 20
    tac = [
        TACInstruction('ADD', "10", "20", "result")
    ]

    bytecode, max_stack, max_locals = generator.generate(tac)

    # Debe contener: bipush 10, bipush 20, iadd, istore
    assert len(bytecode) > 0
    assert max_stack >= 2, "Suma requiere al menos stack de 2"

    print(f"  ✓ ADD generado correctamente")
    print(f"  ✓ max_stack: {max_stack}, max_locals: {max_locals}")

    # Test SUB, MUL, DIV, MOD
    for op in ['SUB', 'MUL', 'DIV', 'MOD']:
        generator = JVMGenerator(ConstantPool())
        tac = [TACInstruction(op, "result", "10", "5")]
        bytecode, _, _ = generator.generate(tac)
        assert len(bytecode) > 0, f"{op} debe generar bytecode"
        print(f"  ✓ {op} generado correctamente")

    print()


def test_comparisons():
    """Test comparaciones."""
    print("[TEST 5] Comparaciones")

    cp = ConstantPool()
    generator = JVMGenerator(cp)

    # TAC: result = (10 < 20)
    tac = [
        TACInstruction('LT', "10", "20", "result")
    ]

    bytecode, max_stack, max_locals = generator.generate(tac)

    assert len(bytecode) > 0
    print(f"  ✓ LT (less than) generado")

    # Test otras comparaciones
    for op in ['GT', 'LE', 'GE',
               'EQ', 'NE']:
        generator = JVMGenerator(ConstantPool())
        tac = [TACInstruction(op, "result", "10", "20")]
        bytecode, _, _ = generator.generate(tac)
        assert len(bytecode) > 0
        print(f"  ✓ {op} generado")

    print()


def test_logical_operations():
    """Test operadores logicos."""
    print("[TEST 6] Operadores logicos")

    # AND
    cp = ConstantPool()
    generator = JVMGenerator(cp)
    tac = [TACInstruction('AND', "1", "1", "result")]
    bytecode, _, _ = generator.generate(tac)
    assert len(bytecode) > 0
    print("  ✓ AND generado")

    # OR
    generator = JVMGenerator(ConstantPool())
    tac = [TACInstruction('OR', "0", "1", "result")]
    bytecode, _, _ = generator.generate(tac)
    assert len(bytecode) > 0
    print("  ✓ OR generado")

    # NOT
    generator = JVMGenerator(ConstantPool())
    tac = [TACInstruction('NOT', "1", None, "result")]
    bytecode, _, _ = generator.generate(tac)
    assert len(bytecode) > 0
    print("  ✓ NOT generado")

    print()


def test_labels_and_jumps():
    """Test labels y saltos."""
    print("[TEST 7] Labels y saltos")

    cp = ConstantPool()
    generator = JVMGenerator(cp)

    # TAC con label y goto
    tac = [
        TACInstruction('ASSIGN', "10", None, "x"),
        TACInstruction('LABEL', label="L1"),
        TACInstruction('ASSIGN', "20", None, "y"),
        TACInstruction('GOTO', "L1")
    ]

    bytecode, max_stack, max_locals = generator.generate(tac)

    assert len(bytecode) > 0
    assert "L1" in generator.labels, "Label L1 debe estar registrado"
    print("  ✓ Labels registrados correctamente")
    print(f"  ✓ Bytecode generado: {len(bytecode)} bytes")

    print()


def test_if_false():
    """Test condicional if_false."""
    print("[TEST 8] Condicional if_false")

    cp = ConstantPool()
    generator = JVMGenerator(cp)

    # TAC: if !condition goto L1
    tac = [
        TACInstruction('ASSIGN', "0", None, "condition"),
        TACInstruction('IF_FALSE', "condition", "L1"),
        TACInstruction('ASSIGN', "10", None, "x"),
        TACInstruction('LABEL', label="L1"),
        TACInstruction('ASSIGN', "20", None, "y")
    ]

    bytecode, max_stack, max_locals = generator.generate(tac)

    assert len(bytecode) > 0
    print("  ✓ IF_FALSE generado correctamente")
    print(f"  ✓ Bytecode: {len(bytecode)} bytes")

    print()


def test_return_statement():
    """Test return."""
    print("[TEST 9] Return statement")

    # Return con valor
    cp = ConstantPool()
    generator = JVMGenerator(cp)
    tac = [
        TACInstruction('ASSIGN', "42", None, "x"),
        TACInstruction('RETURN', "x")
    ]
    bytecode, _, _ = generator.generate(tac)
    assert len(bytecode) > 0
    # Debe contener ireturn (0xAC)
    assert b'\xac' in bytecode, "Debe contener ireturn"
    print("  ✓ Return con valor generado")

    # Return void
    generator = JVMGenerator(ConstantPool())
    tac = [TACInstruction('RETURN')]
    bytecode, _, _ = generator.generate(tac)
    assert len(bytecode) > 0
    # Debe contener return (0xB1)
    assert b'\xb1' in bytecode, "Debe contener return (void)"
    print("  ✓ Return void generado")

    print()


def test_complex_expression():
    """Test expresion compleja."""
    print("[TEST 10] Expresion compleja")

    cp = ConstantPool()
    generator = JVMGenerator(cp)

    # TAC: result = (a + b) * (c - d)
    # Simplificado como:
    # t1 = a + b
    # t2 = c - d
    # result = t1 * t2
    tac = [
        TACInstruction('ASSIGN', "10", None, "a"),
        TACInstruction('ASSIGN', "20", None, "b"),
        TACInstruction('ASSIGN', "30", None, "c"),
        TACInstruction('ASSIGN', "5", None, "d"),
        TACInstruction('ADD', "a", "b", "t1"),
        TACInstruction('SUB', "c", "d", "t2"),
        TACInstruction('MUL', "t1", "t2", "result")
    ]

    bytecode, max_stack, max_locals = generator.generate(tac)

    assert len(bytecode) > 0
    assert max_locals >= 6, "Debe tener slots para a, b, c, d, t1, t2, result"

    print(f"  ✓ Expresion compleja generada")
    print(f"  ✓ Bytecode: {len(bytecode)} bytes")
    print(f"  ✓ max_stack: {max_stack}, max_locals: {max_locals}")
    print(f"  ✓ Variables: {list(generator.local_vars.var_to_slot.keys())}")

    print()


def run_all_tests():
    """Ejecuta todos los tests."""
    print("=" * 70)
    print("TESTS DE JVM GENERATOR - KForge JVM v2.0")
    print("=" * 70)
    print()

    test_local_variable_manager()
    test_stack_depth_tracker()
    test_simple_assignment()
    test_arithmetic_operations()
    test_comparisons()
    test_logical_operations()
    test_labels_and_jumps()
    test_if_false()
    test_return_statement()
    test_complex_expression()

    print("=" * 70)
    print("TODOS LOS TESTS PASARON EXITOSAMENTE")
    print("=" * 70)


if __name__ == '__main__':
    run_all_tests()
