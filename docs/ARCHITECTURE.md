# 🏗️ Arquitectura del Compilador KForge

**Versión**: 2.0 (En desarrollo)
**Objetivo**: Compilador Kotlin → JVM Bytecode Real

---

## 📐 Visión General del Proyecto

KForge es un compilador profesional que traduce un subconjunto de Kotlin a JVM bytecode ejecutable (.class files). El diseño sigue principios de ingeniería de compiladores modernos con separación clara entre frontend, representación intermedia y backend.

---

## 🔄 Pipeline Completo del Compilador

```
┌─────────────────────────────────────────────────────────────────┐
│                     CÓDIGO FUENTE KOTLIN (.kt)                   │
│  Ejemplo: fun suma(a: Int, b: Int): Int { return a + b }       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  FASE 1: ANÁLISIS LÉXICO (Lexer) ✅ v1.0                        │
├─────────────────────────────────────────────────────────────────┤
│  Módulo: core/lexer.py                                          │
│  Entrada: String de código fuente                              │
│  Salida: Lista de Tokens                                        │
│  Responsabilidad:                                               │
│    - Escanear caracteres y generar tokens                       │
│    - Detectar palabras clave, identificadores, literales       │
│    - Manejo de comentarios (// y /* */)                         │
│    - Detección de errores léxicos (40+ tipos)                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  FASE 2: ANÁLISIS SINTÁCTICO (Parser) ✅ v1.0                   │
├─────────────────────────────────────────────────────────────────┤
│  Módulo: core/parser.py                                         │
│  Entrada: Lista de Tokens                                       │
│  Salida: AST (Abstract Syntax Tree)                            │
│  Responsabilidad:                                               │
│    - Parser recursivo descendente                               │
│    - Construcción del AST con nodos tipados                    │
│    - Validación de gramática de Kotlin                         │
│    - Detección de errores sintácticos                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  FASE 3: ANÁLISIS SEMÁNTICO ✅ v1.0                             │
├─────────────────────────────────────────────────────────────────┤
│  Módulo: core/semantic.py                                       │
│  Entrada: AST                                                   │
│  Salida: AST Validado + Tabla de Símbolos                      │
│  Responsabilidad:                                               │
│    - Type checking (validación de tipos)                        │
│    - Scope analysis (análisis de alcance)                       │
│    - Detección de variables no inicializadas                   │
│    - Return path analysis                                       │
│    - Validación de inmutabilidad (val vs var)                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  FASE 4: GENERACIÓN TAC ✅ v1.1                                 │
├─────────────────────────────────────────────────────────────────┤
│  Módulo: core/tac.py                                            │
│  Entrada: AST Validado                                          │
│  Salida: Three-Address Code (TAC)                              │
│  Responsabilidad:                                               │
│    - Traducir AST a representación intermedia de 3 direcciones │
│    - Generar temporales (t1, t2, t3, ...)                      │
│    - Generar labels para control de flujo (L1, L2, ...)        │
│    - Linearización de expresiones complejas                     │
│  Operaciones:                                                   │
│    - ASSIGN, ADD, SUB, MUL, DIV, MOD                           │
│    - LT, GT, LE, GE, EQ, NE, AND, OR, NOT                      │
│    - LABEL, GOTO, IF_FALSE                                      │
│    - PARAM, CALL, RETURN                                        │
│    - ARRAY_LOAD, ARRAY_STORE                                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  FASE 5: BYTECODE STACK-BASED ✅ v1.1 (Educativo)               │
├─────────────────────────────────────────────────────────────────┤
│  Módulo: core/bytecode.py                                       │
│  Entrada: TAC                                                   │
│  Salida: Bytecode Assembly (texto .asm)                        │
│  Responsabilidad:                                               │
│    - Traducir TAC a bytecode stack-based                        │
│    - Formato assembly-like humanizado                           │
│    - NOTA: NO es JVM bytecode real                             │
│  Instrucciones:                                                 │
│    - PUSH, LOAD, STORE                                          │
│    - ADD, SUB, MUL, DIV, MOD                                    │
│    - EQ, LT, GT, LE, GE, NE                                     │
│    - AND, OR, NOT, NEG                                          │
│    - LABEL, JUMP, JUMPF                                         │
│    - CALL, RET, HALT                                            │
│    - ALOAD, ASTORE (arrays)                                     │
└─────────────────────────────────────────────────────────────────┘

                 ┌─────────────────────────────┐
                 │  v2.0: JVM BYTECODE REAL    │
                 │  (EN DESARROLLO)            │
                 └──────────────┬──────────────┘
                                │
              ┌─────────────────┴─────────────────┐
              │                                   │
              ▼                                   ▼
┌─────────────────────────────┐   ┌────────────────────────────────┐
│ FASE 7: CLASSFILE STRUCTURE │   │ FASE 8: JVM INSTRUCTIONS       │
├─────────────────────────────┤   ├────────────────────────────────┤
│ Módulos: core/jvm/          │   │ Módulo: core/jvm/              │
│  - classfile.py             │   │   jvm_generator.py             │
│  - constant_pool.py         │   │                                │
│  - descriptors.py           │   │ TAC → JVM Bytecode             │
│                             │   │ 200+ instrucciones tipadas     │
│ Estructura .class:          │   │                                │
│  - Magic (0xCAFEBABE)       │   │ iload, istore, iadd, isub,    │
│  - Version (Java 8: 52.0)   │   │ dload, dstore, dadd, dsub,    │
│  - Constant Pool            │   │ if_icmpeq, goto, invokestatic,│
│  - Access Flags             │   │ newarray, iaload, iastore,    │
│  - This/Super Class         │   │ ireturn, return, etc.         │
│  - Methods/Fields           │   │                                │
└─────────────────────────────┘   └────────────────────────────────┘
              │                                   │
              └─────────────────┬─────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ FASE 9: STACK MAP FRAMES        │
              ├─────────────────────────────────┤
              │ Módulo: core/jvm/stackmaps.py   │
              │                                 │
              │ Análisis de flujo de control    │
              │ Cálculo de tipos en cada branch│
              │ Generación de StackMapTable     │
              │ (Requerido por JVM desde Java 7)│
              │                                 │
              │ OPCIÓN: Usar ASM library        │
              └────────────────┬────────────────┘
                               │
                               ▼
              ┌─────────────────────────────────┐
              │ FASE 10-11: ATTRIBUTES +        │
              │             RUNTIME SUPPORT     │
              ├─────────────────────────────────┤
              │ Módulos:                        │
              │  - core/jvm/attributes.py       │
              │  - core/jvm/runtime.py          │
              │                                 │
              │ Attributes:                     │
              │  - SourceFile                   │
              │  - LineNumberTable              │
              │  - LocalVariableTable           │
              │                                 │
              │ Runtime:                        │
              │  - println() → System.out       │
              │  - intArrayOf() → newarray      │
              │  - main(String[] args)          │
              └────────────────┬────────────────┘
                               │
                               ▼
              ┌─────────────────────────────────┐
              │ SALIDA: ARCHIVO .class          │
              ├─────────────────────────────────┤
              │ Formato binario JVM             │
              │ Ejecutable con: java ClassName  │
              │                                 │
              │ Verificable con:                │
              │  - javap -c -v ClassName.class │
              │  - jd-gui ClassName.class       │
              └─────────────────────────────────┘
```

---

## 📦 Organización de Módulos

### **core/** - Núcleo del Compilador

```
core/
├── __init__.py
├── utils.py           # Definiciones compartidas (Token, AST, TipoDato)
├── errors.py          # Sistema de manejo de errores
├── controller.py      # Orquestador del pipeline completo
│
├── lexer.py           # ✅ Fase 1: Análisis léxico
├── parser.py          # ✅ Fase 2: Análisis sintáctico
├── semantic.py        # ✅ Fase 3: Análisis semántico
├── tac.py             # ✅ Fase 4: Generación TAC
├── bytecode.py        # ✅ Fase 5: Bytecode educativo
│
└── jvm/               # 📝 v2.0: JVM Bytecode Real
    ├── __init__.py
    ├── classfile.py        # Fase 7: Escritor de .class
    ├── constant_pool.py    # Fase 7: Constant Pool Manager
    ├── descriptors.py      # Fase 7: Type Descriptors
    ├── instructions.py     # Fase 8: JVM Instruction Set
    ├── jvm_generator.py    # Fase 8: TAC → JVM Bytecode
    ├── stackmaps.py        # Fase 9: Stack Map Frames
    ├── attributes.py       # Fase 10: Attributes JVM
    └── runtime.py          # Fase 11: Runtime Support
```

### **ui/** - Interfaz Gráfica

```
ui/
├── __init__.py
├── app_ui.py          # Aplicación principal (ventana root)
├── editor_panel.py    # Editor con pestañas y syntax highlighting
├── console_panel.py   # Consola multi-pestaña (Salida, Errores, Tokens, AST, Código)
├── sidebar.py         # Barra lateral (gestión de archivos)
├── phases_panel.py    # Panel indicador de fases completadas
├── status_bar.py      # Barra de estado inferior
├── theme_manager.py   # Gestión de temas (dark/light)
├── language_manager.py # Internacionalización (i18n)
└── splash_screen.py   # Pantalla de inicio
```

### **tests/** - Suite de Tests

```
tests/
├── test_tac_generator.py      # ✅ 11 tests TAC
├── test_bytecode_generator.py # ✅ 10 tests Bytecode
├── test_fase1_directo.py      # ✅ Tests Fase 1
├── test_fase2_directo.py      # ✅ Tests Fase 2
├── test_fase3_directo.py      # ✅ Tests Fase 3
├── test_v1_final.py           # ✅ Test Bubble Sort
│
└── jvm/                        # 📝 v2.0: Tests JVM
    ├── __init__.py
    ├── test_classfile.py      # Tests estructura .class
    ├── test_constant_pool.py  # Tests constant pool
    ├── test_jvm_generation.py # Tests generación bytecode
    └── test_execution.py      # Tests ejecución real JVM
```

---

## 🔄 Flujo de Datos

### Entrada: Código Kotlin

```kotlin
fun suma(a: Int, b: Int): Int {
    return a + b
}

fun main() {
    val resultado: Int = suma(10, 20)
    println(resultado)
}
```

### Salida Fase 1: Tokens

```
FUN, IDENTIFIER(suma), LPAREN, IDENTIFIER(a), COLON, TYPE(Int), COMMA,
IDENTIFIER(b), COLON, TYPE(Int), RPAREN, COLON, TYPE(Int), LBRACE,
RETURN, IDENTIFIER(a), PLUS, IDENTIFIER(b), RBRACE, ...
```

### Salida Fase 2: AST

```
PROGRAMA
├── FUNCION(suma)
│   ├── PARAMETRO(a: Int)
│   ├── PARAMETRO(b: Int)
│   ├── TIPO_RETORNO(Int)
│   └── BLOQUE
│       └── RETURN
│           └── EXPRESION_BINARIA(+)
│               ├── IDENTIFICADOR(a)
│               └── IDENTIFICADOR(b)
└── FUNCION(main)
    └── BLOQUE
        ├── DECLARACION_VAR(resultado: Int)
        │   └── LLAMADA_FUNCION(suma)
        │       ├── ARGUMENTO(10)
        │       └── ARGUMENTO(20)
        └── LLAMADA_FUNCION(println)
            └── ARGUMENTO(resultado)
```

### Salida Fase 3: Tabla de Símbolos

```
Global Scope:
  - suma: Function(Int, Int) → Int
  - main: Function() → Unit

Scope (suma):
  - a: Int (param, initialized)
  - b: Int (param, initialized)

Scope (main):
  - resultado: Int (val, initialized)
```

### Salida Fase 4: TAC (Three-Address Code)

```tac
; Function: suma
L0:                        ; start of suma
    t1 = a + b
    RETURN t1

; Function: main
L1:                        ; start of main
    PARAM 10
    PARAM 20
    t2 = CALL suma, 2
    resultado = t2
    PARAM resultado
    CALL println, 1
    RETURN
```

### Salida Fase 5: Bytecode Assembly (v1.1 Educativo)

```asm
; Function: suma
L0:
    LOAD a          ; Push a
    LOAD b          ; Push b
    ADD             ; a + b
    STORE t1        ; t1 = result
    LOAD t1         ; Return value
    RET

; Function: main
L1:
    PUSH 10
    PUSH 20
    CALL suma
    STORE resultado
    LOAD resultado
    CALL println
    RET
```

### Salida Fase 7-12: JVM Bytecode (v2.0 Real)

```
Classfile MyClass.class
  Magic: 0xCAFEBABE
  Version: 52.0 (Java 8)

  Constant Pool:
    #1 = Utf8               suma
    #2 = Utf8               (II)I
    #3 = Methodref          #4.#5
    ...

  public static int suma(int, int);
    Code:
      stack=2, locals=2
       0: iload_0
       1: iload_1
       2: iadd
       3: ireturn

  public static void main(java.lang.String[]);
    Code:
      stack=2, locals=2
       0: bipush        10
       2: bipush        20
       4: invokestatic  #3  // suma
       7: istore_1
       8: getstatic     #7  // System.out
      11: iload_1
      12: invokevirtual #13 // println
      15: return
```

---

## 🎯 Principios de Diseño

### 1. Separación de Responsabilidades

Cada módulo tiene una responsabilidad única y bien definida:
- **Lexer**: Solo tokenización, no construcción de AST
- **Parser**: Solo construcción de AST, no validación semántica
- **Semantic**: Solo validación, no generación de código
- **TAC Generator**: Solo generación de IR, no optimización
- **JVM Generator**: Solo generación de bytecode, no ejecución

### 2. Desacoplamiento UI-Compilador

- La lógica del compilador es completamente independiente de la UI
- `core/controller.py` actúa como interfaz entre UI y compilador
- La UI solo consume resultados del controller
- Permite tests sin UI y posible CLI en el futuro

### 3. Manejo Centralizado de Errores

- Todos los errores pasan por `ErrorManager`
- Cada error incluye: tipo, mensaje, línea, columna
- Sistema unificado para errores léxicos, sintácticos y semánticos
- La UI simplemente renderiza los errores del manager

### 4. Extensibilidad

- Fácil agregar nuevos backends (JVM, LLVM, C, JavaScript)
- Todos consumen la misma representación TAC
- TAC actúa como "lingua franca" del compilador

---

## 📊 Estado por Versión

| Versión | Estado | Fases Completadas |
|---------|--------|-------------------|
| **v1.0.0** | ✅ Completada | Fases 1-3: Lexer, Parser, Semantic |
| **v1.0.1** | ✅ Completada | Validación avanzada de errores |
| **v1.1.0** | ✅ Completada | Fases 4-6: TAC, Bytecode, UI |
| **v2.0.0** | 📝 En desarrollo | Fases 7-12: JVM Bytecode Real |

---

## 🛠️ Herramientas de Desarrollo

### Requisitos

- **Python 3.8+**: Lenguaje de implementación
- **Tkinter**: UI (incluido en Python)
- **JDK 8+**: Para ejecutar .class en v2.0
- **javap**: Para verificar bytecode (incluido en JDK)

### Herramientas Opcionales

```bash
# Decompilador gráfico
jd-gui MyClass.class

# ASM Library (para Stack Map Frames)
pip install asm-python
```

---

## 📚 Referencias

- **JVM Specification SE 8**: https://docs.oracle.com/javase/specs/jvms/se8/html/
- **Kotlin Language Spec**: https://kotlinlang.org/spec/
- **Dragon Book**: Compilers: Principles, Techniques, and Tools
- **Crafting Interpreters**: https://craftinginterpreters.com/

---

**Autor**: Gabriel Alejandro Medina Miramontes
**Última actualización**: 2025-11-28
**Versión del documento**: 2.0
