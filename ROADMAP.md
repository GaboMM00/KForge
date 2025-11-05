# 🗺️ KForge Compiler - Roadmap de Desarrollo

**Compilador de Kotlin Educativo**
Versión actual: v0.1 - Fase 1 Completada ✅
Objetivo: Compilador de Kotlin casi completo

---

## 📋 INSTRUCCIONES PARA CONTINUAR EL PROYECTO

### 🎯 Para Cualquier Chat/Agente que Continue este Trabajo

**LEER ESTO PRIMERO ANTES DE HACER CUALQUIER COSA**

---

### 📖 1. ANÁLISIS OBLIGATORIO DEL PROYECTO

**Antes de empezar a implementar cualquier característica, DEBES**:

1. **Leer y comprender estos archivos en orden**:
   - `ROADMAP.md` (este archivo) - Entender el plan completo
   - `README.md` - Descripción general del proyecto
   - `core/utils.py` - Entender tokens, nodos AST y tipos de datos
   - `core/lexer.py` - Entender cómo funciona la tokenización
   - `core/parser.py` - Entender cómo se construye el AST
   - `core/semantic.py` - Entender la validación semántica
   - `core/controller.py` - Entender el flujo de compilación

2. **Verificar el estado actual**:
   - Revisar qué fase está completada (ver sección "Estado Actual" abajo)
   - Leer todos los tests en `test_kt/` para entender qué funciona
   - Ejecutar `python tests/test_fase1_directo.py` para confirmar que Fase 1 pasa

3. **Identificar la siguiente tarea**:
   - Ver la fase actual en la sección "Plan de Implementación"
   - Leer COMPLETAMENTE la descripción de la tarea antes de empezar
   - Entender qué archivos necesitas modificar

---

### 🗂️ 2. ESTRUCTURA DEL PROYECTO

```
KForge/
├── core/                    # Módulos del compilador
│   ├── lexer.py            # Analizador léxico (tokens)
│   ├── parser.py           # Analizador sintáctico (AST)
│   ├── semantic.py         # Analizador semántico (tipos, scopes)
│   ├── codegen.py          # Generador de código Python (futuro)
│   ├── utils.py            # Definiciones: Token, NodoAST, TipoDato, etc.
│   ├── errors.py           # Sistema de manejo de errores
│   └── controller.py       # Controlador principal del compilador
├── ui/                      # Interfaz gráfica Tkinter
│   ├── app_ui.py           # Ventana principal
│   ├── editor.py           # Editor de código con resaltado
│   ├── console.py          # Consola de salida
│   ├── sidebar.py          # Barra lateral funcional
│   └── theme_manager.py    # Gestión de temas
├── test_kt/                 # Tests con código Kotlin (.kt)
│   └── test_fase1.kt       # Test de características Fase 1
├── tests/                   # Tests Python y archivos de prueba
│   ├── test_fase1_directo.py       # Script Python para probar Fase 1
│   ├── test_compilador.py          # Script de prueba general
│   ├── ejemplo_kotlin.txt          # Código de ejemplo
│   ├── prueba_simple.txt           # Prueba simple
│   └── prueba_errores.txt          # Prueba de manejo de errores
├── main.py                  # Lanzador de la UI
└── ROADMAP.md              # Este archivo - plan completo
```

---

### ⚠️ 3. REGLAS IMPORTANTES

#### 📁 Regla de Organización de Tests

1. **Tests con código Kotlin** (`*.kt`) → Carpeta `test_kt/`
   - Ejemplo: `test_kt/test_fase1.kt`
   - Estos son archivos Kotlin que prueban características del lenguaje

2. **Scripts de test Python** (`test_*.py`) → Carpeta `tests/`
   - Ejemplo: `tests/test_fase1_directo.py`
   - Estos son scripts Python que ejecutan el compilador

3. **Archivos de prueba generales** (`*.txt`, datos) → Carpeta `tests/`
   - Ejemplo: `tests/ejemplo_kotlin.txt`
   - Archivos de entrada para pruebas

#### 🔧 Regla de Modificación de Archivos

**NUNCA modifiques archivos sin entender su propósito completo**

| Archivo | Cuándo Modificar | Qué Agregar |
|---------|------------------|-------------|
| `core/utils.py` | Al agregar tokens, nodos AST, o tipos | Enum entries en TipoToken, TipoNodo, TipoDato |
| `core/lexer.py` | Al agregar palabras clave u operadores | Palabras en PALABRAS_CLAVE y patrones regex |
| `core/parser.py` | Al implementar nueva sintaxis | Métodos de parseo para nuevas construcciones |
| `core/semantic.py` | Al agregar validación de tipos/scopes | Métodos `visitar_*` para nuevos nodos |
| `core/codegen.py` | Al implementar generación de código | Métodos para traducir AST a Python |

#### 🧪 Regla de Testing

**CADA característica implementada DEBE tener**:

1. Test en `test_kt/test_faseN.kt` - Código Kotlin que usa la característica
2. Script Python en `tests/test_faseN_directo.py` - Ejecuta el compilador y verifica
3. Verificación de 0 errores en las 3 fases: Léxico, Sintáctico, Semántico

#### 🚫 Regla de No Romper Código Existente

- Antes de hacer commit, ejecuta TODOS los tests de fases anteriores
- Si un test anterior falla, tu código tiene un bug
- NUNCA hagas commit si hay tests rotos

---

### 🔄 4. FLUJO DE TRABAJO PARA IMPLEMENTAR UNA CARACTERÍSTICA

**Ejemplo: Implementar operador `&&` (AND lógico)**

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
```python
# 1. core/utils.py
class TipoToken(Enum):
    AND = auto()  # Agregar aquí

# 2. core/lexer.py
ESPECIFICACION_TOKENS = [
    ('AND', r'&&'),  # Agregar antes de operadores simples
    ...
]

# 3. core/parser.py
def expresion_and(self):
    """Parsea expresiones con AND (&&)."""
    izquierda = self.expresion_comparacion()
    while self.token_actual and self.token_actual.tipo == TipoToken.AND:
        operador = self.token_actual
        self.avanzar()
        derecha = self.expresion_comparacion()
        nodo = NodoAST(
            tipo=TipoNodo.EXPRESION_BINARIA,
            valor='&&',
            hijos=[izquierda, derecha],
            linea=operador.linea,
            columna=operador.columna
        )
        izquierda = nodo
    return izquierda

# 4. core/semantic.py
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
```kotlin
// test_kt/test_fase1.kt
var a: Boolean = true
var b: Boolean = false
if (a && b) {
    // ...
}
```

```python
# tests/test_fase1_directo.py
codigo = """
var a: Boolean = true
var b: Boolean = false
if (a && b) {
    // ...
}
"""
# ... ejecutar compilador y verificar 0 errores
```

#### Paso 4: Ejecutar Tests
```bash
python tests/test_fase1_directo.py
```

#### Paso 5: Verificar Salida
```
============================================================
ANÁLISIS LÉXICO
============================================================
✓ Sin errores léxicos

============================================================
ANÁLISIS SINTÁCTICO
============================================================
✓ Sin errores sintácticos

============================================================
ANÁLISIS SEMÁNTICO
============================================================
✓ Sin errores semánticos

Total de errores: 0
✓ ¡FASE 1 IMPLEMENTADA CORRECTAMENTE!
```

---

### 🐛 5. ERRORES COMUNES Y SOLUCIONES

#### Error: "Token no reconocido"
- **Causa**: Falta agregar el token en lexer.py
- **Solución**: Agregar patrón regex en ESPECIFICACION_TOKENS

#### Error: "Unexpected token"
- **Causa**: Parser no maneja el nuevo token
- **Solución**: Agregar método de parseo correspondiente

#### Error: "Tipo incompatible"
- **Causa**: Validación semántica incorrecta
- **Solución**: Verificar lógica en visitar_expresion_binaria

#### Error: "bool es subclase de int en Python"
- **Causa**: `isinstance(True, int)` retorna True
- **Solución**: Verificar `isinstance(valor, bool)` ANTES de `isinstance(valor, int)`

#### Error Unicode en Windows
- **Causa**: Console Windows usa cp1252
- **Solución**: Agregar al inicio del script:
  ```python
  import sys, io
  sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
  ```

---

### 📊 6. PRECEDENCIA DE OPERADORES (CRÍTICO)

**Orden de mayor a menor precedencia**:

```python
# En parser.py, el orden de métodos IMPORTA:

def expresion(self):
    return self.expresion_or()  # Menor precedencia

def expresion_or(self):
    return self.expresion_and()  # OR < AND

def expresion_and(self):
    return self.expresion_comparacion()  # AND < Comparación

def expresion_comparacion(self):
    return self.expresion_aritmetica()  # Comparación < Aritmética

def expresion_aritmetica(self):
    return self.termino()  # Suma/Resta < Mult/Div

def termino(self):
    return self.expresion_unaria()  # Mult/Div < Unario

def expresion_unaria(self):
    return self.expresion_primaria()  # Unario < Primario

def expresion_primaria(self):
    # Literales, variables, paréntesis, etc.
```

**Nunca alteres este orden sin consultar teoría de compiladores**

---

### 🎯 7. ESTADO ACTUAL DEL PROYECTO (2025-11-04)

#### ✅ Fase 1: COMPLETADA
- Palabra clave `until` ✅
- Palabras clave `break` y `continue` ✅
- Operadores lógicos `&&` y `||` ✅
- Declaración sin inicialización ✅
- Todos los tests pasando ✅

#### ⏳ Fase 2: PENDIENTE (Siguiente a implementar)
- Declaración de funciones (F016 + F017)
- Llamadas a funciones (F006)
- Funciones built-in (F007)

#### ⏳ Fases 3-5: PENDIENTES
- Ver plan detallado abajo

---

### 🚀 8. CÓMO EMPEZAR LA FASE 2

**Cuando estés listo para implementar Fase 2, sigue estos pasos**:

1. **Lee la sección "FASE 2: Funciones y Llamadas" completa**
2. **Empieza con 2.1: Declaración de Funciones**
3. **Crea `test_kt/test_fase2.kt` con código de prueba**
4. **Crea `tests/test_fase2_directo.py` copiando el de Fase 1**
5. **Implementa paso a paso según el flujo de trabajo**

---

### 📝 9. NOTAS FINALES

- **No te saltes pasos**: El orden importa en compiladores
- **Pregunta si no entiendes**: Es mejor preguntar que romper el código
- **Documenta tus cambios**: Agrega comentarios y actualiza el changelog
- **Haz commits pequeños**: Un commit por característica
- **Ejecuta tests frecuentemente**: Detecta bugs temprano

---

## 📊 Estado Actual del Proyecto

### ✅ Características Implementadas

- **Análisis Léxico**: Tokenización completa
- **Análisis Sintáctico**: Parser con AST
- **Análisis Semántico**: Validación de tipos y scopes
- **Variables**: `var` y `val` con tipos `Int`, `Double`, `String`, `Boolean`
- **Operadores Aritméticos**: `+`, `-`, `*`, `/`, `%`
- **Operadores de Comparación**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Operador Unario**: `!` (NOT), `-` (negativo)
- **Estructuras de Control**: `if`/`else`, `while`, `for..in..`
- **Rangos**: `0..10` (operador `..`)
- **Acceso a Índices**: `array[0]`, `matrix[i][j]` (sintaxis, sin arrays reales)
- **UI Moderna**: Tkinter con temas, editor con resaltado, consola multi-pestaña

---

## 🎯 Características Faltantes

### Nivel 1: Críticas (para código Bubble Sort)

| ID | Característica | Prioridad | Complejidad | Estimación |
|---|---|---|---|---|
| F001 | Palabra clave `until` | ⚡ Crítica | 🟢 Baja | 2-3 días |
| F002 | Palabra clave `break` | ⚡ Crítica | 🟡 Media | 2-3 días |
| F003 | Palabra clave `continue` | 🔸 Alta | 🟡 Media | 1-2 días |
| F004 | Declaración sin inicialización | 🔸 Alta | 🟢 Baja | 1 día |
| F005 | Operadores lógicos `&&`, `||` | 🔸 Alta | 🟢 Baja | 2-3 días |
| F006 | Llamadas a funciones | ⚡ Crítica | 🔴 Alta | 1 semana |
| F007 | Funciones built-in básicas | ⚡ Crítica | 🔴 Alta | 1 semana |
| F008 | Operador punto `.` (propiedades) | ⚡ Crítica | 🔴 Alta | 3-4 días |

### Nivel 2: Importantes

| ID | Característica | Prioridad | Complejidad | Estimación |
|---|---|---|---|---|
| F009 | Operadores compuestos `+=`, `-=`, etc. | 🔹 Media | 🟢 Baja | 1-2 días |
| F010 | Incremento/Decremento `++`, `--` | 🔹 Media | 🟡 Media | 2-3 días |
| F011 | Arrays tipados `IntArray`, `Array<T>` | 🔸 Alta | 🔴 Alta | 1-2 semanas |
| F012 | Literales de lista `listOf()` | 🔹 Media | 🔴 Alta | 3-5 días |
| F013 | Métodos de String | 🔹 Media | 🔴 Alta | 3-5 días |
| F014 | Interpolación de strings `$x`, `${expr}` | 🔹 Media | 🟡 Media | 2-3 días |
| F015 | When expression | 🔹 Media | 🟡 Media | 3-5 días |

### Nivel 3: Avanzadas

| ID | Característica | Prioridad | Complejidad | Estimación |
|---|---|---|---|---|
| F016 | Declaración de funciones | 🔸 Alta | 🔴 Alta | 1-2 semanas |
| F017 | Parámetros de función | 🔸 Alta | 🔴 Alta | 1 semana |
| F018 | Null safety `?`, `?.`, `?:` | 🔹 Media | 🟡 Media | 3-5 días |
| F019 | Try-catch-finally | 🔹 Media | 🟡 Media | 3-5 días |
| F020 | Clases y objetos | 🔻 Baja | 🔴 Muy Alta | 3-4 semanas |
| F021 | Data classes | 🔻 Baja | 🔴 Muy Alta | 1-2 semanas |
| F022 | Lambda expressions | 🔻 Baja | 🔴 Alta | 2-3 semanas |
| F023 | Higher-order functions | 🔻 Baja | 🔴 Alta | 2-3 semanas |

---

## 🚀 Plan de Implementación

### **FASE 1: Operadores y Control de Flujo Básico** (2-3 semanas)

**Objetivo**: Hacer que el código de Bubble Sort compile correctamente

#### Tareas:

##### 1.1. Implementar `until` (F001) ✅ COMPLETADO
**Duración**: 2-3 días
**Archivos**: `core/utils.py`, `core/lexer.py`, `core/parser.py`

```markdown
- [x] Agregar token `UNTIL` en TipoToken
- [x] Agregar patrón regex en lexer: ('UNTIL', r'until')
- [x] Modificar parser.py en método `expresion_primaria()`:
      * Detectar `until` como alternativa a `..`
      * Si es `until`, ajustar rango: `0 until 10` = `0..9`
- [x] Tests: `for (i in 0 until 5)` debe iterar 0,1,2,3,4
```

##### 1.2. Implementar `break` (F002) ✅ COMPLETADO
**Duración**: 2-3 días
**Archivos**: `core/utils.py`, `core/lexer.py`, `core/parser.py`, `core/semantic.py`

```markdown
- [x] Agregar token `BREAK` en TipoToken
- [x] Agregar nodo `TipoNodo.BREAK` en utils.py
- [x] Lexer: ('BREAK', r'break')
- [x] Parser: crear método `sentencia_break()`:
      * Consumir token BREAK
      * Crear nodo BREAK
- [x] Semántico: validar que BREAK solo aparezca dentro de `while` o `for`
      * Agregar flag `dentro_de_loop` al analizador semántico
      * Reportar error si break fuera de loop
- [x] Tests: `while (true) { if (x > 5) break }`
```

##### 1.3. Implementar `continue` (F003) ✅ COMPLETADO
**Duración**: 1-2 días
**Archivos**: Similar a `break`

```markdown
- [x] Agregar token `CONTINUE` en TipoToken
- [x] Agregar nodo `TipoNodo.CONTINUE`
- [x] Lexer: ('CONTINUE', r'continue')
- [x] Parser: método `sentencia_continue()`
- [x] Semántico: validar scope igual que break
- [x] Tests: `for (i in 0..10) { if (i == 5) continue }`
```

##### 1.4. Operadores Lógicos `&&`, `||` (F005) ✅ COMPLETADO
**Duración**: 2-3 días
**Archivos**: `core/utils.py`, `core/lexer.py`, `core/parser.py`, `core/semantic.py`

```markdown
- [x] Agregar tokens `AND`, `OR` en TipoToken
- [x] Lexer:
      * ('AND', r'&&')
      * ('OR', r'\|\|')
- [x] Parser: modificar precedencia creando jerarquía correcta:
      * AND tiene mayor precedencia que OR
      * Crear métodos `expresion_and()` y `expresion_or()`
- [x] Semántico: validar que ambos operandos sean Boolean
      * Resultado siempre es Boolean
- [x] Tests: `if (x > 0 && y < 10)`, `if (a || b)`
```

##### 1.5. Declaración sin Inicialización (F004) ✅ COMPLETADO
**Duración**: 1 día
**Archivos**: `core/parser.py`, `core/semantic.py`

```markdown
- [x] Parser: modificar `declaracion_variable()`:
      * Hacer opcional el `= expresion`
      * Si no hay inicialización, crear nodo sin hijo de valor
- [x] Semántico: Ya manejaba correctamente declaraciones sin valor
      * Valida tipo solo si hay expresión de inicialización
- [x] Tests: `var x: Int`, `val nombre: String`
```

---

### **FASE 2: Funciones y Llamadas** (3-4 semanas)

**Objetivo**: Soporte completo para definir y llamar funciones

#### Tareas:

##### 2.1. Declaración de Funciones (F016 + F017)
**Duración**: 2 semanas
**Archivos**: `core/utils.py`, `core/parser.py`, `core/semantic.py`

```markdown
- [ ] Definir estructura de función en utils.py:
      * @dataclass FuncionInfo: nombre, params, tipo_retorno, cuerpo
- [ ] Parser: método `declaracion_funcion()`:
      fun IDENTIFIER ( params ) : TIPO { bloque }
      * Parsear lista de parámetros: nombre: Tipo, ...
      * Parsear tipo de retorno
      * Parsear cuerpo (bloque)
- [ ] Semántico:
      * Agregar funciones a tabla de símbolos global
      * Crear nuevo scope para parámetros
      * Validar que return exista si tipo != Unit
      * Validar tipo de return coincida con firma
- [ ] Tests:
      fun suma(a: Int, b: Int): Int {
          return a + b
      }
```

##### 2.2. Llamadas a Funciones (F006)
**Duración**: 1 semana
**Archivos**: `core/parser.py`, `core/semantic.py`

```markdown
- [ ] Parser: modificar `expresion_primaria()`:
      * Al encontrar IDENTIFIER, verificar si sigue '('
      * Si sí, parsear llamada: IDENTIFIER ( args )
      * Crear nodo LLAMADA_FUNCION con lista de argumentos
- [ ] Semántico:
      * Buscar función en tabla de símbolos
      * Validar número de argumentos
      * Validar tipo de cada argumento
      * Retornar tipo de retorno de la función
- [ ] Tests:
      val resultado = suma(5, 10)
      println(resultado)
```

##### 2.3. Funciones Built-in Básicas (F007)
**Duración**: 3-5 días
**Archivos**: `core/semantic.py`, `core/codegen.py`

```markdown
- [ ] Crear diccionario de funciones built-in en semantic.py:
      FUNCIONES_BUILTIN = {
          'println': FuncionInfo(...),
          'print': FuncionInfo(...),
          'intArrayOf': FuncionInfo(...),
      }
- [ ] Al inicializar analizador semántico, agregar a tabla global
- [ ] Implementar en codegen (generación de código Python):
      * println → print()
      * print → print(end='')
      * intArrayOf → [args]
- [ ] Tests:
      println("Hola Mundo")
      val arr = intArrayOf(1, 2, 3)
```

---

### **FASE 3: Arrays y Propiedades** (3-4 semanas)

**Objetivo**: Soporte completo para arrays y acceso a propiedades

#### Tareas:

##### 3.1. Operador Punto para Propiedades (F008)
**Duración**: 3-4 días
**Archivos**: `core/utils.py`, `core/parser.py`, `core/semantic.py`

```markdown
- [ ] Agregar nodo `TipoNodo.ACCESO_PROPIEDAD`
- [ ] Parser: modificar `expresion_primaria()`:
      * Después de parsear IDENTIFIER, verificar '.'
      * Si hay '.', parsear propiedad: objeto.propiedad
      * Crear nodo ACCESO_PROPIEDAD
- [ ] Semántico: crear tabla de propiedades por tipo:
      PROPIEDADES = {
          TipoDato.ARRAY_INT: {'size': TipoDato.INT},
          TipoDato.STRING: {'length': TipoDato.INT},
      }
      * Validar que tipo tenga la propiedad
      * Retornar tipo de la propiedad
- [ ] Tests:
      val arr = intArrayOf(1, 2, 3)
      val n = arr.size  // 3
```

##### 3.2. Arrays Tipados (F011)
**Duración**: 1-2 semanas
**Archivos**: `core/utils.py`, `core/semantic.py`

```markdown
- [ ] Agregar tipos de array en TipoDato:
      * ARRAY_INT = "IntArray"
      * ARRAY_DOUBLE = "DoubleArray"
      * ARRAY_STRING = "Array<String>"
      * ARRAY_GENERIC = "Array<T>"
- [ ] Función intArrayOf retorna TipoDato.ARRAY_INT
- [ ] Acceso a índice arr[i] retorna tipo elemento (Int)
- [ ] Asignación arr[i] = valor valida tipo
- [ ] Tests:
      val arr: IntArray = intArrayOf(1, 2, 3)
      arr[0] = 5
      val x = arr[1]
```

##### 3.3. Operador Punto para Métodos
**Duración**: 5-7 días
**Archivos**: `core/parser.py`, `core/semantic.py`

```markdown
- [ ] Agregar nodo `TipoNodo.LLAMADA_METODO`
- [ ] Parser: objeto.metodo(args)
- [ ] Semántico: tabla de métodos por tipo
      METODOS = {
          TipoDato.STRING: {
              'substring': (params, tipo_retorno),
              'contains': ...
          }
      }
- [ ] Tests:
      val sub = "Hola".substring(0, 2)  // "Ho"
```

---

### **FASE 4: Características Intermedias** (3-4 semanas)

**Objetivo**: Hacer KForge más expresivo

#### Tareas:

##### 4.1. Interpolación de Strings (F014)
**Duración**: 2-3 días

```markdown
- [ ] Lexer: detectar $ dentro de strings
      * Parsear $identifier o ${expression}
- [ ] Parser: crear nodo INTERPOLACION_STRING
- [ ] Semántico: validar expresiones
- [ ] Codegen: convertir a f-strings de Python
- [ ] Tests: "El valor es $x", "Suma: ${a + b}"
```

##### 4.2. When Expression (F015)
**Duración**: 3-5 días

```markdown
- [ ] Tokens: WHEN, ARROW (->)
- [ ] Parser: when (expr) { valor -> accion, else -> default }
- [ ] Semántico: validar tipos consistentes
- [ ] Tests:
      when (x) {
          1 -> "uno"
          2 -> "dos"
          else -> "otro"
      }
```

##### 4.3. Operadores Compuestos (F009)
**Duración**: 1-2 días

```markdown
- [ ] Tokens: PLUS_ASSIGN (+=), MINUS_ASSIGN, etc.
- [ ] Parser: azúcar sintáctico para x = x + y
- [ ] Tests: i += 1, suma *= 2
```

##### 4.4. Operadores ++ y -- (F010)
**Duración**: 2-3 días

```markdown
- [ ] Tokens: INCREMENT (++), DECREMENT (--)
- [ ] Parser: distinguir prefijo (++i) vs sufijo (i++)
- [ ] Semántico: solo variables numéricas
- [ ] Tests: i++, --j
```

##### 4.5. Null Safety Básico (F018)
**Duración**: 3-5 días

```markdown
- [ ] Tokens: QUESTION (?), ELVIS (?:)
- [ ] Tipos nullable: Int?, String?
- [ ] Operadores: ?. (safe call), ?: (elvis)
- [ ] Tests:
      var x: Int? = null
      val y = x ?: 0
```

##### 4.6. Try-Catch (F019)
**Duración**: 3-5 días

```markdown
- [ ] Tokens: TRY, CATCH, FINALLY, THROW
- [ ] Parser: try { } catch (e: Exception) { }
- [ ] Semántico: validar tipos de excepciones
- [ ] Tests: manejo básico de errores
```

---

### **FASE 5: Características Avanzadas** (Opcional, 2-3 meses)

#### Tareas:

- Clases y objetos (F020)
- Data classes (F021)
- Lambda expressions (F022)
- Higher-order functions (F023)
- Extension functions
- Companion objects

---

## 📅 Cronograma Estimado

| Fase | Duración | Fecha Inicio | Fecha Fin | Estado |
|---|---|---|---|---|
| Fase 1 | 2-3 semanas | 2025-11-04 | 2025-11-04 | ✅ Completada |
| Fase 2 | 3-4 semanas | TBD | TBD | ⏳ Pendiente |
| Fase 3 | 3-4 semanas | TBD | TBD | ⏳ Pendiente |
| Fase 4 | 3-4 semanas | TBD | TBD | ⏳ Pendiente |
| Fase 5 | 2-3 meses | TBD | TBD | ⏳ Pendiente |

**Total (Fases 1-4)**: ~3-4 meses
**Total (con Fase 5)**: ~5-7 meses

---

## 🎯 Hitos del Proyecto

### Hito 1: "Operadores y Control de Flujo" (Fin Fase 1) ✅ COMPLETADO
- ✅ Palabra clave `until` implementada
- ✅ Palabras clave `break` y `continue` implementadas
- ✅ Operadores lógicos `&&` y `||` implementados
- ✅ Declaraciones sin inicialización soportadas
- ⚠️ Código Bubble Sort original aún requiere Fase 2 (funciones) y Fase 3 (arrays)

### Hito 2: "Funciones Completas" (Fin Fase 2)
- ✅ Declarar y llamar funciones personalizadas
- ✅ Funciones built-in básicas funcionando

### Hito 3: "Arrays Reales" (Fin Fase 3)
- ✅ Arrays tipados con propiedades y métodos
- ✅ Operador punto funcional

### Hito 4: "Kotlin Expresivo" (Fin Fase 4)
- ✅ When, interpolación, null safety
- ✅ Manejo de errores básico

### Hito 5: "Kotlin Orientado a Objetos" (Fin Fase 5)
- ✅ Clases, lambdas, funciones de orden superior
- ✅ Compilador casi completo

---

## 🧪 Estrategia de Testing

### Tests por Implementar

Cada característica debe tener:
1. **Tests unitarios** del lexer (tokens correctos)
2. **Tests del parser** (AST correcto)
3. **Tests semánticos** (validación de tipos)
4. **Tests de integración** (código completo que compila)

### Código de Prueba Principal

```kotlin
// Bubble Sort - Objetivo Fase 1
val arr = intArrayOf(64, 34, 25, 12, 22, 11, 90)
val n = arr.size
var swapped: Boolean

for (i in 0 until n - 1) {
    swapped = false
    for (j in 0 until n - i - 1) {
        if (arr[j] > arr[j + 1]) {
            val temp = arr[j]
            arr[j] = arr[j + 1]
            arr[j + 1] = temp
            swapped = true
        }
    }
    if (!swapped) break
}

println("Array ordenado:")
for (elemento in arr) {
    println(elemento)
}
```

---

## 📝 Notas Técnicas

### Archivos Principales a Modificar

| Archivo | Propósito | Fases que lo modifican |
|---|---|---|
| `core/utils.py` | Tokens, nodos AST, tipos de datos | Todas |
| `core/lexer.py` | Tokenización | Todas |
| `core/parser.py` | Construcción del AST | Todas |
| `core/semantic.py` | Validación semántica | Todas |
| `core/codegen.py` | Generación de código | 2, 3, 4, 5 |
| `tests/` | Tests unitarios | Todas |

### Decisiones de Diseño

1. **Precedencia de Operadores**:
   ```
   Unario (!, -, ++, --)
   Multiplicación (*, /, %)
   Suma (+, -)
   Comparación (<, >, <=, >=)
   Igualdad (==, !=)
   AND lógico (&&)
   OR lógico (||)
   ```

2. **Sistema de Tipos**:
   - Empezar simple: tipos primitivos
   - Fase 3: tipos de array
   - Fase 4: tipos nullable
   - Fase 5: tipos genéricos

3. **Tabla de Símbolos**:
   - Actual: solo variables
   - Fase 2: agregar funciones
   - Fase 5: agregar clases

---

## 🔗 Referencias

- [Kotlin Language Specification](https://kotlinlang.org/spec/)
- [Kotlin Grammar](https://kotlinlang.org/docs/reference/grammar.html)
- [Crafting Interpreters](https://craftinginterpreters.com/)
- [Dragon Book - Compilers: Principles, Techniques, and Tools](https://suif.stanford.edu/dragonbook/)

---

## 📌 Changelog

- **2025-11-04**:
  - Creación del roadmap inicial
  - ✅ **FASE 1 COMPLETADA** en el mismo día
    - Implementado soporte para `until`
    - Implementado soporte para `break` y `continue`
    - Implementados operadores lógicos `&&` y `||`
    - Soportadas declaraciones sin inicialización
    - Todos los tests pasando correctamente
  - 📁 **REORGANIZACIÓN DE ESTRUCTURA DE TESTS**:
    - Creada carpeta `test_kt/` para archivos Kotlin de prueba (.kt)
    - Reorganizada carpeta `tests/` para scripts Python y archivos de datos
    - Movido `test_fase1.kt` → `test_kt/test_fase1.kt`
    - Movido `test_fase1_directo.py` → `tests/test_fase1_directo.py`
    - Movido `test_compilador.py` → `tests/test_compilador.py`
  - 📝 **ACTUALIZACIÓN DEL ROADMAP**:
    - Agregadas instrucciones detalladas para continuación del proyecto
    - Documentada estructura completa del proyecto
    - Agregadas reglas de organización y flujo de trabajo
    - Agregados ejemplos prácticos de implementación
    - Documentados errores comunes y soluciones
- **TBD**: Inicio Fase 2

---

## 👤 Autor

Desarrollado como proyecto educativo para aprender compiladores e implementación de lenguajes.

**Licencia**: MIT (o la que prefieras)
