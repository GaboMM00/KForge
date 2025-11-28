# 🤝 Guía de Contribución - KForge Compiler

**Compilador Profesional Kotlin → JVM Bytecode**

Esta guía define las reglas y mejores prácticas para contribuir al desarrollo de KForge.

**Versión Actual**: v1.1.0 ✅ COMPLETADA
**En Desarrollo**: v2.0 - JVM Bytecode Real

---

## 📋 Antes de Empezar

### 🎯 Para Cualquier Desarrollador que Continue este Trabajo

**LEER ESTO PRIMERO ANTES DE HACER CUALQUIER COSA**

### 📖 1. Análisis Obligatorio del Proyecto

**Antes de implementar cualquier característica, DEBES**:

1. **Leer y comprender estos archivos en orden**:
   - `README.md` - Descripción general del proyecto
   - `ROADMAP.md` - Plan de desarrollo y estado actual
   - `CONTRIBUTING.md` (este archivo) - Reglas de contribución
   - `core/utils.py` - Entender tokens, nodos AST y tipos de datos
   - `core/lexer.py` - Entender cómo funciona la tokenización
   - `core/parser.py` - Entender cómo se construye el AST
   - `core/semantic.py` - Entender la validación semántica
   - `core/controller.py` - Entender el flujo de compilación

2. **Verificar el estado actual**:
   - Revisar qué fase está completada en `ROADMAP.md`
   - Leer todos los tests en `test_kt/` para entender qué funciona
   - Ejecutar tests de fases implementadas para confirmar que pasan

3. **Identificar la siguiente tarea**:
   - Ver el plan de implementación en `ROADMAP.md`
   - Leer COMPLETAMENTE la descripción de la tarea antes de empezar
   - Entender qué archivos necesitas modificar

---

## 🗂️ Estructura del Proyecto (v2.0)

```
KForge/
├── core/                         # Núcleo del compilador
│   ├── lexer.py                  # ✅ Análisis léxico
│   ├── parser.py                 # ✅ Análisis sintáctico
│   ├── semantic.py               # ✅ Análisis semántico
│   ├── tac.py                    # ✅ Generación TAC (v1.1)
│   ├── bytecode.py               # ✅ Bytecode educativo (v1.1)
│   ├── controller.py             # ✅ Orquestador del pipeline
│   ├── errors.py                 # ✅ Sistema de manejo de errores
│   ├── utils.py                  # ✅ Token, AST, TipoDato
│   └── jvm/                      # 📝 JVM Bytecode Real (v2.0)
│       ├── classfile.py          # Escritor de .class
│       ├── constant_pool.py      # Constant Pool Manager
│       ├── descriptors.py        # Type descriptors JVM
│       ├── instructions.py       # JVM Instruction Set
│       ├── jvm_generator.py      # TAC → JVM Bytecode
│       ├── stackmaps.py          # Stack Map Frames
│       ├── attributes.py         # Attributes (SourceFile, etc.)
│       └── runtime.py            # Runtime support (println, arrays)
│
├── ui/                           # Interfaz gráfica Tkinter
│   ├── app_ui.py                 # Ventana principal
│   ├── editor_panel.py           # Editor con pestañas
│   ├── console_panel.py          # Consola multi-pestaña
│   ├── sidebar.py                # Barra lateral
│   ├── theme_manager.py          # Gestión de temas
│   ├── phases_panel.py           # Panel de fases
│   ├── status_bar.py             # Barra de estado
│   └── splash_screen.py          # Pantalla de inicio
│
├── tests/                        # Scripts de test Python
│   ├── test_tac_generator.py     # ✅ 11 tests TAC
│   ├── test_bytecode_generator.py # ✅ 10 tests Bytecode
│   ├── test_fase1_directo.py     # ✅ Tests Fase 1
│   ├── test_fase2_directo.py     # ✅ Tests Fase 2
│   ├── test_fase3_directo.py     # ✅ Tests Fase 3
│   ├── test_v1_final.py          # ✅ Test Bubble Sort
│   └── jvm/                       # 📝 Tests JVM (v2.0)
│       ├── test_classfile.py     # Tests ClassFile
│       ├── test_jvm_generation.py # Tests generación
│       └── test_execution.py     # Tests ejecución JVM
│
├── test_kt/                      # Código Kotlin de prueba
│   ├── test_fase1.kt             # Test Fase 1
│   ├── test_fase2.kt             # Test Fase 2
│   ├── test_fase3.kt             # Test Fase 3
│   └── test_v1_final.kt          # Test Bubble Sort
│
├── docs/                         # Documentación técnica
│   ├── ARCHITECTURE.md           # Arquitectura completa del compilador
│   ├── JVM_BYTECODE_GUIDE.md     # Guía implementación JVM
│   ├── ARQUITECTURA_CODEGEN.md   # Diseño del pipeline de código
│   ├── errores_lexicos_pendientes.md
│   └── errores_pendientes_implementacion.md
│
├── main_modern.py                # Punto de entrada de la UI
├── README.md                     # Documentación principal
├── ROADMAP.md                    # Plan de desarrollo v2.0
├── CONTRIBUTING.md               # Este archivo
├── CHANGELOG.md                  # Historial de cambios
└── LICENSE                       # GPL-3.0
```

---

## ⚠️ Reglas Importantes

### 📁 Regla de Organización de Tests

1. **Tests con código Kotlin** (`*.kt`) → Carpeta `test_kt/`
   - Ejemplo: `test_kt/test_fase1.kt`
   - Estos son archivos Kotlin que prueban características del lenguaje

2. **Scripts de test Python** (`test_*.py`) → Carpeta `tests/`
   - Ejemplo: `tests/test_fase1_directo.py`
   - Estos son scripts Python que ejecutan el compilador

3. **Archivos de prueba generales** (`*.txt`, datos) → Carpeta `tests/`
   - Archivos de entrada para pruebas adicionales

### 🔧 Regla de Modificación de Archivos

**NUNCA modifiques archivos sin entender su propósito completo**

| Archivo | Cuándo Modificar | Qué Agregar |
|---------|------------------|-------------|
| `core/utils.py` | Al agregar tokens, nodos AST, o tipos | Enum entries en `TipoToken`, `TipoNodo`, `TipoDato` |
| `core/lexer.py` | Al agregar palabras clave u operadores | Palabras en `PALABRAS_CLAVE` y patrones regex |
| `core/parser.py` | Al implementar nueva sintaxis | Métodos de parseo para nuevas construcciones |
| `core/semantic.py` | Al agregar validación de tipos/scopes | Métodos `visitar_*` para nuevos nodos |
| `core/tac.py` | Al modificar generación TAC | Métodos `_generate_*` para nuevas construcciones |
| `core/jvm/*.py` | Al implementar JVM bytecode (v2.0) | Ver `docs/JVM_BYTECODE_GUIDE.md` |

### 🧪 Regla de Testing

**CADA característica implementada DEBE tener**:

1. ✅ Test en `test_kt/test_faseN.kt` - Código Kotlin que usa la característica
2. ✅ Script Python en `tests/test_faseN_directo.py` - Ejecuta el compilador y verifica
3. ✅ Verificación de 0 errores en las 3 fases: Léxico, Sintáctico, Semántico

**Ejecutar tests**:
```bash
# Test individual
python tests/test_fase1_directo.py

# Todos los tests
python tests/test_fase1_directo.py && python tests/test_fase2_directo.py && python tests/test_fase3_directo.py
```

### 🚫 Regla de No Romper Código Existente

- ⚠️ Antes de hacer commit, ejecuta TODOS los tests de fases anteriores
- ⚠️ Si un test anterior falla, tu código tiene un bug
- ⚠️ NUNCA hagas commit si hay tests rotos
- ⚠️ Mantén compatibilidad hacia atrás con código Kotlin ya funcional

---

## 🔄 Flujo de Trabajo para Implementar una Característica

### Ejemplo: Implementar operador `&&` (AND lógico)

#### Paso 1: Planificar (5 minutos)
```markdown
Característica: Operador && (AND lógico)
Archivos a modificar:
  - core/utils.py (agregar token AND)
  - core/lexer.py (agregar regex para &&)
  - core/parser.py (agregar método expresion_and)
  - core/semantic.py (validar tipos Boolean)
Tests necesarios:
  - test_kt/test_fase1.kt (código con &&)
  - tests/test_fase1_directo.py (verificar compilación)
```

#### Paso 2: Implementar en orden

**1. Agregar Token (`core/utils.py`)**
```python
class TipoToken(Enum):
    AND = auto()  # Agregar token
```

**2. Agregar Patrón Léxico (`core/lexer.py`)**
```python
ESPECIFICACION_TOKENS = [
    ('AND', r'&&'),  # Agregar ANTES de operadores simples
    ...
]
```

**3. Agregar Parsing (`core/parser.py`)**
```python
def expresion_and(self):
    """Parsea expresiones con AND (&&)."""
    izquierda = self.expresion_comparacion()
    while self.verificar(TipoToken.AND):
        operador = self.token_actual
        self.avanzar()
        derecha = self.expresion_comparacion()
        nodo = NodoAST(
            TipoNodo.EXPRESION_BINARIA,
            '&&',
            linea=operador.linea,
            columna=operador.columna
        )
        nodo.agregar_hijo(izquierda)
        nodo.agregar_hijo(derecha)
        izquierda = nodo
    return izquierda
```

**4. Agregar Validación Semántica (`core/semantic.py`)**
```python
def visitar_expresion_binaria(self, nodo: NodoAST):
    # En la sección de operadores lógicos
    elif operador == '&&':
        if tipo_izq != TipoDato.BOOLEAN:
            self.error_manager.agregar_error(...)
        if tipo_der != TipoDato.BOOLEAN:
            self.error_manager.agregar_error(...)
        return TipoDato.BOOLEAN
```

#### Paso 3: Crear Tests

**Test Kotlin (`test_kt/test_fase1.kt`)**
```kotlin
var a: Boolean = true
var b: Boolean = false
if (a && b) {
    println("Ambos son verdaderos")
}
```

**Script Python (`tests/test_fase1_directo.py`)**
```python
codigo = """
var a: Boolean = true
var b: Boolean = false
if (a && b) {
    println("Test")
}
"""
# ... ejecutar compilador y verificar 0 errores
```

#### Paso 4: Ejecutar Tests
```bash
python tests/test_fase1_directo.py
# Verificar: Total de errores: 0
```

#### Paso 5: Documentar

**Actualizar `ROADMAP.md`**:
```markdown
- **2025-XX-XX**:
  - ✅ Implementado operador lógico AND (&&)
  - 📦 Archivos modificados: utils.py, lexer.py, parser.py, semantic.py
```

**Actualizar `CHANGELOG.md`**:
```markdown
## [X.X.X] - 2025-XX-XX
### Added
- Operador lógico AND (&&) para expresiones booleanas
```

---

## 📝 Convenciones de Código

### Estilo Python

- Sigue PEP 8
- Nombres de variables: `snake_case`
- Nombres de clases: `PascalCase`
- Constantes: `UPPER_CASE`
- Docstrings en español para métodos públicos

### Mensajes de Commit

⚠️ **REGLA OBLIGATORIA**: Cada cambio relevante en el proyecto DEBE incluir un commit descriptivo siguiendo este formato.

**Formato**: `tipo(scope): descripción corta`

**Tipos**:
- `feat`: Nueva característica o funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `refactor`: Refactorización sin cambios funcionales
- `test`: Agregar o modificar tests
- `chore`: Tareas de mantenimiento
- `style`: Cambios de formato sin afectar funcionalidad

**Scopes Comunes**:
- `lexer`, `parser`, `semantic`: Componentes del frontend
- `tac`, `bytecode`, `jvm`: Generadores de código
- `ui`: Interfaz gráfica
- `docs`: Documentación
- `tests`: Sistema de tests
- `v2.0`: Cambios relacionados con versión 2.0

**Estructura del Mensaje**:
```
tipo(scope): descripción corta (max 72 caracteres)

- Detalle de cambio 1
- Detalle de cambio 2
- Detalle de cambio 3

Archivos modificados: archivo1.py, archivo2.py
Tests: X/X passing
```

**Ejemplos Reales del Proyecto**:
```bash
# Característica nueva
feat(parser): add main() return type inference

# Corrección de bug
fix(ui): sync font size for syntax highlighting tags

# Documentación
docs(readme): update with v1.0 features

# Tests
test(phase3): add comprehensive array tests

# Generación de código
feat(codegen): implement TAC and Stack-Based Bytecode generation with UI integration

# Versión 2.0
docs(v2.0): complete project reorganization for JVM bytecode implementation
```

**Cuándo Hacer Commit**:
- ✅ Después de completar una característica funcional
- ✅ Después de arreglar un bug y verificar con tests
- ✅ Después de actualizar documentación importante
- ✅ Al finalizar una fase del ROADMAP
- ❌ NO hacer commits de código que no compila
- ❌ NO hacer commits sin ejecutar tests relevantes

---

## 🐛 Reportar Bugs

Al reportar un bug, incluye:

1. **Descripción del problema**
2. **Código Kotlin que reproduce el error**
3. **Mensaje de error completo**
4. **Comportamiento esperado**
5. **Versión de KForge** (ver `ROADMAP.md`)

---

## 💡 Sugerir Características

Para sugerir nuevas características:

1. Verifica que no esté ya en `ROADMAP.md`
2. Explica el caso de uso
3. Proporciona ejemplos de código Kotlin
4. Indica si es compatible con Kotlin estándar

---

## 📚 Recursos

- **Kotlin Reference**: https://kotlinlang.org/docs/reference/
- **Compiladores**: "Compilers: Principles, Techniques, and Tools" (Dragon Book)
- **Python AST**: https://docs.python.org/3/library/ast.html

---

## 👤 Autor

Gabriel Alejandro Medina Miramontes

Desarrollado como proyecto educativo para aprender compiladores e implementación de lenguajes.

**Licencia**: MIT
