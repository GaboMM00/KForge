"""
Analizador Semántico para el compilador de Kotlin.
Verifica la correctitud semántica del AST generado por el parser.
"""

from typing import Optional
from core.utils import NodoAST, TipoNodo, TablaSimbolos, Simbolo, TipoDato
from core.errors import SemanticError, ErrorManager


class AnalizadorSemantico:
    """Analizador semántico que verifica la correctitud del AST."""

    def __init__(self, error_manager: ErrorManager = None):
        """
        Inicializa el analizador semántico.

        Args:
            error_manager: Gestor de errores para registrar errores semánticos.
        """
        self.error_manager = error_manager or ErrorManager()
        self.tabla_simbolos_global = TablaSimbolos()
        self.tabla_simbolos_actual = self.tabla_simbolos_global
        self.resultados = []
        self.dentro_de_loop = False  # Flag para validar break/continue

    def analizar(self, ast: NodoAST) -> list:
        """
        Analiza semánticamente el AST.

        Args:
            ast: Árbol sintáctico abstracto a analizar.

        Returns:
            Lista de resultados del análisis semántico.
        """
        self.resultados = []
        self.tabla_simbolos_actual = self.tabla_simbolos_global

        if ast:
            self.visitar(ast)

        return self.resultados

    def visitar(self, nodo: NodoAST):
        """
        Visita un nodo del AST y delega al método correspondiente.

        Args:
            nodo: Nodo a visitar.
        """
        if nodo.tipo == TipoNodo.PROGRAMA:
            self.visitar_programa(nodo)
        elif nodo.tipo == TipoNodo.DECLARACION_VARIABLE:
            self.visitar_declaracion_variable(nodo)
        elif nodo.tipo == TipoNodo.ASIGNACION:
            self.visitar_asignacion(nodo)
        elif nodo.tipo == TipoNodo.IF:
            self.visitar_if(nodo)
        elif nodo.tipo == TipoNodo.WHILE:
            self.visitar_while(nodo)
        elif nodo.tipo == TipoNodo.FOR:
            self.visitar_for(nodo)
        elif nodo.tipo == TipoNodo.BREAK:
            self.visitar_break(nodo)
        elif nodo.tipo == TipoNodo.CONTINUE:
            self.visitar_continue(nodo)
        elif nodo.tipo == TipoNodo.BLOQUE:
            self.visitar_bloque(nodo)
        elif nodo.tipo == TipoNodo.EXPRESION_BINARIA:
            return self.visitar_expresion_binaria(nodo)
        elif nodo.tipo == TipoNodo.EXPRESION_UNARIA:
            return self.visitar_expresion_unaria(nodo)
        elif nodo.tipo == TipoNodo.EXPRESION_LITERAL:
            return self.visitar_expresion_literal(nodo)
        elif nodo.tipo == TipoNodo.EXPRESION_VARIABLE:
            return self.visitar_expresion_variable(nodo)
        elif nodo.tipo == TipoNodo.EXPRESION_INDICE:
            return self.visitar_expresion_indice(nodo)

    def visitar_programa(self, nodo: NodoAST):
        """Visita el nodo programa."""
        for hijo in nodo.hijos:
            self.visitar(hijo)

        # Resumen de la tabla de símbolos
        self.resultados.append("=== Tabla de Símbolos ===")
        for nombre, simbolo in self.tabla_simbolos_global.simbolos.items():
            tipo_declaracion = "val" if simbolo.es_constante else "var"
            self.resultados.append(f"{tipo_declaracion} {nombre}: {simbolo.tipo.value}")

    def visitar_declaracion_variable(self, nodo: NodoAST):
        """Visita el nodo de declaración de variable."""
        nombre = nodo.valor
        tipo_str = nodo.metadata.get('tipo')
        es_constante = nodo.metadata.get('es_constante', False)

        # Verificar si ya existe en el scope actual
        if self.tabla_simbolos_actual.existe_en_scope_actual(nombre):
            error = SemanticError(
                f"Variable '{nombre}' ya declarada en este scope",
                nodo.linea,
                nodo.columna
            )
            self.error_manager.agregar_error(error)
            return

        # Crear símbolo
        tipo_dato = TipoDato.desde_string(tipo_str)
        simbolo = Simbolo(nombre, tipo_dato, es_constante, nodo.linea, nodo.columna)

        # Verificar tipo de la expresión de inicialización
        if nodo.hijos:
            tipo_expresion = self.visitar(nodo.hijos[0])
            if tipo_expresion and not self.tipos_compatibles(tipo_dato, tipo_expresion):
                error = SemanticError(
                    f"Tipo incompatible en la declaración de '{nombre}': "
                    f"esperado {tipo_dato.value}, encontrado {tipo_expresion.value}",
                    nodo.linea,
                    nodo.columna
                )
                self.error_manager.agregar_error(error)

        # Agregar a la tabla de símbolos
        self.tabla_simbolos_actual.declarar(simbolo)
        tipo_declaracion = "val" if es_constante else "var"
        self.resultados.append(f"Declaración: {tipo_declaracion} {nombre}: {tipo_dato.value}")

    def visitar_asignacion(self, nodo: NodoAST):
        """Visita el nodo de asignación (soporta variables y elementos de arreglos)."""
        nombre = nodo.valor

        if len(nodo.hijos) < 2:
            # Formato antiguo (compatible hacia atrás)
            simbolo = self.tabla_simbolos_actual.buscar(nombre)
            if not simbolo:
                error = SemanticError(
                    f"Variable '{nombre}' no declarada",
                    nodo.linea,
                    nodo.columna
                )
                self.error_manager.agregar_error(error)
                return

            if simbolo.es_constante:
                error = SemanticError(
                    f"No se puede reasignar a la constante '{nombre}' (declarada con 'val')",
                    nodo.linea,
                    nodo.columna
                )
                self.error_manager.agregar_error(error)
                return

            if nodo.hijos:
                tipo_expresion = self.visitar(nodo.hijos[0])
                if tipo_expresion and not self.tipos_compatibles(simbolo.tipo, tipo_expresion):
                    error = SemanticError(
                        f"Tipo incompatible en la asignación a '{nombre}': "
                        f"esperado {simbolo.tipo.value}, encontrado {tipo_expresion.value}",
                        nodo.linea,
                        nodo.columna
                    )
                    self.error_manager.agregar_error(error)

            self.resultados.append(f"Asignación válida: {nombre}")
        else:
            # Nuevo formato: hijos[0] = lado izquierdo, hijos[1] = valor
            nodo_izq = nodo.hijos[0]
            valor = nodo.hijos[1]

            # Si es un acceso a índice, validar el arreglo base
            if nodo_izq.tipo == TipoNodo.EXPRESION_INDICE:
                tipo_izq = self.visitar(nodo_izq)
            else:
                # Asignación a variable simple
                simbolo = self.tabla_simbolos_actual.buscar(nombre)
                if not simbolo:
                    error = SemanticError(
                        f"Variable '{nombre}' no declarada",
                        nodo.linea,
                        nodo.columna
                    )
                    self.error_manager.agregar_error(error)
                    return

                if simbolo.es_constante:
                    error = SemanticError(
                        f"No se puede reasignar a la constante '{nombre}' (declarada con 'val')",
                        nodo.linea,
                        nodo.columna
                    )
                    self.error_manager.agregar_error(error)
                    return

                tipo_izq = simbolo.tipo

            # Verificar tipo del valor
            tipo_valor = self.visitar(valor)
            if tipo_izq and tipo_valor and not self.tipos_compatibles(tipo_izq, tipo_valor):
                error = SemanticError(
                    f"Tipo incompatible en la asignación: "
                    f"esperado {tipo_izq.value}, encontrado {tipo_valor.value}",
                    nodo.linea,
                    nodo.columna
                )
                self.error_manager.agregar_error(error)

            self.resultados.append(f"Asignación válida: {nombre}")

    def visitar_if(self, nodo: NodoAST):
        """Visita el nodo if."""
        # Verificar condición
        if nodo.hijos:
            tipo_condicion = self.visitar(nodo.hijos[0])
            if tipo_condicion and tipo_condicion != TipoDato.BOOLEAN:
                error = SemanticError(
                    f"La condición del 'if' debe ser de tipo Boolean, encontrado {tipo_condicion.value}",
                    nodo.linea,
                    nodo.columna
                )
                self.error_manager.agregar_error(error)

            # Visitar bloque verdadero
            if len(nodo.hijos) > 1:
                self.visitar(nodo.hijos[1])

            # Visitar bloque falso (else)
            if len(nodo.hijos) > 2:
                self.visitar(nodo.hijos[2])

        self.resultados.append("Sentencia 'if' válida")

    def visitar_while(self, nodo: NodoAST):
        """Visita el nodo while."""
        # Verificar condición
        if nodo.hijos:
            tipo_condicion = self.visitar(nodo.hijos[0])
            if tipo_condicion and tipo_condicion != TipoDato.BOOLEAN:
                error = SemanticError(
                    f"La condición del 'while' debe ser de tipo Boolean, encontrado {tipo_condicion.value}",
                    nodo.linea,
                    nodo.columna
                )
                self.error_manager.agregar_error(error)

            # Marcar que estamos dentro de un loop
            estaba_en_loop = self.dentro_de_loop
            self.dentro_de_loop = True

            # Visitar cuerpo
            if len(nodo.hijos) > 1:
                self.visitar(nodo.hijos[1])

            # Restaurar estado
            self.dentro_de_loop = estaba_en_loop

        self.resultados.append("Sentencia 'while' válida")

    def visitar_for(self, nodo: NodoAST):
        """Visita el nodo for."""
        # Crear nuevo scope para la variable del for
        tabla_anterior = self.tabla_simbolos_actual
        self.tabla_simbolos_actual = TablaSimbolos(tabla_anterior)

        # Declarar variable del for (implícitamente de tipo Int)
        nombre_variable = nodo.valor
        simbolo = Simbolo(nombre_variable, TipoDato.INT, True, nodo.linea, nodo.columna)
        self.tabla_simbolos_actual.declarar(simbolo)

        # Verificar rango
        if nodo.hijos:
            tipo_rango = self.visitar(nodo.hijos[0])

            # Marcar que estamos dentro de un loop
            estaba_en_loop = self.dentro_de_loop
            self.dentro_de_loop = True

            # Visitar cuerpo
            if len(nodo.hijos) > 1:
                self.visitar(nodo.hijos[1])

            # Restaurar estado
            self.dentro_de_loop = estaba_en_loop

        # Restaurar scope anterior
        self.tabla_simbolos_actual = tabla_anterior
        self.resultados.append("Sentencia 'for' válida")

    def visitar_break(self, nodo: NodoAST):
        """Visita el nodo break."""
        if not self.dentro_de_loop:
            error = SemanticError(
                "'break' solo puede usarse dentro de un loop (while o for)",
                nodo.linea,
                nodo.columna
            )
            self.error_manager.agregar_error(error)
            return

        self.resultados.append("Sentencia 'break' válida")

    def visitar_continue(self, nodo: NodoAST):
        """Visita el nodo continue."""
        if not self.dentro_de_loop:
            error = SemanticError(
                "'continue' solo puede usarse dentro de un loop (while o for)",
                nodo.linea,
                nodo.columna
            )
            self.error_manager.agregar_error(error)
            return

        self.resultados.append("Sentencia 'continue' válida")

    def visitar_bloque(self, nodo: NodoAST):
        """Visita el nodo bloque."""
        # Crear nuevo scope
        tabla_anterior = self.tabla_simbolos_actual
        self.tabla_simbolos_actual = TablaSimbolos(tabla_anterior)

        # Visitar sentencias del bloque
        for hijo in nodo.hijos:
            self.visitar(hijo)

        # Restaurar scope anterior
        self.tabla_simbolos_actual = tabla_anterior

    def visitar_expresion_binaria(self, nodo: NodoAST) -> Optional[TipoDato]:
        """Visita el nodo de expresión binaria y retorna su tipo."""
        if len(nodo.hijos) < 2:
            return TipoDato.UNKNOWN

        tipo_izq = self.visitar(nodo.hijos[0])
        tipo_der = self.visitar(nodo.hijos[1])

        operador = nodo.valor

        # Operadores aritméticos
        if operador in ['+', '-', '*', '/', '%']:
            if tipo_izq in [TipoDato.INT, TipoDato.DOUBLE] and tipo_der in [TipoDato.INT, TipoDato.DOUBLE]:
                # Si alguno es Double, el resultado es Double
                if tipo_izq == TipoDato.DOUBLE or tipo_der == TipoDato.DOUBLE:
                    return TipoDato.DOUBLE
                return TipoDato.INT
            else:
                error = SemanticError(
                    f"Operador '{operador}' requiere operandos numéricos",
                    nodo.linea,
                    nodo.columna
                )
                self.error_manager.agregar_error(error)
                return TipoDato.UNKNOWN

        # Operadores de comparación
        elif operador in ['==', '!=', '<', '<=', '>', '>=']:
            return TipoDato.BOOLEAN

        # Operadores lógicos
        elif operador in ['&&', '||']:
            # Ambos operandos deben ser Boolean
            if tipo_izq != TipoDato.BOOLEAN:
                error = SemanticError(
                    f"Operador '{operador}' requiere operando izquierdo Boolean, encontrado {tipo_izq.value if tipo_izq else 'Unknown'}",
                    nodo.linea,
                    nodo.columna
                )
                self.error_manager.agregar_error(error)
                return TipoDato.UNKNOWN

            if tipo_der != TipoDato.BOOLEAN:
                error = SemanticError(
                    f"Operador '{operador}' requiere operando derecho Boolean, encontrado {tipo_der.value if tipo_der else 'Unknown'}",
                    nodo.linea,
                    nodo.columna
                )
                self.error_manager.agregar_error(error)
                return TipoDato.UNKNOWN

            return TipoDato.BOOLEAN

        # Operador de rango (.. y until)
        elif operador in ['..', 'until']:
            if tipo_izq == TipoDato.INT and tipo_der == TipoDato.INT:
                return TipoDato.INT  # Representa un rango
            else:
                error = SemanticError(
                    f"El operador de rango '{operador}' requiere operandos de tipo Int",
                    nodo.linea,
                    nodo.columna
                )
                self.error_manager.agregar_error(error)
                return TipoDato.UNKNOWN

        return TipoDato.UNKNOWN

    def visitar_expresion_unaria(self, nodo: NodoAST) -> Optional[TipoDato]:
        """Visita el nodo de expresión unaria y retorna su tipo."""
        if len(nodo.hijos) < 1:
            return TipoDato.UNKNOWN

        tipo_operando = self.visitar(nodo.hijos[0])
        operador = nodo.valor

        # Operador NOT (!)
        if operador == '!':
            if tipo_operando != TipoDato.BOOLEAN:
                error = SemanticError(
                    f"Operador '!' requiere operando de tipo Boolean, encontrado {tipo_operando.value if tipo_operando else 'Unknown'}",
                    nodo.linea,
                    nodo.columna
                )
                self.error_manager.agregar_error(error)
                return TipoDato.UNKNOWN
            return TipoDato.BOOLEAN

        # Operador MINUS unario (-)
        elif operador == '-':
            if tipo_operando not in [TipoDato.INT, TipoDato.DOUBLE]:
                error = SemanticError(
                    f"Operador unario '-' requiere operando numérico, encontrado {tipo_operando.value if tipo_operando else 'Unknown'}",
                    nodo.linea,
                    nodo.columna
                )
                self.error_manager.agregar_error(error)
                return TipoDato.UNKNOWN
            return tipo_operando

        return TipoDato.UNKNOWN

    def visitar_expresion_literal(self, nodo: NodoAST) -> TipoDato:
        """Visita el nodo de expresión literal y retorna su tipo."""
        valor = nodo.valor

        # IMPORTANTE: Verificar bool PRIMERO porque bool es subclase de int en Python
        if isinstance(valor, bool):
            return TipoDato.BOOLEAN
        elif isinstance(valor, int):
            return TipoDato.INT
        elif isinstance(valor, float):
            return TipoDato.DOUBLE
        elif isinstance(valor, str):
            return TipoDato.STRING

        return TipoDato.UNKNOWN

    def visitar_expresion_variable(self, nodo: NodoAST) -> Optional[TipoDato]:
        """Visita el nodo de expresión variable y retorna su tipo."""
        nombre = nodo.valor

        # Buscar en la tabla de símbolos
        simbolo = self.tabla_simbolos_actual.buscar(nombre)
        if not simbolo:
            error = SemanticError(
                f"Variable '{nombre}' no declarada",
                nodo.linea,
                nodo.columna
            )
            self.error_manager.agregar_error(error)
            return TipoDato.UNKNOWN

        return simbolo.tipo

    def visitar_expresion_indice(self, nodo: NodoAST) -> Optional[TipoDato]:
        """
        Visita el nodo de expresión de acceso a índice y retorna su tipo.
        Ejemplo: array[0], matriz[i][j]
        """
        if len(nodo.hijos) < 2:
            return TipoDato.UNKNOWN

        # Visitar el arreglo/lista (hijo 0)
        tipo_arreglo = self.visitar(nodo.hijos[0])

        # Visitar el índice (hijo 1)
        tipo_indice = self.visitar(nodo.hijos[1])

        # Validar que el índice sea de tipo Int
        if tipo_indice and tipo_indice != TipoDato.INT:
            error = SemanticError(
                f"El índice debe ser de tipo Int, encontrado {tipo_indice.value}",
                nodo.linea,
                nodo.columna
            )
            self.error_manager.agregar_error(error)

        # Por ahora, asumimos que el acceso a un arreglo retorna el mismo tipo
        # (esto es una simplificación, en un compilador completo necesitaríamos
        # un sistema de tipos más sofisticado para arreglos tipados)
        return tipo_arreglo

    def tipos_compatibles(self, tipo_esperado: TipoDato, tipo_actual: TipoDato) -> bool:
        """
        Verifica si dos tipos son compatibles.

        Args:
            tipo_esperado: Tipo esperado.
            tipo_actual: Tipo actual.

        Returns:
            True si son compatibles, False en caso contrario.
        """
        if tipo_esperado == tipo_actual:
            return True

        # Int puede convertirse a Double
        if tipo_esperado == TipoDato.DOUBLE and tipo_actual == TipoDato.INT:
            return True

        return False

    def obtener_resumen(self) -> str:
        """Genera un resumen del análisis semántico."""
        if not self.resultados:
            return "No se realizó análisis semántico."

        resumen = "=== Análisis Semántico ===\n"
        resumen += "\n".join(self.resultados)
        return resumen
