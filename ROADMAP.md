# 🗺️ KForge Compiler - Roadmap de Desarrollo

**Compilador Educativo de Kotlin**
**Versión actual**: v1.1.0 - ¡GENERACIÓN DE CÓDIGO COMPLETADA! 🎉
**Objetivo**: Compilador de Kotlin con backend TAC y Bytecode

---

## 📖 Documentación del Proyecto

- 📘 **[README.md](README.md)** - Descripción general y características
- 📋 **[CONTRIBUTING.md](CONTRIBUTING.md)** - Reglas de trabajo y flujo de desarrollo ⚠️ **LEER PRIMERO**
- 📝 **[CHANGELOG.md](CHANGELOG.md)** - Historial de cambios por versión
- 🗺️ **ROADMAP.md** (este archivo) - Plan de desarrollo y estado actual

---

## 📊 Estado Actual del Proyecto - VERSIÓN 1.0 ✅

### ✅ Características Implementadas (v1.0)

#### Fase 1 - Fundamentos ✅
- **Análisis Léxico**: Tokenización completa de Kotlin
- **Análisis Sintáctico**: Parser con AST completo
- **Análisis Semántico**: Validación de tipos, scopes y tabla de símbolos
- **Variables**: `var` con tipos `Int`, `Double`, `String`, `Boolean`
- **Operadores Aritméticos**: `+`, `-`, `*`, `/`, `%`
- **Operadores de Comparación**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Operadores Lógicos**: `&&`, `||`, `!` (NOT)
- **Operador Unario**: `-` (negativo)
- **Estructuras de Control**: `if`/`else`, `while`, `for..in..`
- **Rangos**: `0..10` (operador `..`), `0 until n` con expresiones aritméticas
- **Sentencias**: `break`, `continue`
- **Declaraciones sin inicialización**: `var x: Int`

#### Fase 2 - Funciones ✅
- **Declaración de Funciones**: `fun nombre(params): Tipo { ... }`
- **Función main()**: Inferencia de tipo `Unit` si se omite (solo para main)
- **Parámetros**: Múltiples parámetros con tipos
- **Return**: Validación de tipos de retorno
- **Llamadas a Funciones**: Con argumentos y validación de tipos
- **Funciones Built-in**: `println()`, `print()`, `intArrayOf()`, `doubleArrayOf()`

#### Fase 3 - Arrays y Propiedades ✅
- **Arrays Tipados**: `IntArray`, `DoubleArray`
- **Creación de Arrays**: `intArrayOf()`, `doubleArrayOf()` con varargs
- **Acceso a Elementos**: `array[i]` con validación de tipos
- **Modificación de Elementos**: `array[i] = value`
- **Propiedad .size**: Para arrays (retorna Int)
- **Propiedad .length**: Para strings (retorna Int)
- **Operador Punto**: Acceso a propiedades con validación
- **Índices Complejos**: `arr[j + 1]`, `arr[n - i - 1]`
- **Encadenamiento**: `array[0].size`, propiedades en expresiones

#### Interfaz de Usuario ✅
- **UI Moderna**: Tkinter con temas dark/light
- **Editor de Código**: Resaltado de sintaxis para Kotlin
- **Editor con Pestañas**: Múltiples archivos abiertos simultáneamente
- **Consola Multi-pestaña**: Salida, Errores, AST, Tokens
- **Panel de Configuración**: Temas y tamaño de fuente
- **Barra Lateral**: Gestión de archivos y configuración
- **Numeración de Líneas**: Sincronizada con scroll

---

## 🎯 Test Final v1.0

**Algoritmo**: Bubble Sort (Ordenamiento de Burbuja)

El compilador puede compilar exitosamente un algoritmo completo de ordenamiento que demuestra todas las características de las Fases 1, 2 y 3:

- ✅ Función `main()` sin tipo de retorno explícito
- ✅ Arrays con `intArrayOf()`
- ✅ Propiedad `.size` en expresiones
- ✅ Loops `for` anidados con expresiones aritméticas complejas
- ✅ Acceso y modificación de elementos con índices aritméticos
- ✅ Variables temporales y swap de elementos
- ✅ Operador de negación `!` y sentencia `break`

**Ejecutar test**:
```bash
python tests/test_v1_final.py
```

---

## 🚀 Plan de Implementación

### ✅ Versión 1.0 - COMPLETADA

- [x] **Fase 1**: Fundamentos (variables, operadores, estructuras de control)
- [x] **Fase 2**: Funciones (declaración, llamadas, parámetros, retorno)
- [x] **Fase 3**: Arrays y Propiedades (arrays tipados, acceso, propiedades)
- [x] **Test Final**: Algoritmo Bubble Sort completo

### ✅ Versión 1.0.1 - Validación Avanzada - COMPLETADA

- [x] **Comentarios de bloque** `/* */` con detección de sin cerrar
- [x] **Validación de números**: Múltiples puntos, overflow, sufijos inválidos
- [x] **Validación de escape sequences** en strings
- [x] **Detección de variables no inicializadas**
- [x] **Validación de return en todas las rutas**
- [x] **Tests de errores ampliados** (léxicos +6, semánticos +3)

### ✅ Versión 1.1 - Generación de Código Intermedio - COMPLETADA

**📘 Ver**: [docs/ARQUITECTURA_CODEGEN.md](docs/ARQUITECTURA_CODEGEN.md)

**Objetivo**: Backend con TAC y Bytecode para requisitos académicos

#### Fase 4: Código Intermedio TAC ✅
- [x] **TACGenerator**: Generador de código de 3 direcciones
  - [x] Operaciones básicas: ASSIGN, ADD, SUB, MUL, DIV, MOD
  - [x] Comparaciones: LT, GT, LE, GE, EQ, NE
  - [x] Lógicos: AND, OR, NOT, NEG
  - [x] Control de flujo: LABEL, GOTO, IF_FALSE
  - [x] Funciones: PARAM, CALL, RETURN
  - [x] Arrays: ARRAY_LOAD, ARRAY_STORE
- [x] **Tests TAC**: Cobertura completa de generación (11/11 tests passing)
- [x] **Módulo**: `core/tac.py` con clases `TACInstruction` y `TACGenerator`

#### Fase 5: Bytecode Stack-Based ✅
- [x] **BytecodeGenerator**: Traductor TAC → Bytecode
  - [x] Stack: PUSH, LOAD, STORE
  - [x] Aritmética: ADD, SUB, MUL, DIV, MOD
  - [x] Comparaciones: EQ, LT, GT, LE, GE, NE
  - [x] Lógicos: AND, OR, NOT, NEG
  - [x] Control: JUMP, JUMPF, CALL, RET, HALT
  - [x] Arrays: ALOAD, ASTORE
- [x] **Formateador Assembly**: Output legible con comentarios
- [x] **Tests Bytecode**: Verificación TAC → Bytecode (10/10 tests passing)
- [x] **Módulo**: `core/bytecode.py` con clases `BytecodeInstruction` y `BytecodeGenerator`

#### Fase 6: Integración con UI ✅
- [x] **Nueva pestaña "Código"** en ConsolePanel
  - [x] Botón "Ver TAC"
  - [x] Botón "Ver Bytecode"
  - [x] Botón "Guardar Código" (.tac / .asm)
- [x] **Actualizar controller.py**: Pipeline integrado automáticamente
- [x] **Temas**: Syntax highlighting aplicado a código generado
- [x] **CodeTab**: Nueva clase con visualización y exportación
- [x] **Integración**: Métodos `_run_semantic()`, `_run_complete()` y `_run_codegen()` actualizados

**Entregable**: ✅ "Código ensamblador" visible y exportable en UI

---

### ⚡ Versión 1.2 - Optimizaciones (PLANEADA)

**Objetivo**: Mejorar calidad del código TAC generado

#### Fase 7: Optimizador de TAC
- [ ] **Constant Folding**: `t1 = 2 + 3` → `t1 = 5`
- [ ] **Dead Code Elimination**: Código inalcanzable
- [ ] **Copy Propagation**: `t1 = x; t2 = t1` → `t2 = x`
- [ ] **Common Subexpression Elimination**
- [ ] **Tests de Optimización**: Verificar mejoras

**Entregable**: Compilador con optimizaciones medibles

---

### 🚀 Versión 1.3 - Backend C Ejecutable (PLANEADA)

**Objetivo**: Generar código C ejecutable

#### Fase 8: Generador de C
- [ ] **C Backend**: TAC → C
  - [ ] Variables y expresiones
  - [ ] Control de flujo (if, while, for)
  - [ ] Funciones y llamadas
  - [ ] Arrays
- [ ] **Integración gcc**: Compilar automáticamente
- [ ] **Ejecutor**: Correr desde UI
- [ ] **Tests de Ejecución**: Verificar salida

**Entregable**: Ejecutables nativos desde Kotlin

---

### 🎯 Versión 1.4 - Más Características Kotlin (PLANEADA)

**Objetivo**: Expandir lenguaje soportado

#### Expresiones y Operadores
- [ ] **String Templates**: `"$variable"`
- [ ] **Operadores Compuestos**: `+=`, `-=`, `*=`, `/=`
- [ ] **Incremento/Decremento**: `++`, `--`

#### Estructuras
- [ ] **When Expression**: Switch mejorado
- [ ] **Ranges Avanzados**: `downTo`, `step`

**Entregable**: Más features de Kotlin real

---

### 🌟 Versión 2.0 - Nivel Profesional (FUTURO)

**Objetivo**: Compilador industrial

#### Backend LLVM
- [ ] **LLVM IR Generator**
- [ ] **Optimizaciones LLVM**
- [ ] **Ejecutables nativos optimizados**

#### Características Avanzadas
- [ ] **Lambdas**: `{ x -> x * 2 }`
- [ ] **Higher-Order Functions**: map, filter, reduce
- [ ] **Null Safety**: `?`, `!!`, `?.`, `?:`
- [ ] **Clases y Objetos**: POO básica

**Entregable**: Compilador profesional

---

## 📅 Cronograma de Implementación

| Versión | Descripción | Estado | Fecha |
|---------|-------------|--------|-------|
| **v1.0.0** | Frontend Completo | ✅ Completada | 2025-11-06 |
| **v1.0.1** | Validación Avanzada | ✅ Completada | 2025-11-22 |
| **v1.1** | Código Intermedio (TAC + Bytecode) | 🔄 En Desarrollo | Dic 2025 |
| **v1.2** | Optimizaciones de TAC | 📝 Planeada | Ene 2026 |
| **v1.3** | Backend C Ejecutable | 📝 Planeada | Feb 2026 |
| **v1.4** | Más Features Kotlin | 📝 Planeada | Mar 2026 |
| **v2.0** | Backend LLVM + Avanzado | 🔮 Futuro | 2026+ |

---

## 🔄 Historial de Desarrollo

Ver [CHANGELOG.md](CHANGELOG.md) para historial detallado de cambios.

### Hitos Principales

- **2025-11-22**: ✨ **v1.0.1 Lanzada** - Validación avanzada de errores
- **2025-11-06**: 🎉 **v1.0 Lanzada** - Compilador funcional con test final
- **2025-11-05**: ✅ Fase 3 completada - Arrays y propiedades
- **2025-11-04**: ✅ Fase 2 completada - Funciones y llamadas
- **2025-11-03**: ✅ Fase 1 completada - Fundamentos del lenguaje
- **2025-11-02**: 🚀 Inicio del proyecto KForge

---

## 📊 Resumen de Estado Actual

### ✅ Implementado (v1.0.1)
- **Frontend Completo**: Lexer, Parser, Semantic Analyzer
- **Detección de 40+ tipos de errores**:
  - Léxicos: Caracteres inválidos, strings sin cerrar, números mal formados, escape sequences
  - Sintácticos: Gramática completa, validación de estructura
  - Semánticos: Tipos, scopes, inicialización, return paths
- **Características del Lenguaje**:
  - Variables (var/val), tipos básicos
  - Operadores completos (aritméticos, lógicos, comparación)
  - Control de flujo (if, while, for, break, continue)
  - Funciones con parámetros y return
  - Arrays tipados con propiedades
  - Comentarios de línea y bloque
- **UI Moderna**: Editor multi-pestaña, consola, temas, configuración

### 🔄 En Desarrollo (v1.1)
- **Generación de Código Intermedio**: TAC + Bytecode
- **Integración con UI**: Pestaña de código, exportación
- **Tests de Generación**: Cobertura completa

### 📝 Pendiente
- **v1.2**: Optimizaciones (constant folding, dead code)
- **v1.3**: Backend C ejecutable
- **v1.4+**: Más características de Kotlin
- **v2.0**: LLVM backend profesional

---

## 🛠️ Cómo Continuar el Desarrollo

1. **Lee [CONTRIBUTING.md](CONTRIBUTING.md)** - Reglas de trabajo y flujo de desarrollo
2. **Elige una característica** de la sección "Características Faltantes"
3. **Sigue el flujo de trabajo** definido en CONTRIBUTING.md
4. **Crea tests** antes de implementar (TDD recomendado)
5. **Ejecuta todos los tests** de fases anteriores antes de commit
6. **Actualiza documentación** (ROADMAP.md y CHANGELOG.md)
7. **Haz commit** con mensaje descriptivo

---

## 📚 Recursos y Referencias

### Kotlin Reference
- **Documentación Oficial**: https://kotlinlang.org/docs/reference/
- **Kotlin Grammar**: https://kotlinlang.org/docs/reference/grammar.html

### Compiladores
- **Dragon Book**: "Compilers: Principles, Techniques, and Tools"
- **Modern Compiler Implementation**: Andrew Appel
- **Crafting Interpreters**: https://craftinginterpreters.com/

### Python y AST
- **Python AST**: https://docs.python.org/3/library/ast.html
- **Tokenize**: https://docs.python.org/3/library/tokenize.html

---

## 👤 Autor

**Gabriel Alejandro Medina Miramontes**

Desarrollado como proyecto educativo para aprender compiladores e implementación de lenguajes.

**Licencia**: MIT

---

## 🙏 Agradecimientos

Gracias a todos los recursos educativos y a la comunidad de compiladores que hacen posible proyectos como este.

---

**¿Preguntas? ¿Sugerencias?** Abre un issue o contribuye siguiendo [CONTRIBUTING.md](CONTRIBUTING.md)
