# 🔨 KForge - Compilador Kotlin

<div align="center">

**Compilador modular y extensible para el lenguaje Kotlin**

*Desarrollado en Python con interfaz gráfica Tkinter*

**Versión 1.0** - ¡Primera versión funcional! 🎉

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Kotlin](https://img.shields.io/badge/Kotlin-Subset-purple.svg)](https://kotlinlang.org/)
[![License](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](LICENSE)

</div>

---

## 📋 Descripción

KForge es un **compilador modular** para el lenguaje Kotlin que implementa las fases fundamentales del proceso de compilación: análisis léxico, sintáctico y semántico. Diseñado con una arquitectura limpia y modular, puede compilar algoritmos completos como Bubble Sort.

### 🎯 Versión 1.0 - Características Principales

El compilador KForge v1.0 puede compilar exitosamente:
- ✅ **Variables y tipos básicos** (Int, Double, String, Boolean)
- ✅ **Operadores** (aritméticos, lógicos, comparación)
- ✅ **Estructuras de control** (if/else, for, while, break, continue)
- ✅ **Funciones** (declaración, parámetros, retorno, llamadas)
- ✅ **Arrays tipados** (IntArray, DoubleArray)
- ✅ **Propiedades** (.size para arrays, .length para strings)
- ✅ **Algoritmos completos** (test final: Bubble Sort)

---

## ✨ Características

### Compilador
- 🔤 **Análisis Léxico**: Tokenización completa de Kotlin
- 🌳 **Análisis Sintáctico**: Generación de AST (Árbol Sintáctico Abstracto)
- ✔️ **Análisis Semántico**: Validación de tipos, scopes y tabla de símbolos
- 📊 **Soporte de Kotlin**:
  - Fase 1: Fundamentos (variables, operadores, estructuras de control)
  - Fase 2: Funciones (declaración, llamadas, parámetros, retorno)
  - Fase 3: Arrays y Propiedades (arrays tipados, acceso, propiedades)

### Interfaz de Usuario
- 🎨 **UI Moderna**: Diseño tipo JetBrains/VSCode
- 📝 **Editor con Pestañas**: Múltiples archivos simultáneos
- 🎨 **Resaltado de Sintaxis**: Para Kotlin con temas personalizables
- 📊 **Consola Multi-pestaña**: Salida, Errores, AST, Tokens
- 🌓 **Temas**: Dark (Darcula) y Light
- ⚙️ **Configuración**: Tamaño de fuente ajustable
- 📏 **Numeración de Líneas**: Sincronizada con scroll

---

## 🚀 Inicio Rápido

### Requisitos

- Python 3.8 o superior
- Tkinter (incluido en la mayoría de instalaciones de Python)

### Instalación y Ejecución

```bash
# Clonar o descargar el proyecto
cd KForge

# Ejecutar el compilador
python main_modern.py
```

### Ejecutar Tests

```bash
# Test individual de fase
python tests/test_fase1_directo.py
python tests/test_fase2_directo.py
python tests/test_fase3_directo.py

# Test final v1.0 (Bubble Sort)
python tests/test_v1_final.py
```

---

## 📖 Documentación

- 📘 **[README.md](README.md)** (este archivo) - Inicio rápido y características
- 🗺️ **[ROADMAP.md](ROADMAP.md)** - Plan de desarrollo y estado actual
- 📋 **[CONTRIBUTING.md](CONTRIBUTING.md)** - Reglas de trabajo y desarrollo
- 📝 **[CHANGELOG.md](CHANGELOG.md)** - Historial de cambios por versión

---

## 📂 Estructura del Proyecto

```
KForge/
├── core/                         # Módulos del compilador
│   ├── __init__.py
│   ├── lexer.py                  # Analizador léxico
│   ├── parser.py                 # Analizador sintáctico
│   ├── semantic.py               # Analizador semántico
│   ├── controller.py             # Controlador principal
│   ├── errors.py                 # Sistema de manejo de errores
│   ├── utils.py                  # Definiciones (Token, AST, TipoDato)
│   └── codegen.py                # Generación de código (futuro)
├── ui/                           # Interfaz gráfica moderna
│   ├── __init__.py
│   ├── app_ui.py                 # Aplicación principal
│   ├── editor_panel.py           # Editor con pestañas
│   ├── console_panel.py          # Consola multi-pestaña
│   ├── sidebar.py                # Barra lateral
│   ├── theme_manager.py          # Gestión de temas
│   ├── phases_panel.py           # Panel de fases
│   ├── status_bar.py             # Barra de estado
│   └── splash_screen.py          # Pantalla de inicio
├── test_kt/                      # Tests en Kotlin
│   ├── test_fase1.kt             # Test Fase 1
│   ├── test_fase2.kt             # Test Fase 2
│   ├── test_fase3.kt             # Test Fase 3
│   └── test_v1_final.kt          # Test final (Bubble Sort)
├── tests/                        # Scripts de test Python
│   ├── test_compilador.py        # Test general CLI
│   ├── test_fase1_directo.py     # Test Fase 1
│   ├── test_fase2_directo.py     # Test Fase 2
│   ├── test_fase3_directo.py     # Test Fase 3
│   ├── test_main_sin_tipo.py     # Test main() sin tipo
│   └── test_v1_final.py          # Test final v1.0
├── main_modern.py                # Punto de entrada de la aplicación
├── README.md                     # Este archivo
├── ROADMAP.md                    # Plan de desarrollo
├── CONTRIBUTING.md               # Guía de contribución
├── CHANGELOG.md                  # Historial de cambios
└── LICENSE                       # Licencia del proyecto
```

---

## 💡 Uso

### Interfaz Gráfica

1. **Abrir**: `python main_modern.py`
2. **Escribir código Kotlin** en el editor
3. **Compilar**: Usar botón "Compilar" o `Ctrl+Enter`
4. **Ver resultados**: En las pestañas de la consola

### Atajos de Teclado

| Atajo | Acción |
|-------|--------|
| `Ctrl + N` | Nuevo archivo |
| `Ctrl + O` | Abrir archivo |
| `Ctrl + S` | Guardar |
| `Ctrl + Shift + S` | Guardar como |
| `Ctrl + Enter` | Compilar |

### Uso Programático

```python
from core.controller import CompiladorController
from core.errors import ErrorManager

# Crear controlador
error_manager = ErrorManager()
controlador = CompiladorController(error_manager)

# Código Kotlin
codigo = """
fun main() {
    var arr: IntArray = intArrayOf(3, 1, 2)
    var n: Int = arr.size
    println("Array creado")
}
"""

# Ejecutar compilación
exito = controlador.ejecutar_completo(codigo)

# Verificar resultados
if error_manager.tiene_errores():
    for error in error_manager.errores:
        print(error)
else:
    print("Compilación exitosa!")
```

---

## 🎯 Sintaxis Soportada

### Variables y Tipos

```kotlin
// Variables mutables
var edad: Int = 25
var precio: Double = 19.99
var nombre: String = "KForge"
var activo: Boolean = true

// Sin inicialización
var contador: Int
```

### Operadores

```kotlin
// Aritméticos: + - * / %
var suma: Int = 10 + 5
var resta: Int = 10 - 5

// Comparación: == != < > <= >=
var mayor: Boolean = 10 > 5

// Lógicos: && || !
var resultado: Boolean = true && false
```

### Estructuras de Control

```kotlin
// If-Else
if (edad >= 18) {
    println("Mayor de edad")
} else {
    println("Menor de edad")
}

// While
var i: Int = 0
while (i < 10) {
    i = i + 1
}

// For con rangos
for (i in 0..10) {
    println(i)
}

for (i in 0 until 10) {
    println(i)
}

// Break y Continue
for (i in 0..10) {
    if (i == 5) break
    if (i == 3) continue
    println(i)
}
```

### Funciones

```kotlin
// Función con retorno explícito
fun suma(a: Int, b: Int): Int {
    return a + b
}

// Función main sin tipo de retorno
fun main() {
    var resultado: Int = suma(5, 3)
    println(resultado)
}

// Funciones built-in
println("Hola Mundo")
print("Sin salto de línea")
```

### Arrays y Propiedades

```kotlin
// Crear arrays
var numeros: IntArray = intArrayOf(1, 2, 3, 4, 5)
var decimales: DoubleArray = doubleArrayOf(1.5, 2.5, 3.5)

// Acceso a elementos
var primero: Int = numeros[0]
numeros[1] = 10

// Propiedades
var tamano: Int = numeros.size
var longitud: Int = "Hola".length

// Uso en expresiones
for (i in 0 until numeros.size) {
    println(numeros[i])
}
```

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

---

## 🏗️ Arquitectura

### Principios de Diseño

1. **Separación de Responsabilidades**: UI desacoplada de la lógica del compilador
2. **Modularidad**: Cada fase es independiente
3. **Extensibilidad**: Fácil añadir nuevas características
4. **Manejo Centralizado de Errores**: Todos los errores usan `ErrorManager`

### Flujo de Compilación

```
Código Kotlin
    ↓
[Análisis Léxico] → Tokens
    ↓
[Análisis Sintáctico] → AST
    ↓
[Análisis Semántico] → Validación de Tipos
    ↓
✅ Compilación Exitosa
```

---

## 🧪 Tests

### Ejecutar Todos los Tests

```bash
# Fase 1: Fundamentos
python tests/test_fase1_directo.py

# Fase 2: Funciones
python tests/test_fase2_directo.py

# Fase 3: Arrays y Propiedades
python tests/test_fase3_directo.py

# Test final v1.0
python tests/test_v1_final.py
```

### Resultado Esperado

```
Total de errores: 0
✓ ¡VERSIÓN 1.0 DEL COMPILADOR COMPLETADA!
```

---

## 🚧 Limitaciones Actuales

La versión 1.0 NO incluye:
- ❌ String templates (`"Resultado: ${x}"`)
- ❌ Método `.joinToString()` para arrays
- ❌ Inmutabilidad completa con `val`
- ❌ When expression
- ❌ Null safety (`?`, `!!`, `?.`)
- ❌ Lambdas y funciones de orden superior
- ❌ Clases y objetos (POO)
- ❌ Generación de código ejecutable

**Ver [ROADMAP.md](ROADMAP.md) para plan de versión 1.1+**

---

## 🔮 Futuras Mejoras

### Versión 1.1 (Planeada)
- [ ] String templates con interpolación
- [ ] Método `.joinToString()` para arrays
- [ ] Soporte completo de `val` con inmutabilidad
- [ ] When expression

### Versión 2.0 (Futuro)
- [ ] Null safety básico
- [ ] Lambdas y funciones anónimas
- [ ] Clases y objetos (POO básica)
- [ ] Generación de código Python

---

## 🤝 Contribuciones

Para contribuir al proyecto:

1. Lee [CONTRIBUTING.md](CONTRIBUTING.md) para reglas de trabajo
2. Revisa [ROADMAP.md](ROADMAP.md) para características planeadas
3. Ejecuta todos los tests antes de hacer commit
4. Sigue el formato de commits: `tipo(scope): descripción`

---

## 📄 Licencia

**GNU General Public License v3.0 (GPL-3.0)**

Este proyecto está licenciado bajo la GNU General Public License v3.0. Esto significa que:

- ✅ Puedes usar el código libremente
- ✅ Puedes modificar el código
- ✅ Puedes distribuir el código
- ⚠️ **PERO**: Cualquier trabajo derivado DEBE ser de código abierto bajo la misma licencia
- ⚠️ **PERO**: Debes mantener los créditos del autor original
- ⚠️ **PERO**: Debes compartir tus modificaciones bajo GPL-3.0

Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👤 Autor

**Gabriel Alejandro Medina Miramontes**

Creador y desarrollador principal de KForge.

Compilador modular de Kotlin desarrollado para demostrar implementación profesional de lenguajes de programación.

---

## 🙏 Agradecimientos

- Documentación oficial de Kotlin
- Comunidad de compiladores y lenguajes de programación
- Recursos sobre compiladores (Dragon Book, Crafting Interpreters)

---

<div align="center">

**KForge v1.0** - Compilador Kotlin Modular

*Hecho con ❤️ usando Python y Tkinter*

[Reportar Bug](https://github.com/usuario/kforge/issues) · [Solicitar Característica](https://github.com/usuario/kforge/issues) · [Documentación](ROADMAP.md)

</div>
