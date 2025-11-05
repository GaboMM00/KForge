# Test Scripts and Data (`tests/`)

Esta carpeta contiene **scripts de prueba Python** y **archivos de datos de prueba** para el compilador KForge.

## 📁 Propósito

Los archivos en esta carpeta son:
1. **Scripts Python** (`test_*.py`) que ejecutan el compilador y verifican resultados
2. **Archivos de texto** (`*.txt`) con código Kotlin para pruebas generales

## 📝 Archivos Actuales

### Scripts de Test Python

#### `test_fase1_directo.py`
Script Python que prueba todas las características de la **Fase 1**.

**Uso**:
```bash
# Desde la raíz del proyecto
python tests/test_fase1_directo.py
```

**Qué hace**:
- Ejecuta el análisis léxico, sintáctico y semántico
- Verifica que no haya errores en ninguna fase
- Muestra un reporte detallado con checkmarks ✓
- Imprime la tabla de símbolos generada

**Salida esperada**:
```
============================================================
ANÁLISIS LÉXICO
============================================================
✓ Sin errores léxicos

============================================================
ANÁLISIS SINTÁCTICO
============================================================
✓ Sin errores sintácticos

============================================================
ANÁLISIS SEMÁNTICO
============================================================
✓ Sin errores semánticos

Total de errores: 0
✓ ¡FASE 1 IMPLEMENTADA CORRECTAMENTE!
```

#### `test_compilador.py`
Script general de prueba del compilador.

**Uso**:
```bash
# Prueba básica predefinida
python tests/test_compilador.py

# Compilar un archivo específico
python tests/test_compilador.py test_kt/test_fase1.kt
python tests/test_compilador.py tests/ejemplo_kotlin.txt

# Ver ayuda
python tests/test_compilador.py --help
```

### Archivos de Datos de Prueba

#### `ejemplo_kotlin.txt`
Código Kotlin de ejemplo para pruebas generales.

#### `prueba_simple.txt`
Prueba simple del compilador.

#### `prueba_errores.txt`
Casos de prueba que deben generar errores (para probar el manejo de errores).

## ➕ Crear Nuevos Scripts de Test

### Para una Nueva Fase

Cuando implementes Fase 2, crea `test_fase2_directo.py`:

```python
"""
Script de prueba directo para la Fase 2
"""
import sys
import io
from pathlib import Path

# Agregar el directorio raíz al path para poder importar 'core'
sys.path.insert(0, str(Path(__file__).parent.parent))

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from core.lexer import Lexer
from core.parser import Parser
from core.semantic import AnalizadorSemantico
from core.errors import ErrorManager

# Código de prueba para Fase 2
codigo = """
// Test de funciones
fun suma(a: Int, b: Int): Int {
    return a + b
}

val resultado = suma(5, 10)
println(resultado)
"""

# Crear gestor de errores
error_manager = ErrorManager()

# Análisis léxico
print("=" * 60)
print("ANÁLISIS LÉXICO")
print("=" * 60)
lexer = Lexer(error_manager)
tokens = lexer.tokenizar(codigo)
print(f"Tokens generados: {len(tokens)}")

if error_manager.tiene_errores():
    print("\\nERRORES LÉXICOS:")
    for error in error_manager.errores:
        print(f"  - {error}")
else:
    print("✓ Sin errores léxicos")

# Análisis sintáctico
print("\\n" + "=" * 60)
print("ANÁLISIS SINTÁCTICO")
print("=" * 60)
parser = Parser(tokens, error_manager)
ast = parser.parsear()

if error_manager.tiene_errores():
    print("\\nERRORES SINTÁCTICOS:")
    for error in error_manager.errores:
        if "Sintáctico" in str(error):
            print(f"  - {error}")
else:
    print("✓ Sin errores sintácticos")

if ast:
    print("\\nAST generado correctamente")
    print(f"Tipo de nodo raíz: {ast.tipo.name}")

# Análisis semántico
print("\\n" + "=" * 60)
print("ANÁLISIS SEMÁNTICO")
print("=" * 60)
analizador_semantico = AnalizadorSemantico(error_manager)
resultados = analizador_semantico.analizar(ast)

if error_manager.tiene_errores():
    print("\\nERRORES SEMÁNTICOS:")
    for error in error_manager.errores:
        if "Semántico" in str(error):
            print(f"  - {error}")
else:
    print("✓ Sin errores semánticos")

# Resumen final
print("\\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)
print(f"Total de errores: {len(error_manager.errores)}")
if not error_manager.tiene_errores():
    print("✓ ¡FASE 2 IMPLEMENTADA CORRECTAMENTE!")
    print("\\nCaracterísticas probadas:")
    print("  ✓ Declaración de funciones")
    print("  ✓ Llamadas a funciones")
    print("  ✓ Funciones built-in")
else:
    print("✗ Hay errores que corregir")
```

## 🔧 Nota Importante sobre Imports

**TODOS los scripts en esta carpeta deben incluir** estas líneas al inicio:

```python
import sys
from pathlib import Path

# Agregar el directorio raíz al path para poder importar 'core'
sys.path.insert(0, str(Path(__file__).parent.parent))
```

Esto permite importar el módulo `core` desde cualquier subcarpeta.

## ✅ Convenciones

1. **Nombres de scripts**: `test_faseN_directo.py` para tests de fase específica
2. **Encoding UTF-8**: Siempre incluir `sys.stdout = io.TextIOWrapper(...)` para Windows
3. **Reportes claros**: Usar checkmarks ✓ y símbolos ✗ para mostrar resultados
4. **Separadores visuales**: Usar `"=" * 60` para separar secciones

## 🚀 Flujo de Testing

1. Implementar característica nueva
2. Agregar código de prueba a `test_kt/test_faseN.kt`
3. Actualizar o crear `tests/test_faseN_directo.py`
4. Ejecutar: `python tests/test_faseN_directo.py`
5. Verificar que todas las fases pasen sin errores (0 errores)
6. Si hay errores, depurar y volver a ejecutar

## 📚 Referencias

- Ver `ROADMAP.md` para el plan completo de implementación
- Ver `test_kt/README.md` para los archivos Kotlin de prueba
- Ver `core/` para entender los módulos del compilador
