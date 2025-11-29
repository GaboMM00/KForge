# Fase 9: Enfoque Java 6 - Sin Stack Map Frames

**Versión**: v2.0.0-alpha.4
**Fecha**: 2025-11-28
**Estrategia**: Pragmática - Generar bytecode Java 6 (version 50.0)

---

## Decisión Técnica

En lugar de implementar Stack Map Frames (requeridos para Java 7+), KForge v2.0 genera bytecode compatible con Java 6 (version 50.0) que **no requiere** Stack Map Frames.

### Razones

1. **Simplicidad**: Java 6 no requiere Stack Map Frames para verificación
2. **Compatibilidad**: Java 6 bytecode sigue siendo válido en JVMs modernas
3. **Pragmatismo**: La biblioteca `asm-python` para generación automática de Stack Map Frames no está disponible/mantenida en Python
4. **Funcionalidad completa**: Todas las características de KForge funcionan correctamente en Java 6 bytecode

### Alternativas Consideradas

| Opción | Descripción | Razón de Rechazo |
|--------|-------------|------------------|
| **Opción A**: ASM library | Usar asm-python para generar Stack Map Frames automáticamente | Librería no disponible/mantenida |
| **Opción B**: Implementación manual | Implementar Stack Map Frames manualmente según JVM Spec | Complejidad excesiva para proyecto educativo |
| **Opción C**: Java 6 bytecode | Generar bytecode Java 6 sin Stack Map Frames | **✓ SELECCIONADA** |

---

## Implementación

### 1. Configuración de Versiones

El `ClassFileWriter` ahora soporta múltiples versiones de Java:

```python
from core.jvm.classfile import ClassFileWriter

# Java 6 (default) - Sin Stack Map Frames
writer = ClassFileWriter("MyClass", java_version=6)
# major_version = 50, requires_stack_maps = False

# Java 7 - Requiere Stack Map Frames (no implementado)
writer = ClassFileWriter("MyClass", java_version=7)
# major_version = 51, requires_stack_maps = True

# Java 8 - Requiere Stack Map Frames (no implementado)
writer = ClassFileWriter("MyClass", java_version=8)
# major_version = 52, requires_stack_maps = True
```

### 2. Estructura del .class

```
ClassFile {
    u4 magic = 0xCAFEBABE
    u2 minor_version = 0
    u2 major_version = 50        // Java 6
    ... (resto del class file)
}
```

### 3. Verificación JVM

Java 6 usa **type inference** para verificar bytecode:

- **Java 6**: Inferencia de tipos en tiempo de carga
- **Java 7+**: Stack Map Frames explícitos + verificación

Ambos métodos garantizan seguridad de tipos, pero Java 6 es más flexible.

---

## Compatibilidad

### Versiones de JVM

| JVM Version | Compatibilidad | Notas |
|-------------|----------------|-------|
| Java 6 | ✓ Completa | Versión target |
| Java 7 | ✓ Completa | Acepta bytecode Java 6 |
| Java 8 | ✓ Completa | Acepta bytecode Java 6 |
| Java 11+ | ✓ Completa | Acepta bytecode Java 6 |

### Características Soportadas

Todas las características de KForge funcionan correctamente:

- ✓ Variables locales (Int, Double, String, Boolean)
- ✓ Operaciones aritméticas (+, -, *, /, %)
- ✓ Comparaciones (<, >, <=, >=, ==, !=)
- ✓ Operadores lógicos (&&, ||, !)
- ✓ Control de flujo (if, while, for)
- ✓ Funciones y llamadas
- ✓ Arrays
- ✓ Strings
- ✓ Expresiones complejas

---

## Verificación de Archivos .class

### Con javap (JDK)

```bash
# Generar .class
python tests/jvm/test_classfile.py

# Verificar con javap
javap -v -p tests/jvm/output/HelloWorld.class
```

**Salida esperada**:
```
Classfile tests/jvm/output/HelloWorld.class
  Last modified ...
  SHA-256 checksum ...
  Compiled from "HelloWorld.kt"
public class HelloWorld
  minor version: 0
  major version: 50              <-- Java 6
  flags: (0x0021) ACC_PUBLIC, ACC_SUPER
  this_class: #2                 // HelloWorld
  super_class: #4                // java/lang/Object
  ...
```

### Con la JVM

```bash
# Ejecutar (si tiene método main)
java -cp tests/jvm/output HelloWorld
```

---

## Tests

Todos los tests JVM verifican bytecode Java 6:

```bash
# Ejecutar todos los tests JVM
venv/Scripts/python run_all_jvm_tests.py
```

**Tests incluidos**:
1. `test_constant_pool.py` - Constant Pool
2. `test_classfile.py` - ClassFile Writer (11 tests, incluye test de versiones)
3. `test_instructions.py` - JVM Instructions
4. `test_jvm_generator.py` - TAC to JVM Bytecode
5. `test_jvm_validation.py` - Validación de .class generados

**Total**: 42+ tests, todos pasando ✓

---

## Limitaciones

### Actuales

- No se generan Stack Map Frames (no requeridos para Java 6)
- Version fija en Java 6 (50.0) por defecto

### Futuras Mejoras (Opcional)

Si se desea soporte para Java 7+:

1. **Implementar Stack Map Frame Generator**:
   - Analizar flujo de control (basic blocks)
   - Calcular tipos en cada punto de merge
   - Generar frames según JVM Spec §4.7.4

2. **Agregar StackMapTable Attribute**:
   ```python
   class StackMapTableAttribute(AttributeInfo):
       def __init__(self, name_index: int, frames: List[StackMapFrame]):
           # Implementation
   ```

3. **Actualizar CodeAttribute**:
   - Agregar StackMapTable como sub-atributo
   - Solo para major_version >= 51

**Esfuerzo estimado**: 2-3 semanas de trabajo adicional

---

## Referencias

### JVM Specification

- [JVM SE 6 Spec](https://docs.oracle.com/javase/specs/jvms/se6/html/VMSpecTOC.doc.html)
- [JVM SE 7 Spec - Stack Map Frames](https://docs.oracle.com/javase/specs/jvms/se7/html/jvms-4.html#jvms-4.7.4)
- [Type Checking Verification](https://docs.oracle.com/javase/specs/jvms/se6/html/ClassFile.doc.html#9916)

### Archivos Relevantes

```
core/jvm/
├── classfile.py           # ClassFileWriter con soporte multi-versión
├── constant_pool.py       # Constant Pool
├── descriptors.py         # Type Descriptors
├── instructions.py        # JVM Instructions
└── jvm_generator.py       # TAC to JVM Generator

tests/jvm/
├── test_constant_pool.py
├── test_classfile.py      # Incluye test_java_version_configuration()
├── test_instructions.py
├── test_jvm_generator.py
└── test_jvm_validation.py
```

---

## Conclusión

El enfoque de Java 6 bytecode es **pragmático y funcional**:

✓ **Simple**: No requiere implementar Stack Map Frames
✓ **Compatible**: Funciona en todas las JVMs modernas
✓ **Completo**: Soporta todas las características de KForge
✓ **Verificable**: Archivos .class válidos que pasan verificación JVM
✓ **Extensible**: Arquitectura preparada para agregar Java 7+ en el futuro

**Estado**: Fase 9 completada con enfoque Java 6 ✓
