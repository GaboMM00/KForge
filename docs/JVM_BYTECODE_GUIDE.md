# 🔧 Gu

ía de Implementación JVM Bytecode

**Objetivo**: Generar archivos `.class` ejecutables desde código Kotlin
**Versión**: 2.0 (En desarrollo - Fase 7)

---

## 📋 Índice

1. [Introducción](#introducción)
2. [Estructura de Archivos .class](#estructura-de-archivos-class)
3. [Constant Pool](#constant-pool)
4. [JVM Instruction Set](#jvm-instruction-set)
5. [Stack Map Frames](#stack-map-frames)
6. [Attributes](#attributes)
7. [Runtime Support](#runtime-support)
8. [Plan de Implementación](#plan-de-implementación)

---

## 🎯 Introducción

### ¿Qué es JVM Bytecode?

JVM bytecode es el código ejecutable de bajo nivel que la Java Virtual Machine entiende. A diferencia del bytecode educativo que generamos en v1.1 (formato texto assembly), el JVM bytecode es:

- **Binario**: Archivo .class en formato binario
- **Tipado**: Cada instrucción es específica para un tipo (iload para Int, dload para Double)
- **Verificable**: La JVM valida el bytecode antes de ejecutarlo
- **Portable**: Ejecutable en cualquier JVM (Windows, Linux, macOS)

### Diferencia con Bytecode v1.1

| Aspecto | v1.1 (Educativo) | v2.0 (JVM Real) |
|---------|------------------|-----------------|
| **Formato** | Texto .asm | Binario .class |
| **Instrucciones** | ~25 genéricas | 200+ tipadas |
| **Ejecución** | No ejecutable | `java ClassName` |
| **Verificación** | No | Stack Map Frames |
| **Constantes** | Inline | Constant Pool |

---

## 📦 Estructura de Archivos .class

### Formato General

```
ClassFile {
    u4             magic;                    // 0xCAFEBABE
    u2             minor_version;            // 0
    u2             major_version;            // 52 (Java 8)
    u2             constant_pool_count;      // N + 1
    cp_info        constant_pool[count-1];   // Constant pool entries
    u2             access_flags;             // PUBLIC, SUPER
    u2             this_class;               // Index en constant pool
    u2             super_class;              // Index a java/lang/Object
    u2             interfaces_count;         // 0 (no interfaces por ahora)
    u2             interfaces[count];        // []
    u2             fields_count;             // 0 (no fields por ahora)
    field_info     fields[count];            // []
    u2             methods_count;            // Número de métodos
    method_info    methods[count];           // main(), suma(), etc.
    u2             attributes_count;         // SourceFile, etc.
    attribute_info attributes[count];        // []
}
```

### Ejemplo Mínimo

Para generar el .class más simple posible:

```python
import struct

def write_minimal_class(filename="MinimalClass.class"):
    with open(filename, 'wb') as f:
        # Magic number
        f.write(struct.pack('>I', 0xCAFEBABE))

        # Version (Java 8 = 52.0)
        f.write(struct.pack('>HH', 0, 52))

        # Constant pool (count = 1 significa vacío)
        f.write(struct.pack('>H', 1))

        # Access flags (PUBLIC | SUPER = 0x0021)
        f.write(struct.pack('>H', 0x0021))

        # this_class (index 0 = invalid por ahora)
        f.write(struct.pack('>H', 0))

        # super_class (index 0)
        f.write(struct.pack('>H', 0))

        # interfaces_count
        f.write(struct.pack('>H', 0))

        # fields_count
        f.write(struct.pack('>H', 0))

        # methods_count
        f.write(struct.pack('>H', 0))

        # attributes_count
        f.write(struct.pack('>H', 0))
```

**Nota**: Este .class es inválido pero muestra la estructura básica.

---

## 🗂️ Constant Pool

### ¿Qué es el Constant Pool?

El Constant Pool es una tabla de constantes referenciadas por el bytecode:
- Strings literales
- Nombres de clases y métodos
- Valores numéricos
- Descriptores de tipos

### Tipos de Constantes

```python
CONSTANT_Utf8 = 1              # Strings UTF-8
CONSTANT_Integer = 3           # int de 4 bytes
CONSTANT_Float = 4             # float de 4 bytes
CONSTANT_Long = 5              # long de 8 bytes (ocupa 2 slots!)
CONSTANT_Double = 6            # double de 8 bytes (ocupa 2 slots!)
CONSTANT_Class = 7             # Referencia a clase
CONSTANT_String = 8            # Referencia a string
CONSTANT_Fieldref = 9          # Referencia a field
CONSTANT_Methodref = 10        # Referencia a método
CONSTANT_InterfaceMethodref = 11
CONSTANT_NameAndType = 12      # Nombre + descriptor
```

### Estructura de Constantes

#### CONSTANT_Utf8

```
CONSTANT_Utf8_info {
    u1 tag;                    // 1
    u2 length;                 // Longitud en bytes
    u1 bytes[length];          // UTF-8 encoding
}
```

#### CONSTANT_Class

```
CONSTANT_Class_info {
    u1 tag;                    // 7
    u2 name_index;             // Index a CONSTANT_Utf8
}
```

#### CONSTANT_Methodref

```
CONSTANT_Methodref_info {
    u1 tag;                    // 10
    u2 class_index;            // Index a CONSTANT_Class
    u2 name_and_type_index;    // Index a CONSTANT_NameAndType
}
```

#### CONSTANT_NameAndType

```
CONSTANT_NameAndType_info {
    u1 tag;                    // 12
    u2 name_index;             // Index a CONSTANT_Utf8 (nombre)
    u2 descriptor_index;       // Index a CONSTANT_Utf8 (descriptor)
}
```

### Ejemplo de Constant Pool

Para el método `suma(int, int)`:

```
Constant Pool:
   #1 = Utf8               MyClass
   #2 = Class              #1          // MyClass
   #3 = Utf8               java/lang/Object
   #4 = Class              #3          // java/lang/Object
   #5 = Utf8               suma
   #6 = Utf8               (II)I
   #7 = NameAndType        #5:#6       // suma:(II)I
   #8 = Methodref          #2.#7       // MyClass.suma:(II)I
   #9 = Utf8               Code
  #10 = Utf8               LineNumberTable
  #11 = Utf8               SourceFile
  #12 = Utf8               MyClass.kt
```

### Gestión de Índices

⚠️ **IMPORTANTE**: Los índices del Constant Pool empiezan en 1, NO en 0!

```python
class ConstantPool:
    def __init__(self):
        self.constants = []  # La posición 0 NO se usa

    def add_utf8(self, text: str) -> int:
        """Agrega un CONSTANT_Utf8 y retorna su índice (1-based)"""
        # Verificar si ya existe
        for i, const in enumerate(self.constants):
            if const.tag == 1 and const.text == text:
                return i + 1  # Índices empiezan en 1

        # Agregar nuevo
        self.constants.append(Utf8Constant(text))
        return len(self.constants)  # 1-based
```

⚠️ **CUIDADO**: Long y Double ocupan 2 slots:

```python
def add_long(self, value: int) -> int:
    index = len(self.constants) + 1
    self.constants.append(LongConstant(value))
    self.constants.append(None)  # Slot vacío!
    return index
```

---

## 🔧 JVM Instruction Set

### Instrucciones por Tipo

#### Load/Store (Variables Locales)

| Instrucción | Opcode | Descripción | Stack Effect |
|-------------|--------|-------------|--------------|
| `iload_0` | 0x1A | Load int from local 0 | → value |
| `iload_1` | 0x1B | Load int from local 1 | → value |
| `iload <n>` | 0x15 | Load int from local n | → value |
| `istore_0` | 0x3B | Store int to local 0 | value → |
| `istore <n>` | 0x36 | Store int to local n | value → |
| `dload_0` | 0x26 | Load double from local 0 | → value |
| `dstore_0` | 0x47 | Store double to local 0 | value → |
| `aload_0` | 0x2A | Load reference from local 0 | → objectref |
| `astore_0` | 0x4B | Store reference to local 0 | objectref → |

#### Constantes

| Instrucción | Opcode | Descripción | Stack Effect |
|-------------|--------|-------------|--------------|
| `iconst_m1` | 0x02 | Push int -1 | → -1 |
| `iconst_0` | 0x03 | Push int 0 | → 0 |
| `iconst_1` | 0x04 | Push int 1 | → 1 |
| `iconst_2` - `iconst_5` | 0x05-0x08 | Push int 2-5 | → value |
| `bipush <byte>` | 0x10 | Push byte (-128 to 127) | → value |
| `sipush <short>` | 0x11 | Push short (-32768 to 32767) | → value |
| `ldc <index>` | 0x12 | Push from const pool | → value |
| `dconst_0` | 0x0E | Push double 0.0 | → 0.0 |
| `dconst_1` | 0x0F | Push double 1.0 | → 1.0 |

#### Aritmética

| Instrucción | Opcode | Descripción | Stack Effect |
|-------------|--------|-------------|--------------|
| `iadd` | 0x60 | Add int | value1, value2 → result |
| `isub` | 0x64 | Subtract int | value1, value2 → result |
| `imul` | 0x68 | Multiply int | value1, value2 → result |
| `idiv` | 0x6C | Divide int | value1, value2 → result |
| `irem` | 0x70 | Remainder int (%) | value1, value2 → result |
| `ineg` | 0x74 | Negate int | value → result |
| `dadd` | 0x63 | Add double | value1, value2 → result |
| `dsub` | 0x67 | Subtract double | value1, value2 → result |
| `dmul` | 0x6B | Multiply double | value1, value2 → result |
| `ddiv` | 0x6F | Divide double | value1, value2 → result |

#### Comparaciones y Saltos

| Instrucción | Opcode | Descripción | Stack Effect |
|-------------|--------|-------------|--------------|
| `if_icmpeq <offset>` | 0x9F | if value1 == value2 | value1, value2 → |
| `if_icmpne <offset>` | 0xA0 | if value1 != value2 | value1, value2 → |
| `if_icmplt <offset>` | 0xA1 | if value1 < value2 | value1, value2 → |
| `if_icmpge <offset>` | 0xA2 | if value1 >= value2 | value1, value2 → |
| `if_icmpgt <offset>` | 0xA3 | if value1 > value2 | value1, value2 → |
| `if_icmple <offset>` | 0xA4 | if value1 <= value2 | value1, value2 → |
| `ifeq <offset>` | 0x99 | if value == 0 | value → |
| `ifne <offset>` | 0x9A | if value != 0 | value → |
| `iflt <offset>` | 0x9B | if value < 0 | value → |
| `ifge <offset>` | 0x9C | if value >= 0 | value → |
| `ifgt <offset>` | 0x9D | if value > 0 | value → |
| `ifle <offset>` | 0x9E | if value <= 0 | value → |
| `goto <offset>` | 0xA7 | Unconditional jump | - |

#### Arrays

| Instrucción | Opcode | Descripción | Stack Effect |
|-------------|--------|-------------|--------------|
| `newarray <type>` | 0xBC | Create new array | count → arrayref |
| `iaload` | 0x2E | Load int from array | arrayref, index → value |
| `iastore` | 0x4F | Store int in array | arrayref, index, value → |
| `daload` | 0x31 | Load double from array | arrayref, index → value |
| `dastore` | 0x52 | Store double in array | arrayref, index, value → |
| `arraylength` | 0xBE | Get array length | arrayref → length |

Tipos para `newarray`:
- `T_INT = 10`
- `T_DOUBLE = 7`

#### Invocaciones

| Instrucción | Opcode | Descripción | Stack Effect |
|-------------|--------|-------------|--------------|
| `invokestatic <index>` | 0xB8 | Invoke static method | [args...] → [result] |
| `invokevirtual <index>` | 0xB6 | Invoke instance method | objectref, [args...] → [result] |

#### Return

| Instrucción | Opcode | Descripción | Stack Effect |
|-------------|--------|-------------|--------------|
| `ireturn` | 0xAC | Return int | value → [empty] |
| `dreturn` | 0xAF | Return double | value → [empty] |
| `areturn` | 0xB0 | Return reference | objectref → [empty] |
| `return` | 0xB1 | Return void | → [empty] |

#### Otros

| Instrucción | Opcode | Descripción | Stack Effect |
|-------------|--------|-------------|--------------|
| `pop` | 0x57 | Pop top value | value → |
| `dup` | 0x59 | Duplicate top value | value → value, value |
| `getstatic <index>` | 0xB2 | Get static field | → value |
| `putstatic <index>` | 0xB3 | Set static field | value → |

### Ejemplo de Traducción TAC → JVM

#### TAC:
```tac
t1 = a + b
RETURN t1
```

#### JVM Bytecode:
```
iload_0        ; Load 'a' (local 0)
iload_1        ; Load 'b' (local 1)
iadd           ; a + b
istore_2       ; Store in 't1' (local 2)
iload_2        ; Load 't1'
ireturn        ; Return value
```

#### Optimizado:
```
iload_0        ; Load 'a'
iload_1        ; Load 'b'
iadd           ; a + b
ireturn        ; Return directly (no temp needed)
```

---

## 🗺️ Stack Map Frames

### ¿Por qué son necesarios?

Desde Java 7, la JVM requiere **Stack Map Frames** para verificación de bytecode. Estos frames describen el estado del stack y variables locales en cada punto de salto (branch).

### Opciones de Implementación

#### Opción A: Usar ASM Library (RECOMENDADA)

```bash
pip install asm-python
```

```python
from org.objectweb.asm import ClassWriter, MethodVisitor

writer = ClassWriter(ClassWriter.COMPUTE_FRAMES)
# ASM calcula frames automáticamente
```

**Ventajas**:
- ✅ ASM calcula frames automáticamente
- ✅ Menos propenso a errores
- ✅ Implementación más rápida

**Desventajas**:
- ❌ Dependencia externa
- ❌ Menos control fino

#### Opción B: Implementación Manual

```python
class StackMapFrame:
    """Representa el estado en un punto de branch"""
    def __init__(self):
        self.offset = 0
        self.locals = []   # Tipos de variables locales
        self.stack = []    # Tipos en el stack
```

**Ventajas**:
- ✅ Sin dependencias externas
- ✅ Control total del proceso

**Desventajas**:
- ❌ Muy complejo de implementar correctamente
- ❌ Alto riesgo de bugs
- ❌ Requiere análisis de flujo de control completo

**Recomendación**: Usar ASM para v2.0, implementación manual para v2.1+ si se desea.

---

## 📋 Attributes

### SourceFile Attribute

```
SourceFile_attribute {
    u2 attribute_name_index;    // Index a "SourceFile" en constant pool
    u4 attribute_length;        // 2
    u2 sourcefile_index;        // Index al nombre del archivo .kt
}
```

### LineNumberTable Attribute

Mapea PC offset → línea de código fuente (para debugging):

```
LineNumberTable_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
    u2 line_number_table_length;
    {   u2 start_pc;
        u2 line_number;
    } line_number_table[length];
}
```

### LocalVariableTable Attribute

Mapea slots de variables locales a nombres (para debugging):

```
LocalVariableTable_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
    u2 local_variable_table_length;
    {   u2 start_pc;
        u2 length;
        u2 name_index;
        u2 descriptor_index;
        u2 index;
    } local_variable_table[length];
}
```

---

## 🔧 Runtime Support

### println() → System.out.println

```kotlin
println(42)
```

Genera:

```
getstatic java/lang/System.out Ljava/io/PrintStream;
bipush 42
invokevirtual java/io/PrintStream.println (I)V
```

Constant Pool necesario:
```
#1 = Fieldref  java/lang/System.out:Ljava/io/PrintStream;
#2 = Methodref java/io/PrintStream.println:(I)V
```

### intArrayOf() → newarray

```kotlin
var arr: IntArray = intArrayOf(1, 2, 3)
```

Genera:

```
iconst_3       ; array length
newarray 10    ; T_INT = 10
dup
iconst_0
iconst_1
iastore        ; arr[0] = 1
dup
iconst_1
iconst_2
iastore        ; arr[1] = 2
dup
iconst_2
iconst_3
iastore        ; arr[2] = 3
astore_0       ; store in local 0
```

### main() Method Signature

```kotlin
fun main() { ... }
```

Debe generar:

```
public static void main(java.lang.String[]);
  descriptor: ([Ljava/lang/String;)V
  flags: (0x0009) ACC_PUBLIC, ACC_STATIC
```

---

## 📅 Plan de Implementación

### Fase 7: ClassFile + Constant Pool (Semanas 1-2)

**Objetivo**: Generar un archivo .class válido (vacío pero estructuralmente correcto)

**Entregables**:
1. `core/jvm/classfile.py` - Escritor de estructura .class
2. `core/jvm/constant_pool.py` - Gestor de constant pool
3. `core/jvm/descriptors.py` - Generador de descriptors JVM
4. `tests/jvm/test_classfile.py` - Tests unitarios

**Milestone**: Ejecutar `javap -c -v EmptyClass.class` sin errores

### Fase 8: JVM Instructions (Semanas 3-4)

**Objetivo**: Generador TAC → JVM bytecode

**Entregables**:
1. `core/jvm/instructions.py` - Definiciones de instrucciones
2. `core/jvm/jvm_generator.py` - Generador TAC → JVM
3. `tests/jvm/test_jvm_generation.py` - Tests de generación

**Milestone**: Compilar `val x = 5 + 3` a bytecode válido

### Fase 9: Stack Map Frames (Semana 5)

**Objetivo**: Bytecode verificable por JVM

**Entregables**:
1. `core/jvm/stackmaps.py` - Generador de stack map frames (o integración con ASM)
2. Tests de verificación

**Milestone**: JVM acepta el bytecode sin errores de verificación

### Fase 10: Attributes (Semana 6)

**Objetivo**: Debugging info

**Entregables**:
1. `core/jvm/attributes.py` - SourceFile, LineNumberTable, LocalVariableTable
2. Tests de attributes

**Milestone**: `javap -c -v` muestra info de debugging

### Fase 11: Runtime Support (Semana 7)

**Objetivo**: println, arrays, main()

**Entregables**:
1. `core/jvm/runtime.py` - Soporte runtime
2. Tests de I/O y arrays

**Milestone**: Ejecutar `java MyClass` imprime correctamente

### Fase 12: Integration + Testing (Semana 8)

**Objetivo**: Pipeline completo funcional

**Entregables**:
1. Integración en `core/controller.py`
2. Integración en UI (`ui/app_ui.py`)
3. Suite completa de tests
4. Test final: Bubble Sort ejecutable

**Milestone**: **v2.0 RELEASE** - Compilador JVM funcional

---

## 📚 Referencias

- **JVM Spec SE 8**: https://docs.oracle.com/javase/specs/jvms/se8/html/
- **Class File Format**: https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html
- **Instruction Set**: https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-6.html
- **ASM Library**: https://asm.ow2.io/

---

**Autor**: Gabriel Alejandro Medina Miramontes
**Fecha**: 2025-11-28
**Versión**: 1.0
