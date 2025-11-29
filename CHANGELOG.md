# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [2.0.0-alpha.1] - 2025-11-28

### Added - Fase 7: Fundamentos JVM (ClassFile + Constant Pool)

- **Estructura del Proyecto**
  - Nueva carpeta `core/jvm/` para componentes de generación JVM
  - Nueva carpeta `tests/jvm/` para tests de componentes JVM
  - Reorganización: `tests/phases/` y `tests/integration/`
  - Carpeta `deprecated/` para código obsoleto

- **Constant Pool (`core/jvm/constant_pool.py`)**
  - Implementación completa del Constant Pool JVM
  - Soporte para todos los tipos de constantes: Utf8, Integer, Float, Long, Double, Class, String, Fieldref, Methodref, NameAndType
  - Indexación 1-based conforme a JVM Specification
  - Cache automático de constantes (deduplicación)
  - Manejo especial de Long/Double (ocupan 2 slots)
  - Gestión automática de dependencias (ej: Methodref agrega automáticamente todas sus constantes necesarias)
  - Conversión a bytes big-endian

- **Type Descriptors (`core/jvm/descriptors.py`)**
  - Clase `TypeDescriptor` para convertir tipos Kotlin a descriptores JVM
  - Mapeo de tipos: Int→'I', Double→'D', String→'Ljava/lang/String;', Boolean→'Z', Unit→'V'
  - Generación de method descriptors: `(param1param2...)returnType`
  - Descriptores predefinidos para métodos comunes (println, main)

- **ClassFile Writer (`core/jvm/classfile.py`)**
  - Clase `ClassFileWriter` para generar archivos .class válidos
  - Magic number 0xCAFEBABE y versión Java 8 (52.0)
  - Access flags (ACC_PUBLIC, ACC_SUPER, ACC_STATIC, etc.)
  - Clase `MethodInfo` para definir métodos
  - Clase `AttributeInfo` y subclases (`CodeAttribute`, `SourceFileAttribute`)
  - Escritura binaria big-endian conforme a JVM Specification
  - Funciones helper: `create_minimal_class()`, `create_hello_world_class()`
  - Método `get_class_info()` para debugging

- **Tests Completos JVM**
  - `tests/jvm/test_constant_pool.py`: 8 tests completos (UTF-8, Integer, Long/Double slots, Class, Methodref, conversión a bytes)
  - `tests/jvm/test_classfile.py`: 10 tests completos (magic number, versión, estructura, attributes, methods)
  - `tests/jvm/test_jvm_validation.py`: 4 tests de validación (estructura bytecode, javap integration)
  - Todos los tests: 22/22 passing ✅

- **Documentación**
  - `docs/ARCHITECTURE.md`: Arquitectura completa del compilador
  - `docs/JVM_BYTECODE_GUIDE.md`: Guía detallada de implementación JVM (571 líneas)
  - `docs/PROJECT_REORGANIZATION.md`: Plan de reorganización v1.1 → v2.0
  - README.md actualizado con objetivo JVM bytecode
  - ROADMAP.md actualizado con plan v2.0 (Fases 7-12)
  - CONTRIBUTING.md actualizado con reglas de commit obligatorias

### Changed
- `core/__init__.py`: Removido import obsoleto de `CodeGenerator`
- `core/controller.py`: Comentado código obsoleto de generación de código intermedio v1.1
- `core/utils.py`: Verificado que usa `TipoDato.VOID` en lugar de `TipoDato.UNIT`

### Fixed
- Encoding UTF-8 en tests para soporte de caracteres Unicode (checkmarks)
- Paths de importación en tests relocalizados a `tests/phases/`

### Deprecated
- `core/codegen.py` → movido a `deprecated/codegen.py.deprecated`
- Bytecode stack-based educativo de v1.1 (mantenido para referencia)

---

## [1.1.0] - 2025-11-22

### Added - Generación de Código Intermedio (TAC) y Bytecode
- **Fase 4: Three-Address Code (TAC) Generator**
  - Nuevo módulo `core/tac.py` con clases `TACInstruction` y `TACGenerator`
  - Operaciones TAC: ASSIGN, ADD, SUB, MUL, DIV, MOD, LT, GT, LE, GE, EQ, NE, AND, OR, NOT, NEG
  - Control de flujo: LABEL, GOTO, IF_FALSE
  - Funciones: PARAM, CALL, RETURN
  - Arrays: ARRAY_LOAD, ARRAY_STORE
  - Soporte para sentencias globales (código sin funciones)
  - Soporte para break/continue con loop_stack
  - Formato de salida humanizado con numeración de líneas
  - Tests completos: `tests/test_tac_generator.py` (11 tests, 100% passing)

- **Fase 5: Bytecode Assembly Generator**
  - Nuevo módulo `core/bytecode.py` con clases `BytecodeInstruction` y `BytecodeGenerator`
  - Arquitectura de pila (stack-based) con instrucciones: PUSH, LOAD, STORE, ADD, SUB, MUL, DIV, etc.
  - Salida en formato assembly con comentarios descriptivos
  - **NOTA**: Bytecode educativo, NO es JVM bytecode real
  - Tests completos: `tests/test_bytecode_generator.py` (10 tests, 100% passing)

- **Fase 6: Integración con UI**
  - Nueva pestaña "Código" en `ui/console_panel.py` con clase `CodeTab`
  - Botones "Ver TAC" y "Ver Bytecode" para alternar visualización
  - Botón "Guardar Código" para exportar a archivos .tac o .asm
  - Syntax highlighting para TAC y Bytecode (comentarios, labels, instrucciones)
  - Soporte de temas (dark/light) para código generado
  - Integración en métodos `_run_semantic()`, `_run_complete()` y `_run_codegen()` de `ui/app_ui.py`

- **Documentación**
  - Nuevo archivo `docs/ARQUITECTURA_CODEGEN.md` con diseño del pipeline de generación de código
  - Scripts de prueba: `test_ui_integration.py`, `test_global_statements.py`, `test_ui_global.py`

### Changed
- `core/controller.py` ahora incluye generadores TAC y Bytecode en el pipeline
- Resultado de compilación incluye campos: `codigo_intermedio`, `bytecode`, `tac`, `bytecode_instructions`
- Generación automática de TAC y Bytecode después del análisis semántico exitoso
- `ConsolePanel` ahora muestra estadísticas de código generado en la pestaña "Salida"
- `core/tac.py`: Agregado `loop_stack` para manejo de break/continue
- `core/tac.py`: `_generate_program()` ahora soporta sentencias globales

### Fixed
- Corrección de encoding en salida de tests (reemplazo de caracteres Unicode → ASCII)
- Corrección de atributo de tema: `button_hover_bg` → `button_hover`
- Bug en generación TAC: Código global (sin funciones) ahora se genera correctamente
- Bug en break/continue: Implementación correcta con loop_stack

### Project Status
- **v1.1.0 COMPLETADA** - Frontend + TAC + Bytecode Educativo
- **Próximo objetivo**: v2.0 - JVM Bytecode Real (.class files ejecutables)

---

## [1.0.1] - 2025-11-22

### Added - Validación Avanzada de Errores
- **Comentarios de bloque**: Soporte `/* */` con detección de comentarios sin cerrar
- **Validación de números**: Detección de múltiples puntos decimales, overflow y sufijos inválidos (L, f, F, d, D)
- **Validación de escape sequences**: Secuencias en strings (`\n`, `\t`, `\uXXXX`, `\k`, etc.)
- **Variables no inicializadas**: Detección de uso antes de asignación
- **Return path analysis**: Validación de que funciones no-Unit retornen en todos los caminos
- Documentación: `docs/errores_pendientes_implementacion.md`

### Changed
- Estructura `Simbolo` ahora incluye campo `inicializada` para tracking
- Variables de loop (`for`) y parámetros marcados como inicializados automáticamente
- Tests de errores ampliados: léxicos (+6 casos), semánticos (+3 casos, total 21)

### Fixed
- Inmutabilidad de `val` ahora se valida correctamente (ya estaba implementada, verificada)

---

## [1.0.0] - 2025-11-06

### 🎉 Lanzamiento de la Versión 1.0

Primera versión funcional del compilador KForge capaz de compilar algoritmos completos de Kotlin.

### Added
- Inferencia de tipo `Unit` para la función `main()` sin tipo de retorno explícito
- Test final v1.0 con algoritmo Bubble Sort completo
- Script de validación automática `tests/test_v1_final.py`
- Test unitario para `main()` sin tipo: `tests/test_main_sin_tipo.py`
- Documentación completa reorganizada:
  - `CONTRIBUTING.md` con reglas de desarrollo
  - `CHANGELOG.md` (este archivo)
  - `ROADMAP.md` simplificado y actualizado

### Changed
- Reorganizada documentación del proyecto
- ROADMAP.md ahora hace referencia a CONTRIBUTING.md para reglas de trabajo
- Versión actualizada a v1.0

### Fixed
- Bug en tamaño de fuente del resaltado de sintaxis ahora se sincroniza correctamente

### Removed
- Archivos de documentación obsoletos:
  - `INSTRUCCIONES.md` (duplicado con README)
  - `RESUMEN_PROYECTO.md` (duplicado con README)
  - `UI_MODERNA_README.md` (ya no relevante)
  - `REFACTORIZACION_UI.md` (documentación de proceso completado)
  - `analisis_test_final.md` (análisis temporal)

---

## [0.3.0] - 2025-11-05

### Added - Fase 3: Arrays y Propiedades
- Operador punto (`.`) para acceso a propiedades
- Propiedad `.size` para arrays (IntArray, DoubleArray)
- Propiedad `.length` para strings
- Función built-in `doubleArrayOf()` para crear arrays de Double
- Soporte para índices con expresiones aritméticas: `arr[j + 1]`
- Encadenamiento de propiedades: `array[0].size`
- Test completo de Fase 3: `test_kt/test_fase3.kt`
- Script de validación: `tests/test_fase3_directo.py`

### Changed
- Mejorado acceso a elementos de array con validación de tipos correcta
- Parser mejorado para manejar propiedades en rangos: `for (i in 0 until arr.size)`

### Fixed
- Validación de tipos para arrays: IntArray vs DoubleArray correctamente distinguidos

---

## [0.2.0] - 2025-11-04

### Added - Fase 2: Funciones y Llamadas
- Declaración de funciones con parámetros y tipos de retorno
- Llamadas a funciones con validación de tipos de argumentos
- Sentencia `return` con validación semántica
- Funciones built-in:
  - `println()` - Impresión con salto de línea
  - `print()` - Impresión sin salto de línea
  - `intArrayOf()` - Creación de arrays de enteros (varargs)
- Validación de tipos de retorno vs tipo declarado
- Tabla de funciones en analizador semántico
- Test completo de Fase 2: `test_kt/test_fase2.kt`
- Script de validación: `tests/test_fase2_directo.py`

### Changed
- Agregadas clases `Parametro` y `FuncionInfo` en `core/utils.py`
- Extendido analizador semántico con validación de funciones

---

## [0.1.0] - 2025-11-03

### Added - Fase 1: Fundamentos
- Análisis léxico completo (Lexer) con tokenización de Kotlin
- Análisis sintáctico completo (Parser) con generación de AST
- Análisis semántico con validación de tipos y scopes
- Variables con palabra clave `var`
- Tipos de datos: `Int`, `Double`, `String`, `Boolean`
- Operadores aritméticos: `+`, `-`, `*`, `/`, `%`
- Operadores de comparación: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Operadores lógicos: `&&`, `||`, `!`
- Operador unario: `-` (negativo)
- Estructuras de control:
  - `if`/`else` con bloques
  - `while` loops
  - `for..in..` loops con rangos
- Rangos con operadores `..` y `until`
- Sentencias `break` y `continue`
- Declaraciones sin inicialización: `var x: Int`
- Test completo de Fase 1: `test_kt/test_fase1.kt`
- Script de validación: `tests/test_fase1_directo.py`

### Added - Interfaz de Usuario
- Interfaz gráfica moderna con Tkinter
- Editor de código con resaltado de sintaxis para Kotlin
- Editor con pestañas para múltiples archivos
- Numeración de líneas sincronizada con scroll
- Consola multi-pestaña:
  - Pestaña de Salida
  - Pestaña de Errores
  - Pestaña de AST
  - Pestaña de Tokens
- Panel de configuración:
  - Selector de tema (Dark/Light)
  - Ajuste de tamaño de fuente
- Barra lateral con gestión de archivos
- Sistema de temas con `theme_manager.py`

---

## [0.0.1] - 2025-11-02

### Added
- Estructura inicial del proyecto
- Módulos del compilador:
  - `core/utils.py` - Definiciones de Token, NodoAST, TipoDato
  - `core/errors.py` - Sistema de manejo de errores
  - `core/controller.py` - Controlador principal
- Sistema de manejo de errores:
  - `LexicalError`
  - `SyntaxError`
  - `SemanticError`
  - `ErrorManager`
- Documentación inicial:
  - `README.md`
  - `ROADMAP.md` con plan de desarrollo
- Punto de entrada: `main_modern.py`

---

## Tipos de Cambios

- `Added` - Para nuevas características
- `Changed` - Para cambios en funcionalidad existente
- `Deprecated` - Para características que serán removidas
- `Removed` - Para características removidas
- `Fixed` - Para corrección de bugs
- `Security` - Para parches de seguridad

---

[1.0.0]: https://github.com/usuario/kforge/releases/tag/v1.0.0
[0.3.0]: https://github.com/usuario/kforge/releases/tag/v0.3.0
[0.2.0]: https://github.com/usuario/kforge/releases/tag/v0.2.0
[0.1.0]: https://github.com/usuario/kforge/releases/tag/v0.1.0
[0.0.1]: https://github.com/usuario/kforge/releases/tag/v0.0.1
