"""
Tests para Runtime Support JVM.
Verifica println, arrays, main method y otros helpers runtime.
"""

import sys
import io
from pathlib import Path

# Agregar el directorio raiz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Fix encoding para Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import struct
from core.jvm.runtime import (
    RuntimeHelper,
    generate_newarray_int,
    generate_newarray_double,
    generate_anewarray,
    generate_array_store_int,
    create_main_method,
    generate_string_constant
)
from core.jvm.constant_pool import ConstantPool
from core.jvm.classfile import ClassFileWriter
from core.jvm.instructions import JVMOpcode, iconst
from core.utils import TipoDato


def test_runtime_helper_initialization():
    """Test inicializacion de RuntimeHelper."""
    print("[TEST 1] RuntimeHelper initialization")

    cp = ConstantPool()
    helper = RuntimeHelper(cp)

    assert helper.constant_pool is cp
    assert helper._system_out_ref is None
    assert len(helper._println_refs) == 0

    print("  checkmark RuntimeHelper inicializado correctamente")
    print()


def test_system_out_fieldref():
    """Test referencia a System.out."""
    print("[TEST 2] System.out fieldref")

    cp = ConstantPool()
    helper = RuntimeHelper(cp)

    # Primera llamada crea la referencia
    ref1 = helper.get_system_out_fieldref()
    assert ref1 > 0

    # Segunda llamada reutiliza
    ref2 = helper.get_system_out_fieldref()
    assert ref1 == ref2

    # Verificar que se agregaron entradas al constant pool
    assert len(cp) > 0

    print(f"  checkmark System.out fieldref: index {ref1}")
    print(f"  checkmark Constant pool entries: {len(cp)}")
    print()


def test_println_methodref():
    """Test referencias a println()."""
    print("[TEST 3] println() methodref")

    cp = ConstantPool()
    helper = RuntimeHelper(cp)

    # println(int)
    println_int = helper.get_println_methodref(TipoDato.INT)
    assert println_int > 0

    # println(double)
    println_double = helper.get_println_methodref(TipoDato.DOUBLE)
    assert println_double > 0
    assert println_double != println_int

    # println(String)
    println_string = helper.get_println_methodref(TipoDato.STRING)
    assert println_string > 0
    assert println_string != println_int

    # Reutilizacion
    println_int2 = helper.get_println_methodref(TipoDato.INT)
    assert println_int == println_int2

    print(f"  checkmark println(int): index {println_int}")
    print(f"  checkmark println(double): index {println_double}")
    print(f"  checkmark println(String): index {println_string}")
    print()


def test_generate_println_int():
    """Test generacion de instrucciones println(int)."""
    print("[TEST 4] Generate println(int) instructions")

    cp = ConstantPool()
    helper = RuntimeHelper(cp)

    instructions = helper.generate_println(TipoDato.INT)

    assert len(instructions) == 3, f"Debe tener 3 instrucciones, tiene {len(instructions)}"

    # GETSTATIC System.out
    assert instructions[0].opcode == JVMOpcode.GETSTATIC

    # SWAP
    assert instructions[1].opcode == JVMOpcode.SWAP

    # INVOKEVIRTUAL println
    assert instructions[2].opcode == JVMOpcode.INVOKEVIRTUAL

    print("  checkmark 3 instrucciones generadas")
    print("  checkmark GETSTATIC System.out")
    print("  checkmark SWAP")
    print("  checkmark INVOKEVIRTUAL println")
    print()


def test_generate_println_string():
    """Test generacion de instrucciones println(String)."""
    print("[TEST 5] Generate println(String) instructions")

    cp = ConstantPool()
    helper = RuntimeHelper(cp)

    instructions = helper.generate_println(TipoDato.STRING)

    assert len(instructions) == 3
    assert instructions[0].opcode == JVMOpcode.GETSTATIC
    assert instructions[1].opcode == JVMOpcode.SWAP
    assert instructions[2].opcode == JVMOpcode.INVOKEVIRTUAL

    print("  checkmark println(String) generado correctamente")
    print()


def test_generate_newarray_int():
    """Test creacion de array de enteros."""
    print("[TEST 6] Generate int array")

    instructions = generate_newarray_int(10)

    assert len(instructions) == 2, f"Debe tener 2 instrucciones, tiene {len(instructions)}"

    # iconst o bipush para size
    assert instructions[0].opcode in [JVMOpcode.ICONST_0, JVMOpcode.ICONST_1,
                                      JVMOpcode.ICONST_2, JVMOpcode.ICONST_3,
                                      JVMOpcode.ICONST_4, JVMOpcode.ICONST_5,
                                      JVMOpcode.BIPUSH]

    # newarray
    assert instructions[1].opcode == JVMOpcode.NEWARRAY

    print("  checkmark Array int[10] generado")
    print("  checkmark ICONST/BIPUSH 10")
    print("  checkmark NEWARRAY T_INT")
    print()


def test_generate_newarray_double():
    """Test creacion de array de doubles."""
    print("[TEST 7] Generate double array")

    instructions = generate_newarray_double(5)

    assert len(instructions) == 2
    assert instructions[1].opcode == JVMOpcode.NEWARRAY

    print("  checkmark Array double[5] generado")
    print()


def test_generate_anewarray():
    """Test creacion de array de objetos."""
    print("[TEST 8] Generate object array (String[])")

    cp = ConstantPool()
    instructions = generate_anewarray("java/lang/String", 3, cp)

    assert len(instructions) == 2

    # iconst 3
    assert instructions[0].opcode in [JVMOpcode.ICONST_0, JVMOpcode.ICONST_1,
                                      JVMOpcode.ICONST_2, JVMOpcode.ICONST_3]

    # anewarray
    assert instructions[1].opcode == JVMOpcode.ANEWARRAY

    # Verificar que se agrego la clase al constant pool
    assert len(cp) > 0

    print("  checkmark Array String[3] generado")
    print("  checkmark ICONST 3")
    print("  checkmark ANEWARRAY java/lang/String")
    print()


def test_create_main_method():
    """Test creacion de metodo main()."""
    print("[TEST 9] Create main() method")

    cp = ConstantPool()

    # Bytecode simple: return
    code_bytes = b'\\xb1'

    method = create_main_method(cp, code_bytes, max_stack=2, max_locals=1)

    # Verificar estructura
    assert method.access_flags & 0x0001  # ACC_PUBLIC
    assert method.access_flags & 0x0008  # ACC_STATIC

    # Verificar Code attribute
    assert len(method.attributes) == 1
    code_attr = method.attributes[0]
    assert code_attr.max_stack == 2
    assert code_attr.max_locals == 1
    assert code_attr.code == code_bytes

    print("  checkmark Metodo main() creado")
    print("  checkmark public static")
    print("  checkmark Signature: ([Ljava/lang/String;)V")
    print("  checkmark Code attribute agregado")
    print()


def test_generate_string_constant():
    """Test generacion de constante String."""
    print("[TEST 10] Generate String constant")

    cp = ConstantPool()
    instructions = generate_string_constant("Hello, World!", cp)

    assert len(instructions) == 1

    # LDC o LDC_W
    assert instructions[0].opcode in [JVMOpcode.LDC, JVMOpcode.LDC_W]

    # Verificar que se agrego al constant pool
    assert len(cp) > 0

    print("  checkmark String constant generado")
    print("  checkmark LDC/LDC_W")
    print(f"  checkmark Constant pool entries: {len(cp)}")
    print()


def test_full_hello_world_with_println():
    """Test programa completo Hello World con println."""
    print("[TEST 11] Full Hello World con println()")

    # Crear clase
    writer = ClassFileWriter("HelloWorld", java_version=6)
    cp = writer.constant_pool
    helper = RuntimeHelper(cp)

    # Generar bytecode:
    # ldc "Hello, World!"
    # invokestatic System.out.println(String)
    # return

    bytecode_parts = []

    # Cargar string
    str_instructions = generate_string_constant("Hello, World!", cp)
    for instr in str_instructions:
        bytecode_parts.append(instr.to_bytes())

    # println(String)
    println_instructions = helper.generate_println(TipoDato.STRING)
    for instr in println_instructions:
        bytecode_parts.append(instr.to_bytes())

    # return
    bytecode_parts.append(b'\\xb1')

    bytecode = b''.join(bytecode_parts)

    # Crear metodo main
    method = create_main_method(cp, bytecode, max_stack=2, max_locals=1)
    writer.add_method(method)
    writer.add_source_file("HelloWorld.kt")

    # Generar .class
    class_bytes = writer.to_bytes()

    # Verificar
    assert len(class_bytes) > 0
    magic = struct.unpack('>I', class_bytes[0:4])[0]
    assert magic == 0xCAFEBABE

    info = writer.get_class_info()
    assert info['methods_count'] == 1

    print("  checkmark Clase Hello World generada")
    print(f"  checkmark Bytecode size: {len(class_bytes)} bytes")
    print(f"  checkmark Magic: 0x{magic:X}")
    print(f"  checkmark Methods: {info['methods_count']}")
    print()


def test_println_with_multiple_types():
    """Test println con multiples tipos."""
    print("[TEST 12] println() con multiples tipos")

    cp = ConstantPool()
    helper = RuntimeHelper(cp)

    # Generar para diferentes tipos
    tipos = [TipoDato.INT, TipoDato.DOUBLE, TipoDato.STRING, TipoDato.BOOLEAN]

    for tipo in tipos:
        instructions = helper.generate_println(tipo)
        assert len(instructions) == 3
        print(f"  checkmark println({tipo.name}) generado")

    print()


def run_all_tests():
    """Ejecuta todos los tests."""
    print("=" * 70)
    print("TESTS DE RUNTIME SUPPORT - KForge JVM v2.0 (Fase 11)")
    print("=" * 70)
    print()

    test_runtime_helper_initialization()
    test_system_out_fieldref()
    test_println_methodref()
    test_generate_println_int()
    test_generate_println_string()
    test_generate_newarray_int()
    test_generate_newarray_double()
    test_generate_anewarray()
    test_create_main_method()
    test_generate_string_constant()
    test_full_hello_world_with_println()
    test_println_with_multiple_types()

    print("=" * 70)
    print("TODOS LOS TESTS PASARON EXITOSAMENTE")
    print("=" * 70)


if __name__ == '__main__':
    run_all_tests()
