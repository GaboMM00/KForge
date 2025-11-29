"""
Tests para JVM Instructions.
Verifica que las instrucciones se generen correctamente con sus opcodes.
"""

import sys
import io
from pathlib import Path

# Agregar el directorio raiz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Fix encoding para Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from core.jvm.instructions import (
    JVMOpcode,
    JVMInstruction,
    iconst,
    iload,
    istore,
    dload,
    dstore,
    aload,
    astore,
    ArrayType
)


def test_opcodes_values():
    """Test que los opcodes tengan los valores correctos."""
    print("[TEST 1] Valores de opcodes")

    # Constants
    assert JVMOpcode.NOP.value == 0x00
    assert JVMOpcode.ICONST_0.value == 0x03
    assert JVMOpcode.ICONST_1.value == 0x04
    assert JVMOpcode.BIPUSH.value == 0x10
    assert JVMOpcode.LDC.value == 0x12

    # Loads
    assert JVMOpcode.ILOAD.value == 0x15
    assert JVMOpcode.ILOAD_0.value == 0x1A
    assert JVMOpcode.DLOAD.value == 0x18
    assert JVMOpcode.ALOAD.value == 0x19

    # Stores
    assert JVMOpcode.ISTORE.value == 0x36
    assert JVMOpcode.ISTORE_0.value == 0x3B
    assert JVMOpcode.DSTORE.value == 0x39
    assert JVMOpcode.ASTORE.value == 0x3A

    # Arithmetic
    assert JVMOpcode.IADD.value == 0x60
    assert JVMOpcode.ISUB.value == 0x64
    assert JVMOpcode.IMUL.value == 0x68
    assert JVMOpcode.IDIV.value == 0x6C
    assert JVMOpcode.IREM.value == 0x70

    assert JVMOpcode.DADD.value == 0x63
    assert JVMOpcode.DSUB.value == 0x67
    assert JVMOpcode.DMUL.value == 0x6B
    assert JVMOpcode.DDIV.value == 0x6F

    # Comparisons
    assert JVMOpcode.IF_ICMPEQ.value == 0x9F
    assert JVMOpcode.IF_ICMPNE.value == 0xA0
    assert JVMOpcode.IF_ICMPLT.value == 0xA1
    assert JVMOpcode.IF_ICMPGE.value == 0xA2
    assert JVMOpcode.IF_ICMPGT.value == 0xA3
    assert JVMOpcode.IF_ICMPLE.value == 0xA4

    # Control flow
    assert JVMOpcode.GOTO.value == 0xA7
    assert JVMOpcode.IRETURN.value == 0xAC
    assert JVMOpcode.RETURN.value == 0xB1

    # Method invocation
    assert JVMOpcode.INVOKEVIRTUAL.value == 0xB6
    assert JVMOpcode.INVOKESTATIC.value == 0xB8

    # Arrays
    assert JVMOpcode.NEWARRAY.value == 0xBC
    assert JVMOpcode.IALOAD.value == 0x2E
    assert JVMOpcode.IASTORE.value == 0x4F
    assert JVMOpcode.ARRAYLENGTH.value == 0xBE

    print("  ✓ Todos los opcodes tienen valores correctos")
    print()


def test_instruction_creation():
    """Test creacion de instrucciones."""
    print("[TEST 2] Creacion de instrucciones")

    # Instruccion sin operandos
    inst1 = JVMInstruction(JVMOpcode.RETURN)
    assert inst1.opcode == JVMOpcode.RETURN
    assert inst1.operands == []
    assert inst1.label is None

    # Instruccion con 1 operando
    inst2 = JVMInstruction(JVMOpcode.BIPUSH, [5])
    assert inst2.opcode == JVMOpcode.BIPUSH
    assert inst2.operands == [5]

    # Instruccion con 2 operandos
    inst3 = JVMInstruction(JVMOpcode.IINC, [1, 10])
    assert inst3.opcode == JVMOpcode.IINC
    assert inst3.operands == [1, 10]

    # Instruccion con label
    inst4 = JVMInstruction(JVMOpcode.GOTO, [10], label="L1")
    assert inst4.label == "L1"

    print("  ✓ Instrucciones creadas correctamente")
    print()


def test_instruction_to_bytes():
    """Test conversion de instrucciones a bytes."""
    print("[TEST 3] Conversion a bytes")

    # Instruccion simple (return)
    inst1 = JVMInstruction(JVMOpcode.RETURN)
    bytecode1 = inst1.to_bytes()
    assert bytecode1 == b'\xb1', f"Expected b'\\xb1', got {bytecode1.hex()}"

    # Instruccion con operando de 1 byte (bipush)
    inst2 = JVMInstruction(JVMOpcode.BIPUSH, [5])
    bytecode2 = inst2.to_bytes()
    assert bytecode2 == b'\x10\x05', f"Expected b'\\x10\\x05', got {bytecode2.hex()}"

    # Instruccion con operando de 2 bytes (goto)
    inst3 = JVMInstruction(JVMOpcode.GOTO, [100])
    bytecode3 = inst3.to_bytes()
    assert bytecode3 == b'\xa7\x00\x64', f"Expected b'\\xa7\\x00\\x64', got {bytecode3.hex()}"

    # Instrucciones aritmeticas
    inst4 = JVMInstruction(JVMOpcode.IADD)
    assert inst4.to_bytes() == b'\x60'

    inst5 = JVMInstruction(JVMOpcode.IMUL)
    assert inst5.to_bytes() == b'\x68'

    print("  ✓ Conversion a bytes correcta")
    print()


def test_iconst_helper():
    """Test helper function iconst."""
    print("[TEST 4] Helper iconst")

    # iconst_m1
    inst = iconst(-1)
    assert inst.opcode == JVMOpcode.ICONST_M1
    assert inst.to_bytes() == b'\x02'

    # iconst_0 a iconst_5
    for i in range(6):
        inst = iconst(i)
        expected_opcode = [JVMOpcode.ICONST_0, JVMOpcode.ICONST_1,
                           JVMOpcode.ICONST_2, JVMOpcode.ICONST_3,
                           JVMOpcode.ICONST_4, JVMOpcode.ICONST_5][i]
        assert inst.opcode == expected_opcode

    # bipush (-128 a 127)
    inst = iconst(10)
    assert inst.opcode == JVMOpcode.BIPUSH
    assert inst.operands == [10]

    inst = iconst(-50)
    assert inst.opcode == JVMOpcode.BIPUSH
    # -50 en unsigned byte = 206
    assert inst.operands == [206]

    # sipush
    inst = iconst(1000)
    assert inst.opcode == JVMOpcode.SIPUSH
    assert inst.operands == [1000]

    print("  ✓ iconst helper funciona correctamente")
    print()


def test_iload_istore_helpers():
    """Test helpers iload e istore."""
    print("[TEST 5] Helpers iload/istore")

    # iload_0 a iload_3
    for i in range(4):
        inst = iload(i)
        expected = [JVMOpcode.ILOAD_0, JVMOpcode.ILOAD_1,
                    JVMOpcode.ILOAD_2, JVMOpcode.ILOAD_3][i]
        assert inst.opcode == expected

    # iload con indice > 3
    inst = iload(10)
    assert inst.opcode == JVMOpcode.ILOAD
    assert inst.operands == [10]

    # istore_0 a istore_3
    for i in range(4):
        inst = istore(i)
        expected = [JVMOpcode.ISTORE_0, JVMOpcode.ISTORE_1,
                    JVMOpcode.ISTORE_2, JVMOpcode.ISTORE_3][i]
        assert inst.opcode == expected

    # istore con indice > 3
    inst = istore(5)
    assert inst.opcode == JVMOpcode.ISTORE
    assert inst.operands == [5]

    print("  ✓ iload/istore helpers funcionan correctamente")
    print()


def test_dload_dstore_helpers():
    """Test helpers dload y dstore."""
    print("[TEST 6] Helpers dload/dstore")

    # dload_0 a dload_3
    for i in range(4):
        inst = dload(i)
        expected = [JVMOpcode.DLOAD_0, JVMOpcode.DLOAD_1,
                    JVMOpcode.DLOAD_2, JVMOpcode.DLOAD_3][i]
        assert inst.opcode == expected

    inst = dload(7)
    assert inst.opcode == JVMOpcode.DLOAD
    assert inst.operands == [7]

    # dstore_0 a dstore_3
    for i in range(4):
        inst = dstore(i)
        expected = [JVMOpcode.DSTORE_0, JVMOpcode.DSTORE_1,
                    JVMOpcode.DSTORE_2, JVMOpcode.DSTORE_3][i]
        assert inst.opcode == expected

    inst = dstore(6)
    assert inst.opcode == JVMOpcode.DSTORE
    assert inst.operands == [6]

    print("  ✓ dload/dstore helpers funcionan correctamente")
    print()


def test_aload_astore_helpers():
    """Test helpers aload y astore."""
    print("[TEST 7] Helpers aload/astore")

    # aload_0 a aload_3
    for i in range(4):
        inst = aload(i)
        expected = [JVMOpcode.ALOAD_0, JVMOpcode.ALOAD_1,
                    JVMOpcode.ALOAD_2, JVMOpcode.ALOAD_3][i]
        assert inst.opcode == expected

    # astore_0 a astore_3
    for i in range(4):
        inst = astore(i)
        expected = [JVMOpcode.ASTORE_0, JVMOpcode.ASTORE_1,
                    JVMOpcode.ASTORE_2, JVMOpcode.ASTORE_3][i]
        assert inst.opcode == expected

    print("  ✓ aload/astore helpers funcionan correctamente")
    print()


def test_array_types():
    """Test tipos de arrays."""
    print("[TEST 8] Tipos de arrays")

    assert ArrayType.T_INT.value == 10
    assert ArrayType.T_DOUBLE.value == 7
    assert ArrayType.T_BOOLEAN.value == 4
    assert ArrayType.T_CHAR.value == 5

    print("  ✓ Array types correctos")
    print()


def test_instruction_str():
    """Test representacion en string."""
    print("[TEST 9] Representacion en string")

    inst1 = JVMInstruction(JVMOpcode.RETURN)
    assert str(inst1) == "RETURN"

    inst2 = JVMInstruction(JVMOpcode.BIPUSH, [10])
    assert str(inst2) == "BIPUSH 10"

    inst3 = JVMInstruction(JVMOpcode.GOTO, [100], label="L1")
    assert str(inst3) == "L1: GOTO 100"

    inst4 = JVMInstruction(JVMOpcode.IINC, [1, 5])
    assert str(inst4) == "IINC 1, 5"

    print("  ✓ Representacion en string correcta")
    print()


def test_bytecode_sequence():
    """Test secuencia de bytecode."""
    print("[TEST 10] Secuencia de bytecode")

    # Simular: int x = 5; x = x + 3;
    instructions = [
        iconst(5),              # iconst_5
        istore(1),              # istore_1
        iload(1),               # iload_1
        iconst(3),              # iconst_3
        JVMInstruction(JVMOpcode.IADD),  # iadd
        istore(1),              # istore_1
        JVMInstruction(JVMOpcode.RETURN) # return
    ]

    # Generar bytecode
    bytecode = b''.join(inst.to_bytes() for inst in instructions)

    # Verificar
    expected = b'\x08\x3c\x1b\x06\x60\x3c\xb1'
    assert bytecode == expected, f"Expected {expected.hex()}, got {bytecode.hex()}"

    print("  ✓ Secuencia de bytecode correcta")
    print(f"  ✓ Bytecode generado: {bytecode.hex()}")
    print()


def run_all_tests():
    """Ejecuta todos los tests."""
    print("=" * 70)
    print("TESTS DE JVM INSTRUCTIONS - KForge JVM v2.0")
    print("=" * 70)
    print()

    test_opcodes_values()
    test_instruction_creation()
    test_instruction_to_bytes()
    test_iconst_helper()
    test_iload_istore_helpers()
    test_dload_dstore_helpers()
    test_aload_astore_helpers()
    test_array_types()
    test_instruction_str()
    test_bytecode_sequence()

    print("=" * 70)
    print("TODOS LOS TESTS PASARON EXITOSAMENTE")
    print("=" * 70)


if __name__ == '__main__':
    run_all_tests()
