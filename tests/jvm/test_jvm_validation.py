"""
Tests de validación JVM - Verificación con javap

Estos tests generan archivos .class reales y los verifican usando javap
(si está disponible en el sistema).

javap es una herramienta que viene con el JDK y permite desensamblar
archivos .class para verificar su estructura.
"""

import sys
import io
import subprocess
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Fix encoding para Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from core.jvm.classfile import (
    create_minimal_class,
    create_hello_world_class
)


def is_javap_available() -> bool:
    """Verifica si javap está disponible en el sistema."""
    try:
        result = subprocess.run(
            ['javap', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def run_javap(class_file: Path) -> tuple[bool, str]:
    """
    Ejecuta javap en un archivo .class.

    Returns:
        (success, output): Tupla con éxito y salida de javap
    """
    try:
        result = subprocess.run(
            ['javap', '-v', '-p', str(class_file)],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0, result.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return False, str(e)


def test_minimal_class_with_javap():
    """Test clase mínima con javap."""
    print("[TEST 1] Validación de clase mínima con javap")

    # Crear directorio de salida
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    # Generar clase mínima
    writer = create_minimal_class("MinimalTest", "MinimalTest.kt")
    output_file = output_dir / "MinimalTest.class"
    writer.write_to_file(str(output_file))

    print(f"  ✓ Archivo generado: {output_file}")
    print(f"  ✓ Tamaño: {output_file.stat().st_size} bytes")

    # Verificar con javap si está disponible
    if is_javap_available():
        print("  ✓ javap detectado, verificando...")
        success, output = run_javap(output_file)

        if success:
            print("  ✓ javap validó el archivo exitosamente")
            print("\n  Salida de javap:")
            print("  " + "-" * 66)
            for line in output.split('\n')[:20]:  # Primeras 20 líneas
                print(f"  {line}")
            if len(output.split('\n')) > 20:
                print("  ...")
            print("  " + "-" * 66)
        else:
            print(f"  ✗ javap falló: {output}")
            return False
    else:
        print("  ℹ javap no disponible, saltando validación")

    # Limpiar
    output_file.unlink()

    print()
    return True


def test_hello_world_with_javap():
    """Test Hello World con javap."""
    print("[TEST 2] Validación de HelloWorld con javap")

    # Crear directorio de salida
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    # Generar Hello World
    writer = create_hello_world_class()
    output_file = output_dir / "HelloWorld.class"
    writer.write_to_file(str(output_file))

    print(f"  ✓ Archivo generado: {output_file}")
    print(f"  ✓ Tamaño: {output_file.stat().st_size} bytes")

    # Verificar con javap si está disponible
    if is_javap_available():
        print("  ✓ javap detectado, verificando...")
        success, output = run_javap(output_file)

        if success:
            print("  ✓ javap validó el archivo exitosamente")

            # Verificar que contenga el método main
            if 'public static void main(java.lang.String[])' in output:
                print("  ✓ Método main detectado correctamente")
            else:
                print("  ✗ Método main no encontrado en la salida")

            # Verificar SourceFile
            if 'SourceFile: "HelloWorld.kt"' in output:
                print("  ✓ Atributo SourceFile detectado correctamente")

            print("\n  Salida de javap:")
            print("  " + "-" * 66)
            for line in output.split('\n')[:30]:  # Primeras 30 líneas
                print(f"  {line}")
            if len(output.split('\n')) > 30:
                print("  ...")
            print("  " + "-" * 66)
        else:
            print(f"  ✗ javap falló: {output}")
            return False
    else:
        print("  ℹ javap no disponible, saltando validación")

    # Limpiar
    output_file.unlink()

    print()
    return True


def test_bytecode_structure():
    """Test estructura del bytecode generado."""
    print("[TEST 3] Verificación de estructura del bytecode")

    writer = create_hello_world_class()
    bytecode = writer.to_bytes()

    # Verificar magic number
    magic = int.from_bytes(bytecode[0:4], 'big')
    assert magic == 0xCAFEBABE, f"Magic incorrecto: 0x{magic:X}"
    print("  ✓ Magic number: 0xCAFEBABE")

    # Verificar version
    minor = int.from_bytes(bytecode[4:6], 'big')
    major = int.from_bytes(bytecode[6:8], 'big')
    assert minor == 0 and major == 52, f"Version incorrecta: {major}.{minor}"
    print(f"  ✓ Version: {major}.{minor} (Java 8)")

    # Verificar constant pool count
    cp_count = int.from_bytes(bytecode[8:10], 'big')
    assert cp_count > 0, "Constant pool count debe ser > 0"
    print(f"  ✓ Constant pool count: {cp_count}")

    print(f"  ✓ Tamaño total del bytecode: {len(bytecode)} bytes")
    print()


def test_class_file_info():
    """Test información detallada del class file."""
    print("[TEST 4] Información detallada del class file")

    writer = create_hello_world_class()
    info = writer.get_class_info()

    print("  Información del class file:")
    print(f"    • Nombre: {info['class_name']}")
    print(f"    • Magic: {info['magic']}")
    print(f"    • Version: {info['version']}")
    print(f"    • Access flags: {info['access_flags']}")
    print(f"    • Constant pool count: {info['constant_pool_count']}")
    print(f"    • Constant pool entries: {info['constant_pool_entries']}")
    print(f"    • Methods count: {info['methods_count']}")
    print(f"    • Attributes count: {info['attributes_count']}")
    print(f"    • Bytecode size: {info['bytecode_size']} bytes")

    # Verificaciones
    assert info['magic'] == '0xCAFEBABE'
    assert info['version'] == '52.0'
    assert info['methods_count'] >= 1
    assert info['bytecode_size'] > 100

    print("  ✓ Toda la información es válida")
    print()


def run_all_tests():
    """Ejecuta todos los tests de validación."""
    print("=" * 70)
    print("TESTS DE VALIDACIÓN JVM - KForge v2.0")
    print("=" * 70)
    print()

    # Info sobre javap
    if is_javap_available():
        print("✓ javap está disponible - se ejecutarán validaciones completas")
    else:
        print("ℹ javap no está disponible - se ejecutarán validaciones básicas")
        print("  Para validación completa, instalar JDK y agregar javap al PATH")
    print()

    all_passed = True

    if not test_minimal_class_with_javap():
        all_passed = False

    if not test_hello_world_with_javap():
        all_passed = False

    test_bytecode_structure()
    test_class_file_info()

    # Limpiar directorio output si está vacío
    output_dir = Path(__file__).parent / "output"
    if output_dir.exists() and not any(output_dir.iterdir()):
        output_dir.rmdir()

    print("=" * 70)
    if all_passed:
        print("TODOS LOS TESTS PASARON EXITOSAMENTE")
    else:
        print("ALGUNOS TESTS FALLARON")
    print("=" * 70)


if __name__ == '__main__':
    run_all_tests()
