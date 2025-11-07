# Lista Completa de Errores Pendientes de Implementación

**Proyecto**: KForge - Compilador Kotlin Modular
**Versión Actual**: 1.0
**Fecha**: 2025-11-07

Este documento lista todos los errores que el compilador KForge **NO** detecta actualmente y que deberían ser implementados en futuras versiones.

---

## 📊 Resumen Ejecutivo

| Fase | Errores Implementados | Errores Pendientes | % Cobertura |
|------|----------------------|-------------------|-------------|
| **Léxica** | 2 tipos | 5 tipos | ~29% |
| **Sintáctica** | 15+ tipos | 5+ tipos | ~75% |
| **Semántica** | 12+ tipos | 8+ tipos | ~60% |

---

## 🔤 FASE LÉXICA - Errores Pendientes

### 1. Números con Formato Inválido

**Prioridad**: Alta
**Estado**: ❌ No implementado
**Descripción**: El lexer no valida el formato completo de los números

#### Casos no detectados:

```kotlin
// ERROR: Múltiples puntos decimales
var x: Double = 3.14.159  // Se tokeniza: 3.14, ., 159

// ERROR: Sufijos de tipo no soportados
var largo: Int = 100L     // Se tokeniza: 100, L (identificador)
var flotante: Double = 3.14f  // Se tokeniza: 3.14, f (identificador)

// ERROR: Número sin dígito antes del punto
var decimal: Double = .5  // Se tokeniza: ., 5

// ERROR: Notación hexadecimal no soportada
var hex: Int = 0xFF       // Se tokeniza: 0, xFF (identificador)
var octal: Int = 0o77     // Se tokeniza: 0, o77 (identificador)

// ERROR: Notación científica no soportada
var cientifico: Double = 1.5e10  // Se tokeniza: 1.5, e10 (identificador)
```

**Implementación requerida**:
- Validar que números Double tengan exactamente un punto decimal
- Rechazar sufijos de tipo si no están soportados
- Validar formato completo en el lexer o post-procesamiento

---

### 2. Comentarios de Bloque Sin Cerrar

**Prioridad**: Alta
**Estado**: ❌ No implementado (feature no soportada)
**Descripción**: El lexer solo soporta comentarios de línea `//`, no comentarios de bloque

#### Casos no detectados:

```kotlin
// ERROR: Comentario de bloque sin cerrar
/* Este es un comentario
   que nunca se cierra
var x: Int = 10

// ERROR: Comentario de bloque anidado sin cerrar
/* Comentario externo
   /* Comentario interno */
var y: Int = 20
```

**Implementación requerida**:
- Agregar soporte para comentarios de bloque `/* ... */`
- Detectar comentarios sin cerrar
- Opcionalmente: soportar anidamiento de comentarios

---

### 3. Secuencias de Escape Inválidas en Strings

**Prioridad**: Media
**Estado**: ❌ No implementado
**Descripción**: El lexer acepta cualquier secuencia `\X` sin validar

#### Casos no detectados:

```kotlin
// ERROR: Secuencia de escape no reconocida
var texto1: String = "Hola\kMundo"  // \k no es válido

// ERROR: Escape hexadecimal inválido
var texto2: String = "Valor\xZZ"    // \xZZ no es hex válido

// ERROR: Escape unicode incompleto
var texto3: String = "Unicode\u123" // \u requiere 4 dígitos
```

**Secuencias válidas en Kotlin**:
- `\t` (tab), `\n` (newline), `\r` (carriage return)
- `\"` (comillas), `\'` (apóstrofo), `\\` (backslash)
- `\$` (signo de dólar)
- `\uXXXX` (unicode con 4 dígitos hex)

**Implementación requerida**:
- Validar secuencias de escape después de tokenizar strings
- Reportar error léxico para secuencias no reconocidas

---

### 4. Secuencias de Operadores Inválidas

**Prioridad**: Baja
**Estado**: ⚠️ Parcialmente implementado
**Descripción**: Algunos operadores inválidos no se detectan correctamente

#### Casos no detectados:

```kotlin
// ERROR: Operador de comparación de VB
var comp1: Boolean = x <> y  // Se tokeniza: <, >

// ERROR: Operador de asignación de Pascal
var x: Int := 10  // Se tokeniza: :, =
```

**Nota**: Los operadores `&` (sin `&&`) y `|` (sin `||`) ya se detectan correctamente.

**Implementación requerida**:
- Detectar secuencias problemáticas en el lexer
- O detectar en el parser cuando aparecen juntos

---

### 5. Literales de Carácter No Soportados

**Prioridad**: Baja
**Estado**: ❌ No implementado (feature no soportada)
**Descripción**: Kotlin soporta `'a'` para caracteres, pero KForge no

#### Casos no detectados:

```kotlin
// ERROR: Literal de carácter no soportado
var c: Char = 'a'  // Se tokeniza como error o identificador inválido
```

**Implementación requerida**:
- Agregar tipo `Char` al lenguaje
- Agregar patrón regex para literales de carácter
- Validar que solo contengan un carácter

---

## 🌳 FASE SINTÁCTICA - Errores Pendientes

### 6. Declaración de Función Sin Cuerpo ni '='

**Prioridad**: Media
**Estado**: ❌ No implementado
**Descripción**: El parser no valida si una función tiene cuerpo o expresión

#### Casos no detectados:

```kotlin
// ERROR: Función declarada pero sin implementación
fun calcular(x: Int): Int
// Debería dar error o requerir 'external' o similar

// En Kotlin válido sería:
fun calcular(x: Int): Int = x * 2  // Función de expresión
```

**Implementación requerida**:
- Validar que toda función tenga cuerpo `{ ... }` o expresión con `=`

---

### 7. Uso de 'val' Sin Validación de Inmutabilidad

**Prioridad**: Alta (si se soporta `val`)
**Estado**: ⚠️ Parcialmente implementado
**Descripción**: El lexer reconoce `val`, pero el parser no lo distingue de `var`

#### Casos no detectados:

```kotlin
// ERROR: Reasignación de val
val x: Int = 10
x = 20  // Debería dar error semántico
```

**Implementación requerida**:
- Diferenciar entre `var` (mutable) y `val` (inmutable) en el AST
- Agregar validación semántica de inmutabilidad

---

### 8. Expresiones con Precedencia Incorrecta

**Prioridad**: Baja
**Estado**: ⚠️ Necesita verificación
**Descripción**: Verificar que la precedencia de operadores es correcta

#### Casos a verificar:

```kotlin
// ¿Se parsea correctamente?
var resultado: Int = 10 + 5 * 2  // Debería ser 10 + (5 * 2) = 20

// ¿Y esto?
var comp: Boolean = x > 5 && y < 10  // (x > 5) && (y < 10)
```

**Implementación requerida**:
- Verificar tabla de precedencia en el parser
- Agregar tests específicos de precedencia

---

### 9. Parámetros con Valores por Defecto

**Prioridad**: Baja
**Estado**: ❌ No implementado (feature no soportada)
**Descripción**: Kotlin permite parámetros con valores por defecto

#### Casos no detectados:

```kotlin
// ERROR: Valor por defecto en parámetro
fun saludar(nombre: String = "Usuario"): String {
    return "Hola " + nombre
}
```

**Implementación requerida**:
- Agregar soporte sintáctico para `param: Type = defaultValue`
- Validar semánticamente que el valor por defecto sea del tipo correcto

---

### 10. Expresiones Lambda y Funciones Anónimas

**Prioridad**: Baja (feature v2.0)
**Estado**: ❌ No implementado
**Descripción**: Kotlin soporta lambdas, pero KForge no

#### Casos no detectados:

```kotlin
// ERROR: Lambda no soportada
var suma: (Int, Int) -> Int = { a, b -> a + b }

// ERROR: Función anónima
var cuadrado = fun(x: Int): Int { return x * x }
```

**Implementación requerida**:
- Agregar sintaxis de tipos funcionales
- Parsear expresiones lambda
- Validar semánticamente

---

## ✔️ FASE SEMÁNTICA - Errores Pendientes

### 11. Variable Usada Antes de Ser Inicializada

**Prioridad**: Alta
**Estado**: ❌ No implementado completamente
**Descripción**: Se permite declarar sin inicializar, pero no se valida uso posterior

#### Casos no detectados:

```kotlin
fun test() {
    var x: Int  // Declarada pero no inicializada
    var y: Int = x + 5  // ERROR: 'x' no tiene valor
}

fun test2() {
    var contador: Int
    if (true) {
        contador = 10
    }
    println(contador)  // ERROR: podría no estar inicializada
}
```

**Implementación requerida**:
- Rastrear estado de inicialización de variables por scope
- Validar flujo de control (if, while) para asegurar inicialización
- Reportar error si se usa variable sin inicializar

---

### 12. Operación de Módulo con Double

**Prioridad**: Media
**Estado**: ❌ No implementado
**Descripción**: Kotlin permite `%` con Double, pero podría no estar validado

#### Casos a verificar:

```kotlin
// ¿Esto da error actualmente?
var x: Double = 10.5
var y: Double = 3.0
var resto: Double = x % y  // En Kotlin es válido, ¿en KForge?
```

**Implementación requerida**:
- Verificar si el operador `%` está permitido para Double
- Si no, reportar error semántico

---

### 13. Type Casting y Conversiones

**Prioridad**: Media
**Estado**: ❌ No implementado (feature no soportada)
**Descripción**: No hay forma de convertir entre tipos

#### Casos no detectados:

```kotlin
// ERROR: No hay forma de convertir Int a Double
var entero: Int = 10
var decimal: Double = entero  // Debería dar error o requerir conversión

// En Kotlin se haría:
var decimal: Double = entero.toDouble()
```

**Implementación requerida**:
- Agregar funciones de conversión (`.toInt()`, `.toDouble()`, etc.)
- O agregar casting explícito `(Double)entero`
- Validar compatibilidad de tipos

---

### 14. Sobrecarga de Funciones

**Prioridad**: Baja
**Estado**: ❌ No implementado (feature no soportada)
**Descripción**: No se puede tener múltiples funciones con mismo nombre

#### Casos no detectados:

```kotlin
// ERROR: Sobrecarga no soportada
fun sumar(a: Int, b: Int): Int {
    return a + b
}

fun sumar(a: Double, b: Double): Double {
    return a + b
}
```

**Implementación requerida**:
- Modificar tabla de funciones para soportar sobrecarga
- Validar que las firmas sean diferentes
- Resolver llamadas basándose en tipos de argumentos

---

### 15. Validación de Rango de Valores

**Prioridad**: Baja
**Estado**: ❌ No implementado
**Descripción**: No se valida si los valores literales están en rango

#### Casos no detectados:

```kotlin
// ERROR: Int overflow (si Int es 32-bit)
var grande: Int = 9999999999999  // Fuera de rango de Int32

// ERROR: Índice negativo en array
var arr: IntArray = intArrayOf(1, 2, 3)
var x: Int = arr[-1]  // Debería dar error
```

**Implementación requerida**:
- Validar rangos de Int y Double en tiempo de compilación
- Validar índices de array (al menos negativos)

---

### 16. Detección de Código Inalcanzable

**Prioridad**: Baja (warning, no error)
**Estado**: ❌ No implementado
**Descripción**: No se detecta código después de return, break, continue

#### Casos no detectados:

```kotlin
fun test(): Int {
    return 42
    var x: Int = 10  // WARNING: Código inalcanzable
}

fun test2() {
    while (true) {
        break
        println("Nunca se ejecuta")  // WARNING: Código inalcanzable
    }
}
```

**Implementación requerida**:
- Analizar flujo de control en funciones y loops
- Reportar warning (no error) para código inalcanzable

---

### 17. Validación de Return en Todas las Rutas

**Prioridad**: Alta
**Estado**: ❌ No implementado
**Descripción**: No se valida que funciones no-Unit retornen en todas las rutas

#### Casos no detectados:

```kotlin
// ERROR: No todos los caminos retornan un valor
fun absoluto(x: Int): Int {
    if (x > 0) {
        return x
    }
    // Falta return en el caso x <= 0
}

fun mayorQue(a: Int, b: Int): Boolean {
    if (a > b) {
        return true
    } else if (a < b) {
        return false
    }
    // Falta return cuando a == b
}
```

**Implementación requerida**:
- Analizar todas las rutas de ejecución en funciones
- Validar que todas retornen valor (excepto Unit)
- Reportar error si alguna ruta no tiene return

---

### 18. Validación de Parámetros Named y Orden

**Prioridad**: Baja (feature no soportada)
**Estado**: ❌ No implementado
**Descripción**: Kotlin permite parámetros nombrados, KForge no

#### Casos no detectados:

```kotlin
fun crear(nombre: String, edad: Int, activo: Boolean): String {
    return nombre
}

// ERROR: Parámetros nombrados no soportados
var resultado: String = crear(edad = 25, nombre = "Juan", activo = true)
```

**Implementación requerida**:
- Agregar soporte para parámetros nombrados en llamadas
- Validar que los nombres existan
- Permitir orden arbitrario

---

## 📋 Resumen por Prioridad

### Prioridad Alta (Implementar en v1.1)

1. ✅ **Números con múltiples puntos decimales** (Léxica)
2. ✅ **Comentarios de bloque sin cerrar** (Léxica)
3. ✅ **Variable usada antes de inicializar** (Semántica)
4. ✅ **Return en todas las rutas** (Semántica)
5. ✅ **Soporte completo de `val`** (Sintáctica/Semántica)

### Prioridad Media (Implementar en v1.2)

6. ⚠️ **Secuencias de escape en strings** (Léxica)
7. ⚠️ **Función sin cuerpo** (Sintáctica)
8. ⚠️ **Módulo con Double** (Semántica)
9. ⚠️ **Type casting** (Semántica)

### Prioridad Baja (v2.0+)

10. 📝 **Sufijos de tipo en números** (Léxica)
11. 📝 **Literales de carácter** (Léxica)
12. 📝 **Precedencia de operadores** (Sintáctica)
13. 📝 **Valores por defecto** (Sintáctica)
14. 📝 **Lambdas** (Sintáctica/Semántica)
15. 📝 **Sobrecarga de funciones** (Semántica)
16. 📝 **Validación de rangos** (Semántica)
17. 📝 **Código inalcanzable** (Semántica - warning)
18. 📝 **Parámetros nombrados** (Semántica)

---

## 🎯 Plan de Acción Recomendado

### Para v1.1 (Próxima versión)

1. Implementar validación de inicialización de variables
2. Agregar validación de return en todas las rutas
3. Implementar distinción completa entre `var` y `val`
4. Agregar validación de números con formato inválido
5. Agregar soporte para comentarios de bloque

### Para v1.2

6. Implementar validación de secuencias de escape
7. Agregar soporte para type casting básico
8. Mejorar mensajes de error con sugerencias

### Para v2.0

9. Implementar características avanzadas (lambdas, sobrecarga, etc.)
10. Agregar análisis de flujo más complejo
11. Implementar sistema de warnings además de errores

---

**Última actualización**: 2025-11-07
**Mantenido por**: Gabriel Alejandro Medina Miramontes
**Proyecto**: KForge v1.0
