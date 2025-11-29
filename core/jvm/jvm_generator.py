"""
JVM Generator - Generador de bytecode JVM desde TAC

Convierte el codigo intermedio TAC (Three-Address Code) a bytecode JVM real.
Maneja:
- Traduccion de operaciones TAC a instrucciones JVM
- Gestion de variables locales (local variable slots)
- Calculo de max_stack y max_locals
- Generacion de metodos completos con Code attributes

Referencias:
- core/tac.py - Instrucciones TAC de entrada
- core/jvm/instructions.py - Instrucciones JVM de salida
"""

from typing import Dict, List, Optional, Tuple
from core.tac import TACInstruction
from core.jvm.instructions import (
    JVMInstruction, JVMOpcode, iconst, iload, istore,
    dload, dstore, aload, astore, ArrayType
)
from core.jvm.constant_pool import ConstantPool
from core.jvm.descriptors import TypeDescriptor
from core.utils import TipoDato


class LocalVariableManager:
    """
    Gestiona la asignacion de local variable slots.

    En JVM, cada variable local ocupa un slot:
    - int, float, reference: 1 slot
    - long, double: 2 slots

    Slot 0 en metodos de instancia es 'this'
    Slot 0 en metodos estaticos es primer parametro
    """

    def __init__(self, is_static: bool = True, param_count: int = 0):
        self.is_static = is_static
        self.next_slot = 0 if is_static else 1  # this ocupa slot 0 si no es estatico
        self.var_to_slot: Dict[str, int] = {}
        self.var_types: Dict[str, TipoDato] = {}

        # Reservar slots para parametros
        for i in range(param_count):
            self.next_slot += 1

    def get_or_allocate(self, var_name: str, var_type: TipoDato = TipoDato.INT) -> int:
        """
        Obtiene o asigna un slot para una variable.

        Args:
            var_name: Nombre de la variable
            var_type: Tipo de la variable (para calcular slots)

        Returns:
            Indice del slot asignado
        """
        if var_name in self.var_to_slot:
            return self.var_to_slot[var_name]

        # Asignar nuevo slot
        slot = self.next_slot
        self.var_to_slot[var_name] = slot
        self.var_types[var_name] = var_type

        # long y double ocupan 2 slots
        if var_type in [TipoDato.DOUBLE]:
            self.next_slot += 2
        else:
            self.next_slot += 1

        return slot

    def get_max_locals(self) -> int:
        """Retorna el numero maximo de local variables usado."""
        return self.next_slot


class StackDepthTracker:
    """
    Rastrea la profundidad del stack para calcular max_stack.

    Cada instruccion JVM modifica el stack:
    - iconst, iload: +1
    - iadd, isub: -1 (consume 2, produce 1)
    - istore: -1
    etc.
    """

    def __init__(self):
        self.current_depth = 0
        self.max_depth = 0

    def push(self, count: int = 1):
        """Simula push de valores al stack."""
        self.current_depth += count
        if self.current_depth > self.max_depth:
            self.max_depth = self.current_depth

    def pop(self, count: int = 1):
        """Simula pop de valores del stack."""
        self.current_depth -= count
        if self.current_depth < 0:
            self.current_depth = 0  # Safety

    def get_max_stack(self) -> int:
        """Retorna la profundidad maxima alcanzada."""
        return self.max_depth


class JVMGenerator:
    """
    Generador de bytecode JVM desde TAC.

    Convierte una lista de instrucciones TAC a bytecode JVM,
    gestionando variables locales y calculando max_stack/max_locals.
    """

    def __init__(self, constant_pool: ConstantPool):
        self.constant_pool = constant_pool
        self.local_vars = LocalVariableManager(is_static=True)
        self.stack_tracker = StackDepthTracker()
        self.instructions: List[JVMInstruction] = []
        self.labels: Dict[str, int] = {}  # label -> instruction offset

    def generate(self, tac_instructions: List[TACInstruction]) -> Tuple[bytes, int, int]:
        """
        Genera bytecode JVM desde instrucciones TAC.

        Args:
            tac_instructions: Lista de instrucciones TAC

        Returns:
            Tupla (bytecode, max_stack, max_locals)
        """
        self.instructions = []
        self.labels = {}

        # Primera pasada: generar instrucciones JVM
        for tac_inst in tac_instructions:
            self._translate_instruction(tac_inst)

        # Segunda pasada: resolver labels y offsets
        bytecode = self._resolve_labels_and_generate_bytecode()

        return bytecode, self.stack_tracker.get_max_stack(), self.local_vars.get_max_locals()

    def _translate_instruction(self, tac_inst: TACInstruction):
        """Traduce una instruccion TAC a una o mas instrucciones JVM."""

        op = tac_inst.op

        if op == 'LABEL':
            # Marcar label (se resuelve en segunda pasada)
            self.labels[tac_inst.label] = len(self.instructions)

        elif op == 'ASSIGN':
            # result = arg1
            self._generate_load(tac_inst.arg1)
            self._generate_store(tac_inst.result)

        elif op in ['ADD', 'SUB', 'MUL',
                    'DIV', 'MOD']:
            # result = arg1 op arg2
            self._generate_load(tac_inst.arg1)
            self._generate_load(tac_inst.arg2)
            self._generate_arithmetic(op)
            self._generate_store(tac_inst.result)

        elif op == 'NEG':
            # result = -arg1
            self._generate_load(tac_inst.arg1)
            self.instructions.append(JVMInstruction(JVMOpcode.INEG))
            self.stack_tracker.pop()
            self.stack_tracker.push()
            self._generate_store(tac_inst.result)

        elif op == 'NOT':
            # result = !arg1
            # En JVM: xor con 1 (invierte boolean)
            self._generate_load(tac_inst.arg1)
            self.instructions.append(iconst(1))
            self.stack_tracker.push()
            self.instructions.append(JVMInstruction(JVMOpcode.IXOR))
            self.stack_tracker.pop(2)
            self.stack_tracker.push()
            self._generate_store(tac_inst.result)

        elif op in ['LT', 'GT', 'LE',
                    'GE', 'EQ', 'NE']:
            # Comparaciones: result = arg1 op arg2
            self._generate_comparison(op, tac_inst.arg1, tac_inst.arg2, tac_inst.result)

        elif op in ['AND', 'OR']:
            # Operadores logicos
            self._generate_logical(op, tac_inst.arg1, tac_inst.arg2, tac_inst.result)

        elif op == 'GOTO':
            # goto label (label esta en arg1)
            self.instructions.append(JVMInstruction(JVMOpcode.GOTO, [0], label=tac_inst.arg1))

        elif op == 'IF_FALSE':
            # if !arg1 goto arg2
            self._generate_load(tac_inst.arg1)
            self.instructions.append(JVMInstruction(JVMOpcode.IFEQ, [0], label=tac_inst.arg2))
            self.stack_tracker.pop()

        elif op == 'RETURN':
            # return arg1 (o return si es void)
            if tac_inst.arg1:
                self._generate_load(tac_inst.arg1)
                # Determinar tipo de return
                # Por ahora asumimos int, pero deberia verificarse el tipo
                self.instructions.append(JVMInstruction(JVMOpcode.IRETURN))
                self.stack_tracker.pop()
            else:
                self.instructions.append(JVMInstruction(JVMOpcode.RETURN))

        elif op == 'PARAM':
            # Parametro para llamada (se maneja en CALL)
            pass

        elif op == 'CALL':
            # result = call arg1(params)
            # Por ahora simplificado, necesita mejora
            # TODO: Implementar llamadas a metodos completas
            pass

        elif op == 'ARRAY_LOAD':
            # result = arr[index]
            self._generate_array_load(tac_inst.arg1, tac_inst.arg2, tac_inst.result)

        elif op == 'ARRAY_STORE':
            # arr[index] = value
            self._generate_array_store(tac_inst.result, tac_inst.arg1, tac_inst.arg2)

    def _generate_load(self, operand: str):
        """Genera instruccion para cargar un operando al stack."""
        # Verificar si es literal numerico
        if operand.lstrip('-').isdigit():
            value = int(operand)
            inst = iconst(value)
            if inst:
                self.instructions.append(inst)
                self.stack_tracker.push()
            else:
                # Necesita ldc (constant pool)
                index = self.constant_pool.add_integer(value)
                self.instructions.append(JVMInstruction(JVMOpcode.LDC, [index]))
                self.stack_tracker.push()
        # Verificar si es float/double
        elif '.' in operand:
            value = float(operand)
            index = self.constant_pool.add_double(value)
            self.instructions.append(JVMInstruction(JVMOpcode.LDC2_W, [index]))
            self.stack_tracker.push(2)  # double ocupa 2 slots en stack
        else:
            # Es una variable
            slot = self.local_vars.get_or_allocate(operand)
            var_type = self.local_vars.var_types.get(operand, TipoDato.INT)

            if var_type == TipoDato.DOUBLE:
                self.instructions.append(dload(slot))
                self.stack_tracker.push(2)
            elif var_type in [TipoDato.STRING, TipoDato.ARRAY_INT, TipoDato.ARRAY_DOUBLE]:
                self.instructions.append(aload(slot))
                self.stack_tracker.push()
            else:
                self.instructions.append(iload(slot))
                self.stack_tracker.push()

    def _generate_store(self, var_name: str):
        """Genera instruccion para almacenar del stack a variable local."""
        slot = self.local_vars.get_or_allocate(var_name)
        var_type = self.local_vars.var_types.get(var_name, TipoDato.INT)

        if var_type == TipoDato.DOUBLE:
            self.instructions.append(dstore(slot))
            self.stack_tracker.pop(2)
        elif var_type in [TipoDato.STRING, TipoDato.ARRAY_INT, TipoDato.ARRAY_DOUBLE]:
            self.instructions.append(astore(slot))
            self.stack_tracker.pop()
        else:
            self.instructions.append(istore(slot))
            self.stack_tracker.pop()

    def _generate_arithmetic(self, op: str):
        """Genera instruccion aritmetica JVM."""
        # Por ahora asumimos int, deberia verificar tipos
        opcode_map = {
            'ADD': JVMOpcode.IADD,
            'SUB': JVMOpcode.ISUB,
            'MUL': JVMOpcode.IMUL,
            'DIV': JVMOpcode.IDIV,
            'MOD': JVMOpcode.IREM,
        }

        self.instructions.append(JVMInstruction(opcode_map[op]))
        self.stack_tracker.pop(2)  # Consume 2 operandos
        self.stack_tracker.push()  # Produce 1 resultado

    def _generate_comparison(self, op: str, arg1: str, arg2: str, result: str):
        """Genera codigo para comparaciones."""
        # Cargar operandos
        self._generate_load(arg1)
        self._generate_load(arg2)

        # Mapa de operaciones a opcodes
        opcode_map = {
            'EQ': JVMOpcode.IF_ICMPEQ,
            'NE': JVMOpcode.IF_ICMPNE,
            'LT': JVMOpcode.IF_ICMPLT,
            'GE': JVMOpcode.IF_ICMPGE,
            'GT': JVMOpcode.IF_ICMPGT,
            'LE': JVMOpcode.IF_ICMPLE,
        }

        # En JVM, comparaciones son branch instructions
        # Para obtener valor boolean, usamos patron:
        # if_icmpXX true_label
        # iconst_0 (false)
        # goto end_label
        # true_label:
        # iconst_1 (true)
        # end_label:

        true_label = f"CMP_TRUE_{len(self.instructions)}"
        end_label = f"CMP_END_{len(self.instructions)}"

        self.instructions.append(JVMInstruction(opcode_map[op], [0], label=true_label))
        self.stack_tracker.pop(2)

        # False path
        self.instructions.append(iconst(0))
        self.stack_tracker.push()
        self.instructions.append(JVMInstruction(JVMOpcode.GOTO, [0], label=end_label))

        # True path
        self.labels[true_label] = len(self.instructions)
        self.instructions.append(iconst(1))
        self.stack_tracker.push()

        # End
        self.labels[end_label] = len(self.instructions)

        # Almacenar resultado
        self._generate_store(result)

    def _generate_logical(self, op: str, arg1: str, arg2: str, result: str):
        """Genera codigo para operadores logicos AND/OR."""
        if op == 'AND':
            # AND: arg1 && arg2
            self._generate_load(arg1)
            self._generate_load(arg2)
            self.instructions.append(JVMInstruction(JVMOpcode.IAND))
            self.stack_tracker.pop(2)
            self.stack_tracker.push()
            self._generate_store(result)

        elif op == 'OR':
            # OR: arg1 || arg2
            self._generate_load(arg1)
            self._generate_load(arg2)
            self.instructions.append(JVMInstruction(JVMOpcode.IOR))
            self.stack_tracker.pop(2)
            self.stack_tracker.push()
            self._generate_store(result)

    def _generate_array_load(self, array: str, index: str, result: str):
        """Genera codigo para cargar elemento de array."""
        self._generate_load(array)  # Array reference
        self._generate_load(index)  # Index
        self.instructions.append(JVMInstruction(JVMOpcode.IALOAD))  # Por ahora int arrays
        self.stack_tracker.pop(2)
        self.stack_tracker.push()
        self._generate_store(result)

    def _generate_array_store(self, array: str, index: str, value: str):
        """Genera codigo para almacenar en array."""
        self._generate_load(array)  # Array reference
        self._generate_load(index)  # Index
        self._generate_load(value)  # Value
        self.instructions.append(JVMInstruction(JVMOpcode.IASTORE))  # Por ahora int arrays
        self.stack_tracker.pop(3)

    def _resolve_labels_and_generate_bytecode(self) -> bytes:
        """
        Segunda pasada: resuelve labels y genera bytecode final.

        Calcula offsets para branches (goto, if_xxx) basado en posiciones de labels.
        """
        # Primero calcular posiciones de cada instruccion
        positions = {}
        current_pos = 0

        for i, inst in enumerate(self.instructions):
            positions[i] = current_pos
            current_pos += len(inst.to_bytes())

        # Resolver offsets de branches
        for i, inst in enumerate(self.instructions):
            if inst.label and inst.opcode in [
                JVMOpcode.GOTO, JVMOpcode.IFEQ, JVMOpcode.IFNE,
                JVMOpcode.IF_ICMPEQ, JVMOpcode.IF_ICMPNE,
                JVMOpcode.IF_ICMPLT, JVMOpcode.IF_ICMPGE,
                JVMOpcode.IF_ICMPGT, JVMOpcode.IF_ICMPLE
            ]:
                # Encontrar indice de instruccion con el label
                target_label = inst.label
                if target_label in self.labels:
                    target_index = self.labels[target_label]
                    target_pos = positions[target_index]
                    current_pos = positions[i]
                    offset = target_pos - current_pos

                    # Actualizar operando con offset
                    inst.operands = [offset & 0xFFFF]  # 2 bytes signed

        # Generar bytecode final
        bytecode = b''.join(inst.to_bytes() for inst in self.instructions)
        return bytecode
