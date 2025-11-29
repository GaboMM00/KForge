"""
Modulo JVM - Generacion de bytecode JVM real

Componentes implementados:
- Constant Pool: Gestion de constantes del .class
- Descriptors: Conversion de tipos Kotlin a descriptores JVM
- ClassFile: Escritor de archivos .class validos

Proximos componentes (Fases 8-12):
- Instructions: Conjunto de instrucciones JVM
- JVM Generator: Conversor TAC a Bytecode JVM
- Stack Maps: Stack Map Frames para verificacion
- Attributes: LineNumberTable, LocalVariableTable
- Runtime: Soporte runtime (println, arrays)
"""

from core.jvm.constant_pool import (
    ConstantPool,
    ConstantPoolEntry,
    Utf8Constant,
    IntegerConstant,
    FloatConstant,
    LongConstant,
    DoubleConstant,
    ClassConstant,
    StringConstant,
    FieldrefConstant,
    MethodrefConstant,
    NameAndTypeConstant
)

from core.jvm.descriptors import (
    TypeDescriptor
)

from core.jvm.classfile import (
    ClassFileWriter,
    MethodInfo,
    AttributeInfo,
    CodeAttribute,
    SourceFileAttribute,
    AccessFlags,
    create_minimal_class,
    create_hello_world_class
)

from core.jvm.instructions import (
    JVMOpcode,
    JVMInstruction,
    ArrayType,
    iconst,
    iload,
    istore,
    dload,
    dstore,
    aload,
    astore
)

from core.jvm.jvm_generator import (
    JVMGenerator,
    LocalVariableManager,
    StackDepthTracker
)

from core.jvm.attributes import (
    LineNumberTableAttribute,
    LocalVariableTableAttribute,
    LineNumberEntry,
    LocalVariableEntry,
    create_line_number_table,
    create_local_variable_table
)

__all__ = [
    # Constant Pool
    'ConstantPool',
    'ConstantPoolEntry',
    'Utf8Constant',
    'IntegerConstant',
    'FloatConstant',
    'LongConstant',
    'DoubleConstant',
    'ClassConstant',
    'StringConstant',
    'FieldrefConstant',
    'MethodrefConstant',
    'NameAndTypeConstant',

    # Descriptors
    'TypeDescriptor',

    # ClassFile
    'ClassFileWriter',
    'MethodInfo',
    'AttributeInfo',
    'CodeAttribute',
    'SourceFileAttribute',
    'AccessFlags',
    'create_minimal_class',
    'create_hello_world_class',

    # Instructions
    'JVMOpcode',
    'JVMInstruction',
    'ArrayType',
    'iconst',
    'iload',
    'istore',
    'dload',
    'dstore',
    'aload',
    'astore',

    # Generator
    'JVMGenerator',
    'LocalVariableManager',
    'StackDepthTracker',

    # Attributes
    'LineNumberTableAttribute',
    'LocalVariableTableAttribute',
    'LineNumberEntry',
    'LocalVariableEntry',
    'create_line_number_table',
    'create_local_variable_table'
]
