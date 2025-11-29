"""
Tests para el ClassFile Writer de JVM.
Verifica que se generen archivos .class válidos.
"""

import sys
import io
import struct
import os
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Fix encoding para Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from core.jvm.classfile import (
    ClassFileWriter,
    MethodInfo,
    CodeAttribute,
    SourceFileAttribute,
    AccessFlags,
    create_minimal_class,
    create_hello_world_class
)
from core.jvm.constant_pool import ConstantPool


def test_magic_and_version():
    """Test que magic number y version sean correctos."""
    print("[TEST 1] Magic number y version")

    writer = ClassFileWriter("TestClass")
    bytecode = writer.to_bytes()

    # Leer magic number (primeros 4 bytes)
    magic = struct.unpack('>I', bytecode[0:4])[0]
    assert magic == 0xCAFEBABE, f"Magic debería ser 0xCAFEBABE, fue 0x{magic:X}"

    # Leer version (bytes 4-8)
    minor, major = struct.unpack('>HH', bytecode[4:8])
    assert minor == 0, f"Minor version debería ser 0, fue {minor}"
    assert major == 50, f"Major version debería ser 50 (Java 6 - default), fue {major}"

    print("  ✓ Magic number: 0xCAFEBABE")
    print("  ✓ Version: 50.0 (Java 6 - default)")
    print()


def test_minimal_class_structure():
    """Test estructura de una clase mínima."""
    print("[TEST 2] Estructura de clase mínima")

    writer = create_minimal_class("MinimalClass", "MinimalClass.kt")
    bytecode = writer.to_bytes()

    # Verificar que se generó bytecode
    assert len(bytecode) > 0, "Bytecode no debería estar vacío"

    # Verificar access flags (offset 8 + constant_pool_size)
    # Por simplicidad, solo verificamos que el bytecode tenga tamaño razonable
    assert len(bytecode) > 50, f"Clase mínima debería tener al menos 50 bytes, tiene {len(bytecode)}"

    print(f"  ✓ Bytecode generado: {len(bytecode)} bytes")
    print(f"  ✓ Constant pool entries: {len(writer.constant_pool)}")
    print(f"  ✓ Access flags: 0x{writer.access_flags:04X}")
    print()


def test_constant_pool_integration():
    """Test integración con Constant Pool."""
    print("[TEST 3] Integración con Constant Pool")

    writer = ClassFileWriter("MyClass")

    # Verificar que se agregaron las clases necesarias
    assert len(writer.constant_pool) >= 4, "Debería tener al menos 4 entries"

    # Verificar this_class y super_class
    assert writer.this_class is not None, "this_class no debería ser None"
    assert writer.super_class is not None, "super_class no debería ser None"
    assert writer.this_class != writer.super_class, "this_class y super_class deben ser diferentes"

    print(f"  ✓ this_class index: {writer.this_class}")
    print(f"  ✓ super_class index: {writer.super_class}")
    print(f"  ✓ Constant pool count: {writer.constant_pool.get_count()}")
    print()


def test_source_file_attribute():
    """Test atributo SourceFile."""
    print("[TEST 4] Atributo SourceFile")

    writer = ClassFileWriter("TestClass")
    writer.add_source_file("TestClass.kt")

    assert len(writer.attributes) == 1, "Debería tener 1 atributo"
    assert isinstance(writer.attributes[0], SourceFileAttribute), "Debería ser SourceFileAttribute"

    bytecode = writer.to_bytes()
    assert len(bytecode) > 0, "Bytecode debería generarse correctamente"

    print("  ✓ SourceFile attribute agregado correctamente")
    print(f"  ✓ Total attributes: {len(writer.attributes)}")
    print()


def test_empty_method():
    """Test método vacío (solo return)."""
    print("[TEST 5] Método vacío")

    writer = ClassFileWriter("TestClass")

    # Crear método main vacío
    name_index = writer.constant_pool.add_utf8("main")
    descriptor_index = writer.constant_pool.add_utf8("([Ljava/lang/String;)V")

    method = MethodInfo(
        AccessFlags.ACC_PUBLIC | AccessFlags.ACC_STATIC,
        name_index,
        descriptor_index
    )

    # Agregar Code attribute con solo return
    code_name_index = writer.constant_pool.add_utf8("Code")
    code_bytes = b'\xb1'  # return

    code_attr = CodeAttribute(
        code_name_index,
        max_stack=0,
        max_locals=1,
        code=code_bytes
    )

    method.add_attribute(code_attr)
    writer.add_method(method)

    assert len(writer.methods) == 1, "Debería tener 1 método"
    assert len(method.attributes) == 1, "Método debería tener 1 atributo"

    bytecode = writer.to_bytes()
    assert len(bytecode) > 0, "Bytecode debería generarse correctamente"

    print("  ✓ Método main creado correctamente")
    print(f"  ✓ Code length: {len(code_bytes)} bytes")
    print(f"  ✓ Method attributes: {len(method.attributes)}")
    print()


def test_access_flags():
    """Test access flags."""
    print("[TEST 6] Access Flags")

    # Clase pública
    writer = ClassFileWriter("PublicClass")
    assert writer.access_flags & AccessFlags.ACC_PUBLIC, "Debería tener ACC_PUBLIC"
    assert writer.access_flags & AccessFlags.ACC_SUPER, "Debería tener ACC_SUPER"

    # Método public static
    flags = AccessFlags.ACC_PUBLIC | AccessFlags.ACC_STATIC
    assert flags & AccessFlags.ACC_PUBLIC, "Debería tener ACC_PUBLIC"
    assert flags & AccessFlags.ACC_STATIC, "Debería tener ACC_STATIC"
    assert not (flags & AccessFlags.ACC_PRIVATE), "NO debería tener ACC_PRIVATE"

    print("  ✓ ACC_PUBLIC flag funciona correctamente")
    print("  ✓ ACC_SUPER flag funciona correctamente")
    print("  ✓ ACC_STATIC flag funciona correctamente")
    print()


def test_hello_world_class():
    """Test clase completa Hello World."""
    print("[TEST 7] Clase Hello World completa")

    writer = create_hello_world_class()

    # Verificar estructura
    assert len(writer.methods) == 1, "Debería tener 1 método (main)"
    assert len(writer.attributes) == 1, "Debería tener 1 atributo (SourceFile)"

    # Generar bytecode
    bytecode = writer.to_bytes()
    assert len(bytecode) > 100, f"Hello World debería tener al menos 100 bytes, tiene {len(bytecode)}"

    # Obtener info
    info = writer.get_class_info()
    assert info['magic'] == '0xCAFEBABE'
    assert info['version'] == '50.0'
    assert info['class_name'] == 'HelloWorld'

    print("  ✓ Clase HelloWorld generada correctamente")
    print(f"  ✓ Bytecode size: {info['bytecode_size']} bytes")
    print(f"  ✓ Methods: {info['methods_count']}")
    print(f"  ✓ Constant pool entries: {info['constant_pool_entries']}")
    print()


def test_write_to_file():
    """Test escritura a archivo .class."""
    print("[TEST 8] Escritura a archivo")

    writer = create_minimal_class("MinimalClass", "MinimalClass.kt")

    # Crear directorio temporal si no existe
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    # Escribir archivo
    output_file = output_dir / "MinimalClass.class"
    writer.write_to_file(str(output_file))

    # Verificar que se creó
    assert output_file.exists(), "Archivo .class debería existir"

    # Verificar que tiene contenido
    file_size = output_file.stat().st_size
    assert file_size > 0, "Archivo .class no debería estar vacío"

    # Leer y verificar magic number
    with open(output_file, 'rb') as f:
        magic = struct.unpack('>I', f.read(4))[0]
        assert magic == 0xCAFEBABE, "Magic number incorrecto en archivo"

    print(f"  ✓ Archivo escrito: {output_file}")
    print(f"  ✓ Tamaño: {file_size} bytes")
    print(f"  ✓ Magic number verificado: 0x{magic:X}")
    print()

    # Limpiar
    output_file.unlink()
    if not any(output_dir.iterdir()):
        output_dir.rmdir()


def test_code_attribute_structure():
    """Test estructura del atributo Code."""
    print("[TEST 9] Estructura del atributo Code")

    writer = ClassFileWriter("TestClass")
    code_name_index = writer.constant_pool.add_utf8("Code")

    # Crear Code attribute
    code_bytes = b'\x10\x05\x3c\xb1'  # bipush 5; istore_1; return
    code_attr = CodeAttribute(
        code_name_index,
        max_stack=1,
        max_locals=2,
        code=code_bytes
    )

    # Verificar valores
    assert code_attr.max_stack == 1
    assert code_attr.max_locals == 2
    assert code_attr.code == code_bytes
    assert len(code_attr.exception_table) == 0
    assert len(code_attr.attributes) == 0

    # Generar bytes
    code_bytecode = code_attr.to_bytes()
    assert len(code_bytecode) > 0, "Code attribute debería generar bytes"

    print("  ✓ max_stack configurado correctamente")
    print("  ✓ max_locals configurado correctamente")
    print(f"  ✓ Code length: {len(code_bytes)} bytes")
    print(f"  ✓ Code attribute size: {len(code_bytecode)} bytes")
    print()


def test_class_info():
    """Test información del class file."""
    print("[TEST 10] Información del class file")

    writer = create_hello_world_class()
    info = writer.get_class_info()

    # Verificar campos
    assert 'magic' in info
    assert 'version' in info
    assert 'class_name' in info
    assert 'constant_pool_count' in info
    assert 'methods_count' in info
    assert 'bytecode_size' in info

    # Verificar valores
    assert info['magic'] == '0xCAFEBABE'
    assert info['version'] == '50.0'
    assert info['class_name'] == 'HelloWorld'
    assert info['methods_count'] == 1
    assert info['bytecode_size'] > 0

    print("  ✓ Información del class file:")
    for key, value in info.items():
        print(f"    - {key}: {value}")
    print()


def test_java_version_configuration():
    """Test configuración de versiones de Java."""
    print("[TEST 11] Configuración de versiones de Java")

    # Java 6 (default)
    writer6 = ClassFileWriter("TestClass", java_version=6)
    assert writer6.major_version == 50
    assert writer6.requires_stack_maps == False
    bytecode6 = writer6.to_bytes()
    _, major6 = struct.unpack('>HH', bytecode6[4:8])
    assert major6 == 50
    print("  ✓ Java 6 (version 50.0) - Sin Stack Map Frames")

    # Java 7
    writer7 = ClassFileWriter("TestClass", java_version=7)
    assert writer7.major_version == 51
    assert writer7.requires_stack_maps == True
    bytecode7 = writer7.to_bytes()
    _, major7 = struct.unpack('>HH', bytecode7[4:8])
    assert major7 == 51
    print("  ✓ Java 7 (version 51.0) - Requiere Stack Map Frames")

    # Java 8
    writer8 = ClassFileWriter("TestClass", java_version=8)
    assert writer8.major_version == 52
    assert writer8.requires_stack_maps == True
    bytecode8 = writer8.to_bytes()
    _, major8 = struct.unpack('>HH', bytecode8[4:8])
    assert major8 == 52
    print("  ✓ Java 8 (version 52.0) - Requiere Stack Map Frames")

    # Invalid version (should default to Java 6)
    writer_invalid = ClassFileWriter("TestClass", java_version=99)
    assert writer_invalid.major_version == 50
    print("  ✓ Versión inválida usa default (Java 6)")

    print()


def run_all_tests():
    """Ejecuta todos los tests."""
    print("=" * 70)
    print("TESTS DE CLASSFILE WRITER - KForge JVM v2.0")
    print("=" * 70)
    print()

    test_magic_and_version()
    test_minimal_class_structure()
    test_constant_pool_integration()
    test_source_file_attribute()
    test_empty_method()
    test_access_flags()
    test_hello_world_class()
    test_write_to_file()
    test_code_attribute_structure()
    test_class_info()
    test_java_version_configuration()

    print("=" * 70)
    print("TODOS LOS TESTS PASARON EXITOSAMENTE")
    print("=" * 70)


if __name__ == '__main__':
    run_all_tests()
