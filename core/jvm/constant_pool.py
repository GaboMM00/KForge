"""
Gestor del Constant Pool para archivos .class de JVM.

El Constant Pool es una tabla de constantes referenciadas por el bytecode JVM.
Incluye strings, nombres de clases, métodos, tipos, y valores numéricos.

Especificación: https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html#jvms-4.4
"""

from typing import Optional, List, Dict
from dataclasses import dataclass
import struct


# Tags de tipos de constantes JVM
CONSTANT_Utf8 = 1
CONSTANT_Integer = 3
CONSTANT_Float = 4
CONSTANT_Long = 5
CONSTANT_Double = 6
CONSTANT_Class = 7
CONSTANT_String = 8
CONSTANT_Fieldref = 9
CONSTANT_Methodref = 10
CONSTANT_InterfaceMethodref = 11
CONSTANT_NameAndType = 12
CONSTANT_MethodHandle = 15
CONSTANT_MethodType = 16
CONSTANT_InvokeDynamic = 18


@dataclass
class ConstantPoolEntry:
    """Entrada base del Constant Pool."""
    tag: int

    def to_bytes(self) -> bytes:
        """Convierte la entrada a bytes para el archivo .class."""
        raise NotImplementedError("Subclasses must implement to_bytes()")


@dataclass
class Utf8Constant(ConstantPoolEntry):
    """CONSTANT_Utf8: String en formato UTF-8."""
    text: str

    def __init__(self, text: str):
        super().__init__(CONSTANT_Utf8)
        self.text = text

    def to_bytes(self) -> bytes:
        """
        Formato:
        u1 tag = 1
        u2 length
        u1 bytes[length]
        """
        utf8_bytes = self.text.encode('utf-8')
        return struct.pack('>BH', self.tag, len(utf8_bytes)) + utf8_bytes

    def __eq__(self, other):
        return isinstance(other, Utf8Constant) and self.text == other.text

    def __hash__(self):
        return hash(('Utf8', self.text))


@dataclass
class IntegerConstant(ConstantPoolEntry):
    """CONSTANT_Integer: Entero de 4 bytes."""
    value: int

    def __init__(self, value: int):
        super().__init__(CONSTANT_Integer)
        self.value = value

    def to_bytes(self) -> bytes:
        """
        Formato:
        u1 tag = 3
        u4 bytes (big-endian)
        """
        return struct.pack('>Bi', self.tag, self.value)

    def __eq__(self, other):
        return isinstance(other, IntegerConstant) and self.value == other.value

    def __hash__(self):
        return hash(('Integer', self.value))


@dataclass
class FloatConstant(ConstantPoolEntry):
    """CONSTANT_Float: Float de 4 bytes."""
    value: float

    def __init__(self, value: float):
        super().__init__(CONSTANT_Float)
        self.value = value

    def to_bytes(self) -> bytes:
        """
        Formato:
        u1 tag = 4
        u4 bytes (big-endian, IEEE 754)
        """
        return struct.pack('>Bf', self.tag, self.value)

    def __eq__(self, other):
        return isinstance(other, FloatConstant) and self.value == other.value

    def __hash__(self):
        return hash(('Float', self.value))


@dataclass
class LongConstant(ConstantPoolEntry):
    """CONSTANT_Long: Long de 8 bytes (ocupa 2 slots!)."""
    value: int

    def __init__(self, value: int):
        super().__init__(CONSTANT_Long)
        self.value = value

    def to_bytes(self) -> bytes:
        """
        Formato:
        u1 tag = 5
        u8 bytes (big-endian)
        """
        return struct.pack('>Bq', self.tag, self.value)

    def __eq__(self, other):
        return isinstance(other, LongConstant) and self.value == other.value

    def __hash__(self):
        return hash(('Long', self.value))


@dataclass
class DoubleConstant(ConstantPoolEntry):
    """CONSTANT_Double: Double de 8 bytes (ocupa 2 slots!)."""
    value: float

    def __init__(self, value: float):
        super().__init__(CONSTANT_Double)
        self.value = value

    def to_bytes(self) -> bytes:
        """
        Formato:
        u1 tag = 6
        u8 bytes (big-endian, IEEE 754)
        """
        return struct.pack('>Bd', self.tag, self.value)

    def __eq__(self, other):
        return isinstance(other, DoubleConstant) and self.value == other.value

    def __hash__(self):
        return hash(('Double', self.value))


@dataclass
class ClassConstant(ConstantPoolEntry):
    """CONSTANT_Class: Referencia a una clase."""
    name_index: int

    def __init__(self, name_index: int):
        super().__init__(CONSTANT_Class)
        self.name_index = name_index

    def to_bytes(self) -> bytes:
        """
        Formato:
        u1 tag = 7
        u2 name_index (índice a CONSTANT_Utf8)
        """
        return struct.pack('>BH', self.tag, self.name_index)

    def __eq__(self, other):
        return isinstance(other, ClassConstant) and self.name_index == other.name_index

    def __hash__(self):
        return hash(('Class', self.name_index))


@dataclass
class StringConstant(ConstantPoolEntry):
    """CONSTANT_String: Referencia a un string."""
    string_index: int

    def __init__(self, string_index: int):
        super().__init__(CONSTANT_String)
        self.string_index = string_index

    def to_bytes(self) -> bytes:
        """
        Formato:
        u1 tag = 8
        u2 string_index (índice a CONSTANT_Utf8)
        """
        return struct.pack('>BH', self.tag, self.string_index)

    def __eq__(self, other):
        return isinstance(other, StringConstant) and self.string_index == other.string_index

    def __hash__(self):
        return hash(('String', self.string_index))


@dataclass
class FieldrefConstant(ConstantPoolEntry):
    """CONSTANT_Fieldref: Referencia a un field."""
    class_index: int
    name_and_type_index: int

    def __init__(self, class_index: int, name_and_type_index: int):
        super().__init__(CONSTANT_Fieldref)
        self.class_index = class_index
        self.name_and_type_index = name_and_type_index

    def to_bytes(self) -> bytes:
        """
        Formato:
        u1 tag = 9
        u2 class_index
        u2 name_and_type_index
        """
        return struct.pack('>BHH', self.tag, self.class_index, self.name_and_type_index)

    def __eq__(self, other):
        return (isinstance(other, FieldrefConstant) and
                self.class_index == other.class_index and
                self.name_and_type_index == other.name_and_type_index)

    def __hash__(self):
        return hash(('Fieldref', self.class_index, self.name_and_type_index))


@dataclass
class MethodrefConstant(ConstantPoolEntry):
    """CONSTANT_Methodref: Referencia a un método."""
    class_index: int
    name_and_type_index: int

    def __init__(self, class_index: int, name_and_type_index: int):
        super().__init__(CONSTANT_Methodref)
        self.class_index = class_index
        self.name_and_type_index = name_and_type_index

    def to_bytes(self) -> bytes:
        """
        Formato:
        u1 tag = 10
        u2 class_index
        u2 name_and_type_index
        """
        return struct.pack('>BHH', self.tag, self.class_index, self.name_and_type_index)

    def __eq__(self, other):
        return (isinstance(other, MethodrefConstant) and
                self.class_index == other.class_index and
                self.name_and_type_index == other.name_and_type_index)

    def __hash__(self):
        return hash(('Methodref', self.class_index, self.name_and_type_index))


@dataclass
class NameAndTypeConstant(ConstantPoolEntry):
    """CONSTANT_NameAndType: Nombre y descriptor de un field o método."""
    name_index: int
    descriptor_index: int

    def __init__(self, name_index: int, descriptor_index: int):
        super().__init__(CONSTANT_NameAndType)
        self.name_index = name_index
        self.descriptor_index = descriptor_index

    def to_bytes(self) -> bytes:
        """
        Formato:
        u1 tag = 12
        u2 name_index (índice a CONSTANT_Utf8)
        u2 descriptor_index (índice a CONSTANT_Utf8)
        """
        return struct.pack('>BHH', self.tag, self.name_index, self.descriptor_index)

    def __eq__(self, other):
        return (isinstance(other, NameAndTypeConstant) and
                self.name_index == other.name_index and
                self.descriptor_index == other.descriptor_index)

    def __hash__(self):
        return hash(('NameAndType', self.name_index, self.descriptor_index))


class ConstantPool:
    """
    Gestor del Constant Pool de JVM.

    IMPORTANTE: Los índices del Constant Pool empiezan en 1, NO en 0!
    Long y Double ocupan 2 slots (el siguiente slot queda en None).
    """

    def __init__(self):
        """Inicializa un Constant Pool vacío."""
        # La posición 0 NO se usa en JVM (índices empiezan en 1)
        self.entries: List[Optional[ConstantPoolEntry]] = []
        # Cache para evitar duplicados
        self.cache: Dict[ConstantPoolEntry, int] = {}

    def add_utf8(self, text: str) -> int:
        """
        Agrega un CONSTANT_Utf8 y retorna su índice (1-based).
        Si ya existe, retorna el índice existente.
        """
        entry = Utf8Constant(text)

        # Verificar si ya existe en cache
        if entry in self.cache:
            return self.cache[entry]

        # Agregar nuevo
        self.entries.append(entry)
        index = len(self.entries)  # 1-based
        self.cache[entry] = index
        return index

    def add_integer(self, value: int) -> int:
        """Agrega un CONSTANT_Integer y retorna su índice."""
        entry = IntegerConstant(value)

        if entry in self.cache:
            return self.cache[entry]

        self.entries.append(entry)
        index = len(self.entries)
        self.cache[entry] = index
        return index

    def add_float(self, value: float) -> int:
        """Agrega un CONSTANT_Float y retorna su índice."""
        entry = FloatConstant(value)

        if entry in self.cache:
            return self.cache[entry]

        self.entries.append(entry)
        index = len(self.entries)
        self.cache[entry] = index
        return index

    def add_long(self, value: int) -> int:
        """
        Agrega un CONSTANT_Long y retorna su índice.
        IMPORTANTE: Long ocupa 2 slots, el siguiente queda en None.
        """
        entry = LongConstant(value)

        if entry in self.cache:
            return self.cache[entry]

        self.entries.append(entry)
        index = len(self.entries)
        self.cache[entry] = index

        # Agregar slot vacío (Long ocupa 2 posiciones)
        self.entries.append(None)

        return index

    def add_double(self, value: float) -> int:
        """
        Agrega un CONSTANT_Double y retorna su índice.
        IMPORTANTE: Double ocupa 2 slots, el siguiente queda en None.
        """
        entry = DoubleConstant(value)

        if entry in self.cache:
            return self.cache[entry]

        self.entries.append(entry)
        index = len(self.entries)
        self.cache[entry] = index

        # Agregar slot vacío (Double ocupa 2 posiciones)
        self.entries.append(None)

        return index

    def add_class(self, class_name: str) -> int:
        """
        Agrega un CONSTANT_Class y retorna su índice.
        Automáticamente agrega el CONSTANT_Utf8 para el nombre.
        """
        name_index = self.add_utf8(class_name)
        entry = ClassConstant(name_index)

        if entry in self.cache:
            return self.cache[entry]

        self.entries.append(entry)
        index = len(self.entries)
        self.cache[entry] = index
        return index

    def add_string(self, text: str) -> int:
        """
        Agrega un CONSTANT_String y retorna su índice.
        Automáticamente agrega el CONSTANT_Utf8 para el texto.
        """
        string_index = self.add_utf8(text)
        entry = StringConstant(string_index)

        if entry in self.cache:
            return self.cache[entry]

        self.entries.append(entry)
        index = len(self.entries)
        self.cache[entry] = index
        return index

    def add_fieldref(self, class_name: str, field_name: str, descriptor: str) -> int:
        """
        Agrega un CONSTANT_Fieldref y retorna su índice.
        Automáticamente agrega todas las constantes necesarias.
        """
        class_index = self.add_class(class_name)
        name_index = self.add_utf8(field_name)
        descriptor_index = self.add_utf8(descriptor)
        name_and_type_index = self.add_name_and_type(name_index, descriptor_index)

        entry = FieldrefConstant(class_index, name_and_type_index)

        if entry in self.cache:
            return self.cache[entry]

        self.entries.append(entry)
        index = len(self.entries)
        self.cache[entry] = index
        return index

    def add_methodref(self, class_name: str, method_name: str, descriptor: str) -> int:
        """
        Agrega un CONSTANT_Methodref y retorna su índice.
        Automáticamente agrega todas las constantes necesarias.
        """
        class_index = self.add_class(class_name)
        name_index = self.add_utf8(method_name)
        descriptor_index = self.add_utf8(descriptor)
        name_and_type_index = self.add_name_and_type(name_index, descriptor_index)

        entry = MethodrefConstant(class_index, name_and_type_index)

        if entry in self.cache:
            return self.cache[entry]

        self.entries.append(entry)
        index = len(self.entries)
        self.cache[entry] = index
        return index

    def add_name_and_type(self, name_index: int, descriptor_index: int) -> int:
        """Agrega un CONSTANT_NameAndType y retorna su índice."""
        entry = NameAndTypeConstant(name_index, descriptor_index)

        if entry in self.cache:
            return self.cache[entry]

        self.entries.append(entry)
        index = len(self.entries)
        self.cache[entry] = index
        return index

    def get_count(self) -> int:
        """
        Retorna el count del constant pool.
        En JVM, constant_pool_count = número_de_entries + 1
        """
        return len(self.entries) + 1

    def to_bytes(self) -> bytes:
        """Convierte todo el Constant Pool a bytes para el archivo .class."""
        result = b''

        # Escribir constant_pool_count (u2)
        result += struct.pack('>H', self.get_count())

        # Escribir cada entrada
        for entry in self.entries:
            if entry is not None:
                result += entry.to_bytes()

        return result

    def __len__(self) -> int:
        """Retorna el número de entries (sin contar el slot 0 virtual)."""
        return len(self.entries)

    def __repr__(self) -> str:
        """Representación para debugging."""
        lines = [f"ConstantPool (count={self.get_count()}):"]
        for i, entry in enumerate(self.entries, start=1):
            if entry is None:
                lines.append(f"  #{i} = (slot vacío - Long/Double)")
            else:
                lines.append(f"  #{i} = {entry}")
        return '\n'.join(lines)
