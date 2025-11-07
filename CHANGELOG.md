# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

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
