"""
Runtime Support - Soporte runtime para funciones built-in

Implementa:
- println() para Int, Double, String, Boolean
- print() variantes
- Creacion de arrays (intArrayOf, doubleArrayOf)
- Metodo main() correcto
- Helpers para invocar metodos de System.out y otras clases Java

Referencias:
- System.out.println: java/io/PrintStream
- Arrays: newarray, anewarray
"""

from typing import List, Tuple
from core.jvm.constant_pool import ConstantPool
from core.jvm.instructions import JVMInstruction, JVMOpcode, ArrayType
from core.jvm.descriptors import TypeDescriptor
from core.utils import TipoDato


class RuntimeHelper:
    """
    Helper para generar codigo runtime (println, arrays, etc).

    Gestiona:
    - Referencias a System.out
    - Llamadas a println/print
    - Creacion de arrays
    - Inicializacion de arrays
    """

    def __init__(self, constant_pool: ConstantPool):
        """
        Inicializa RuntimeHelper.

        Args:
            constant_pool: Constant pool donde agregar referencias
        """
        self.constant_pool = constant_pool
        self._system_out_ref = None
        self._println_refs = {}  # {tipo: methodref_index}
        self._print_refs = {}    # {tipo: methodref_index}

    def get_system_out_fieldref(self) -> int:
        """
        Obtiene o crea la referencia a System.out.

        Returns:
            Index en constant pool de System.out (Fieldref)
        """
        if self._system_out_ref is None:
            # System.out es un field estatico de tipo PrintStream
            # Fieldref: System.out:Ljava/io/PrintStream;
            self._system_out_ref = self.constant_pool.add_fieldref(
                "java/lang/System",
                "out",
                "Ljava/io/PrintStream;"
            )
        return self._system_out_ref

    def get_println_methodref(self, tipo: TipoDato) -> int:
        """
        Obtiene o crea la referencia a println() para un tipo especifico.

        Args:
            tipo: Tipo de dato (INT, DOUBLE, STRING, BOOLEAN)

        Returns:
            Index en constant pool del methodref
        """
        if tipo not in self._println_refs:
            # Determinar descriptor segun tipo
            if tipo == TipoDato.INT:
                descriptor = "(I)V"
            elif tipo == TipoDato.DOUBLE:
                descriptor = "(D)V"
            elif tipo == TipoDato.STRING:
                descriptor = "(Ljava/lang/String;)V"
            elif tipo == TipoDato.BOOLEAN:
                descriptor = "(Z)V"
            else:
                descriptor = "(Ljava/lang/Object;)V"

            # Methodref: PrintStream.println(tipo)V
            self._println_refs[tipo] = self.constant_pool.add_methodref(
                "java/io/PrintStream",
                "println",
                descriptor
            )

        return self._println_refs[tipo]

    def get_print_methodref(self, tipo: TipoDato) -> int:
        """
        Obtiene o crea la referencia a print() para un tipo especifico.

        Args:
            tipo: Tipo de dato (INT, DOUBLE, STRING, BOOLEAN)

        Returns:
            Index en constant pool del methodref
        """
        if tipo not in self._print_refs:
            # Determinar descriptor segun tipo
            if tipo == TipoDato.INT:
                descriptor = "(I)V"
            elif tipo == TipoDato.DOUBLE:
                descriptor = "(D)V"
            elif tipo == TipoDato.STRING:
                descriptor = "(Ljava/lang/String;)V"
            elif tipo == TipoDato.BOOLEAN:
                descriptor = "(Z)V"
            else:
                descriptor = "(Ljava/lang/Object;)V"

            # Methodref: PrintStream.print(tipo)V
            self._print_refs[tipo] = self.constant_pool.add_methodref(
                "java/io/PrintStream",
                "print",
                descriptor
            )

        return self._print_refs[tipo]

    def generate_println(self, tipo: TipoDato) -> List[JVMInstruction]:
        """
        Genera instrucciones para println(value).

        Asume que el valor ya esta en el stack.

        Args:
            tipo: Tipo del valor a imprimir

        Returns:
            Lista de instrucciones JVM
        """
        instructions = []

        # Cargar System.out
        system_out_ref = self.get_system_out_fieldref()
        instructions.append(JVMInstruction(JVMOpcode.GETSTATIC, [
            (system_out_ref >> 8) & 0xFF,
            system_out_ref & 0xFF
        ]))

        # Swap para poner valor despues de System.out
        # Stack antes: [value]
        # Despues de GETSTATIC: [value, System.out]
        # Despues de SWAP: [System.out, value]
        instructions.append(JVMInstruction(JVMOpcode.SWAP))

        # Invocar println
        println_ref = self.get_println_methodref(tipo)
        instructions.append(JVMInstruction(JVMOpcode.INVOKEVIRTUAL, [
            (println_ref >> 8) & 0xFF,
            println_ref & 0xFF
        ]))

        return instructions

    def generate_print(self, tipo: TipoDato) -> List[JVMInstruction]:
        """
        Genera instrucciones para print(value) sin newline.

        Asume que el valor ya esta en el stack.

        Args:
            tipo: Tipo del valor a imprimir

        Returns:
            Lista de instrucciones JVM
        """
        instructions = []

        # Cargar System.out
        system_out_ref = self.get_system_out_fieldref()
        instructions.append(JVMInstruction(JVMOpcode.GETSTATIC, [
            (system_out_ref >> 8) & 0xFF,
            system_out_ref & 0xFF
        ]))

        # Swap
        instructions.append(JVMInstruction(JVMOpcode.SWAP))

        # Invocar print
        print_ref = self.get_print_methodref(tipo)
        instructions.append(JVMInstruction(JVMOpcode.INVOKEVIRTUAL, [
            (print_ref >> 8) & 0xFF,
            print_ref & 0xFF
        ]))

        return instructions


def generate_newarray_int(size: int) -> List[JVMInstruction]:
    """
    Genera instrucciones para crear array de enteros.

    Args:
        size: Tamaño del array

    Returns:
        Lista de instrucciones JVM que dejan el array en el stack
    """
    from core.jvm.instructions import iconst

    instructions = []

    # Push size al stack
    instructions.append(iconst(size))

    # Crear array
    instructions.append(JVMInstruction(JVMOpcode.NEWARRAY, [ArrayType.T_INT.value]))

    return instructions


def generate_newarray_double(size: int) -> List[JVMInstruction]:
    """
    Genera instrucciones para crear array de doubles.

    Args:
        size: Tamaño del array

    Returns:
        Lista de instrucciones JVM que dejan el array en el stack
    """
    from core.jvm.instructions import iconst

    instructions = []

    # Push size al stack
    instructions.append(iconst(size))

    # Crear array
    instructions.append(JVMInstruction(JVMOpcode.NEWARRAY, [ArrayType.T_DOUBLE.value]))

    return instructions


def generate_anewarray(class_name: str, size: int, constant_pool: ConstantPool) -> List[JVMInstruction]:
    """
    Genera instrucciones para crear array de objetos.

    Args:
        class_name: Nombre de la clase (ej: "java/lang/String")
        size: Tamaño del array
        constant_pool: Constant pool donde agregar class ref

    Returns:
        Lista de instrucciones JVM que dejan el array en el stack
    """
    from core.jvm.instructions import iconst

    instructions = []

    # Push size al stack
    instructions.append(iconst(size))

    # Obtener class index
    class_idx = constant_pool.add_class(class_name)

    # Crear array de referencias
    instructions.append(JVMInstruction(JVMOpcode.ANEWARRAY, [
        (class_idx >> 8) & 0xFF,
        class_idx & 0xFF
    ]))

    return instructions


def generate_array_store_int(index: int) -> List[JVMInstruction]:
    """
    Genera instrucciones para arr[index] = value (int).

    Asume stack: [arrayref, value]

    Args:
        index: Indice donde almacenar

    Returns:
        Lista de instrucciones JVM
    """
    from core.jvm.instructions import iconst

    instructions = []

    # Stack: [arrayref, value]
    # Push index
    instructions.append(iconst(index))
    # Stack: [arrayref, value, index]

    # Swap para poner en orden: arrayref, index, value
    instructions.append(JVMInstruction(JVMOpcode.DUP_X1))
    # Stack: [arrayref, index, value, index]
    instructions.append(JVMInstruction(JVMOpcode.POP))
    # Stack: [arrayref, index, value]

    # Almacenar
    instructions.append(JVMInstruction(JVMOpcode.IASTORE))

    return instructions


def create_main_method(constant_pool: ConstantPool, code_bytes: bytes,
                       max_stack: int, max_locals: int):
    """
    Crea el metodo main correcto para JVM.

    Signature: public static void main(String[] args)

    Args:
        constant_pool: Constant pool
        code_bytes: Bytecode del metodo
        max_stack: Stack maximo
        max_locals: Variables locales maximas (minimo 1 para args)

    Returns:
        MethodInfo configurado
    """
    from core.jvm.classfile import MethodInfo, CodeAttribute, AccessFlags

    # Asegurar max_locals minimo de 1 (para args[])
    max_locals = max(max_locals, 1)

    # Crear indices en constant pool
    name_idx = constant_pool.add_utf8("main")
    descriptor_idx = constant_pool.add_utf8("([Ljava/lang/String;)V")

    # Crear metodo
    method = MethodInfo(
        AccessFlags.ACC_PUBLIC | AccessFlags.ACC_STATIC,
        name_idx,
        descriptor_idx
    )

    # Agregar Code attribute
    code_name_idx = constant_pool.add_utf8("Code")
    code_attr = CodeAttribute(
        code_name_idx,
        max_stack=max_stack,
        max_locals=max_locals,
        code=code_bytes
    )

    method.add_attribute(code_attr)

    return method


def generate_string_constant(value: str, constant_pool: ConstantPool) -> List[JVMInstruction]:
    """
    Genera instrucciones para cargar una constante String.

    Args:
        value: Valor del string
        constant_pool: Constant pool

    Returns:
        Lista de instrucciones JVM que dejan el String en el stack
    """
    instructions = []

    # Agregar string al constant pool
    string_idx = constant_pool.add_string(value)

    # Cargar con ldc o ldc_w segun indice
    if string_idx < 256:
        instructions.append(JVMInstruction(JVMOpcode.LDC, [string_idx]))
    else:
        instructions.append(JVMInstruction(JVMOpcode.LDC_W, [
            (string_idx >> 8) & 0xFF,
            string_idx & 0xFF
        ]))

    return instructions
