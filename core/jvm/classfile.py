"""
ClassFile Writer - Generador de archivos .class JVM

Implementa la estructura completa del formato .class según la JVM Specification.
Genera archivos .class válidos que pueden ser ejecutados por la JVM.

Estructura de un .class file:
    ClassFile {
        u4             magic;              // 0xCAFEBABE
        u2             minor_version;      // 0
        u2             major_version;      // 52 (Java 8)
        u2             constant_pool_count;
        cp_info        constant_pool[constant_pool_count-1];
        u2             access_flags;       // PUBLIC, SUPER
        u2             this_class;         // Index en constant pool
        u2             super_class;        // Index en constant pool
        u2             interfaces_count;   // 0 por ahora
        u2             interfaces[interfaces_count];
        u2             fields_count;       // 0 por ahora
        field_info     fields[fields_count];
        u2             methods_count;
        method_info    methods[methods_count];
        u2             attributes_count;
        attribute_info attributes[attributes_count];
    }

Referencias:
- https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html
"""

import struct
from typing import List, Optional
from core.jvm.constant_pool import ConstantPool


# Access Flags para clases (JVM Spec Table 4.1-B)
class AccessFlags:
    """Access flags para clases, métodos y fields."""

    # Class access flags
    ACC_PUBLIC = 0x0001      # Declarado public
    ACC_FINAL = 0x0010       # Declarado final
    ACC_SUPER = 0x0020       # Tratar invocaciones superclass especiales (siempre set en Java moderno)
    ACC_INTERFACE = 0x0200   # Es una interface
    ACC_ABSTRACT = 0x0400    # Declarado abstract
    ACC_SYNTHETIC = 0x1000   # Generado por compilador
    ACC_ANNOTATION = 0x2000  # Es una annotation
    ACC_ENUM = 0x4000        # Es un enum

    # Method access flags
    ACC_PRIVATE = 0x0002     # Declarado private
    ACC_PROTECTED = 0x0004   # Declarado protected
    ACC_STATIC = 0x0008      # Declarado static
    ACC_SYNCHRONIZED = 0x0020  # Declarado synchronized
    ACC_BRIDGE = 0x0040      # Bridge method (generado por compilador)
    ACC_VARARGS = 0x0080     # Usa varargs
    ACC_NATIVE = 0x0100      # Declarado native
    ACC_STRICT = 0x0800      # Usa strict floating point


class MethodInfo:
    """
    Representa un método en el .class file.

    method_info {
        u2             access_flags;
        u2             name_index;          // Index en constant pool
        u2             descriptor_index;    // Index en constant pool
        u2             attributes_count;
        attribute_info attributes[attributes_count];
    }
    """

    def __init__(self, access_flags: int, name_index: int, descriptor_index: int):
        self.access_flags = access_flags
        self.name_index = name_index
        self.descriptor_index = descriptor_index
        self.attributes: List['AttributeInfo'] = []

    def add_attribute(self, attribute: 'AttributeInfo'):
        """Agrega un atributo al método (Code, Exceptions, etc.)."""
        self.attributes.append(attribute)

    def to_bytes(self) -> bytes:
        """Convierte el método a bytes."""
        result = struct.pack('>HHH',
            self.access_flags,
            self.name_index,
            self.descriptor_index
        )

        # Attributes
        result += struct.pack('>H', len(self.attributes))
        for attr in self.attributes:
            result += attr.to_bytes()

        return result


class AttributeInfo:
    """
    Clase base para atributos.

    attribute_info {
        u2 attribute_name_index;  // Index en constant pool
        u4 attribute_length;      // Longitud de info[]
        u1 info[attribute_length];
    }
    """

    def __init__(self, name_index: int, info: bytes):
        self.name_index = name_index
        self.info = info

    def to_bytes(self) -> bytes:
        """Convierte el atributo a bytes."""
        return struct.pack('>HI',
            self.name_index,
            len(self.info)
        ) + self.info


class CodeAttribute(AttributeInfo):
    """
    Atributo Code para métodos.

    Code_attribute {
        u2 attribute_name_index;
        u4 attribute_length;
        u2 max_stack;             // Tamaño máximo del stack
        u2 max_locals;            // Número de variables locales
        u4 code_length;           // Longitud del bytecode
        u1 code[code_length];     // Bytecode real
        u2 exception_table_length;
        {   u2 start_pc;
            u2 end_pc;
            u2 handler_pc;
            u2 catch_type;
        } exception_table[exception_table_length];
        u2 attributes_count;
        attribute_info attributes[attributes_count];
    }
    """

    def __init__(self, name_index: int, max_stack: int, max_locals: int, code: bytes):
        self.name_index = name_index
        self.max_stack = max_stack
        self.max_locals = max_locals
        self.code = code
        self.exception_table: List[tuple] = []  # (start_pc, end_pc, handler_pc, catch_type)
        self.attributes: List[AttributeInfo] = []

    def to_bytes(self) -> bytes:
        """Convierte el atributo Code a bytes."""
        # Construir info del atributo
        info = struct.pack('>HH', self.max_stack, self.max_locals)
        info += struct.pack('>I', len(self.code))
        info += self.code

        # Exception table
        info += struct.pack('>H', len(self.exception_table))
        for entry in self.exception_table:
            info += struct.pack('>HHHH', *entry)

        # Sub-attributes (LineNumberTable, LocalVariableTable, etc.)
        info += struct.pack('>H', len(self.attributes))
        for attr in self.attributes:
            info += attr.to_bytes()

        # Atributo completo
        return struct.pack('>HI',
            self.name_index,
            len(info)
        ) + info


class SourceFileAttribute(AttributeInfo):
    """
    Atributo SourceFile para indicar el archivo .kt original.

    SourceFile_attribute {
        u2 attribute_name_index;
        u4 attribute_length;      // Siempre 2
        u2 sourcefile_index;      // Index en constant pool
    }
    """

    def __init__(self, name_index: int, sourcefile_index: int):
        self.name_index = name_index
        self.sourcefile_index = sourcefile_index

    def to_bytes(self) -> bytes:
        """Convierte el atributo SourceFile a bytes."""
        info = struct.pack('>H', self.sourcefile_index)
        return struct.pack('>HI',
            self.name_index,
            len(info)
        ) + info


class ClassFileWriter:
    """
    Escritor de archivos .class JVM.

    Genera archivos .class válidos siguiendo la JVM Specification.

    Soporta dos modos:
    - Java 6 (50.0): No requiere Stack Map Frames (más simple)
    - Java 7+ (51.0+): Requiere Stack Map Frames para verificación
    """

    # Magic number del formato .class
    MAGIC = 0xCAFEBABE

    # Versiones soportadas
    JAVA_6_MAJOR = 50  # Java 6 - No requiere Stack Map Frames
    JAVA_7_MAJOR = 51  # Java 7 - Requiere Stack Map Frames
    JAVA_8_MAJOR = 52  # Java 8 - Requiere Stack Map Frames

    MINOR_VERSION = 0

    def __init__(self, class_name: str, java_version: int = 6):
        """
        Inicializa el ClassFile writer.

        Args:
            class_name: Nombre de la clase (formato: "com/example/MyClass")
            java_version: Versión de Java target (6, 7, o 8). Default: 6 (sin Stack Map Frames)
        """
        self.class_name = class_name
        self.constant_pool = ConstantPool()
        self.access_flags = AccessFlags.ACC_PUBLIC | AccessFlags.ACC_SUPER

        # Configurar versión según target
        if java_version == 6:
            self.major_version = self.JAVA_6_MAJOR
        elif java_version == 7:
            self.major_version = self.JAVA_7_MAJOR
        elif java_version == 8:
            self.major_version = self.JAVA_8_MAJOR
        else:
            # Default a Java 6 para simplicidad
            self.major_version = self.JAVA_6_MAJOR

        self.minor_version = self.MINOR_VERSION
        self.requires_stack_maps = self.major_version >= self.JAVA_7_MAJOR
        self.this_class: Optional[int] = None
        self.super_class: Optional[int] = None
        self.interfaces: List[int] = []
        self.fields: List = []  # Por implementar en Fase 8
        self.methods: List[MethodInfo] = []
        self.attributes: List[AttributeInfo] = []

        # Configurar clase actual y superclase por defecto
        self._setup_basic_class()

    def _setup_basic_class(self):
        """Configura la clase básica con Object como superclase."""
        self.this_class = self.constant_pool.add_class(self.class_name)
        self.super_class = self.constant_pool.add_class("java/lang/Object")

    def add_method(self, method: MethodInfo):
        """Agrega un método a la clase."""
        self.methods.append(method)

    def add_attribute(self, attribute: AttributeInfo):
        """Agrega un atributo a la clase (SourceFile, etc.)."""
        self.attributes.append(attribute)

    def add_source_file(self, source_file: str):
        """
        Agrega el atributo SourceFile.

        Args:
            source_file: Nombre del archivo fuente (ej: "Main.kt")
        """
        sourcefile_name_index = self.constant_pool.add_utf8("SourceFile")
        sourcefile_index = self.constant_pool.add_utf8(source_file)
        attr = SourceFileAttribute(sourcefile_name_index, sourcefile_index)
        self.add_attribute(attr)

    def to_bytes(self) -> bytes:
        """
        Genera el contenido completo del archivo .class como bytes.

        Returns:
            Bytes del archivo .class válido
        """
        result = b''

        # 1. Magic number
        result += struct.pack('>I', self.MAGIC)

        # 2. Version (minor, major)
        result += struct.pack('>HH', self.minor_version, self.major_version)

        # 3. Constant pool
        result += self.constant_pool.to_bytes()

        # 4. Access flags
        result += struct.pack('>H', self.access_flags)

        # 5. This class
        result += struct.pack('>H', self.this_class)

        # 6. Super class
        result += struct.pack('>H', self.super_class)

        # 7. Interfaces
        result += struct.pack('>H', len(self.interfaces))
        for interface in self.interfaces:
            result += struct.pack('>H', interface)

        # 8. Fields
        result += struct.pack('>H', len(self.fields))
        for field in self.fields:
            result += field.to_bytes()

        # 9. Methods
        result += struct.pack('>H', len(self.methods))
        for method in self.methods:
            result += method.to_bytes()

        # 10. Attributes
        result += struct.pack('>H', len(self.attributes))
        for attr in self.attributes:
            result += attr.to_bytes()

        return result

    def write_to_file(self, filename: str):
        """
        Escribe el archivo .class al disco.

        Args:
            filename: Ruta del archivo a escribir (debe terminar en .class)
        """
        bytecode = self.to_bytes()
        with open(filename, 'wb') as f:
            f.write(bytecode)

    def get_class_info(self) -> dict:
        """
        Retorna información del .class generado para debugging.

        Returns:
            Diccionario con información del class file
        """
        return {
            'magic': f'0x{self.MAGIC:X}',
            'version': f'{self.major_version}.{self.minor_version}',
            'class_name': self.class_name,
            'constant_pool_count': self.constant_pool.get_count(),
            'constant_pool_entries': len(self.constant_pool),
            'access_flags': f'0x{self.access_flags:04X}',
            'methods_count': len(self.methods),
            'attributes_count': len(self.attributes),
            'bytecode_size': len(self.to_bytes())
        }


def create_minimal_class(class_name: str, source_file: str, java_version: int = 6) -> ClassFileWriter:
    """
    Crea una clase mínima válida (sin métodos).

    Útil para testing y como punto de partida.

    Args:
        class_name: Nombre de la clase (ej: "MinimalClass")
        source_file: Nombre del archivo fuente (ej: "MinimalClass.kt")
        java_version: Versión de Java target (6, 7, o 8). Default: 6

    Returns:
        ClassFileWriter configurado
    """
    writer = ClassFileWriter(class_name, java_version=java_version)
    writer.add_source_file(source_file)
    return writer


def create_hello_world_class(java_version: int = 6) -> ClassFileWriter:
    """
    Crea una clase con un método main vacío.

    class HelloWorld {
        public static void main(String[] args) {
            return;  // Solo retorna
        }
    }

    Args:
        java_version: Versión de Java target (6, 7, o 8). Default: 6

    Returns:
        ClassFileWriter configurado
    """
    writer = ClassFileWriter("HelloWorld", java_version=java_version)
    writer.add_source_file("HelloWorld.kt")

    # Crear método main
    name_index = writer.constant_pool.add_utf8("main")
    descriptor_index = writer.constant_pool.add_utf8("([Ljava/lang/String;)V")

    method = MethodInfo(
        AccessFlags.ACC_PUBLIC | AccessFlags.ACC_STATIC,
        name_index,
        descriptor_index
    )

    # Agregar atributo Code vacío (solo return)
    code_name_index = writer.constant_pool.add_utf8("Code")
    code_bytes = b'\xb1'  # return (0xb1)

    code_attr = CodeAttribute(
        code_name_index,
        max_stack=0,      # No usa el stack
        max_locals=1,     # args[]
        code=code_bytes
    )

    method.add_attribute(code_attr)
    writer.add_method(method)

    return writer
