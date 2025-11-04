# KForge - Compilador Kotlin

<div align="center">

**Compilador modular y extensible para el lenguaje Kotlin**

*Desarrollado en Python con interfaz gráfica Tkinter*

</div>

---

## 📋 Descripción

KForge es un compilador modular para el lenguaje Kotlin que implementa las fases fundamentales del proceso de compilación: análisis léxico, sintáctico y semántico. Diseñado con una arquitectura limpia y desacoplada, permite la fácil extensión y modificación de reglas del lenguaje.

## ✨ Características

- ✅ **Análisis Léxico**: Tokenización del código fuente con detección de errores
- ✅ **Análisis Sintáctico**: Generación de AST (Árbol Sintáctico Abstracto)
- ✅ **Análisis Semántico**: Verificación de tipos y símbolos
- 🔜 **Generación de Código Intermedio**: Preparado para implementación futura
- 🎨 **Dos Interfaces Gráficas**:
  - **Clásica**: Editor simple y funcional (legacy)
  - **Moderna**: Interfaz modular tipo JetBrains/VSCode ⭐ **NUEVO**
- 🏗️ **Arquitectura Modular**: Fácil extensión y mantenimiento
- 🔍 **Resaltado de Sintaxis**: Avanzado con keywords.json compartido
- 🌍 **Multilenguaje**: Español e Inglés
- 🎨 **Temas**: Oscuro (Darcula) y Claro

## 🚀 Instalación y Ejecución

### Requisitos

- Python 3.8 o superior
- Tkinter (incluido en la mayoría de instalaciones de Python)

### Ejecución

```bash
# Clonar o descargar el proyecto
cd KForge

# Interfaz MODERNA (recomendada) ⭐
python main_modern.py

# Interfaz CLÁSICA (legacy)
python main.py
```

### Estructura del Proyecto

```
KForge/
├── main.py                      # Punto de entrada (interfaz clásica)
├── main_modern.py              # Punto de entrada (interfaz moderna) ⭐
├── core/                        # Lógica del compilador
│   ├── __init__.py
│   ├── controller.py            # Controlador principal
│   ├── lexer.py                 # Analizador léxico
│   ├── parser.py                # Analizador sintáctico
│   ├── semantic.py              # Analizador semántico
│   ├── codegen.py               # Generación de código (placeholder)
│   ├── errors.py                # Manejo de errores
│   └── utils.py                 # Utilidades y estructuras de datos
├── ui/                          # Interfaces gráficas
│   ├── __init__.py
│   ├── app_ui.py                # 🆕 Aplicación moderna integrada
│   ├── theme_manager.py         # 🆕 Gestión de temas y lenguajes
│   ├── editor_panel.py          # 🆕 Editor con pestañas
│   ├── console_panel.py         # 🆕 Consola multi-pestaña
│   ├── sidebar.py               # 🆕 Barra lateral tipo VSCode
│   ├── phases_panel.py          # 🆕 Panel de fases animado
│   ├── status_bar.py            # 🆕 Barra de estado
│   ├── splash_screen.py         # 🆕 Pantalla de inicio
│   ├── interfaz.py              # Interfaz clásica (legacy)
│   ├── editor.py                # Editor clásico (legacy)
│   └── consola.py               # Consola clásica (legacy)
├── resources/                   # 🆕 Recursos compartidos
│   ├── keywords.json            # 🆕 Palabras clave y colores
│   └── lang.json                # 🆕 Traducciones ES/EN
├── tests/                       # Archivos de prueba
│   └── ejemplo_kotlin.txt       # Código Kotlin de ejemplo
├── README.md                    # Este archivo
└── UI_MODERNA_README.md        # 🆕 Documentación de UI moderna
```

## 📖 Uso

### Interfaz Moderna (Recomendada) ⭐

1. **Abrir**: `python main_modern.py`
2. **Características exclusivas**:
   - Splash screen animado al inicio
   - Editor con pestañas para múltiples archivos
   - Consola con 4 pestañas (Salida, Errores, Tokens, AST)
   - Panel de fases con animaciones
   - Barra lateral tipo VSCode
   - Barra de estado con info en tiempo real
   - Temas oscuro/claro
   - Soporte multilenguaje (ES/EN)

**Ver documentación completa**: [UI_MODERNA_README.md](UI_MODERNA_README.md)

### Interfaz Clásica (Legacy)

1. **Abrir**: `python main.py`
2. **Escribir código**: En el editor superior
3. **Compilar**: Usar el menú `Compilador` o atajos de teclado
4. **Ver resultados**: En la consola inferior

### Atajos de Teclado

| Atajo | Acción |
|-------|--------|
| `Ctrl + N` | Nuevo archivo |
| `Ctrl + O` | Abrir archivo |
| `Ctrl + S` | Guardar |
| `Ctrl + Shift + S` | Guardar como |
| `F5` | Análisis Léxico |
| `F6` | Análisis Sintáctico |
| `F7` | Análisis Semántico |
| `F8` | Compilación Completa |
| `F9` | Código Intermedio |

### Uso Programático

```python
from core.controller import CompiladorController

# Crear controlador
controlador = CompiladorController()

# Código Kotlin
codigo = """
var a: Int = 5
var b: Int = 10
if (a < b) {
    a = a + 1
}
"""

# Ejecutar compilación
resultado = controlador.ejecutar(codigo)

# Verificar éxito
if resultado["exito"]:
    print("Compilación exitosa")
    print("Tokens:", resultado["tokens"])
    print("AST:", resultado["arbol"])
    print("Semántico:", resultado["semantico"])
else:
    print("Errores:", resultado["errores"])
```

## 🎯 Sintaxis Soportada

### Declaración de Variables

```kotlin
// Variable mutable
var nombre: Int = 10

// Variable inmutable
val PI: Double = 3.14
```

### Tipos de Datos

- `Int` - Enteros
- `Double` - Números decimales
- `String` - Cadenas de texto
- `Boolean` - Valores lógicos (true/false)

### Operadores

**Aritméticos**: `+`, `-`, `*`, `/`, `%`

**Comparación**: `==`, `!=`, `<`, `<=`, `>`, `>=`

**Asignación**: `=`

### Estructuras de Control

#### Condicional If-Else

```kotlin
if (a < b) {
    a = a + 1
} else {
    b = b - 1
}
```

#### Ciclo While

```kotlin
while (contador < 10) {
    contador = contador + 1
}
```

#### Ciclo For

```kotlin
for (i in 1..10) {
    suma = suma + i
}
```

### Comentarios

```kotlin
// Comentario de una línea
```

## 🏗️ Arquitectura

### Principios de Diseño

1. **Separación de Responsabilidades**: La interfaz está completamente desacoplada de la lógica del compilador
2. **Modularidad**: Cada fase (léxico, sintáctico, semántico) es independiente
3. **Extensibilidad**: Fácil añadir nuevas reglas gramaticales
4. **Manejo Centralizado de Errores**: Todos los errores pasan por `ErrorManager`

### Flujo de Compilación

```
Código Fuente
    ↓
[Análisis Léxico] → Tokens
    ↓
[Análisis Sintáctico] → AST
    ↓
[Análisis Semántico] → Validación
    ↓
[Generación de Código] → Código Intermedio (futuro)
```

### Componentes Principales

#### 1. Analizador Léxico (`lexer.py`)

- Convierte el código fuente en tokens
- Usa expresiones regulares para reconocer patrones
- Ignora espacios en blanco y comentarios

#### 2. Analizador Sintáctico (`parser.py`)

- Genera un AST a partir de los tokens
- Implementa gramática descendente recursiva
- Cada regla sintáctica es una función independiente

#### 3. Analizador Semántico (`semantic.py`)

- Verifica tipos de datos
- Valida declaración de variables
- Gestiona tabla de símbolos con scopes

#### 4. Controlador (`controller.py`)

- Coordina todas las fases
- Proporciona interfaz unificada
- Gestiona errores de todas las fases

## 🔧 Extensión del Compilador

### Añadir Nuevas Palabras Clave

1. Agregar en `core/utils.py` → `TipoToken`
2. Agregar en `core/lexer.py` → `PALABRAS_CLAVE`
3. Implementar regla en `core/parser.py`

### Añadir Nuevas Estructuras

```python
# En parser.py
def sentencia_when(self) -> NodoAST:
    """
    sentencia_when -> when ( expresion ) { caso* }
    """
    token_when = self.consumir(TipoToken.WHEN)
    # ... implementación
    return nodo
```

### Implementar Generación de Código

Modificar `core/codegen.py`:

```python
def generar(self, ast: NodoAST) -> str:
    self.limpiar()
    self.visitar(ast)
    return self.obtener_codigo()

def visitar(self, nodo: NodoAST):
    if nodo.tipo == TipoNodo.DECLARACION_VARIABLE:
        # Generar código para declaración
        pass
    # ... más casos
```

## 🧪 Pruebas

### Archivo de Ejemplo

Usar el archivo `tests/ejemplo_kotlin.txt` para probar todas las características soportadas.

### Ejecutar Pruebas

```bash
# Abrir archivo de prueba desde la interfaz
Archivo → Abrir → tests/ejemplo_kotlin.txt

# Ejecutar compilación completa
F8 o Compilador → Compilación Completa
```

## 📚 Ejemplos de Código

### Ejemplo 1: Variables y Operaciones

```kotlin
var a: Int = 10
var b: Int = 20
var resultado: Int = 0

resultado = a + b
resultado = resultado * 2
```

### Ejemplo 2: Condicionales

```kotlin
var edad: Int = 18

if (edad >= 18) {
    var mensaje: String = "Mayor de edad"
} else {
    var mensaje: String = "Menor de edad"
}
```

### Ejemplo 3: Ciclos

```kotlin
// Suma de 1 a 10
var suma: Int = 0
for (i in 1..10) {
    suma = suma + i
}

// Contador con while
var contador: Int = 0
while (contador < 5) {
    contador = contador + 1
}
```

## ⚠️ Limitaciones Actuales

- No soporta funciones definidas por el usuario
- No soporta arrays o colecciones
- No soporta clases u objetos
- No soporta imports
- Generación de código intermedio no implementada
- Sin optimizaciones

## 🚀 Mejoras Futuras

- [ ] Soporte para funciones (`fun`)
- [ ] Arrays y colecciones
- [ ] Clases y objetos
- [ ] Expresiones lambda
- [ ] Operador `when` (switch)
- [ ] Try-catch para manejo de excepciones
- [ ] Generación de bytecode o código intermedio
- [ ] Optimizaciones del compilador
- [ ] Mejor manejo de errores con sugerencias
- [ ] Autocompletado en el editor

## 🤝 Contribuciones

Este es un proyecto académico. Las sugerencias y mejoras son bienvenidas.

## 📄 Licencia

Proyecto académico - Uso educativo

## 👥 Autores

Desarrollado como proyecto de compiladores.

---

<div align="center">

**KForge** - Compilador Kotlin Modular

*Hecho con Python y Tkinter*

</div>
