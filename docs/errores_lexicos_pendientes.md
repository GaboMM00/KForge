# Análisis de Detección de Errores Léxicos

## Estado Actual del Lexer

El analizador léxico actual de KForge utiliza expresiones regulares para tokenizar el código Kotlin. La detección de errores léxicos está limitada a:

### ✅ Errores Actualmente Detectados

1. **Caracteres no reconocidos (MISMATCH)**: Cualquier carácter que no coincida con ningún patrón definido
   - Ejemplo: `@`, `#`, `$`, `~`, `^`, `` ` ``
   - Detección: Token `MISMATCH` → `LexicalError`

2. **Strings sin cerrar**: El patrón regex `r'"([^"\\]|\\.)*"'` requiere que el string esté cerrado
   - Ejemplo: `var x: String = "hola` (sin comillas de cierre)
   - Detección: El carácter `"` se trata como MISMATCH después de procesar el resto

### ❌ Errores Léxicos NO Detectados (Pendientes de Implementación)

#### 1. Números con Formato Inválido
**Estado**: No detectado
**Razón**: El regex acepta cualquier secuencia de dígitos o dígitos con punto
**Casos problemáticos**:
- `3.14.159` (múltiples puntos decimales) → Se tokeniza como `3.14`, `.`, `159`
- `100L` (sufijos de tipo) → Se tokeniza como `100` y `L` (identificador)
- `0xFF` (hexadecimal) → Se tokeniza como `0` y `xFF` (identificador)
- `.5` (sin dígito antes del punto) → Se tokeniza como `.` y `5`

**Implementación requerida**:
- Validar que los números Double tengan exactamente un punto decimal
- Rechazar sufijos de tipo (`L`, `f`, `F`, `d`, `D`)
- Rechazar notación hexadecimal/octal si no está soportada
- Validar formato completo de números

#### 2. Identificadores Inválidos
**Estado**: No detectado
**Razón**: El regex `r'[a-zA-Z_][a-zA-Z0-9_]*'` solo acepta identificadores válidos
**Casos problemáticos**:
- `123variable` → Se tokeniza como `123` (número) y `variable` (identificador)
- `mi-variable` → Se tokeniza como `mi`, `-`, `variable`
- `mi$variable` → Se tokeniza como `mi`, `$` (MISMATCH), `variable`

**Nota**: Estos casos ya son manejados correctamente por el lexer (se tokeniza en partes separadas), pero no se reportan como error léxico explícito.

#### 3. Operadores Compuestos Incompletos
**Estado**: Parcialmente detectado
**Casos**:
- `x & y` (solo `&` en vez de `&&`) → Se detecta como MISMATCH ✅
- `x | y` (solo `|` en vez de `||`) → Se detecta como MISMATCH ✅
- `x := y` (operador Pascal) → `:` se tokeniza, `=` se tokeniza por separado
- `x <> y` (operador VB) → Se tokeniza como `<`, `>` ❌

**Implementación requerida**:
- Detectar secuencias de operadores inválidas (`<>`, `:=`, etc.)

#### 4. Comentarios de Bloque Sin Cerrar
**Estado**: No soportado
**Razón**: El lexer solo soporta comentarios de línea (`//`)
**Casos problemáticos**:
- `/* comentario sin cerrar` → No se reconoce, se tokeniza como operadores

**Implementación requerida**:
- Agregar soporte para comentarios de bloque `/* ... */`
- Detectar comentarios de bloque sin cerrar

#### 5. Caracteres de Escape Inválidos en Strings
**Estado**: No detectado
**Razón**: El regex acepta cualquier secuencia de escape `\\.`
**Casos problemáticos**:
- `"Hola\xMundo"` (escape hexadecimal inválido) → Se acepta sin validación
- `"Test\k"` (escape desconocido) → Se acepta sin validación

**Implementación requerida**:
- Validar secuencias de escape en strings (`\n`, `\t`, `\"`, `\\`, etc.)
- Rechazar secuencias de escape no reconocidas

#### 6. Espacios en Identificadores
**Estado**: Detectado indirectamente
**Razón**: Los espacios se tratan como WHITESPACE, separando tokens
**Casos**:
- `var mi variable: Int` → Se tokeniza como `var`, `mi`, `variable`, `:`, `Int`

**Nota**: Este caso ya es manejado correctamente por el parser (error sintáctico), no requiere cambio en lexer.

## Resumen de Implementación Pendiente

### Prioridad Alta
1. ✅ Caracteres no reconocidos (ya implementado)
2. ❌ Números con múltiples puntos decimales
3. ❌ Comentarios de bloque sin cerrar

### Prioridad Media
4. ❌ Secuencias de escape inválidas en strings
5. ❌ Sufijos de tipo en números (si no están soportados)

### Prioridad Baja
6. ❌ Secuencias de operadores inválidas (la mayoría ya detectadas)
7. ✅ Identificadores inválidos (ya manejado correctamente)

## Recomendaciones

1. **Para números inválidos**: Agregar validación post-regex para verificar formato
2. **Para comentarios de bloque**: Agregar patrón regex para `/* ... */` y validar cierre
3. **Para secuencias de escape**: Procesar y validar contenido de strings después de extraerlos
4. **Para testing**: El test actual debería enfocarse en errores que YA están implementados

## Test Actual vs Realidad

El archivo `test_errores_lexicos.kt` contiene 15 tipos de errores, pero el lexer actual solo detecta 3-4 de ellos. Se recomienda:
- Crear un test realista con solo los errores que el lexer detecta
- Documentar los errores pendientes de implementación
- Implementar gradualmente la detección de más errores léxicos
