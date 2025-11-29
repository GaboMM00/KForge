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

#### Fase 8: JVM Instruction Set
**Duración**: 14 días
**Prioridad**: 🔴 CRÍTICA

- [ ] **JVM Opcodes** (`core/jvm/instructions.py`)
  - [ ] Load/Store tipados: `iload`, `istore`, `dload`, `dstore`, `aload`, `astore`
  - [ ] Constantes: `iconst_0`, `iconst_1`, `bipush`, `ldc`
  - [ ] Aritmética: `iadd`, `isub`, `imul`, `idiv`, `irem`, `dadd`, `dsub`, `dmul`, `ddiv`
  - [ ] Comparaciones: `if_icmpeq`, `if_icmpne`, `if_icmplt`, `if_icmpge`, `if_icmpgt`, `if_icmple`
  - [ ] Control: `goto`, `ifeq`, `ifne`
  - [ ] Arrays: `newarray`, `iaload`, `iastore`, `daload`, `dastore`, `arraylength`
  - [ ] Invocaciones: `invokestatic`, `invokevirtual`
  - [ ] Return: `ireturn`, `dreturn`, `areturn`, `return`

- [ ] **JVM Generator** (`core/jvm/jvm_generator.py`)
  - [ ] Traductor TAC → JVM bytecode
  - [ ] Mapeo de operaciones con tipos
  - [ ] Gestión de local variable slots
  - [ ] Cálculo de max_stack y max_locals

**Entregable**: Generador básico TAC → JVM

---

### 📅 Semana 5: Verificación de Bytecode

#### Fase 9: Stack Map Frames
**Duración**: 7 días
**Prioridad**: 🔴 MUY COMPLEJA

**OPCIÓN A (Recomendada)**: Usar librería ASM
```bash
pip install asm-python
```
- [ ] Integrar ASM para cálculo automático de frames
- [ ] Configurar `COMPUTE_FRAMES` flag

**OPCIÓN B (Avanzada)**: Implementación manual
- [ ] Análisis de flujo de control
- [ ] Cálculo de tipos en cada branch
- [ ] Generación de StackMapTable attribute

**Entregable**: Bytecode verificable por JVM

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
| **1-2** | Fase 7 | ClassFile + Constant Pool | 📝 Siguiente |
| **3-4** | Fase 8 | JVM Instructions | 📝 Planeada |
| **5** | Fase 9 | Stack Map Frames | 📝 Planeada |
| **6** | Fase 10 | Attributes + Metadata | 📝 Planeada |
| **7** | Fase 11 | Runtime Support | 📝 Planeada |
| **8** | Fase 12 | Integration + Tests | 📝 Planeada |

**Tiempo total estimado**: 8 semanas (~60 días)

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
│   └── jvm/                  📝 NUEVO
│       ├── __init__.py
│       ├── classfile.py      📝 Fase 7
│       ├── constant_pool.py  📝 Fase 7
│       ├── descriptors.py    📝 Fase 7
│       ├── instructions.py   📝 Fase 8
│       ├── jvm_generator.py  📝 Fase 8
│       ├── stackmaps.py      📝 Fase 9
│       ├── attributes.py     📝 Fase 10
│       └── runtime.py        📝 Fase 11
├── tests/
│   ├── test_tac_generator.py   ✅ 11/11
│   ├── test_bytecode_generator.py ✅ 10/10
│   └── jvm/                     📝 NUEVO
│       ├── test_classfile.py
│       ├── test_jvm_generation.py
│       └── test_execution.py
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
- **Versión**: v1.1.0 ✅ COMPLETADA
- **Siguiente**: v2.0.0 (JVM Bytecode Real)
- **Fase Actual**: Transición → **Fase 7** (ClassFile + Constant Pool)
- **Estado**: Listo para comenzar desarrollo JVM

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
