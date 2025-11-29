"""
Script para ejecutar todos los tests JVM en el venv.
"""

import subprocess
import sys
import io

# Fix encoding para Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def run_test(test_path):
    """Ejecuta un test y retorna True si pasa."""
    try:
        result = subprocess.run(
            [sys.executable, test_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error ejecutando {test_path}: {e}")
        return False

def main():
    print("=" * 70)
    print("EJECUTANDO TODOS LOS TESTS JVM - KForge v2.0")
    print("=" * 70)
    print()

    tests = [
        'tests/jvm/test_constant_pool.py',
        'tests/jvm/test_classfile.py',
        'tests/jvm/test_instructions.py',
        'tests/jvm/test_jvm_generator.py',
        'tests/jvm/test_jvm_validation.py'
    ]

    results = []

    for test in tests:
        test_name = test.split('/')[-1]
        print(f"Ejecutando {test_name}...", end=' ')
        passed = run_test(test)
        results.append((test_name, passed))
        print("PASS" if passed else "FAIL")

    print()
    print("=" * 70)
    print("RESUMEN DE TESTS")
    print("=" * 70)

    for test_name, passed in results:
        status = "✓" if passed else "✗"
        print(f"{status} {test_name}")

    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)

    print()
    print(f"Total: {total_passed}/{total_tests} tests pasaron")
    print("=" * 70)

    return 0 if total_passed == total_tests else 1

if __name__ == '__main__':
    sys.exit(main())
