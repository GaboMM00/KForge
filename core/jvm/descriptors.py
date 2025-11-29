"""
Generador de descriptores de tipos para JVM.

Los descriptores de tipos en JVM son strings que describen tipos de datos,
parámetros de métodos y valores de retorno.

Especificación: https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html#jvms-4.3
"""

from typing import List
from core.utils import TipoDato


class TypeDescriptor:
    """Generador de descriptores de tipos JVM."""

    # Mapeo de tipos de Kotlin a descriptores JVM
    TYPE_MAP = {
        TipoDato.INT: 'I',
        TipoDato.DOUBLE: 'D',
        TipoDato.STRING: 'Ljava/lang/String;',
        TipoDato.BOOLEAN: 'Z',
        TipoDato.VOID: 'V',  # void en JVM (Unit en Kotlin)
        # Arrays
        'IntArray': '[I',
        'DoubleArray': '[D',
    }

    @staticmethod
    def get_type_descriptor(tipo: TipoDato) -> str:
        """
        Obtiene el descriptor JVM para un tipo de Kotlin.

        Args:
            tipo: Tipo de dato de Kotlin

        Returns:
            Descriptor JVM (ej: 'I' para Int, 'Ljava/lang/String;' para String)

        Examples:
            Int → 'I'
            Double → 'D'
            String → 'Ljava/lang/String;'
            Boolean → 'Z'
            Unit → 'V'
        """
        if tipo in TypeDescriptor.TYPE_MAP:
            return TypeDescriptor.TYPE_MAP[tipo]
        else:
            raise ValueError(f"Tipo no soportado: {tipo}")

    @staticmethod
    def get_array_descriptor(element_type: TipoDato) -> str:
        """
        Obtiene el descriptor JVM para un array.

        Args:
            element_type: Tipo de los elementos del array

        Returns:
            Descriptor de array JVM (ej: '[I' para IntArray)

        Examples:
            Int → '[I'
            Double → '[D'
        """
        element_descriptor = TypeDescriptor.get_type_descriptor(element_type)
        return f'[{element_descriptor}'

    @staticmethod
    def get_method_descriptor(param_types: List[TipoDato], return_type: TipoDato) -> str:
        """
        Genera un descriptor de método JVM.

        Formato: (param1param2...paramN)returnType

        Args:
            param_types: Lista de tipos de los parámetros
            return_type: Tipo de retorno

        Returns:
            Descriptor de método (ej: '(II)I' para suma(Int, Int): Int)

        Examples:
            suma(a: Int, b: Int): Int → '(II)I'
            println(s: String): Unit → '(Ljava/lang/String;)V'
            main(): Unit → '()V'
            concat(a: String, b: String): String → '(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;'
        """
        # Construir parte de parámetros
        params = ''.join(TypeDescriptor.get_type_descriptor(t) for t in param_types)

        # Obtener descriptor de retorno
        ret = TypeDescriptor.get_type_descriptor(return_type)

        return f'({params}){ret}'

    @staticmethod
    def get_field_descriptor(field_type: TipoDato) -> str:
        """
        Genera un descriptor de field JVM.

        Args:
            field_type: Tipo del field

        Returns:
            Descriptor de field

        Examples:
            Int → 'I'
            String → 'Ljava/lang/String;'
            IntArray → '[I'
        """
        return TypeDescriptor.get_type_descriptor(field_type)

    @staticmethod
    def parse_class_name(kotlin_name: str) -> str:
        """
        Convierte un nombre de clase de Kotlin a formato JVM.

        Args:
            kotlin_name: Nombre en formato Kotlin (ej: 'java.lang.String')

        Returns:
            Nombre en formato JVM (ej: 'java/lang/String')

        Examples:
            'MyClass' → 'MyClass'
            'java.lang.String' → 'java/lang/String'
            'com.example.MyClass' → 'com/example/MyClass'
        """
        return kotlin_name.replace('.', '/')

    @staticmethod
    def get_class_descriptor(class_name: str) -> str:
        """
        Genera un descriptor de clase JVM.

        Args:
            class_name: Nombre de la clase

        Returns:
            Descriptor de clase (ej: 'Ljava/lang/String;')

        Examples:
            'String' → 'Ljava/lang/String;'
            'Object' → 'Ljava/lang/Object;'
            'MyClass' → 'LMyClass;'
        """
        jvm_name = TypeDescriptor.parse_class_name(class_name)
        return f'L{jvm_name};'


class MethodSignature:
    """
    Representa una signatura de método completa con información adicional.
    """

    def __init__(self, name: str, param_types: List[TipoDato], return_type: TipoDato):
        """
        Crea una signatura de método.

        Args:
            name: Nombre del método
            param_types: Tipos de parámetros
            return_type: Tipo de retorno
        """
        self.name = name
        self.param_types = param_types
        self.return_type = return_type
        self.descriptor = TypeDescriptor.get_method_descriptor(param_types, return_type)

    def __str__(self) -> str:
        """Representación como string."""
        return f"{self.name}{self.descriptor}"

    def __repr__(self) -> str:
        """Representación para debugging."""
        params = ', '.join(str(t) for t in self.param_types)
        return f"MethodSignature(name='{self.name}', params=[{params}], return={self.return_type})"


# Descriptores de métodos comunes de JVM

# System.out.println
PRINTLN_INT_DESCRIPTOR = '(I)V'
PRINTLN_DOUBLE_DESCRIPTOR = '(D)V'
PRINTLN_STRING_DESCRIPTOR = '(Ljava/lang/String;)V'
PRINTLN_BOOLEAN_DESCRIPTOR = '(Z)V'

# System.out.print
PRINT_INT_DESCRIPTOR = '(I)V'
PRINT_DOUBLE_DESCRIPTOR = '(D)V'
PRINT_STRING_DESCRIPTOR = '(Ljava/lang/String;)V'

# main method
MAIN_METHOD_DESCRIPTOR = '([Ljava/lang/String;)V'

# Object methods
OBJECT_INIT_DESCRIPTOR = '()V'  # Constructor <init>
OBJECT_TOSTRING_DESCRIPTOR = '()Ljava/lang/String;'

# Array methods
ARRAY_LENGTH_DESCRIPTOR = 'I'  # Field descriptor para array.length


def get_println_descriptor(tipo: TipoDato) -> str:
    """
    Obtiene el descriptor correcto para println según el tipo.

    Args:
        tipo: Tipo del argumento

    Returns:
        Descriptor de println para ese tipo
    """
    if tipo == TipoDato.INT:
        return PRINTLN_INT_DESCRIPTOR
    elif tipo == TipoDato.DOUBLE:
        return PRINTLN_DOUBLE_DESCRIPTOR
    elif tipo == TipoDato.STRING:
        return PRINTLN_STRING_DESCRIPTOR
    elif tipo == TipoDato.BOOLEAN:
        return PRINTLN_BOOLEAN_DESCRIPTOR
    else:
        # Por defecto, convertir a String primero
        return PRINTLN_STRING_DESCRIPTOR


def get_print_descriptor(tipo: TipoDato) -> str:
    """
    Obtiene el descriptor correcto para print según el tipo.

    Args:
        tipo: Tipo del argumento

    Returns:
        Descriptor de print para ese tipo
    """
    if tipo == TipoDato.INT:
        return PRINT_INT_DESCRIPTOR
    elif tipo == TipoDato.DOUBLE:
        return PRINT_DOUBLE_DESCRIPTOR
    elif tipo == TipoDato.STRING:
        return PRINT_STRING_DESCRIPTOR
    else:
        return PRINT_STRING_DESCRIPTOR


# Nombres de clases JVM comunes
CLASS_OBJECT = 'java/lang/Object'
CLASS_STRING = 'java/lang/String'
CLASS_SYSTEM = 'java/lang/System'
CLASS_PRINTSTREAM = 'java/io/PrintStream'


if __name__ == '__main__':
    # Ejemplos de uso
    print("=== Ejemplos de Descriptores JVM ===\n")

    # Tipos básicos
    print("Tipos Básicos:")
    print(f"  Int → {TypeDescriptor.get_type_descriptor(TipoDato.INT)}")
    print(f"  Double → {TypeDescriptor.get_type_descriptor(TipoDato.DOUBLE)}")
    print(f"  String → {TypeDescriptor.get_type_descriptor(TipoDato.STRING)}")
    print(f"  Boolean → {TypeDescriptor.get_type_descriptor(TipoDato.BOOLEAN)}")
    print(f"  Unit → {TypeDescriptor.get_type_descriptor(TipoDato.UNIT)}")

    # Arrays
    print("\nArrays:")
    print(f"  IntArray → {TypeDescriptor.get_array_descriptor(TipoDato.INT)}")
    print(f"  DoubleArray → {TypeDescriptor.get_array_descriptor(TipoDato.DOUBLE)}")

    # Métodos
    print("\nMétodos:")
    sig1 = MethodSignature('suma', [TipoDato.INT, TipoDato.INT], TipoDato.INT)
    print(f"  fun suma(a: Int, b: Int): Int → {sig1}")

    sig2 = MethodSignature('println', [TipoDato.STRING], TipoDato.UNIT)
    print(f"  fun println(s: String): Unit → {sig2}")

    sig3 = MethodSignature('main', [], TipoDato.UNIT)
    print(f"  fun main(): Unit → {sig3}")

    # Descriptores comunes
    print("\nDescriptores Comunes:")
    print(f"  main(String[]): void → {MAIN_METHOD_DESCRIPTOR}")
    print(f"  println(int): void → {PRINTLN_INT_DESCRIPTOR}")
    print(f"  println(String): void → {PRINTLN_STRING_DESCRIPTOR}")
