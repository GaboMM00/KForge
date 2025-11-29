"""
Atributos Avanzados JVM - LineNumberTable y LocalVariableTable

Implementa atributos de debugging para archivos .class:
- LineNumberTable: Mapeo PC offset -> linea de codigo fuente
- LocalVariableTable: Informacion de variables locales (nombres, tipos, scope)

Estos atributos son opcionales pero esenciales para debugging.

Referencias:
- JVM Spec 4.7.12: LineNumberTable
- JVM Spec 4.7.13: LocalVariableTable
"""

import struct
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class LineNumberEntry:
    """
    Entrada en LineNumberTable.

    Representa mapeo: PC offset -> linea de codigo

    Attributes:
        start_pc: Offset en bytecode donde comienza la linea
        line_number: Numero de linea en archivo fuente
    """
    start_pc: int
    line_number: int

    def to_bytes(self) -> bytes:
        """Convierte la entrada a bytes."""
        return struct.pack('>HH', self.start_pc, self.line_number)


class LineNumberTableAttribute:
    """
    LineNumberTable Attribute - Mapeo PC offset a lineas de codigo.

    Estructura:
        LineNumberTable_attribute {
            u2 attribute_name_index;
            u4 attribute_length;
            u2 line_number_table_length;
            {   u2 start_pc;
                u2 line_number;
            } line_number_table[line_number_table_length];
        }

    Este atributo es un sub-atributo del Code attribute.
    """

    def __init__(self, name_index: int):
        """
        Inicializa LineNumberTable.

        Args:
            name_index: Index en constant pool de "LineNumberTable"
        """
        self.name_index = name_index
        self.entries: List[LineNumberEntry] = []

    def add_entry(self, start_pc: int, line_number: int):
        """
        Agrega una entrada de mapeo.

        Args:
            start_pc: Offset en bytecode
            line_number: Numero de linea en fuente
        """
        self.entries.append(LineNumberEntry(start_pc, line_number))

    def to_bytes(self) -> bytes:
        """Convierte el atributo a bytes."""
        # Info del atributo
        info = struct.pack('>H', len(self.entries))  # line_number_table_length

        for entry in self.entries:
            info += entry.to_bytes()

        # Atributo completo
        return struct.pack('>HI',
            self.name_index,
            len(info)
        ) + info


@dataclass
class LocalVariableEntry:
    """
    Entrada en LocalVariableTable.

    Representa informacion de una variable local.

    Attributes:
        start_pc: PC donde la variable entra en scope
        length: Longitud del scope en bytes
        name_index: Index en constant pool del nombre de variable
        descriptor_index: Index en constant pool del descriptor de tipo
        index: Slot de variable local
    """
    start_pc: int
    length: int
    name_index: int
    descriptor_index: int
    index: int

    def to_bytes(self) -> bytes:
        """Convierte la entrada a bytes."""
        return struct.pack('>HHHHH',
            self.start_pc,
            self.length,
            self.name_index,
            self.descriptor_index,
            self.index
        )


class LocalVariableTableAttribute:
    """
    LocalVariableTable Attribute - Informacion de variables locales.

    Estructura:
        LocalVariableTable_attribute {
            u2 attribute_name_index;
            u4 attribute_length;
            u2 local_variable_table_length;
            {   u2 start_pc;
                u2 length;
                u2 name_index;
                u2 descriptor_index;
                u2 index;
            } local_variable_table[local_variable_table_length];
        }

    Este atributo es un sub-atributo del Code attribute.
    Permite a debuggers mostrar nombres de variables.
    """

    def __init__(self, name_index: int):
        """
        Inicializa LocalVariableTable.

        Args:
            name_index: Index en constant pool de "LocalVariableTable"
        """
        self.name_index = name_index
        self.entries: List[LocalVariableEntry] = []

    def add_entry(self, start_pc: int, length: int, name_index: int,
                  descriptor_index: int, index: int):
        """
        Agrega una entrada de variable local.

        Args:
            start_pc: PC donde variable entra en scope
            length: Longitud del scope
            name_index: Index del nombre en constant pool
            descriptor_index: Index del descriptor en constant pool
            index: Slot de variable local
        """
        self.entries.append(LocalVariableEntry(
            start_pc, length, name_index, descriptor_index, index
        ))

    def to_bytes(self) -> bytes:
        """Convierte el atributo a bytes."""
        # Info del atributo
        info = struct.pack('>H', len(self.entries))  # local_variable_table_length

        for entry in self.entries:
            info += entry.to_bytes()

        # Atributo completo
        return struct.pack('>HI',
            self.name_index,
            len(info)
        ) + info


class StackMapTableAttribute:
    """
    StackMapTable Attribute - Stack Map Frames para Java 7+.

    NOTA: No implementado en Fase 9 - KForge usa Java 6 bytecode.
    Esta clase es un placeholder para futura implementacion.

    Estructura (simplificada):
        StackMapTable_attribute {
            u2 attribute_name_index;
            u4 attribute_length;
            u2 number_of_entries;
            stack_map_frame entries[number_of_entries];
        }

    Referencias:
    - JVM Spec 4.7.4: StackMapTable
    - docs/PHASE9_JAVA6_APPROACH.md para upgrade path
    """

    def __init__(self, name_index: int):
        """
        Inicializa StackMapTable (placeholder).

        Args:
            name_index: Index en constant pool de "StackMapTable"
        """
        self.name_index = name_index
        # TODO: Implementar en upgrade a Java 7+
        raise NotImplementedError(
            "StackMapTable no implementado. "
            "KForge usa Java 6 bytecode (sin Stack Map Frames). "
            "Ver docs/PHASE9_JAVA6_APPROACH.md para mas informacion."
        )


def create_line_number_table(constant_pool, pc_to_line: List[Tuple[int, int]]) -> LineNumberTableAttribute:
    """
    Crea LineNumberTable attribute.

    Args:
        constant_pool: Constant pool donde agregar "LineNumberTable"
        pc_to_line: Lista de tuplas (pc_offset, line_number)

    Returns:
        LineNumberTableAttribute configurado

    Example:
        >>> cp = ConstantPool()
        >>> lnt = create_line_number_table(cp, [(0, 1), (5, 2), (10, 3)])
        >>> lnt.to_bytes()
    """
    name_index = constant_pool.add_utf8("LineNumberTable")
    attr = LineNumberTableAttribute(name_index)

    for pc, line in pc_to_line:
        attr.add_entry(pc, line)

    return attr


def create_local_variable_table(constant_pool, variables: List[Tuple[int, int, str, str, int]]) -> LocalVariableTableAttribute:
    """
    Crea LocalVariableTable attribute.

    Args:
        constant_pool: Constant pool donde agregar entries
        variables: Lista de tuplas (start_pc, length, name, descriptor, index)

    Returns:
        LocalVariableTableAttribute configurado

    Example:
        >>> cp = ConstantPool()
        >>> lvt = create_local_variable_table(cp, [
        ...     (0, 10, "x", "I", 0),
        ...     (5, 5, "y", "D", 1)
        ... ])
        >>> lvt.to_bytes()
    """
    name_index = constant_pool.add_utf8("LocalVariableTable")
    attr = LocalVariableTableAttribute(name_index)

    for start_pc, length, var_name, descriptor, index in variables:
        var_name_index = constant_pool.add_utf8(var_name)
        descriptor_index = constant_pool.add_utf8(descriptor)
        attr.add_entry(start_pc, length, var_name_index, descriptor_index, index)

    return attr
