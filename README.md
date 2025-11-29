# 🔨 KForge - Compilador Profesional Kotlin → JVM

<div align="center">

**Compilador de Kotlin a JVM Bytecode Real**

*Genera archivos .class ejecutables en cualquier Java Virtual Machine*

**Versión Actual: 1.1.0 ✅** | **Objetivo: v2.0 - JVM Bytecode Real**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Kotlin](https://img.shields.io/badge/Kotlin-Subset-purple.svg)](https://kotlinlang.org/)
[![JVM](https://img.shields.io/badge/Target-JVM%20Bytecode-orange.svg)](https://docs.oracle.com/javase/specs/jvms/se8/html/)
[![License](https://img.shields.io/badge/License-GPL--3.0-green.svg)](LICENSE)

[Documentación](#-documentación) • [Inicio Rápido](#-inicio-rápido) • [Características](#-características) • [Roadmap](#-roadmap)

</div>

---

## 📋 Descripción

**KForge** es un compilador profesional que traduce un subconjunto de Kotlin a **JVM bytecode real** ejecutable. El proyecto implementa un pipeline completo de compilación desde análisis léxico hasta generación de archivos `.class` compatibles con el estándar JVM.

### 🎯 Objetivo del Proyecto

Generar archivos `.class` ejecutables compatibles con JVM (Java 8+), permitiendo:

- ✅ Ejecutar programas Kotlin en cualquier JVM estándar
- ✅ Interoperabilidad con el ecosistema Java
- ✅ Compatibilidad con herramientas JVM (javap, jd-gui)
- ✅ Demostración de implementación profesional de compiladores

---

## 🚀 Estado Actual

### ✅ Versión 1.1.0 - COMPLETADA

**Pipeline Implementado:**
```
Kotlin → Lexer → Parser → Semantic → TAC → Bytecode Stack-Based (educativo)
```

**Componentes Funcionales:**

| Componente | Estado | Tests | Descripción |
|------------|--------|-------|-------------|
| **Lexer** | ✅ Completo | ✅ Integrado | Tokenización con 40+ errores detectados |
| **Parser** | ✅ Completo | ✅ Integrado | Generación de AST |
| **Semantic** | ✅ Completo | ✅ Integrado | Tipos, scopes, return paths |
| **TAC Generator** | ✅ Completo | ✅ 11/11 | Three-Address Code |
| **Bytecode (educativo)** | ✅ Completo | ✅ 10/10 | Stack-based assembly |
| **UI Moderna** | ✅ Completo | ✅ Manual | Editor + consola multi-pestaña |

**Subconjunto de Kotlin Soportado:**
- Variables: `var`, `val` con tipos `Int`, `Double`, `String`, `Boolean`
- Operadores: Aritméticos, lógicos, comparación
- Control: `if`/`else`, `while`, `for..in`, `break`, `continue`
- Funciones: Declaración, parámetros, retorno, llamadas
- Arrays: `IntArray`, `DoubleArray`, acceso `[]`, propiedad `.size`
- Built-ins: `println()`, `print()`, `intArrayOf()`, `doubleArrayOf()`

### 🎯 Versión 2.0 - EN DESARROLLO

**Pipeline Objetivo:**
```
Kotlin → Lexer → Parser → Semantic → TAC → JVM Bytecode → .class → Ejecución
```

**Plan de Implementación (8 semanas):**

| Fase | Componente | Duración | Estado |
|------|-----------|----------|--------|
| **7** | ClassFile + Constant Pool | 2 semanas | ✅ Completada |
| **8** | JVM Instruction Set | 2 semanas | ✅ Completada |
| **9** | Stack Map Frames | 1 semana | 📝 En Desarrollo |
| **10** | Attributes + Metadata | 1 semana | 📝 Planeada |
| **11** | Runtime Support | 1 semana | 📝 Planeada |
| **12** | Integration + Testing | 1 semana | 📝 Planeada |

**Entregable v2.0:**
- Archivos `.class` ejecutables (`java ClassName`)
- Debugging info (SourceFile, LineNumberTable)
- I/O completo (`println`, `print`)
- Arrays con inicialización

Ver **[ROADMAP.md](ROADMAP.md)** para el plan completo.

---

## 🚀 Inicio Rápido

### Requisitos

- **Python 3.8+** (con Tkinter incluido)
- **JDK 8+** (opcional, para verificar .class files con javap)

### Instalación

```bash
# Clonar el repositorio
git clone <repository-url>
cd KForge

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instalar dependencias (actualmente solo biblioteca estándar)
pip install -r requirements.txt

# Verificar Python
python --version  # Debe ser 3.8+
```

**📖 Ver [INSTALL.md](INSTALL.md) para instrucciones detalladas de instalación y configuración**

### Ejecutar el Compilador

```bash
# Lanzar interfaz gráfica
python main_modern.py
```

### Ejecutar Tests

```bash
# Tests completos v1.1
python tests/test_tac_generator.py       # 11/11 tests TAC
python tests/test_bytecode_generator.py  # 10/10 tests Bytecode
python tests/test_v1_final.py            # Bubble Sort completo

# Tests de fases
python tests/test_fase1_directo.py       # Fundamentos
python tests/test_fase2_directo.py       # Funciones
python tests/test_fase3_directo.py       # Arrays
```

---

## ✨ Características

### 🔤 Frontend de Compilación (v1.0)

- **Análisis Léxico**: Tokenización completa con comentarios de bloque (`//`, `/* */`)
- **Análisis Sintáctico**: Parser recursivo descendente con generación de AST
- **Análisis Semántico**:
  - Type checking (validación de tipos)
  - Scope analysis (análisis de alcance)
  - Detección de variables no inicializadas
  - Return path analysis
  - Validación de inmutabilidad (`val` vs `var`)
- **Detección de 40+ Errores**: Léxicos, sintácticos y semánticos

### 🔧 Generación de Código (v1.1)

- **TAC Generator**:
  - Three-Address Code (representación intermedia)
  - Operaciones: ASSIGN, ADD, SUB, MUL, DIV, MOD, comparaciones, lógicas
  - Control de flujo: LABEL, GOTO, IF_FALSE
  - Funciones: PARAM, CALL, RETURN
  - Arrays: ARRAY_LOAD, ARRAY_STORE
  - Soporte para código global y break/continue

- **Bytecode Generator** (educativo):
  - Stack-based assembly (NO JVM real)
  - Formato texto .asm con comentarios
  - Instrucciones: PUSH, LOAD, STORE, operadores, saltos, llamadas
  - Visualización con syntax highlighting

### 🎨 Interfaz de Usuario

- **Editor Moderno**:
  - Múltiples pestañas para archivos
  - Syntax highlighting para Kotlin
  - Numeración de líneas sincronizada
  - Atajos de teclado (`Ctrl+N`, `Ctrl+O`, `Ctrl+S`, `Ctrl+Enter`)

- **Consola Multi-Pestaña**:
  - **Salida**: Resumen de compilación
  - **Errores**: Detalle de errores detectados
  - **Tokens**: Lista de tokens generados
  - **AST**: Árbol sintáctico abstracto
  - **Código**: TAC y Bytecode con alternador y exportación

- **Temas**: Dark (Darcula) y Light
- **Configuración**: Fuentes y tamaños ajustables

---

## 💡 Uso

### Interfaz Gráfica

```bash
python main_modern.py
```

1. Escribir código Kotlin en el editor
2. Presionar **"Compilar"** o `Ctrl+Enter`
3. Ver resultados en las pestañas de la consola:
   - ✅ Compilación exitosa → Ver TAC/Bytecode en pestaña "Código"
   - ❌ Errores → Ver detalles en pestaña "Errores"

### Uso Programático

```python
from core.controller import CompiladorController

# Crear controlador
controller = CompiladorController()

# Código Kotlin
codigo = """
fun suma(a: Int, b: Int): Int {
    return a + b
}

fun main() {
    val resultado: Int = suma(10, 20)
    println(resultado)
}
"""

# Compilar (incluye TAC y Bytecode en v1.1)
resultado = controller.ejecutar_semantico(codigo)

if resultado['exito']:
    print("✅ Compilación exitosa")
    print(f"TAC: {len(resultado['codigo_intermedio'])} caracteres")
    print(f"Bytecode: {len(resultado['bytecode'])} caracteres")
else:
    for error in resultado['errores']:
        print(f"❌ {error}")
```

---

## 🎯 Sintaxis Soportada

### Ejemplo Completo: Bubble Sort

```kotlin
fun main() {
    var arr: IntArray = intArrayOf(64, 34, 25, 12, 22, 11, 90)
    var n: Int = arr.size
    var swapped: Boolean

    for (i in 0 until n - 1) {
        swapped = false

        for (j in 0 until n - i - 1) {
            if (arr[j] > arr[j + 1]) {
                var temp: Int = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp
                swapped = true
            }
        }

        if (!swapped) {
            break
        }
    }

    println("Array ordenado")
}
```

**Resultado**: ✅ Compilación exitosa (0 errores)

Ver más ejemplos en [test_kt/](test_kt/)

---

## 🏗️ Arquitectura

### Pipeline del Compilador

```
┌─────────────────────────────────────────────────────────────┐
│                    CÓDIGO FUENTE KOTLIN                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
          ┌──────────────────────────────┐
          │  FRONTEND (v1.0 ✅)          │
          ├──────────────────────────────┤
          │  1. Lexer → Tokens           │
          │  2. Parser → AST             │
          │  3. Semantic → Validación    │
          └────────────┬─────────────────┘
                       │
                       ▼
          ┌──────────────────────────────┐
          │  BACKEND (v1.1 ✅)           │
          ├──────────────────────────────┤
          │  4. TAC → Código intermedio  │
          │  5. Bytecode → Assembly      │
          └────────────┬─────────────────┘
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
    ┌──────────┐          ┌──────────────────┐
    │ Bytecode │          │  JVM Bytecode    │
    │ (v1.1 ✅)│          │  (v2.0 📝)       │
    │ .asm     │          │  .class files    │
    └──────────┘          └────────┬─────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │  java ClassName │
                          │  (Ejecutable)   │
                          └─────────────────┘
```

### Estructura de Archivos

```
KForge/
├── core/                    # Núcleo del compilador
│   ├── lexer.py            # ✅ Análisis léxico
│   ├── parser.py           # ✅ Análisis sintáctico
│   ├── semantic.py         # ✅ Análisis semántico
│   ├── tac.py              # ✅ Generador TAC
│   ├── bytecode.py         # ✅ Bytecode educativo
│   ├── controller.py       # ✅ Orquestador
│   ├── errors.py           # ✅ Manejo de errores
│   ├── utils.py            # ✅ Token, AST, tipos
│   └── jvm/                # 📝 v2.0 - JVM Bytecode Real
│       ├── classfile.py
│       ├── constant_pool.py
│       ├── descriptors.py
│       ├── instructions.py
│       ├── jvm_generator.py
│       ├── stackmaps.py
│       ├── attributes.py
│       └── runtime.py
│
├── ui/                      # Interfaz gráfica
│   ├── app_ui.py
│   ├── editor_panel.py
│   ├── console_panel.py
│   └── ...
│
├── tests/                   # Tests del compilador
│   ├── test_tac_generator.py
│   ├── test_bytecode_generator.py
│   ├── phases/              # Tests de fases
│   │   ├── test_fase1_directo.py
│   │   ├── test_fase2_directo.py
│   │   └── test_fase3_directo.py
│   ├── integration/         # Tests de integración
│   └── jvm/                 # 📝 v2.0 - Tests JVM
│
├── test_kt/                 # Código Kotlin de prueba
├── docs/                    # Documentación técnica
├── main_modern.py           # Punto de entrada
└── ...
```

Ver **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** para arquitectura completa.

---

## 📖 Documentación

### Documentación Principal

- 📘 **[README.md](README.md)** - Este archivo
- 🗺️ **[ROADMAP.md](ROADMAP.md)** - Plan de desarrollo v2.0 (Fases 7-12)
- 📝 **[CHANGELOG.md](CHANGELOG.md)** - Historial de cambios
- 🤝 **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guía de contribución

### Documentación Técnica

- 🏗️ **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Arquitectura completa del compilador
- 🔧 **[docs/JVM_BYTECODE_GUIDE.md](docs/JVM_BYTECODE_GUIDE.md)** - Guía de implementación JVM
- 📋 **[docs/PROJECT_REORGANIZATION.md](docs/PROJECT_REORGANIZATION.md)** - Reorganización v1.1 → v2.0

---

## 🧪 Testing

### Tests Actuales (v1.1)

```bash
# TAC Generator (11 tests)
python tests/test_tac_generator.py
# ✅ test_simple_assignment
# ✅ test_arithmetic_operations
# ✅ test_if_statement
# ✅ test_while_loop
# ✅ test_for_loop
# ✅ test_break_continue
# ✅ test_function_declaration
# ✅ test_function_call
# ✅ test_array_creation
# ✅ test_array_access
# ✅ test_bubble_sort

# Bytecode Generator (10 tests)
python tests/test_bytecode_generator.py
# ✅ test_simple_assignment
# ✅ test_arithmetic
# ✅ test_comparisons
# ✅ test_if_statement
# ✅ test_while_loop
# ✅ test_for_loop
# ✅ test_function
# ✅ test_function_call
# ✅ test_arrays
# ✅ test_bubble_sort

# Test final
python tests/test_v1_final.py
# ✅ Bubble Sort completo (0 errores)
```

### Coverage

- ✅ Análisis Léxico: Cubierto por tests de fases
- ✅ Análisis Sintáctico: Cubierto por tests de fases
- ✅ Análisis Semántico: Cubierto por tests de fases
- ✅ TAC Generation: 11/11 tests passing
- ✅ Bytecode Generation: 10/10 tests passing
- ✅ Integración completa: Bubble Sort

---

## 🚧 Limitaciones Actuales

### NO Implementado (v1.1)

- ❌ Generación de JVM bytecode real (.class)
- ❌ String templates (`"Resultado: ${x}"`)
- ❌ When expression
- ❌ Operadores compuestos (`+=`, `-=`, `*=`, `/=`)
- ❌ Incremento/decremento (`++`, `--`)
- ❌ Null safety (`?`, `!!`, `?.`)
- ❌ Lambdas y funciones de orden superior
- ❌ Clases y objetos (POO)

### Planeado para v2.0+

- ✅ **v2.0** (8 semanas): JVM Bytecode real
- 📝 **v2.1+**: Características adicionales de Kotlin

---

## 🤝 Contribuciones

### Para Contribuir

1. Lee **[CONTRIBUTING.md](CONTRIBUTING.md)** para reglas de desarrollo
2. Revisa **[ROADMAP.md](ROADMAP.md)** para la fase actual
3. Lee **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** para entender la arquitectura
4. Ejecuta todos los tests antes de hacer commit
5. Sigue el formato de commits: `tipo(scope): descripción`

### Estado Actual del Desarrollo

**Fase Actual**: Preparación para Fase 7 (ClassFile + Constant Pool)

**Próximos Pasos**:
1. Implementar `core/jvm/classfile.py`
2. Implementar `core/jvm/constant_pool.py`
3. Implementar `core/jvm/descriptors.py`

Ver **[docs/JVM_BYTECODE_GUIDE.md](docs/JVM_BYTECODE_GUIDE.md)** para guía de implementación.

---

## 📚 Recursos Técnicos

### Especificaciones

- **JVM Specification SE 8**: https://docs.oracle.com/javase/specs/jvms/se8/html/
- **Kotlin Language Spec**: https://kotlinlang.org/spec/
- **Class File Format**: https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html

### Herramientas

```bash
# Verificar bytecode JVM (v2.0)
javap -c -v MyClass.class

# Ejecutar bytecode
java MyClass

# Decompilador gráfico
jd-gui MyClass.class
```

### Referencias

- **Dragon Book**: Compilers: Principles, Techniques, and Tools
- **Crafting Interpreters**: https://craftinginterpreters.com/
- **ASM Library**: https://asm.ow2.io/ (para Stack Map Frames)

---

## 📄 Licencia

**GNU General Public License v3.0 (GPL-3.0)**

Este proyecto está licenciado bajo GPL-3.0:

- ✅ Uso libre del código
- ✅ Modificación permitida
- ✅ Distribución permitida
- ⚠️ Trabajos derivados deben ser open source bajo GPL-3.0
- ⚠️ Créditos del autor original deben mantenerse
- ⚠️ Modificaciones deben compartirse bajo la misma licencia

Ver [LICENSE](LICENSE) para más detalles.

---

## 👤 Autor

**Gabriel Alejandro Medina Miramontes**

Proyecto profesional de compilador Kotlin → JVM Bytecode.

Desarrollado para demostrar implementación completa de un compilador real con generación de bytecode ejecutable.

---

## 🙏 Agradecimientos

- **JVM Specification** - Oracle
- **Kotlin Language** - JetBrains
- **Dragon Book** - Aho, Sethi, Ullman
- **Crafting Interpreters** - Robert Nystrom
- Comunidad de compiladores y lenguajes de programación

---

<div align="center">

**KForge v1.1.0** → **v2.0 (JVM Bytecode Real)**

*Hecho con ❤️ para demostrar implementación profesional de compiladores*

[Documentación](ROADMAP.md) • [Contribuir](CONTRIBUTING.md) • [Changelog](CHANGELOG.md) • [Arquitectura](docs/ARCHITECTURE.md)

</div>
