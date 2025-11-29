# 🗺️ KForge Compiler - Roadmap de Desarrollo

**Compilador Profesional de Kotlin → JVM Bytecode**
**Versión actual**: v1.1.0 ✅
**Objetivo**: Compilador completo con generación de JVM Bytecode ejecutable

---

## 📖 Documentación del Proyecto

- 📘 **[README.md](README.md)** - Descripción general y características
- 📋 **[CONTRIBUTING.md](CONTRIBUTING.md)** - Reglas de trabajo y flujo de desarrollo
- 📝 **[CHANGELOG.md](CHANGELOG.md)** - Historial de cambios por versión
- 🗺️ **ROADMAP.md** (este archivo) - Plan de desarrollo y estado actual

---

## 📊 Estado Actual del Proyecto

### ✅ Versión 1.1.0 - COMPLETADA

**Frontend Completo + Generación de Código Intermedio**

#### Características del Lenguaje Soportadas
- **Variables**: `var`, `val` con tipos `Int`, `Double`, `String`, `Boolean`
- **Operadores**: Aritméticos (`+`, `-`, `*`, `/`, `%`), Lógicos (`&&`, `||`, `!`), Comparación (`==`, `!=`, `<`, `>`, `<=`, `>=`)
- **Control de Flujo**: `if`/`else`, `while`, `for..in`, `break`, `continue`
- **Funciones**: Declaración, parámetros, return, llamadas
- **Arrays**: `IntArray`, `DoubleArray`, acceso con `[]`, propiedades (`.size`, `.length`)
- **Built-ins**: `println()`, `print()`, `intArrayOf()`, `doubleArrayOf()`

#### Pipeline de Compilación Actual
```
Código Kotlin
    ↓
[1] Análisis Léxico → Tokens
    ↓
[2] Análisis Sintáctico → AST
    ↓
[3] Análisis Semántico → Validación
    ↓
[4] Generación TAC → Three-Address Code
    ↓
[5] Generación Bytecode → Stack-Based Assembly (educativo)
```

#### Archivos Principales
- `core/lexer.py` - Tokenizador
- `core/parser.py` - Parser recursivo descendente
- `core/semantic.py` - Validador semántico
- `core/tac.py` - Generador TAC (3-address code)
- `core/bytecode.py` - Generador bytecode stack-based (NO JVM)
- `core/controller.py` - Orquestador del pipeline
- `ui/app_ui.py` - Interfaz gráfica moderna

#### Tests Completos
- ✅ 11/11 tests TAC
- ✅ 10/10 tests Bytecode
- ✅ Test final: Bubble Sort completo

---

## 🎯 ROADMAP: Kotlin → JVM Bytecode Real

**OBJETIVO PRINCIPAL**: Generar archivos `.class` ejecutables en cualquier JVM

---

## 🚀 Versión 2.0 - JVM Bytecode Real (EN DESARROLLO)

**Duración estimada**: 6-8 semanas
**Objetivo**: Generar bytecode JVM real (.class) ejecutable

---

### 📅 Semana 1-2: Fundamentos JVM

#### Fase 7: Estructura de Archivos .class ✅ COMPLETADA
**Duración**: 14 días
**Prioridad**: 🔴 CRÍTICA
**Estado**: ✅ Completada - 2025-11-28

- [x] **ClassFile Writer** (`core/jvm/classfile.py`)
  - [x] Magic number (0xCAFEBABE)
  - [x] Version numbers (Java 8: 52.0)
  - [x] Access flags (PUBLIC, SUPER)
  - [x] This class, super class references
  - [x] Escritura binaria big-endian
  - [x] MethodInfo, AttributeInfo classes
  - [x] CodeAttribute para métodos
  - [x] SourceFileAttribute

- [x] **Constant Pool** (`core/jvm/constant_pool.py`)
  - [x] CONSTANT_Utf8 (strings)
  - [x] CONSTANT_Integer, CONSTANT_Double, CONSTANT_Long, CONSTANT_Float
  - [x] CONSTANT_Class (referencias a clases)
  - [x] CONSTANT_String (string literals)
  - [x] CONSTANT_Methodref (referencias a métodos)
  - [x] CONSTANT_Fieldref (referencias a campos)
  - [x] CONSTANT_NameAndType (descriptores)
  - [x] Gestión de índices (1-based)
  - [x] Cache de constantes (deduplicación automática)
  - [x] Soporte para Long/Double (2 slots)

- [x] **Method/Field Descriptors** (`core/jvm/descriptors.py`)
  - [x] Mapeo de tipos: Int→I, Double→D, String→Ljava/lang/String;, Boolean→Z, Unit→V
  - [x] Generación de method signatures: `(II)I`
  - [x] Field descriptors
  - [x] Descriptores predefinidos (main, println)

- [x] **Tests Completos**
  - [x] 8/8 tests Constant Pool
  - [x] 10/10 tests ClassFile Writer
  - [x] 4/4 tests Validación JVM

**Entregable**: ✅ Archivos .class válidos generados (MinimalClass.class, HelloWorld.class)

---

### 📅 Semana 3-4: Instrucciones JVM

#### Fase 8: JVM Instruction Set ✅ COMPLETADA
**Duración**: 14 días
**Prioridad**: 🔴 CRÍTICA
**Estado**: ✅ Completada - 2025-11-28

- [x] **JVM Opcodes** (`core/jvm/instructions.py`)
  - [x] 200+ opcodes JVM definidos (enum JVMOpcode)
  - [x] Load/Store tipados: `iload`, `istore`, `dload`, `dstore`, `aload`, `astore` (optimizados 0-3)
  - [x] Constantes: `iconst_m1` a `iconst_5`, `bipush`, `sipush`, `ldc`, `ldc_w`, `ldc2_w`
  - [x] Aritmética: `iadd`, `isub`, `imul`, `idiv`, `irem`, `dadd`, `dsub`, `dmul`, `ddiv`, `ineg`, `dneg`
  - [x] Comparaciones: `if_icmpeq`, `if_icmpne`, `if_icmplt`, `if_icmpge`, `if_icmpgt`, `if_icmple`
  - [x] Control: `goto`, `ifeq`, `ifne`, `iflt`, `ifge`, `ifgt`, `ifle`
  - [x] Arrays: `newarray`, `iaload`, `iastore`, `daload`, `dastore`, `arraylength`, `anewarray`
  - [x] Invocaciones: `invokestatic`, `invokevirtual`, `invokespecial`, `invokeinterface`
  - [x] Return: `ireturn`, `lreturn`, `dreturn`, `freturn`, `areturn`, `return`
  - [x] Clase JVMInstruction con conversión a bytes
  - [x] Helper functions: iconst(), iload(), istore(), dload(), dstore(), aload(), astore()

- [x] **JVM Generator** (`core/jvm/jvm_generator.py`)
  - [x] Traductor TAC → JVM bytecode completo
  - [x] LocalVariableManager: Gestión de slots con soporte para double (2 slots)
  - [x] StackDepthTracker: Cálculo dinámico de max_stack
  - [x] Mapeo de operaciones: ASSIGN, ADD, SUB, MUL, DIV, MOD, NEG, NOT
  - [x] Comparaciones: LT, GT, LE, GE, EQ, NE con pattern de branch
  - [x] Operadores lógicos: AND, OR con IAND/IOR
  - [x] Control de flujo: LABEL, GOTO, IF_FALSE
  - [x] Return statements (con valor y void)
  - [x] Resolución de labels y offsets (segunda pasada)

- [x] **Tests Completos**
  - [x] 10/10 tests Instructions
  - [x] 10/10 tests JVM Generator
  - [x] Total: 20 tests nuevos + 22 anteriores = 42 tests passing ✅

**Entregable**: ✅ Generador TAC → JVM funcional con soporte para expresiones, control de flujo y variables locales

---

### 📅 Semana 5: Verificación de Bytecode

#### ✅ Fase 9: Stack Map Frames (COMPLETADA)
**Duración**: 1 día (2025-11-28)
**Prioridad**: 🔴 MUY COMPLEJA
**Decisión**: ✅ Enfoque Java 6 (OPCIÓN PRAGMÁTICA)

**Razón**: La librería ASM (asm-python) no está disponible/mantenida para Python. La implementación manual de Stack Map Frames es excesivamente compleja para un proyecto educativo.

**Estrategia Implementada**:

- [x] **Soporte Multi-Versión en ClassFileWriter**
  - [x] Parámetro `java_version` (6, 7, 8)
  - [x] Flag `requires_stack_maps` basado en versión
  - [x] Default a Java 6 (version 50.0)

- [x] **Generación de Bytecode Java 6**
  - [x] Version 50.0 (no requiere Stack Map Frames)
  - [x] Compatible con todas las JVMs modernas
  - [x] Todas las características de KForge funcionan correctamente

- [x] **Tests Actualizados**
  - [x] Test de configuración de versiones Java
  - [x] Verificación de bytecode Java 6
  - [x] 42+ tests JVM pasando ✓

- [x] **Documentación**
  - [x] `docs/PHASE9_JAVA6_APPROACH.md` - Guía completa
  - [x] Explicación de decisión técnica
  - [x] Path de upgrade a Java 7+ (opcional)

**Entregable**: ✅ Bytecode Java 6 válido y verificable por JVM (todas las versiones)
**Documentación**: Ver `docs/PHASE9_JAVA6_APPROACH.md`

---

### 📅 Semana 6: Atributos y Metadata

#### Fase 10: Class Attributes
**Duración**: 7 días
**Prioridad**: 🟡 MEDIA

- [ ] **SourceFile Attribute**
  - [ ] Nombre del archivo fuente .kt

- [ ] **LineNumberTable**
  - [ ] Mapeo PC offset → línea de código
  - [ ] Para debugging

- [ ] **LocalVariableTable**
  - [ ] Nombres de variables locales
  - [ ] Start PC, length, slot

**Entregable**: Bytecode con debugging info

---

### 📅 Semana 7: Runtime Support

#### Fase 11: Built-in Functions y Runtime
**Duración**: 10 días
**Prioridad**: 🔴 ALTA

- [ ] **System I/O**
  - [ ] `println(Int)` → `System.out.println`
  - [ ] `println(Double)`
  - [ ] `println(String)`
  - [ ] `print()` variantes

- [ ] **Array Creation**
  - [ ] `intArrayOf()` → `newarray T_INT`
  - [ ] `doubleArrayOf()` → `newarray T_DOUBLE`
  - [ ] Inicialización de elementos

- [ ] **Main Method**
  - [ ] Signature: `public static void main(String[] args)`
  - [ ] Entry point correcto

**Entregable**: Programas con I/O ejecutables

---

### 📅 Semana 8: Integración y Testing

#### Fase 12: Integración Completa
**Duración**: 9 días
**Prioridad**: 🔴 CRÍTICA

- [ ] **Controller Integration** (`core/controller.py`)
  - [ ] Método `ejecutar_jvm()`
  - [ ] Pipeline: Kotlin → TAC → JVM → .class
  - [ ] Guardar archivo .class

- [ ] **UI Integration** (`ui/app_ui.py`, `ui/console_panel.py`)
  - [ ] Botón "▶️ Ejecutar JVM"
  - [ ] Pestaña "Bytecode JVM" (separada de stack-based)
  - [ ] Mostrar output de ejecución
  - [ ] Botón "Guardar .class"

- [ ] **Execution Engine**
  - [ ] Ejecutar con `java ClassName`
  - [ ] Capturar stdout/stderr
  - [ ] Mostrar en consola

- [ ] **Tests Completos** (`tests/jvm/`)
  - [ ] `test_simple_arithmetic.py` - val x = 5 + 3
  - [ ] `test_functions.py` - fun suma(a, b)
  - [ ] `test_arrays.py` - intArrayOf(1,2,3)
  - [ ] `test_control_flow.py` - if, while, for
  - [ ] `test_bubble_sort.py` - Algoritmo completo
  - [ ] Verificar ejecución real con JVM

**Entregable**: Compilador completo Kotlin → .class ejecutable

---

## 📊 Cronograma Actualizado

| Semana | Fase | Componente | Estado |
|--------|------|-----------|--------|
| **✅ Completadas** | Fase 1-6 | Frontend + TAC + Bytecode educativo | ✅ |
| **✅** | Fase 7 | ClassFile + Constant Pool | ✅ Completada |
| **✅** | Fase 8 | JVM Instructions | ✅ Completada |
| **✅** | Fase 9 | Stack Map Frames (Java 6) | ✅ Completada |
| **6** | Fase 10 | Attributes + Metadata | 📝 Siguiente |
| **7** | Fase 11 | Runtime Support | 📝 Planeada |
| **8** | Fase 12 | Integration + Tests | 📝 Planeada |

**Tiempo total estimado**: 8 semanas (~60 días)
**Progreso actual**: Fases 7-9 completadas (3/6 fases JVM) ✓

---

## 🎯 Hitos del Proyecto

### ✅ Hitos Completados

- **2025-11-22**: v1.1.0 - Generación TAC y Bytecode stack-based
- **2025-11-22**: v1.0.1 - Validación avanzada de errores
- **2025-11-06**: v1.0.0 - Frontend completo con test Bubble Sort

### 📅 Hitos Futuros

- **Semana 2**: Primer .class válido generado
- **Semana 4**: Primera ejecución JVM exitosa
- **Semana 6**: Debugging info completo
- **Semana 8**: **v2.0 RELEASE** - Compilador JVM completo

---

## 🛠️ Estructura de Archivos (v2.0)

```
KForge/
├── core/
│   ├── lexer.py              ✅ Completado
│   ├── parser.py             ✅ Completado
│   ├── semantic.py           ✅ Completado
│   ├── tac.py                ✅ Completado
│   ├── bytecode.py           ✅ Bytecode educativo
│   ├── controller.py         ✅ Completado
│   └── jvm/                  ✅ NUEVO
│       ├── __init__.py       ✅ Completado
│       ├── classfile.py      ✅ Fase 7 (con soporte Java 6/7/8)
│       ├── constant_pool.py  ✅ Fase 7
│       ├── descriptors.py    ✅ Fase 7
│       ├── instructions.py   ✅ Fase 8
│       ├── jvm_generator.py  ✅ Fase 8
│       ├── attributes.py     📝 Fase 10
│       └── runtime.py        📝 Fase 11
├── tests/
│   ├── test_tac_generator.py   ✅ 11/11
│   ├── test_bytecode_generator.py ✅ 10/10
│   └── jvm/                     ✅ NUEVO
│       ├── test_constant_pool.py   ✅ 8 tests
│       ├── test_classfile.py       ✅ 11 tests
│       ├── test_instructions.py    ✅ 10 tests
│       ├── test_jvm_generator.py   ✅ 10 tests
│       └── test_jvm_validation.py  ✅ 4 tests
└── ui/
    ├── app_ui.py             ✅ Actualizar Fase 12
    └── console_panel.py      ✅ Actualizar Fase 12
```

---

## 📚 Recursos Técnicos

### JVM Specification
- **JVM Spec**: https://docs.oracle.com/javase/specs/jvms/se8/html/
- **Class File Format**: Chapter 4
- **Instruction Set**: Chapter 6

### Herramientas
```bash
# JDK (requerido)
sudo apt install openjdk-17-jdk

# Herramientas de análisis
javap -c -v MyClass.class    # Desensamblar
jd-gui MyClass.class         # Decompilador GUI
```

### Librerías Python
```bash
pip install asm-python       # Para Stack Map Frames (recomendado)
```

---

## 🎯 Versión Actual y Fase de Desarrollo

### **📍 ESTAMOS EN:**
- **Versión**: v2.0.0-alpha.4 ✅ EN DESARROLLO
- **Siguiente**: v2.0.0-alpha.5 (Fase 10 - Attributes)
- **Fase Actual**: Fases 7-9 ✅ completadas → **Fase 10** (Attributes + Metadata)
- **Estado**: Generando bytecode Java 6 válido (.class files ejecutables)

### **Pipeline Actual** (v1.1.0):
```
Kotlin → Lexer → Parser → Semantic → TAC → Bytecode Stack-Based → UI
```

### **Pipeline Objetivo** (v2.0.0):
```
Kotlin → Lexer → Parser → Semantic → TAC → JVM Bytecode → .class → Ejecutar
```

---

## 🔄 Cambios vs Roadmap Anterior

### ❌ Removido (No implementado)
- ~~v1.2 - Optimizaciones de TAC~~ (pospuesto)
- ~~v1.3 - Backend C~~ (cancelado)
- ~~v1.4 - Más features Kotlin~~ (pospuesto a v2.1+)
- ~~v2.0 - LLVM Backend~~ (renombrado a v3.0)

### ✅ Nuevo Enfoque (v2.0)
- **JVM Bytecode Real** como objetivo principal
- Generación de .class ejecutables
- Compatibilidad con JVM estándar
- Enfoque profesional sobre académico

---

## 📝 Notas Importantes

### ⚠️ Advertencias Técnicas
1. **Constant Pool**: Índices empiezan en 1 (no 0)
2. **Long/Double**: Ocupan 2 slots en constant pool
3. **Big-Endian**: Todos los valores multi-byte
4. **Stack Map Frames**: La parte más compleja - usar ASM library
5. **Type Checking**: JVM rechaza bytecode mal tipado

### 💡 Recomendaciones
- Empezar con programas simples (aritmética básica)
- Validar .class generado con `javap` constantemente
- Usar ASM library para Stack Map Frames
- Testear ejecución real con JVM desde día 1

---

## 👤 Autor

**Gabriel Alejandro Medina Miramontes**

Proyecto profesional de compilador Kotlin → JVM Bytecode

**Licencia**: GPL-3.0

---

**¿Listo para empezar con la Fase 7?** 🚀
