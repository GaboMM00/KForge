# Instrucciones de Uso - KForge

## Inicio Rápido

### Ejecutar la Interfaz Gráfica

```bash
python main.py
```

Esto abrirá la ventana principal del compilador con:
- Editor de código con numeración de líneas
- Menú con todas las opciones
- Consola de resultados en la parte inferior

### Ejecutar Pruebas desde Línea de Comandos

**Prueba básica:**
```bash
python test_compilador.py
```

**Compilar un archivo:**
```bash
python test_compilador.py tests/ejemplo_kotlin.txt
```

## Uso de la Interfaz Gráfica

### 1. Escribir Código

Escriba su código Kotlin en el editor superior. Ejemplo:

```kotlin
var a: Int = 5
var b: Int = 10

if (a < b) {
    a = a + 1
}
```

### 2. Analizar el Código

Use el menú **Compilador** o los atajos de teclado:

- **F5** - Análisis Léxico (genera tokens)
- **F6** - Análisis Sintáctico (genera AST)
- **F7** - Análisis Semántico (verifica tipos y símbolos)
- **F8** - Compilación Completa (todas las fases)
- **F9** - Código Intermedio (placeholder)

### 3. Ver Resultados

Los resultados aparecerán en la consola inferior con código de colores:
- **Verde** - Éxito
- **Rojo** - Errores
- **Azul** - Información
- **Amarillo** - Advertencias

### 4. Abrir/Guardar Archivos

**Menú Archivo:**
- `Ctrl + O` - Abrir archivo
- `Ctrl + S` - Guardar
- `Ctrl + Shift + S` - Guardar como

## Ejemplos de Código Soportado

### Variables

```kotlin
// Variables mutables
var edad: Int = 25
var precio: Double = 19.99
var nombre: String = "Kotlin"
var activo: Boolean = true

// Variables inmutables (constantes)
val PI: Double = 3.14159
val MAX: Int = 100
```

### Operaciones Aritméticas

```kotlin
var a: Int = 10
var b: Int = 5

var suma: Int = a + b
var resta: Int = a - b
var multiplicacion: Int = a * b
var division: Int = a / b
var modulo: Int = a % b
```

### Condicionales

```kotlin
var edad: Int = 18

if (edad >= 18) {
    var mensaje: String = "Mayor de edad"
} else {
    var mensaje: String = "Menor de edad"
}
```

### Ciclos

**While:**
```kotlin
var contador: Int = 0

while (contador < 10) {
    contador = contador + 1
}
```

**For con rangos:**
```kotlin
var suma: Int = 0

for (i in 1..10) {
    suma = suma + i
}
```

### Estructuras Anidadas

```kotlin
var x: Int = 5

if (x > 0) {
    var y: Int = 10

    while (y > x) {
        y = y - 1

        if (y == 7) {
            y = y - 1
        }
    }
}
```

## Errores Comunes y Soluciones

### Error: Variable no declarada

```kotlin
// INCORRECTO
a = 10  // Error: variable 'a' no declarada

// CORRECTO
var a: Int = 10
```

### Error: Reasignación de constante

```kotlin
// INCORRECTO
val PI: Double = 3.14
PI = 3.14159  // Error: no se puede reasignar 'val'

// CORRECTO
var aproximacion: Double = 3.14
aproximacion = 3.14159
```

### Error: Tipo incompatible

```kotlin
// INCORRECTO
var numero: Int = 3.14  // Error: Double no compatible con Int

// CORRECTO
var numero: Double = 3.14
// o
var numero: Int = 3
```

### Error: Condición no booleana

```kotlin
// INCORRECTO
if (5) {  // Error: esperado Boolean
    // ...
}

// CORRECTO
if (5 > 0) {
    // ...
}
```

## Uso Programático (sin interfaz)

```python
from core.controller import CompiladorController

# Crear instancia del controlador
compilador = CompiladorController()

# Código a compilar
codigo = """
var x: Int = 10
var y: Int = 20
var z: Int = x + y
"""

# Ejecutar análisis completo
resultado = compilador.ejecutar(codigo)

# Verificar resultado
if resultado["exito"]:
    print("Compilacion exitosa!")
    print(f"Tokens: {len(resultado['tokens'])}")
    print(f"AST: {resultado['arbol']}")
else:
    print("Errores:")
    for error in resultado["errores"]:
        print(f"  - {error}")

# Obtener resumen completo
print(compilador.obtener_resumen_completo())
```

### Solo Análisis Léxico

```python
from core.controller import CompiladorController

compilador = CompiladorController()
resultado = compilador.ejecutar_lexico("var x: Int = 5")

for token in resultado["tokens"]:
    print(token)
```

### Solo Análisis Sintáctico

```python
from core.controller import CompiladorController

compilador = CompiladorController()
resultado = compilador.ejecutar_sintactico("var x: Int = 5")

print(resultado["arbol"])
```

## Estructura de Resultados

El método `ejecutar()` retorna un diccionario con:

```python
{
    "tokens": [Token, Token, ...],      # Lista de tokens
    "arbol": NodoAST,                    # Árbol sintáctico
    "semantico": ["info1", "info2"],     # Resultados semánticos
    "codigo_intermedio": "...",          # Código intermedio (futuro)
    "errores": ["error1", "error2"],     # Lista de errores
    "exito": True/False                  # Estado de la compilación
}
```

## Agregar Nuevas Características

### 1. Agregar Nueva Palabra Clave

**En `core/utils.py`:**
```python
class TipoToken(Enum):
    # ... existentes
    WHEN = auto()  # Nueva palabra clave
```

**En `core/lexer.py`:**
```python
PALABRAS_CLAVE = {
    # ... existentes
    'when': TipoToken.WHEN,
}
```

### 2. Agregar Nueva Regla Sintáctica

**En `core/parser.py`:**
```python
def sentencia_when(self) -> NodoAST:
    """
    sentencia_when -> when ( expresion ) { caso* }
    """
    token_when = self.consumir(TipoToken.WHEN)
    # Implementar lógica
    return nodo
```

### 3. Agregar Verificación Semántica

**En `core/semantic.py`:**
```python
def visitar_when(self, nodo: NodoAST):
    """Visita el nodo when."""
    # Implementar verificación
    pass
```

## Archivos de Prueba

- `tests/ejemplo_kotlin.txt` - Ejemplo completo con todas las características

## Solución de Problemas

### La interfaz no abre

Verificar que Tkinter está instalado:
```bash
python -m tkinter
```

### Caracteres extraños en consola de Windows

Usar el script de prueba en lugar de la interfaz:
```bash
python test_compilador.py
```

### Errores de importación

Asegurarse de ejecutar desde el directorio raíz del proyecto:
```bash
cd KForge
python main.py
```

## Contacto y Soporte

Para reportar errores o sugerencias, consultar el archivo README.md.
