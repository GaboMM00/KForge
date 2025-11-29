"""
Tests para el Constant Pool de JVM.
Verifica que las constantes se agreguen correctamente y generen bytecode válido.
"""

import sys
import io
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Fix encoding para Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from core.jvm.constant_pool import (
    ConstantPool,
    Utf8Constant,
    IntegerConstant,
    ClassConstant,
    MethodrefConstant,
    NameAndTypeConstant
)


def test_utf8_constant():
    """Test CONSTANT_Utf8."""
    print("[TEST 1] CONSTANT_Utf8")

    cp = ConstantPool()

    # Agregar UTF-8
    index1 = cp.add_utf8("Hello")
    index2 = cp.add_utf8("World")
    index3 = cp.add_utf8("Hello")  # Duplicado

    assert index1 == 1, f"Primer índice debería ser 1, fue {index1}"
    assert index2 == 2, f"Segundo índice debería ser 2, fue {index2}"
    assert index3 == 1, f"Duplicado debería retornar índice 1, fue {index3}"
    assert len(cp) == 2, f"Debería haber 2 entries, hay {len(cp)}"

    print("  ✓ UTF-8 constants funcionan correctamente")
    print(f"  ✓ Cache evita duplicados correctamente")
    print()


def test_integer_constant():
    """Test CONSTANT_Integer."""
    print("[TEST 2] CONSTANT_Integer")

    cp = ConstantPool()

    index1 = cp.add_integer(42)
    index2 = cp.add_integer(100)
    index3 = cp.add_integer(42)  # Duplicado

    assert index1 == 1
    assert index2 == 2
    assert index3 == 1  # Mismo índice
    assert len(cp) == 2

    print("  ✓ Integer constants funcionan correctamente")
    print()


def test_long_double_two_slots():
    """Test que Long y Double ocupen 2 slots."""
    print("[TEST 3] Long y Double ocupan 2 slots")

    cp = ConstantPool()

    # Agregar Long
    long_index = cp.add_long(9223372036854775807)
    assert long_index == 1
    assert len(cp) == 2, f"Long debería ocupar 2 slots, tiene {len(cp)}"
    assert cp.entries[1] is None, "Segundo slot de Long debería ser None"

    # Agregar Double
    double_index = cp.add_double(3.14159)
    assert double_index == 3  # Salta el slot vacío
    assert len(cp) == 4, f"Long + Double deberían ocupar 4 slots, tiene {len(cp)}"
    assert cp.entries[3] is None, "Segundo slot de Double debería ser None"

    print("  ✓ Long ocupa 2 slots correctamente")
    print("  ✓ Double ocupa 2 slots correctamente")
    print()


def test_class_constant():
    """Test CONSTANT_Class."""
    print("[TEST 4] CONSTANT_Class")

    cp = ConstantPool()

    # Agregar clase (automáticamente agrega UTF-8)
    class_index = cp.add_class("java/lang/Object")

    assert class_index == 2, f"Class debería estar en índice 2, está en {class_index}"
    assert len(cp) == 2, "Debería tener 2 entries (UTF-8 + Class)"

    # Verificar que UTF-8 se agregó automáticamente
    entry0 = cp.entries[0]
    entry1 = cp.entries[1]

    assert isinstance(entry0, Utf8Constant), "Primera entry debería ser UTF-8"
    assert isinstance(entry1, ClassConstant), "Segunda entry debería ser Class"
    assert entry0.text == "java/lang/Object"

    print("  ✓ CONSTANT_Class funciona correctamente")
    print("  ✓ UTF-8 se agrega automáticamente")
    print()


def test_methodref_constant():
    """Test CONSTANT_Methodref con todas sus dependencias."""
    print("[TEST 5] CONSTANT_Methodref completo")

    cp = ConstantPool()

    # Agregar Methodref (automáticamente agrega todas las constantes necesarias)
    methodref_index = cp.add_methodref(
        "java/io/PrintStream",
        "println",
        "(I)V"
    )

    # Verificar que se agregaron todas las constantes necesarias:
    # 1. UTF-8 "java/io/PrintStream"
    # 2. Class java/io/PrintStream
    # 3. UTF-8 "println"
    # 4. UTF-8 "(I)V"
    # 5. NameAndType println:(I)V
    # 6. Methodref #2.#5

    assert len(cp) >= 6, f"Debería tener al menos 6 entries, tiene {len(cp)}"

    # Verificar tipos de entries
    assert isinstance(cp.entries[0], Utf8Constant)  # "java/io/PrintStream"
    assert isinstance(cp.entries[1], ClassConstant)  # Class
    assert isinstance(cp.entries[2], Utf8Constant)  # "println"
    assert isinstance(cp.entries[3], Utf8Constant)  # "(I)V"
    assert isinstance(cp.entries[4], NameAndTypeConstant)  # NameAndType
    assert isinstance(cp.entries[5], MethodrefConstant)  # Methodref

    print("  ✓ CONSTANT_Methodref funciona correctamente")
    print("  ✓ Todas las dependencias se agregaron automáticamente")
    print(f"  ✓ Total de entries: {len(cp)}")
    print()


def test_constant_pool_count():
    """Test que constant_pool_count se calcule correctamente."""
    print("[TEST 6] constant_pool_count")

    cp = ConstantPool()

    # Pool vacío
    assert cp.get_count() == 1, "Pool vacío debería tener count=1"

    # Agregar 3 entries
    cp.add_utf8("Hello")
    cp.add_utf8("World")
    cp.add_integer(42)

    # count = entries + 1
    assert cp.get_count() == 4, f"Con 3 entries, count debería ser 4, es {cp.get_count()}"
    assert len(cp) == 3, "Debería tener 3 entries"

    print("  ✓ constant_pool_count se calcula correctamente")
    print()


def test_to_bytes():
    """Test conversión a bytes."""
    print("[TEST 7] Conversión a bytes")

    cp = ConstantPool()

    # Agregar algunas constantes
    cp.add_utf8("Test")
    cp.add_integer(123)
    cp.add_class("MyClass")

    # Generar bytes
    bytecode = cp.to_bytes()

    assert isinstance(bytecode, bytes), "to_bytes() debería retornar bytes"
    assert len(bytecode) > 0, "Bytecode no debería estar vacío"

    # Los primeros 2 bytes deberían ser el constant_pool_count
    count_bytes = bytecode[:2]
    import struct
    count = struct.unpack('>H', count_bytes)[0]
    assert count == cp.get_count(), f"Count en bytes debería ser {cp.get_count()}, es {count}"

    print("  ✓ Conversión a bytes funciona correctamente")
    print(f"  ✓ Bytecode generado: {len(bytecode)} bytes")
    print()


def test_complex_constant_pool():
    """Test con un Constant Pool más complejo (similar a un .class real)."""
    print("[TEST 8] Constant Pool complejo")

    cp = ConstantPool()

    # Simular constant pool de un programa simple:
    # class MyClass extends java/lang/Object {
    #   public static void main(String[] args) {
    #     System.out.println(42);
    #   }
    # }

    # Clases
    cp.add_class("MyClass")
    cp.add_class("java/lang/Object")

    # main method
    cp.add_methodref("MyClass", "main", "([Ljava/lang/String;)V")

    # println
    cp.add_fieldref("java/lang/System", "out", "Ljava/io/PrintStream;")
    cp.add_methodref("java/io/PrintStream", "println", "(I)V")

    # Strings comunes
    cp.add_utf8("Code")
    cp.add_utf8("LineNumberTable")
    cp.add_utf8("SourceFile")
    cp.add_utf8("MyClass.kt")

    print(f"  ✓ Constant Pool complejo creado")
    print(f"  ✓ Total entries: {len(cp)}")
    print(f"  ✓ Constant pool count: {cp.get_count()}")

    # Verificar que se puede convertir a bytes sin errores
    bytecode = cp.to_bytes()
    print(f"  ✓ Bytecode generado: {len(bytecode)} bytes")
    print()


def run_all_tests():
    """Ejecuta todos los tests."""
    print("=" * 70)
    print("TESTS DE CONSTANT POOL - KForge JVM v2.0")
    print("=" * 70)
    print()

    test_utf8_constant()
    test_integer_constant()
    test_long_double_two_slots()
    test_class_constant()
    test_methodref_constant()
    test_constant_pool_count()
    test_to_bytes()
    test_complex_constant_pool()

    print("=" * 70)
    print("TODOS LOS TESTS PASARON EXITOSAMENTE")
    print("=" * 70)


if __name__ == '__main__':
    run_all_tests()
