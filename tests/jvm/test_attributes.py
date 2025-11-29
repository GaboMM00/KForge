"""
Tests para Attributes Avanzados JVM.
Verifica LineNumberTable y LocalVariableTable.
"""

import sys
import io
from pathlib import Path

# Agregar el directorio raiz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Fix encoding para Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import struct
from core.jvm.attributes import (
    LineNumberTableAttribute,
    LocalVariableTableAttribute,
    LineNumberEntry,
    LocalVariableEntry,
    create_line_number_table,
    create_local_variable_table
)
from core.jvm.constant_pool import ConstantPool
from core.jvm.classfile import (
    ClassFileWriter,
    MethodInfo,
    CodeAttribute,
    AccessFlags
)
from core.jvm.descriptors import TypeDescriptor


def test_line_number_entry():
    """Test LineNumberEntry basico."""
    print("[TEST 1] LineNumberEntry")

    entry = LineNumberEntry(start_pc=0, line_number=1)
    bytecode = entry.to_bytes()

    # Verificar estructura
    assert len(bytecode) == 4, f"LineNumberEntry debe ser 4 bytes, fue {len(bytecode)}"

    # Decodificar
    start_pc, line_number = struct.unpack('>HH', bytecode)
    assert start_pc == 0
    assert line_number == 1

    print("  ✓ LineNumberEntry estructura correcta")
    print(f"  ✓ Bytecode: {bytecode.hex()}")
    print()


def test_line_number_table_attribute():
    """Test LineNumberTable attribute."""
    print("[TEST 2] LineNumberTable Attribute")

    cp = ConstantPool()
    name_index = cp.add_utf8("LineNumberTable")

    lnt = LineNumberTableAttribute(name_index)
    lnt.add_entry(0, 1)
    lnt.add_entry(5, 2)
    lnt.add_entry(10, 3)

    bytecode = lnt.to_bytes()

    # Verificar estructura
    # u2 attribute_name_index + u4 attribute_length + info
    assert len(bytecode) > 6, "Debe tener header + datos"

    # Decodificar header
    attr_name_idx, attr_length = struct.unpack('>HI', bytecode[0:6])
    assert attr_name_idx == name_index
    assert attr_length > 0

    # Decodificar tabla
    table_length = struct.unpack('>H', bytecode[6:8])[0]
    assert table_length == 3, f"Debe tener 3 entries, tiene {table_length}"

    print("  ✓ LineNumberTable creado correctamente")
    print(f"  ✓ Entries: {table_length}")
    print(f"  ✓ Tamaño: {len(bytecode)} bytes")
    print()


def test_local_variable_entry():
    """Test LocalVariableEntry basico."""
    print("[TEST 3] LocalVariableEntry")

    entry = LocalVariableEntry(
        start_pc=0,
        length=10,
        name_index=1,
        descriptor_index=2,
        index=0
    )
    bytecode = entry.to_bytes()

    # Verificar estructura
    assert len(bytecode) == 10, f"LocalVariableEntry debe ser 10 bytes, fue {len(bytecode)}"

    # Decodificar
    start_pc, length, name_idx, desc_idx, index = struct.unpack('>HHHHH', bytecode)
    assert start_pc == 0
    assert length == 10
    assert name_idx == 1
    assert desc_idx == 2
    assert index == 0

    print("  ✓ LocalVariableEntry estructura correcta")
    print(f"  ✓ Bytecode: {bytecode.hex()}")
    print()


def test_local_variable_table_attribute():
    """Test LocalVariableTable attribute."""
    print("[TEST 4] LocalVariableTable Attribute")

    cp = ConstantPool()
    name_index = cp.add_utf8("LocalVariableTable")

    # Indices para variables
    var_x_idx = cp.add_utf8("x")
    desc_int_idx = cp.add_utf8("I")
    var_y_idx = cp.add_utf8("y")
    desc_double_idx = cp.add_utf8("D")

    lvt = LocalVariableTableAttribute(name_index)
    lvt.add_entry(0, 15, var_x_idx, desc_int_idx, 0)
    lvt.add_entry(5, 10, var_y_idx, desc_double_idx, 1)

    bytecode = lvt.to_bytes()

    # Verificar estructura
    assert len(bytecode) > 6, "Debe tener header + datos"

    # Decodificar header
    attr_name_idx, attr_length = struct.unpack('>HI', bytecode[0:6])
    assert attr_name_idx == name_index
    assert attr_length > 0

    # Decodificar tabla
    table_length = struct.unpack('>H', bytecode[6:8])[0]
    assert table_length == 2, f"Debe tener 2 entries, tiene {table_length}"

    print("  ✓ LocalVariableTable creado correctamente")
    print(f"  ✓ Entries: {table_length}")
    print(f"  ✓ Tamaño: {len(bytecode)} bytes")
    print()


def test_create_line_number_table_helper():
    """Test helper create_line_number_table."""
    print("[TEST 5] create_line_number_table helper")

    cp = ConstantPool()
    pc_to_line = [(0, 1), (5, 2), (10, 3), (15, 4)]

    lnt = create_line_number_table(cp, pc_to_line)

    assert len(lnt.entries) == 4
    assert lnt.entries[0].start_pc == 0
    assert lnt.entries[0].line_number == 1
    assert lnt.entries[3].start_pc == 15
    assert lnt.entries[3].line_number == 4

    bytecode = lnt.to_bytes()
    assert len(bytecode) > 0

    print("  ✓ Helper create_line_number_table funciona")
    print(f"  ✓ Entries creados: {len(lnt.entries)}")
    print()


def test_create_local_variable_table_helper():
    """Test helper create_local_variable_table."""
    print("[TEST 6] create_local_variable_table helper")

    cp = ConstantPool()
    variables = [
        (0, 20, "x", "I", 0),
        (5, 15, "y", "D", 1),
        (10, 10, "z", "Ljava/lang/String;", 3)
    ]

    lvt = create_local_variable_table(cp, variables)

    assert len(lvt.entries) == 3
    assert lvt.entries[0].start_pc == 0
    assert lvt.entries[1].length == 15
    assert lvt.entries[2].index == 3

    bytecode = lvt.to_bytes()
    assert len(bytecode) > 0

    print("  ✓ Helper create_local_variable_table funciona")
    print(f"  ✓ Entries creados: {len(lvt.entries)}")
    print()


def test_code_attribute_with_line_numbers():
    """Test CodeAttribute con LineNumberTable."""
    print("[TEST 7] CodeAttribute con LineNumberTable")

    cp = ConstantPool()

    # Crear Code attribute
    code_name_idx = cp.add_utf8("Code")
    code_bytes = b'\x10\x05\x3c\xb1'  # bipush 5, istore_1, return

    code_attr = CodeAttribute(
        code_name_idx,
        max_stack=1,
        max_locals=2,
        code=code_bytes
    )

    # Agregar LineNumberTable
    lnt = create_line_number_table(cp, [(0, 1), (2, 2), (3, 3)])
    code_attr.add_sub_attribute(lnt)

    # Convertir a bytes
    bytecode = code_attr.to_bytes()

    assert len(bytecode) > 0
    assert len(code_attr.attributes) == 1

    print("  ✓ CodeAttribute con LineNumberTable generado")
    print(f"  ✓ Sub-attributes: {len(code_attr.attributes)}")
    print(f"  ✓ Tamaño total: {len(bytecode)} bytes")
    print()


def test_code_attribute_with_local_variables():
    """Test CodeAttribute con LocalVariableTable."""
    print("[TEST 8] CodeAttribute con LocalVariableTable")

    cp = ConstantPool()

    # Crear Code attribute
    code_name_idx = cp.add_utf8("Code")
    code_bytes = b'\x10\x0a\x3c\x10\x14\x3d\x1b\x1c\x60\x3e\xb1'

    code_attr = CodeAttribute(
        code_name_idx,
        max_stack=2,
        max_locals=4,
        code=code_bytes
    )

    # Agregar LocalVariableTable
    variables = [
        (0, 11, "x", "I", 1),
        (3, 8, "y", "I", 2),
        (7, 4, "sum", "I", 3)
    ]
    lvt = create_local_variable_table(cp, variables)
    code_attr.add_sub_attribute(lvt)

    # Convertir a bytes
    bytecode = code_attr.to_bytes()

    assert len(bytecode) > 0
    assert len(code_attr.attributes) == 1

    print("  ✓ CodeAttribute con LocalVariableTable generado")
    print(f"  ✓ Variables: {len(lvt.entries)}")
    print(f"  ✓ Tamaño total: {len(bytecode)} bytes")
    print()


def test_code_attribute_with_both_attributes():
    """Test CodeAttribute con LineNumberTable y LocalVariableTable."""
    print("[TEST 9] CodeAttribute con ambos attributes")

    cp = ConstantPool()

    # Crear Code attribute
    code_name_idx = cp.add_utf8("Code")
    code_bytes = b'\x10\x0a\x3c\x10\x14\x3d\x1b\x1c\x60\x3e\xb1'

    code_attr = CodeAttribute(
        code_name_idx,
        max_stack=2,
        max_locals=4,
        code=code_bytes
    )

    # Agregar LineNumberTable
    lnt = create_line_number_table(cp, [(0, 1), (3, 2), (7, 3), (10, 4)])
    code_attr.add_sub_attribute(lnt)

    # Agregar LocalVariableTable
    variables = [
        (0, 11, "x", "I", 1),
        (3, 8, "y", "I", 2),
        (7, 4, "sum", "I", 3)
    ]
    lvt = create_local_variable_table(cp, variables)
    code_attr.add_sub_attribute(lvt)

    # Convertir a bytes
    bytecode = code_attr.to_bytes()

    assert len(bytecode) > 0
    assert len(code_attr.attributes) == 2

    print("  ✓ CodeAttribute con ambos attributes generado")
    print(f"  ✓ Sub-attributes: {len(code_attr.attributes)}")
    print(f"  ✓ LineNumberTable entries: {len(lnt.entries)}")
    print(f"  ✓ LocalVariableTable entries: {len(lvt.entries)}")
    print(f"  ✓ Tamaño total: {len(bytecode)} bytes")
    print()


def test_full_class_with_debug_info():
    """Test clase completa con debugging info."""
    print("[TEST 10] Clase completa con debugging info")

    # Crear clase
    writer = ClassFileWriter("DebugExample", java_version=6)
    writer.add_source_file("DebugExample.kt")

    # Crear metodo con debugging info
    name_idx = writer.constant_pool.add_utf8("calculate")
    desc_idx = writer.constant_pool.add_utf8("()I")

    method = MethodInfo(
        AccessFlags.ACC_PUBLIC | AccessFlags.ACC_STATIC,
        name_idx,
        desc_idx
    )

    # Codigo: x = 10, y = 20, sum = x + y, return sum
    code_bytes = b'\x10\x0a\x3c\x10\x14\x3d\x1b\x1c\x60\x3e\x1d\xac'

    code_name_idx = writer.constant_pool.add_utf8("Code")
    code_attr = CodeAttribute(
        code_name_idx,
        max_stack=2,
        max_locals=4,
        code=code_bytes
    )

    # Agregar LineNumberTable
    lnt = create_line_number_table(writer.constant_pool, [
        (0, 2),   # x = 10
        (3, 3),   # y = 20
        (6, 4),   # sum = x + y
        (10, 5)   # return sum
    ])
    code_attr.add_sub_attribute(lnt)

    # Agregar LocalVariableTable
    variables = [
        (0, 12, "x", "I", 1),
        (3, 9, "y", "I", 2),
        (6, 6, "sum", "I", 3)
    ]
    lvt = create_local_variable_table(writer.constant_pool, variables)
    code_attr.add_sub_attribute(lvt)

    method.add_attribute(code_attr)
    writer.add_method(method)

    # Generar bytecode
    bytecode = writer.to_bytes()

    assert len(bytecode) > 0
    assert writer.get_class_info()['methods_count'] == 1

    # Verificar magic y version
    magic = struct.unpack('>I', bytecode[0:4])[0]
    assert magic == 0xCAFEBABE

    print("  ✓ Clase con debugging info generada")
    print(f"  ✓ Bytecode size: {len(bytecode)} bytes")
    print(f"  ✓ Methods: {writer.get_class_info()['methods_count']}")
    print(f"  ✓ Magic: 0x{magic:X}")
    print()


def run_all_tests():
    """Ejecuta todos los tests."""
    print("=" * 70)
    print("TESTS DE ATTRIBUTES AVANZADOS - KForge JVM v2.0 (Fase 10)")
    print("=" * 70)
    print()

    test_line_number_entry()
    test_line_number_table_attribute()
    test_local_variable_entry()
    test_local_variable_table_attribute()
    test_create_line_number_table_helper()
    test_create_local_variable_table_helper()
    test_code_attribute_with_line_numbers()
    test_code_attribute_with_local_variables()
    test_code_attribute_with_both_attributes()
    test_full_class_with_debug_info()

    print("=" * 70)
    print("TODOS LOS TESTS PASARON EXITOSAMENTE")
    print("=" * 70)


if __name__ == '__main__':
    run_all_tests()
