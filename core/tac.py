"""
Generador de Código de Tres Direcciones (TAC - Three-Address Code)

Este módulo implementa la generación de código intermedio TAC desde el AST validado.
TAC es una representación intermedia profesional que facilita optimizaciones y
generación de código destino.

Autor: Gabriel Alejandro Medina Miramontes
Versión: 1.1
"""

from dataclasses import dataclass
from typing import List, Optional, Any
from core.utils import NodoAST, TipoNodo, TipoDato


@dataclass
class TACInstruction:
    """
    Instrucción de código de tres direcciones.

    Formato general: result = arg1 op arg2

    Ejemplos:
        t1 = a + b      -> TACInstruction('ADD', 'a', 'b', 't1')
        x = 5           -> TACInstruction('ASSIGN', '5', None, 'x')
        IF_FALSE t1 L1  -> TACInstruction('IF_FALSE', 't1', 'L1', None)
        L1:             -> TACInstruction('LABEL', None, None, None, 'L1')
    """
    op: str                         # Operación (ADD, SUB, ASSIGN, etc.)
    arg1: Optional[str] = None      # Primer operando
    arg2: Optional[str] = None      # Segundo operando
    result: Optional[str] = None    # Resultado
    label: Optional[str] = None     # Etiqueta (para LABEL, GOTO, IF_FALSE)

    def __str__(self) -> str:
        """Representación legible de la instrucción TAC"""
        if self.op == 'LABEL':
            return f"{self.label}:"
        elif self.op == 'GOTO':
            return f"GOTO {self.arg1}"
        elif self.op == 'IF_FALSE':
            return f"IF_FALSE {self.arg1} GOTO {self.arg2}"
        elif self.op == 'ASSIGN':
            return f"{self.result} = {self.arg1}"
        elif self.op == 'RETURN':
            if self.arg1:
                return f"RETURN {self.arg1}"
            return "RETURN"
        elif self.op == 'PARAM':
            return f"PARAM {self.arg1}"
        elif self.op == 'CALL':
            if self.result:
                return f"{self.result} = CALL {self.arg1}, {self.arg2}"
            return f"CALL {self.arg1}, {self.arg2}"
        elif self.op == 'ARRAY_LOAD':
            return f"{self.result} = {self.arg1}[{self.arg2}]"
        elif self.op == 'ARRAY_STORE':
            return f"{self.result}[{self.arg1}] = {self.arg2}"
        elif self.op in ['ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'LT', 'GT', 'LE', 'GE', 'EQ', 'NE', 'AND', 'OR']:
            op_symbol = {
                'ADD': '+', 'SUB': '-', 'MUL': '*', 'DIV': '/', 'MOD': '%',
                'LT': '<', 'GT': '>', 'LE': '<=', 'GE': '>=', 'EQ': '==', 'NE': '!=',
                'AND': '&&', 'OR': '||'
            }.get(self.op, self.op)
            return f"{self.result} = {self.arg1} {op_symbol} {self.arg2}"
        elif self.op == 'NOT':
            return f"{self.result} = !{self.arg1}"
        elif self.op == 'NEG':
            return f"{self.result} = -{self.arg1}"
        else:
            return f"{self.op} {self.arg1} {self.arg2} {self.result}"


class TACGenerator:
    """
    Generador de código de tres direcciones (TAC) desde el AST.

    Convierte el AST validado en una secuencia de instrucciones TAC que:
    - Tienen como máximo 3 operandos por instrucción
    - Usan temporales para expresiones complejas
    - Facilitan optimizaciones posteriores
    - Permiten generación de múltiples backends (bytecode, C, LLVM)
    """

    def __init__(self):
        """Inicializa el generador TAC"""
        self.instructions: List[TACInstruction] = []
        self.temp_counter: int = 0
        self.label_counter: int = 0
        self.current_function: Optional[str] = None
        self.loop_stack: List[tuple] = []  # Stack de (start_label, end_label) para break/continue

    def new_temp(self) -> str:
        """Genera un nuevo nombre de variable temporal"""
        temp_name = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp_name

    def new_label(self) -> str:
        """Genera un nuevo nombre de etiqueta"""
        label_name = f"L{self.label_counter}"
        self.label_counter += 1
        return label_name

    def emit(self, op: str, arg1: Optional[str] = None, arg2: Optional[str] = None,
             result: Optional[str] = None, label: Optional[str] = None):
        """Emite una nueva instrucción TAC"""
        instruction = TACInstruction(op, arg1, arg2, result, label)
        self.instructions.append(instruction)

    def generate(self, ast: NodoAST) -> List[TACInstruction]:
        """
        Genera código TAC completo desde el AST.

        Args:
            ast: Nodo raíz del AST validado

        Returns:
            Lista de instrucciones TAC
        """
        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0

        # Generar código para el programa completo
        self._generate_program(ast)

        return self.instructions

    def _generate_program(self, nodo: NodoAST):
        """Genera código para el programa completo"""
        if nodo.tipo != TipoNodo.PROGRAMA:
            return

        # Generar código para cada declaración
        for hijo in nodo.hijos:
            if hijo.tipo == TipoNodo.FUNCION:
                self._generate_function(hijo)
            else:
                # Generar código para sentencias globales (variables, loops, etc.)
                self._generate_statement(hijo)

    def _generate_function(self, nodo: NodoAST):
        """Genera código para una declaración de función"""
        nombre_funcion = nodo.valor
        self.current_function = nombre_funcion

        # Emitir etiqueta de inicio de función
        self.emit('LABEL', label=f"func_{nombre_funcion}")

        # El cuerpo de la función está en el último hijo
        cuerpo = nodo.hijos[-1]

        # Generar código para el cuerpo
        self._generate_statement(cuerpo)

        # Si es función Unit y no tiene return explícito, agregar RETURN
        if nombre_funcion == "main" or not self._has_return(cuerpo):
            self.emit('RETURN')

        self.current_function = None

    def _has_return(self, nodo: NodoAST) -> bool:
        """Verifica si un nodo contiene una sentencia return"""
        if nodo.tipo == TipoNodo.RETURN:
            return True
        for hijo in nodo.hijos:
            if self._has_return(hijo):
                return True
        return False

    def _generate_statement(self, nodo: NodoAST):
        """Genera código para una sentencia"""
        if nodo.tipo == TipoNodo.BLOQUE:
            # Generar código para cada sentencia del bloque
            for hijo in nodo.hijos:
                self._generate_statement(hijo)

        elif nodo.tipo == TipoNodo.DECLARACION_VARIABLE:
            self._generate_var_declaration(nodo)

        elif nodo.tipo == TipoNodo.ASIGNACION:
            self._generate_assignment(nodo)

        elif nodo.tipo == TipoNodo.IF:
            self._generate_if(nodo)

        elif nodo.tipo == TipoNodo.WHILE:
            self._generate_while(nodo)

        elif nodo.tipo == TipoNodo.FOR:
            self._generate_for(nodo)

        elif nodo.tipo == TipoNodo.RETURN:
            self._generate_return(nodo)

        elif nodo.tipo == TipoNodo.BREAK:
            # Break salta al final del loop actual
            if self.loop_stack:
                _, end_label = self.loop_stack[-1]
                self.emit('GOTO', end_label)

        elif nodo.tipo == TipoNodo.CONTINUE:
            # Continue salta al inicio del loop actual
            if self.loop_stack:
                start_label, _ = self.loop_stack[-1]
                self.emit('GOTO', start_label)

        elif nodo.tipo == TipoNodo.LLAMADA_FUNCION:
            # Llamada a función como sentencia (sin usar resultado)
            self._generate_expression(nodo)

    def _generate_var_declaration(self, nodo: NodoAST):
        """Genera código para declaración de variable"""
        nombre_var = nodo.valor

        # Si tiene inicialización
        if len(nodo.hijos) > 0:
            expr_temp = self._generate_expression(nodo.hijos[0])
            self.emit('ASSIGN', expr_temp, None, nombre_var)

    def _generate_assignment(self, nodo: NodoAST):
        """Genera código para asignación"""
        # Verificar si es asignación a array
        hijo_izq = nodo.hijos[0]
        hijo_der = nodo.hijos[1]

        if hijo_izq.tipo == TipoNodo.EXPRESION_INDICE:
            # Asignación a elemento de array: arr[i] = expr
            # El nodo EXPRESION_INDICE tiene:
            # hijo_izq.hijos[0] = base (array variable)
            # hijo_izq.hijos[1] = índice
            base_expr = hijo_izq.hijos[0]
            indice_expr = hijo_izq.hijos[1]

            if base_expr.tipo == TipoNodo.EXPRESION_VARIABLE:
                nombre_array = base_expr.valor
            else:
                nombre_array = self._generate_expression(base_expr)

            indice_temp = self._generate_expression(indice_expr)
            valor_temp = self._generate_expression(hijo_der)
            self.emit('ARRAY_STORE', indice_temp, valor_temp, nombre_array)
        else:
            # Asignación simple: var = expr
            nombre_var = hijo_izq.valor
            expr_temp = self._generate_expression(hijo_der)
            self.emit('ASSIGN', expr_temp, None, nombre_var)

    def _generate_if(self, nodo: NodoAST):
        """Genera código para if/else"""
        condicion = nodo.hijos[0]
        bloque_then = nodo.hijos[1]
        bloque_else = nodo.hijos[2] if len(nodo.hijos) > 2 else None

        # Generar código para condición
        cond_temp = self._generate_expression(condicion)

        # Etiquetas
        else_label = self.new_label()
        end_label = self.new_label()

        # IF_FALSE cond GOTO else_label
        self.emit('IF_FALSE', cond_temp, else_label)

        # Código del bloque then
        self._generate_statement(bloque_then)

        if bloque_else:
            # GOTO end_label (saltar el else)
            self.emit('GOTO', end_label)

            # else_label:
            self.emit('LABEL', label=else_label)

            # Código del bloque else
            self._generate_statement(bloque_else)

            # end_label:
            self.emit('LABEL', label=end_label)
        else:
            # else_label: (mismo que end)
            self.emit('LABEL', label=else_label)

    def _generate_while(self, nodo: NodoAST):
        """Genera código para while"""
        condicion = nodo.hijos[0]
        cuerpo = nodo.hijos[1]

        # Etiquetas
        start_label = self.new_label()
        end_label = self.new_label()

        # Agregar al stack de loops
        self.loop_stack.append((start_label, end_label))

        # start_label:
        self.emit('LABEL', label=start_label)

        # Evaluar condición
        cond_temp = self._generate_expression(condicion)

        # IF_FALSE cond GOTO end_label
        self.emit('IF_FALSE', cond_temp, end_label)

        # Código del cuerpo
        self._generate_statement(cuerpo)

        # GOTO start_label
        self.emit('GOTO', start_label)

        # end_label:
        self.emit('LABEL', label=end_label)

        # Remover del stack
        self.loop_stack.pop()

    def _generate_for(self, nodo: NodoAST):
        """Genera código para for..in"""
        # for (var in inicio..fin) o for (var in inicio until fin)
        nombre_var = nodo.valor
        rango = nodo.hijos[0]
        cuerpo = nodo.hijos[1]

        # Obtener inicio y fin del rango
        inicio_temp = self._generate_expression(rango.hijos[0])
        fin_temp = self._generate_expression(rango.hijos[1])

        # Etiquetas
        start_label = self.new_label()
        end_label = self.new_label()

        # Agregar al stack de loops
        self.loop_stack.append((start_label, end_label))

        # var = inicio
        self.emit('ASSIGN', inicio_temp, None, nombre_var)

        # start_label:
        self.emit('LABEL', label=start_label)

        # Generar condición (var <= fin o var < fin)
        cond_temp = self.new_temp()
        if rango.valor == 'until':
            self.emit('LT', nombre_var, fin_temp, cond_temp)
        else:  # '..'
            self.emit('LE', nombre_var, fin_temp, cond_temp)

        # IF_FALSE cond GOTO end_label
        self.emit('IF_FALSE', cond_temp, end_label)

        # Código del cuerpo
        self._generate_statement(cuerpo)

        # var = var + 1
        temp_inc = self.new_temp()
        self.emit('ADD', nombre_var, '1', temp_inc)
        self.emit('ASSIGN', temp_inc, None, nombre_var)

        # GOTO start_label
        self.emit('GOTO', start_label)

        # end_label:
        self.emit('LABEL', label=end_label)

        # Remover del stack
        self.loop_stack.pop()

    def _generate_return(self, nodo: NodoAST):
        """Genera código para return"""
        if len(nodo.hijos) > 0:
            # return expr
            expr_temp = self._generate_expression(nodo.hijos[0])
            self.emit('RETURN', expr_temp)
        else:
            # return (sin valor)
            self.emit('RETURN')

    def _generate_expression(self, nodo: NodoAST) -> str:
        """
        Genera código para una expresión y retorna el temporal con el resultado.

        Returns:
            Nombre del temporal que contiene el resultado de la expresión
        """
        if nodo.tipo == TipoNodo.EXPRESION_LITERAL:
            # Literal: retornar el valor directamente
            return str(nodo.valor)

        elif nodo.tipo == TipoNodo.EXPRESION_VARIABLE:
            # Variable: retornar el nombre
            return nodo.valor

        elif nodo.tipo == TipoNodo.EXPRESION_BINARIA:
            return self._generate_binary_expression(nodo)

        elif nodo.tipo == TipoNodo.EXPRESION_UNARIA:
            return self._generate_unary_expression(nodo)

        elif nodo.tipo == TipoNodo.LLAMADA_FUNCION:
            return self._generate_function_call(nodo)

        elif nodo.tipo == TipoNodo.EXPRESION_INDICE:
            return self._generate_array_access(nodo)

        elif nodo.tipo == TipoNodo.EXPRESION_PUNTO:
            return self._generate_property_access(nodo)

        else:
            # Caso por defecto
            return "0"

    def _generate_binary_expression(self, nodo: NodoAST) -> str:
        """Genera código para expresión binaria"""
        operador = nodo.valor
        izq_temp = self._generate_expression(nodo.hijos[0])
        der_temp = self._generate_expression(nodo.hijos[1])

        result_temp = self.new_temp()

        # Mapear operador a operación TAC
        op_map = {
            '+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV', '%': 'MOD',
            '<': 'LT', '>': 'GT', '<=': 'LE', '>=': 'GE', '==': 'EQ', '!=': 'NE',
            '&&': 'AND', '||': 'OR'
        }

        tac_op = op_map.get(operador, operador)
        self.emit(tac_op, izq_temp, der_temp, result_temp)

        return result_temp

    def _generate_unary_expression(self, nodo: NodoAST) -> str:
        """Genera código para expresión unaria"""
        operador = nodo.valor
        operando_temp = self._generate_expression(nodo.hijos[0])

        result_temp = self.new_temp()

        if operador == '!':
            self.emit('NOT', operando_temp, None, result_temp)
        elif operador == '-':
            self.emit('NEG', operando_temp, None, result_temp)

        return result_temp

    def _generate_function_call(self, nodo: NodoAST) -> str:
        """Genera código para llamada a función"""
        nombre_funcion = nodo.valor

        # Generar código para argumentos (en orden inverso para stack)
        args_temps = []
        for arg in nodo.hijos:
            arg_temp = self._generate_expression(arg)
            args_temps.append(arg_temp)

        # Emitir PARAMs
        for arg_temp in args_temps:
            self.emit('PARAM', arg_temp)

        # Llamada a función
        result_temp = self.new_temp()
        num_args = len(args_temps)
        self.emit('CALL', nombre_funcion, str(num_args), result_temp)

        return result_temp

    def _generate_array_access(self, nodo: NodoAST) -> str:
        """Genera código para acceso a array"""
        # El nodo EXPRESION_INDICE tiene la estructura:
        # nodo.hijos[0] = expresión base (la variable array)
        # nodo.hijos[1] = expresión índice
        base_expr = nodo.hijos[0]
        indice_expr = nodo.hijos[1]

        # Generar código para la base (normalmente una variable)
        if base_expr.tipo == TipoNodo.EXPRESION_VARIABLE:
            nombre_array = base_expr.valor
        else:
            nombre_array = self._generate_expression(base_expr)

        # Generar código para el índice
        indice_temp = self._generate_expression(indice_expr)

        result_temp = self.new_temp()
        self.emit('ARRAY_LOAD', nombre_array, indice_temp, result_temp)

        return result_temp

    def _generate_property_access(self, nodo: NodoAST) -> str:
        """Genera código para acceso a propiedad (.size, .length)"""
        objeto_temp = self._generate_expression(nodo.hijos[0])
        propiedad = nodo.valor

        result_temp = self.new_temp()

        # Para .size y .length, generamos una operación especial
        # que será manejada por el backend específico
        if propiedad == 'size' or propiedad == 'length':
            self.emit('ASSIGN', f"{objeto_temp}.{propiedad}", None, result_temp)

        return result_temp

    def format_output(self) -> str:
        """
        Formatea las instrucciones TAC para mostrar en UI.

        Returns:
            String con código TAC formateado
        """
        lines = []
        for i, inst in enumerate(self.instructions):
            lines.append(f"{i:4d}:  {str(inst)}")
        return '\n'.join(lines)
