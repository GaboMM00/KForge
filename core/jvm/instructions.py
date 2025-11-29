"""
JVM Instructions - Conjunto de instrucciones de bytecode JVM

Implementa las instrucciones JVM necesarias para generar bytecode ejecutable.
Cada instruccion tiene su opcode correspondiente segun la JVM Specification.

Referencias:
- https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-6.html
- https://en.wikipedia.org/wiki/Java_bytecode_instruction_listings
"""

from enum import Enum
from typing import Optional, List
import struct


class JVMOpcode(Enum):
    """
    Opcodes de instrucciones JVM.

    Organizados por categoria segun JVM Spec Chapter 6.
    """

    # === CONSTANTS (0x00-0x14) ===
    NOP = 0x00          # Do nothing

    ACONST_NULL = 0x01  # Push null

    ICONST_M1 = 0x02    # Push int constant -1
    ICONST_0 = 0x03     # Push int constant 0
    ICONST_1 = 0x04     # Push int constant 1
    ICONST_2 = 0x05     # Push int constant 2
    ICONST_3 = 0x06     # Push int constant 3
    ICONST_4 = 0x07     # Push int constant 4
    ICONST_5 = 0x08     # Push int constant 5

    LCONST_0 = 0x09     # Push long constant 0
    LCONST_1 = 0x0A     # Push long constant 1

    FCONST_0 = 0x0B     # Push float constant 0.0
    FCONST_1 = 0x0C     # Push float constant 1.0
    FCONST_2 = 0x0D     # Push float constant 2.0

    DCONST_0 = 0x0E     # Push double constant 0.0
    DCONST_1 = 0x0F     # Push double constant 1.0

    BIPUSH = 0x10       # Push byte as int (1 operand: byte)
    SIPUSH = 0x11       # Push short as int (2 operands: short)

    LDC = 0x12          # Push item from constant pool (1 operand: index)
    LDC_W = 0x13        # Push item from constant pool (wide index)
    LDC2_W = 0x14       # Push long or double from constant pool

    # === LOADS (0x15-0x35) ===
    ILOAD = 0x15        # Load int from local variable (1 operand: index)
    LLOAD = 0x16        # Load long from local variable
    FLOAD = 0x17        # Load float from local variable
    DLOAD = 0x18        # Load double from local variable
    ALOAD = 0x19        # Load reference from local variable

    ILOAD_0 = 0x1A      # Load int from local variable 0
    ILOAD_1 = 0x1B      # Load int from local variable 1
    ILOAD_2 = 0x1C      # Load int from local variable 2
    ILOAD_3 = 0x1D      # Load int from local variable 3

    LLOAD_0 = 0x1E      # Load long from local variable 0
    LLOAD_1 = 0x1F      # Load long from local variable 1
    LLOAD_2 = 0x20      # Load long from local variable 2
    LLOAD_3 = 0x21      # Load long from local variable 3

    FLOAD_0 = 0x22      # Load float from local variable 0
    FLOAD_1 = 0x23      # Load float from local variable 1
    FLOAD_2 = 0x24      # Load float from local variable 2
    FLOAD_3 = 0x25      # Load float from local variable 3

    DLOAD_0 = 0x26      # Load double from local variable 0
    DLOAD_1 = 0x27      # Load double from local variable 1
    DLOAD_2 = 0x28      # Load double from local variable 2
    DLOAD_3 = 0x29      # Load double from local variable 3

    ALOAD_0 = 0x2A      # Load reference from local variable 0
    ALOAD_1 = 0x2B      # Load reference from local variable 1
    ALOAD_2 = 0x2C      # Load reference from local variable 2
    ALOAD_3 = 0x2D      # Load reference from local variable 3

    IALOAD = 0x2E       # Load int from array
    LALOAD = 0x2F       # Load long from array
    FALOAD = 0x30       # Load float from array
    DALOAD = 0x31       # Load double from array
    AALOAD = 0x32       # Load reference from array
    BALOAD = 0x33       # Load byte from array
    CALOAD = 0x34       # Load char from array
    SALOAD = 0x35       # Load short from array

    # === STORES (0x36-0x56) ===
    ISTORE = 0x36       # Store int into local variable (1 operand: index)
    LSTORE = 0x37       # Store long into local variable
    FSTORE = 0x38       # Store float into local variable
    DSTORE = 0x39       # Store double into local variable
    ASTORE = 0x3A       # Store reference into local variable

    ISTORE_0 = 0x3B     # Store int into local variable 0
    ISTORE_1 = 0x3C     # Store int into local variable 1
    ISTORE_2 = 0x3D     # Store int into local variable 2
    ISTORE_3 = 0x3E     # Store int into local variable 3

    LSTORE_0 = 0x3F     # Store long into local variable 0
    LSTORE_1 = 0x40     # Store long into local variable 1
    LSTORE_2 = 0x41     # Store long into local variable 2
    LSTORE_3 = 0x42     # Store long into local variable 3

    FSTORE_0 = 0x43     # Store float into local variable 0
    FSTORE_1 = 0x44     # Store float into local variable 1
    FSTORE_2 = 0x45     # Store float into local variable 2
    FSTORE_3 = 0x46     # Store float into local variable 3

    DSTORE_0 = 0x47     # Store double into local variable 0
    DSTORE_1 = 0x48     # Store double into local variable 1
    DSTORE_2 = 0x49     # Store double into local variable 2
    DSTORE_3 = 0x4A     # Store double into local variable 3

    ASTORE_0 = 0x4B     # Store reference into local variable 0
    ASTORE_1 = 0x4C     # Store reference into local variable 1
    ASTORE_2 = 0x4D     # Store reference into local variable 2
    ASTORE_3 = 0x4E     # Store reference into local variable 3

    IASTORE = 0x4F      # Store int into array
    LASTORE = 0x50      # Store long into array
    FASTORE = 0x51      # Store float into array
    DASTORE = 0x52      # Store double into array
    AASTORE = 0x53      # Store reference into array
    BASTORE = 0x54      # Store byte into array
    CASTORE = 0x55      # Store char into array
    SASTORE = 0x56      # Store short into array

    # === STACK MANIPULATION (0x57-0x5F) ===
    POP = 0x57          # Pop top stack value
    POP2 = 0x58         # Pop top two stack values
    DUP = 0x59          # Duplicate top stack value
    DUP_X1 = 0x5A       # Duplicate top value and insert below second
    DUP_X2 = 0x5B       # Duplicate top value and insert below third
    DUP2 = 0x5C         # Duplicate top two values
    DUP2_X1 = 0x5D      # Duplicate top two and insert below third
    DUP2_X2 = 0x5E      # Duplicate top two and insert below fourth
    SWAP = 0x5F         # Swap top two stack values

    # === ARITHMETIC (0x60-0x84) ===
    IADD = 0x60         # Add int
    LADD = 0x61         # Add long
    FADD = 0x62         # Add float
    DADD = 0x63         # Add double

    ISUB = 0x64         # Subtract int
    LSUB = 0x65         # Subtract long
    FSUB = 0x66         # Subtract float
    DSUB = 0x67         # Subtract double

    IMUL = 0x68         # Multiply int
    LMUL = 0x69         # Multiply long
    FMUL = 0x6A         # Multiply float
    DMUL = 0x6B         # Multiply double

    IDIV = 0x6C         # Divide int
    LDIV = 0x6D         # Divide long
    FDIV = 0x6E         # Divide float
    DDIV = 0x6F         # Divide double

    IREM = 0x70         # Remainder int (modulo)
    LREM = 0x71         # Remainder long
    FREM = 0x72         # Remainder float
    DREM = 0x73         # Remainder double

    INEG = 0x74         # Negate int
    LNEG = 0x75         # Negate long
    FNEG = 0x76         # Negate float
    DNEG = 0x77         # Negate double

    ISHL = 0x78         # Shift left int
    LSHL = 0x79         # Shift left long
    ISHR = 0x7A         # Arithmetic shift right int
    LSHR = 0x7B         # Arithmetic shift right long
    IUSHR = 0x7C        # Logical shift right int
    LUSHR = 0x7D        # Logical shift right long

    IAND = 0x7E         # Boolean AND int
    LAND = 0x7F         # Boolean AND long
    IOR = 0x80          # Boolean OR int
    LOR = 0x81          # Boolean OR long
    IXOR = 0x82         # Boolean XOR int
    LXOR = 0x83         # Boolean XOR long

    IINC = 0x84         # Increment local variable (2 operands: index, const)

    # === CONVERSIONS (0x85-0x93) ===
    I2L = 0x85          # Int to long
    I2F = 0x86          # Int to float
    I2D = 0x87          # Int to double
    L2I = 0x88          # Long to int
    L2F = 0x89          # Long to float
    L2D = 0x8A          # Long to double
    F2I = 0x8B          # Float to int
    F2L = 0x8C          # Float to long
    F2D = 0x8D          # Float to double
    D2I = 0x8E          # Double to int
    D2L = 0x8F          # Double to long
    D2F = 0x90          # Double to float
    I2B = 0x91          # Int to byte
    I2C = 0x92          # Int to char
    I2S = 0x93          # Int to short

    # === COMPARISONS (0x94-0xA6) ===
    LCMP = 0x94         # Compare long
    FCMPL = 0x95        # Compare float (less on NaN)
    FCMPG = 0x96        # Compare float (greater on NaN)
    DCMPL = 0x97        # Compare double (less on NaN)
    DCMPG = 0x98        # Compare double (greater on NaN)

    IFEQ = 0x99         # Branch if int == 0 (2 operands: offset)
    IFNE = 0x9A         # Branch if int != 0
    IFLT = 0x9B         # Branch if int < 0
    IFGE = 0x9C         # Branch if int >= 0
    IFGT = 0x9D         # Branch if int > 0
    IFLE = 0x9E         # Branch if int <= 0

    IF_ICMPEQ = 0x9F    # Branch if int comparison ==
    IF_ICMPNE = 0xA0    # Branch if int comparison !=
    IF_ICMPLT = 0xA1    # Branch if int comparison <
    IF_ICMPGE = 0xA2    # Branch if int comparison >=
    IF_ICMPGT = 0xA3    # Branch if int comparison >
    IF_ICMPLE = 0xA4    # Branch if int comparison <=

    IF_ACMPEQ = 0xA5    # Branch if reference comparison ==
    IF_ACMPNE = 0xA6    # Branch if reference comparison !=

    # === CONTROL FLOW (0xA7-0xB1) ===
    GOTO = 0xA7         # Branch always (2 operands: offset)
    JSR = 0xA8          # Jump subroutine (deprecated)
    RET = 0xA9          # Return from subroutine (deprecated)

    TABLESWITCH = 0xAA  # Switch by index
    LOOKUPSWITCH = 0xAB # Switch by key match

    IRETURN = 0xAC      # Return int from method
    LRETURN = 0xAD      # Return long from method
    FRETURN = 0xAE      # Return float from method
    DRETURN = 0xAF      # Return double from method
    ARETURN = 0xB0      # Return reference from method
    RETURN = 0xB1       # Return void from method

    # === FIELD ACCESS (0xB2-0xB5) ===
    GETSTATIC = 0xB2    # Get static field (2 operands: fieldref index)
    PUTSTATIC = 0xB3    # Put static field
    GETFIELD = 0xB4     # Get instance field
    PUTFIELD = 0xB5     # Put instance field

    # === METHOD INVOCATION (0xB6-0xBA) ===
    INVOKEVIRTUAL = 0xB6    # Invoke instance method (2 operands: methodref)
    INVOKESPECIAL = 0xB7    # Invoke instance method (special handling)
    INVOKESTATIC = 0xB8     # Invoke class (static) method
    INVOKEINTERFACE = 0xB9  # Invoke interface method
    INVOKEDYNAMIC = 0xBA    # Invoke dynamic method

    # === OBJECT CREATION (0xBB-0xC1) ===
    NEW = 0xBB          # Create new object (2 operands: class index)
    NEWARRAY = 0xBC     # Create new array (1 operand: atype)
    ANEWARRAY = 0xBD    # Create new array of reference
    ARRAYLENGTH = 0xBE  # Get length of array

    ATHROW = 0xBF       # Throw exception

    CHECKCAST = 0xC0    # Check whether object is of given type
    INSTANCEOF = 0xC1   # Determine if object is of given type

    # === SYNCHRONIZATION (0xC2-0xC3) ===
    MONITORENTER = 0xC2 # Enter monitor for object
    MONITOREXIT = 0xC3  # Exit monitor for object

    # === EXTENDED (0xC4-0xC9) ===
    WIDE = 0xC4         # Extend local variable index
    MULTIANEWARRAY = 0xC5  # Create multidimensional array

    IFNULL = 0xC6       # Branch if reference is null
    IFNONNULL = 0xC7    # Branch if reference is not null

    GOTO_W = 0xC8       # Branch always (wide index)
    JSR_W = 0xC9        # Jump subroutine (wide index, deprecated)


class JVMInstruction:
    """
    Representa una instruccion JVM.

    Cada instruccion tiene:
    - opcode: El codigo de operacion (JVMOpcode)
    - operands: Lista de operandos (opcional)
    - label: Etiqueta para saltos (opcional)
    """

    def __init__(self, opcode: JVMOpcode, operands: Optional[List[int]] = None, label: Optional[str] = None):
        self.opcode = opcode
        self.operands = operands or []
        self.label = label

    def to_bytes(self) -> bytes:
        """
        Convierte la instruccion a bytes.

        Returns:
            Bytes de la instruccion (opcode + operandos)
        """
        result = bytes([self.opcode.value])

        # Agregar operandos segun el tipo de instruccion
        if self.operands:
            for operand in self.operands:
                # La mayoria de operandos son de 1 byte
                # Algunos son de 2 bytes (indices de constant pool, offsets)
                if self.opcode in [
                    JVMOpcode.SIPUSH,
                    JVMOpcode.LDC_W, JVMOpcode.LDC2_W,
                    JVMOpcode.IFEQ, JVMOpcode.IFNE, JVMOpcode.IFLT,
                    JVMOpcode.IFGE, JVMOpcode.IFGT, JVMOpcode.IFLE,
                    JVMOpcode.IF_ICMPEQ, JVMOpcode.IF_ICMPNE,
                    JVMOpcode.IF_ICMPLT, JVMOpcode.IF_ICMPGE,
                    JVMOpcode.IF_ICMPGT, JVMOpcode.IF_ICMPLE,
                    JVMOpcode.IF_ACMPEQ, JVMOpcode.IF_ACMPNE,
                    JVMOpcode.GOTO, JVMOpcode.GOTO_W,
                    JVMOpcode.GETSTATIC, JVMOpcode.PUTSTATIC,
                    JVMOpcode.GETFIELD, JVMOpcode.PUTFIELD,
                    JVMOpcode.INVOKEVIRTUAL, JVMOpcode.INVOKESPECIAL,
                    JVMOpcode.INVOKESTATIC,
                    JVMOpcode.NEW, JVMOpcode.ANEWARRAY,
                    JVMOpcode.CHECKCAST, JVMOpcode.INSTANCEOF,
                    JVMOpcode.IFNULL, JVMOpcode.IFNONNULL
                ]:
                    # Operando de 2 bytes (big-endian)
                    result += struct.pack('>H', operand)
                else:
                    # Operando de 1 byte
                    result += bytes([operand])

        return result

    def __str__(self) -> str:
        """Representacion en string para debugging."""
        operands_str = ', '.join(str(op) for op in self.operands) if self.operands else ''
        label_str = f'{self.label}: ' if self.label else ''
        return f'{label_str}{self.opcode.name} {operands_str}'.strip()

    def __repr__(self) -> str:
        return f'JVMInstruction({self.opcode.name}, {self.operands}, {self.label})'


# === HELPER FUNCTIONS ===

def iconst(value: int) -> JVMInstruction:
    """
    Genera instruccion para push de constante int.

    Optimiza usando iconst_0..iconst_5, bipush, sipush o ldc segun el valor.
    """
    if value == -1:
        return JVMInstruction(JVMOpcode.ICONST_M1)
    elif 0 <= value <= 5:
        opcode = [JVMOpcode.ICONST_0, JVMOpcode.ICONST_1, JVMOpcode.ICONST_2,
                  JVMOpcode.ICONST_3, JVMOpcode.ICONST_4, JVMOpcode.ICONST_5][value]
        return JVMInstruction(opcode)
    elif -128 <= value <= 127:
        # bipush: 1 byte signed
        return JVMInstruction(JVMOpcode.BIPUSH, [value & 0xFF])
    elif -32768 <= value <= 32767:
        # sipush: 2 bytes signed
        return JVMInstruction(JVMOpcode.SIPUSH, [value & 0xFFFF])
    else:
        # ldc: necesita indice del constant pool (se maneja externamente)
        # Por ahora retornamos None para indicar que se necesita ldc
        return None


def iload(index: int) -> JVMInstruction:
    """Genera instruccion iload optimizada (iload_0..iload_3 o iload)."""
    if 0 <= index <= 3:
        opcode = [JVMOpcode.ILOAD_0, JVMOpcode.ILOAD_1,
                  JVMOpcode.ILOAD_2, JVMOpcode.ILOAD_3][index]
        return JVMInstruction(opcode)
    else:
        return JVMInstruction(JVMOpcode.ILOAD, [index])


def istore(index: int) -> JVMInstruction:
    """Genera instruccion istore optimizada (istore_0..istore_3 o istore)."""
    if 0 <= index <= 3:
        opcode = [JVMOpcode.ISTORE_0, JVMOpcode.ISTORE_1,
                  JVMOpcode.ISTORE_2, JVMOpcode.ISTORE_3][index]
        return JVMInstruction(opcode)
    else:
        return JVMInstruction(JVMOpcode.ISTORE, [index])


def dload(index: int) -> JVMInstruction:
    """Genera instruccion dload optimizada."""
    if 0 <= index <= 3:
        opcode = [JVMOpcode.DLOAD_0, JVMOpcode.DLOAD_1,
                  JVMOpcode.DLOAD_2, JVMOpcode.DLOAD_3][index]
        return JVMInstruction(opcode)
    else:
        return JVMInstruction(JVMOpcode.DLOAD, [index])


def dstore(index: int) -> JVMInstruction:
    """Genera instruccion dstore optimizada."""
    if 0 <= index <= 3:
        opcode = [JVMOpcode.DSTORE_0, JVMOpcode.DSTORE_1,
                  JVMOpcode.DSTORE_2, JVMOpcode.DSTORE_3][index]
        return JVMInstruction(opcode)
    else:
        return JVMInstruction(JVMOpcode.DSTORE, [index])


def aload(index: int) -> JVMInstruction:
    """Genera instruccion aload optimizada."""
    if 0 <= index <= 3:
        opcode = [JVMOpcode.ALOAD_0, JVMOpcode.ALOAD_1,
                  JVMOpcode.ALOAD_2, JVMOpcode.ALOAD_3][index]
        return JVMInstruction(opcode)
    else:
        return JVMInstruction(JVMOpcode.ALOAD, [index])


def astore(index: int) -> JVMInstruction:
    """Genera instruccion astore optimizada."""
    if 0 <= index <= 3:
        opcode = [JVMOpcode.ASTORE_0, JVMOpcode.ASTORE_1,
                  JVMOpcode.ASTORE_2, JVMOpcode.ASTORE_3][index]
        return JVMInstruction(opcode)
    else:
        return JVMInstruction(JVMOpcode.ASTORE, [index])


# === ARRAY TYPE CODES ===
class ArrayType(Enum):
    """Tipos de arrays para la instruccion NEWARRAY."""
    T_BOOLEAN = 4
    T_CHAR = 5
    T_FLOAT = 6
    T_DOUBLE = 7
    T_BYTE = 8
    T_SHORT = 9
    T_INT = 10
    T_LONG = 11
