"""
Generador de Bytecode Stack-Based desde TAC

Este módulo implementa un generador de bytecode que traduce código de tres
direcciones (TAC) a un formato de bytecode basado en pila (stack-based),
similar a assembly, que es fácil de leer y puede ser presentado al profesor
como "código ensamblador".

Autor: Gabriel Alejandro Medina Miramontes
Versión: 1.1
"""

from typing import List, Dict, Optional
from core.tac import TACInstruction


class BytecodeInstruction:
    """
    Representa una instrucción de bytecode stack-based.

    El bytecode usa una arquitectura de pila (stack) donde:
    - Operandos se pushean al stack
    - Operaciones consumen elementos del stack
    - Resultados se pushean de vuelta al stack
    """

    def __init__(self, opcode: str, operand: Optional[str] = None, comment: Optional[str] = None):
        """
        Inicializa una instrucción de bytecode.

        Args:
            opcode: Código de operación (PUSH, LOAD, ADD, etc.)
            operand: Operando opcional (variable, literal, label)
            comment: Comentario opcional para documentar la instrucción
        """
        self.opcode = opcode
        self.operand = operand
        self.comment = comment

    def __str__(self) -> str:
        """Representación legible de la instrucción"""
        # Formatear instrucción
        if self.operand:
            instruction = f"{self.opcode:<12} {self.operand}"
        else:
            instruction = f"{self.opcode}"

        # Agregar comentario si existe
        if self.comment:
            instruction = f"{instruction:<30} ; {self.comment}"

        return instruction


class BytecodeGenerator:
    """
    Generador de bytecode stack-based desde código TAC.

    Traduce instrucciones TAC a bytecode que usa una arquitectura de pila.
    El bytecode generado es legible y similar a assembly tradicional.

    Instrucciones Bytecode:
    - PUSH <literal>     : Push literal al stack
    - LOAD <var>         : Push variable al stack
    - STORE <var>        : Pop y guardar en variable
    - ADD, SUB, MUL, DIV : Operaciones aritméticas (pop 2, push resultado)
    - EQ, LT, GT, etc.   : Comparaciones (pop 2, push bool)
    - AND, OR, NOT       : Operaciones lógicas
    - LABEL <name>       : Etiqueta para saltos
    - JUMP <label>       : Salto incondicional
    - JUMPF <label>      : Salto si falso (pop condición)
    - CALL <func>        : Llamar función
    - RET                : Retornar de función
    - HALT               : Fin de programa
    """

    def __init__(self):
        """Inicializa el generador de bytecode"""
        self.instructions: List[BytecodeInstruction] = []
        self.current_function: Optional[str] = None

    def generate(self, tac_instructions: List[TACInstruction]) -> List[BytecodeInstruction]:
        """
        Genera bytecode desde lista de instrucciones TAC.

        Args:
            tac_instructions: Lista de instrucciones TAC

        Returns:
            Lista de instrucciones de bytecode
        """
        self.instructions = []

        for tac in tac_instructions:
            self._translate_instruction(tac)

        # Agregar HALT al final si no existe
        if not self.instructions or self.instructions[-1].opcode != 'HALT':
            self.instructions.append(BytecodeInstruction('HALT', comment="Fin del programa"))

        return self.instructions

    def _translate_instruction(self, tac: TACInstruction):
        """Traduce una instrucción TAC a bytecode"""

        if tac.op == 'LABEL':
            self._translate_label(tac)

        elif tac.op == 'ASSIGN':
            self._translate_assign(tac)

        elif tac.op in ['ADD', 'SUB', 'MUL', 'DIV', 'MOD']:
            self._translate_arithmetic(tac)

        elif tac.op in ['LT', 'GT', 'LE', 'GE', 'EQ', 'NE']:
            self._translate_comparison(tac)

        elif tac.op in ['AND', 'OR']:
            self._translate_logical_binary(tac)

        elif tac.op == 'NOT':
            self._translate_not(tac)

        elif tac.op == 'NEG':
            self._translate_neg(tac)

        elif tac.op == 'GOTO':
            self._translate_goto(tac)

        elif tac.op == 'IF_FALSE':
            self._translate_if_false(tac)

        elif tac.op == 'PARAM':
            self._translate_param(tac)

        elif tac.op == 'CALL':
            self._translate_call(tac)

        elif tac.op == 'RETURN':
            self._translate_return(tac)

        elif tac.op == 'ARRAY_LOAD':
            self._translate_array_load(tac)

        elif tac.op == 'ARRAY_STORE':
            self._translate_array_store(tac)

    def _translate_label(self, tac: TACInstruction):
        """Traduce LABEL a bytecode"""
        self.instructions.append(
            BytecodeInstruction('LABEL', tac.label)
        )

        # Si es una etiqueta de función, actualizar función actual
        if tac.label and tac.label.startswith('func_'):
            func_name = tac.label.replace('func_', '')
            self.current_function = func_name

    def _translate_assign(self, tac: TACInstruction):
        """
        Traduce ASSIGN a bytecode.

        TAC: result = arg1
        Bytecode:
            LOAD arg1    (o PUSH si es literal)
            STORE result
        """
        # Cargar el valor fuente
        if self._is_literal(tac.arg1):
            self.instructions.append(
                BytecodeInstruction('PUSH', tac.arg1, f"Push literal {tac.arg1}")
            )
        else:
            self.instructions.append(
                BytecodeInstruction('LOAD', tac.arg1, f"Load {tac.arg1}")
            )

        # Guardar en destino
        self.instructions.append(
            BytecodeInstruction('STORE', tac.result, f"Store in {tac.result}")
        )

    def _translate_arithmetic(self, tac: TACInstruction):
        """
        Traduce operaciones aritméticas a bytecode.

        TAC: result = arg1 op arg2
        Bytecode:
            LOAD arg1
            LOAD arg2
            OP
            STORE result
        """
        op_name = {
            'ADD': '+', 'SUB': '-', 'MUL': '*', 'DIV': '/', 'MOD': '%'
        }.get(tac.op, tac.op)

        # Cargar operandos
        self._load_operand(tac.arg1, f"Left operand of {op_name}")
        self._load_operand(tac.arg2, f"Right operand of {op_name}")

        # Ejecutar operación
        self.instructions.append(
            BytecodeInstruction(tac.op, comment=f"Compute {tac.arg1} {op_name} {tac.arg2}")
        )

        # Guardar resultado
        self.instructions.append(
            BytecodeInstruction('STORE', tac.result, f"Store result in {tac.result}")
        )

    def _translate_comparison(self, tac: TACInstruction):
        """
        Traduce comparaciones a bytecode.

        TAC: result = arg1 cmp arg2
        Bytecode:
            LOAD arg1
            LOAD arg2
            CMP_OP
            STORE result
        """
        op_symbol = {
            'LT': '<', 'GT': '>', 'LE': '<=', 'GE': '>=', 'EQ': '==', 'NE': '!='
        }.get(tac.op, tac.op)

        # Cargar operandos
        self._load_operand(tac.arg1, f"Left operand")
        self._load_operand(tac.arg2, f"Right operand")

        # Ejecutar comparación
        self.instructions.append(
            BytecodeInstruction(tac.op, comment=f"Compare {tac.arg1} {op_symbol} {tac.arg2}")
        )

        # Guardar resultado
        self.instructions.append(
            BytecodeInstruction('STORE', tac.result, f"Store boolean result in {tac.result}")
        )

    def _translate_logical_binary(self, tac: TACInstruction):
        """Traduce operadores lógicos binarios (AND, OR)"""
        op_symbol = '&&' if tac.op == 'AND' else '||'

        # Cargar operandos
        self._load_operand(tac.arg1, f"Left operand")
        self._load_operand(tac.arg2, f"Right operand")

        # Ejecutar operación lógica
        self.instructions.append(
            BytecodeInstruction(tac.op, comment=f"Compute {tac.arg1} {op_symbol} {tac.arg2}")
        )

        # Guardar resultado
        self.instructions.append(
            BytecodeInstruction('STORE', tac.result, f"Store in {tac.result}")
        )

    def _translate_not(self, tac: TACInstruction):
        """Traduce operador NOT"""
        # Cargar operando
        self._load_operand(tac.arg1, f"Operand")

        # Ejecutar NOT
        self.instructions.append(
            BytecodeInstruction('NOT', comment=f"Logical NOT of {tac.arg1}")
        )

        # Guardar resultado
        self.instructions.append(
            BytecodeInstruction('STORE', tac.result, f"Store in {tac.result}")
        )

    def _translate_neg(self, tac: TACInstruction):
        """Traduce negación unaria"""
        # Cargar operando
        self._load_operand(tac.arg1, f"Operand")

        # Ejecutar NEG
        self.instructions.append(
            BytecodeInstruction('NEG', comment=f"Negate {tac.arg1}")
        )

        # Guardar resultado
        self.instructions.append(
            BytecodeInstruction('STORE', tac.result, f"Store in {tac.result}")
        )

    def _translate_goto(self, tac: TACInstruction):
        """Traduce GOTO a JUMP"""
        self.instructions.append(
            BytecodeInstruction('JUMP', tac.arg1, f"Unconditional jump to {tac.arg1}")
        )

    def _translate_if_false(self, tac: TACInstruction):
        """
        Traduce IF_FALSE a JUMPF.

        TAC: IF_FALSE arg1 GOTO arg2
        Bytecode:
            LOAD arg1
            JUMPF arg2
        """
        # Cargar condición
        self._load_operand(tac.arg1, "Condition")

        # Saltar si falso
        self.instructions.append(
            BytecodeInstruction('JUMPF', tac.arg2, f"Jump to {tac.arg2} if false")
        )

    def _translate_param(self, tac: TACInstruction):
        """
        Traduce PARAM a PUSH.

        Los parámetros se pushean al stack para la llamada de función.
        """
        self._load_operand(tac.arg1, f"Parameter")

    def _translate_call(self, tac: TACInstruction):
        """
        Traduce CALL a bytecode.

        TAC: result = CALL func, num_args
        Bytecode:
            CALL func
            STORE result
        """
        func_name = tac.arg1
        num_args = tac.arg2

        # Llamar función
        self.instructions.append(
            BytecodeInstruction('CALL', func_name, f"Call {func_name} with {num_args} args")
        )

        # Guardar resultado si existe
        if tac.result:
            self.instructions.append(
                BytecodeInstruction('STORE', tac.result, f"Store return value in {tac.result}")
            )

    def _translate_return(self, tac: TACInstruction):
        """
        Traduce RETURN a bytecode.

        TAC: RETURN [arg1]
        Bytecode:
            [LOAD arg1]  (si hay valor de retorno)
            RET
        """
        # Si hay valor de retorno, cargarlo
        if tac.arg1:
            self._load_operand(tac.arg1, "Return value")

        # Retornar
        self.instructions.append(
            BytecodeInstruction('RET', comment="Return from function")
        )

    def _translate_array_load(self, tac: TACInstruction):
        """
        Traduce ARRAY_LOAD a bytecode.

        TAC: result = arr[index]
        Bytecode:
            LOAD arr
            LOAD index
            ALOAD
            STORE result
        """
        # Cargar array
        self._load_operand(tac.arg1, f"Array {tac.arg1}")

        # Cargar índice
        self._load_operand(tac.arg2, f"Index")

        # Cargar elemento del array
        self.instructions.append(
            BytecodeInstruction('ALOAD', comment=f"Load {tac.arg1}[{tac.arg2}]")
        )

        # Guardar resultado
        self.instructions.append(
            BytecodeInstruction('STORE', tac.result, f"Store in {tac.result}")
        )

    def _translate_array_store(self, tac: TACInstruction):
        """
        Traduce ARRAY_STORE a bytecode.

        TAC: arr[index] = value
        Bytecode:
            LOAD arr
            LOAD index
            LOAD value
            ASTORE
        """
        # Cargar array
        array_name = tac.result
        self._load_operand(array_name, f"Array {array_name}")

        # Cargar índice
        self._load_operand(tac.arg1, f"Index")

        # Cargar valor
        self._load_operand(tac.arg2, f"Value")

        # Guardar en array
        self.instructions.append(
            BytecodeInstruction('ASTORE', comment=f"Store in {array_name}[{tac.arg1}]")
        )

    def _load_operand(self, operand: str, comment: str = ""):
        """
        Carga un operando al stack (PUSH si es literal, LOAD si es variable).

        Args:
            operand: Operando a cargar
            comment: Comentario opcional
        """
        if self._is_literal(operand):
            self.instructions.append(
                BytecodeInstruction('PUSH', operand, comment or f"Push {operand}")
            )
        else:
            self.instructions.append(
                BytecodeInstruction('LOAD', operand, comment or f"Load {operand}")
            )

    def _is_literal(self, value: str) -> bool:
        """
        Determina si un valor es un literal (número, string, booleano).

        Args:
            value: Valor a verificar

        Returns:
            True si es literal, False si es variable/temporal
        """
        if not value:
            return False

        # Números
        if value.replace('.', '', 1).replace('-', '', 1).isdigit():
            return True

        # Strings (comienzan y terminan con comillas)
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            return True

        # Booleanos
        if value in ('true', 'false', 'True', 'False'):
            return True

        # Propiedades (contienen punto)
        if '.' in value:
            return False

        return False

    def format_output(self, show_comments: bool = True) -> str:
        """
        Formatea el bytecode para mostrar en UI.

        Args:
            show_comments: Si incluir comentarios en la salida

        Returns:
            String con bytecode formateado estilo assembly
        """
        if not self.instructions:
            return "; No bytecode generated"

        lines = []
        lines.append("; KForge Compiler - Bytecode Assembly")
        lines.append("; Generated from TAC Intermediate Representation")
        lines.append("; Architecture: Stack-Based")
        lines.append("")

        for i, inst in enumerate(self.instructions):
            # Formatear número de línea
            line_num = f"{i:4d}:  "

            # Formatear instrucción
            if inst.opcode == 'LABEL':
                # Labels sin indentación
                if show_comments and inst.comment:
                    line = f"{line_num}{inst.operand}:    ; {inst.comment}"
                else:
                    line = f"{line_num}{inst.operand}:"
            else:
                # Instrucciones normales con indentación
                if inst.operand:
                    instruction = f"    {inst.opcode:<12} {inst.operand}"
                else:
                    instruction = f"    {inst.opcode}"

                if show_comments and inst.comment:
                    line = f"{line_num}{instruction:<40} ; {inst.comment}"
                else:
                    line = f"{line_num}{instruction}"

            lines.append(line)

        return '\n'.join(lines)
