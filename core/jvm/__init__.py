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
    'create_hello_world_class'
]
