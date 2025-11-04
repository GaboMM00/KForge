"""
Analizador Sintáctico (Parser) para el compilador de Kotlin.
Genera un árbol sintáctico abstracto (AST) a partir de los tokens.
"""

from typing import List, Optional
from core.utils import Token, TipoToken, NodoAST, TipoNodo
from core.errors import SyntaxError, ErrorManager


class Parser:
    """Analizador sintáctico que genera un AST a partir de tokens."""

    def __init__(self, tokens: List[Token], error_manager: ErrorManager = None):
        """
        Inicializa el analizador sintáctico.

        Args:
            tokens: Lista de tokens del análisis léxico.
            error_manager: Gestor de errores para registrar errores sintácticos.
        """
        self.tokens = tokens
        self.error_manager = error_manager or ErrorManager()
        self.posicion = 0
        self.token_actual = self.tokens[0] if tokens else None

    def avanzar(self):
        """Avanza al siguiente token."""
        if self.posicion < len(self.tokens) - 1:
            self.posicion += 1
            self.token_actual = self.tokens[self.posicion]

    def retroceder(self):
        """Retrocede al token anterior."""
        if self.posicion > 0:
            self.posicion -= 1
            self.token_actual = self.tokens[self.posicion]

    def verificar(self, tipo_token: TipoToken) -> bool:
        """Verifica si el token actual es del tipo especificado."""
        return self.token_actual and self.token_actual.tipo == tipo_token

    def consumir(self, tipo_token: TipoToken, mensaje_error: str = None) -> Token:
        """
        Consume un token del tipo especificado o lanza un error.

        Args:
            tipo_token: Tipo de token esperado.
            mensaje_error: Mensaje de error personalizado.

        Returns:
            El token consumido.
        """
        if not self.verificar(tipo_token):
            if mensaje_error is None:
                mensaje_error = f"Se esperaba {tipo_token.name}, se encontró {self.token_actual.tipo.name}"
            error = SyntaxError(
                mensaje_error,
                self.token_actual.linea if self.token_actual else None,
                self.token_actual.columna if self.token_actual else None
            )
            self.error_manager.agregar_error(error)
            raise error

        token = self.token_actual
        self.avanzar()
        return token

    def parsear(self) -> Optional[NodoAST]:
        """
        Inicia el análisis sintáctico y genera el AST.

        Returns:
            Nodo raíz del AST o None si hay errores.
        """
        try:
            return self.programa()
        except SyntaxError:
            return None

    # ========== Reglas Gramaticales ==========

    def programa(self) -> NodoAST:
        """
        programa -> sentencia*
        """
        nodo_programa = NodoAST(TipoNodo.PROGRAMA, "programa")

        while not self.verificar(TipoToken.EOF):
            try:
                sentencia = self.sentencia()
                if sentencia:
                    nodo_programa.agregar_hijo(sentencia)
            except SyntaxError as e:
                # Recuperación de errores: avanzar hasta el siguiente punto seguro
                self.sincronizar()

        return nodo_programa

    def sentencia(self) -> Optional[NodoAST]:
        """
        sentencia -> declaracion_variable
                  | asignacion
                  | sentencia_if
                  | sentencia_while
                  | sentencia_for
                  | bloque
        """
        if self.verificar(TipoToken.VAR) or self.verificar(TipoToken.VAL):
            return self.declaracion_variable()
        elif self.verificar(TipoToken.IF):
            return self.sentencia_if()
        elif self.verificar(TipoToken.WHILE):
            return self.sentencia_while()
        elif self.verificar(TipoToken.FOR):
            return self.sentencia_for()
        elif self.verificar(TipoToken.LBRACE):
            return self.bloque()
        elif self.verificar(TipoToken.IDENTIFIER):
            return self.asignacion()
        else:
            error = SyntaxError(
                f"Sentencia inesperada: {self.token_actual.tipo.name}",
                self.token_actual.linea,
                self.token_actual.columna
            )
            self.error_manager.agregar_error(error)
            raise error

    def declaracion_variable(self) -> NodoAST:
        """
        declaracion_variable -> (var|val) IDENTIFIER : TIPO = expresion
        """
        # Guardar si es var o val
        token_tipo_declaracion = self.token_actual
        es_constante = self.verificar(TipoToken.VAL)
        self.avanzar()  # Consumir var o val

        # Identificador
        token_id = self.consumir(TipoToken.IDENTIFIER, "Se esperaba un identificador")

        # Dos puntos
        self.consumir(TipoToken.COLON, "Se esperaba ':' después del identificador")

        # Tipo
        tipo_variable = self.tipo()

        # Asignación opcional
        valor = None
        if self.verificar(TipoToken.ASSIGN):
            self.avanzar()  # Consumir =
            valor = self.expresion()

        # Crear nodo
        nodo = NodoAST(
            TipoNodo.DECLARACION_VARIABLE,
            token_id.valor,
            linea=token_id.linea,
            columna=token_id.columna
        )
        nodo.metadata = {
            'tipo': tipo_variable,
            'es_constante': es_constante
        }
        if valor:
            nodo.agregar_hijo(valor)

        return nodo

    def asignacion(self) -> NodoAST:
        """
        asignacion -> IDENTIFIER = expresion
        """
        token_id = self.consumir(TipoToken.IDENTIFIER)
        self.consumir(TipoToken.ASSIGN, "Se esperaba '=' en la asignación")
        valor = self.expresion()

        nodo = NodoAST(
            TipoNodo.ASIGNACION,
            token_id.valor,
            linea=token_id.linea,
            columna=token_id.columna
        )
        nodo.agregar_hijo(valor)
        return nodo

    def sentencia_if(self) -> NodoAST:
        """
        sentencia_if -> if ( expresion ) bloque (else bloque)?
        """
        token_if = self.consumir(TipoToken.IF)
        self.consumir(TipoToken.LPAREN, "Se esperaba '(' después de 'if'")
        condicion = self.expresion()
        self.consumir(TipoToken.RPAREN, "Se esperaba ')' después de la condición")

        bloque_verdadero = self.bloque()

        bloque_falso = None
        if self.verificar(TipoToken.ELSE):
            self.avanzar()  # Consumir else
            bloque_falso = self.bloque()

        nodo = NodoAST(TipoNodo.IF, "if", linea=token_if.linea, columna=token_if.columna)
        nodo.agregar_hijo(condicion)
        nodo.agregar_hijo(bloque_verdadero)
        if bloque_falso:
            nodo.agregar_hijo(bloque_falso)

        return nodo

    def sentencia_while(self) -> NodoAST:
        """
        sentencia_while -> while ( expresion ) bloque
        """
        token_while = self.consumir(TipoToken.WHILE)
        self.consumir(TipoToken.LPAREN, "Se esperaba '(' después de 'while'")
        condicion = self.expresion()
        self.consumir(TipoToken.RPAREN, "Se esperaba ')' después de la condición")

        bloque_cuerpo = self.bloque()

        nodo = NodoAST(TipoNodo.WHILE, "while", linea=token_while.linea, columna=token_while.columna)
        nodo.agregar_hijo(condicion)
        nodo.agregar_hijo(bloque_cuerpo)

        return nodo

    def sentencia_for(self) -> NodoAST:
        """
        sentencia_for -> for ( IDENTIFIER in expresion ) bloque
        """
        token_for = self.consumir(TipoToken.FOR)
        self.consumir(TipoToken.LPAREN, "Se esperaba '(' después de 'for'")

        token_variable = self.consumir(TipoToken.IDENTIFIER, "Se esperaba identificador en el 'for'")
        self.consumir(TipoToken.IN, "Se esperaba 'in' en el 'for'")

        rango = self.expresion()
        self.consumir(TipoToken.RPAREN, "Se esperaba ')' después del rango")

        bloque_cuerpo = self.bloque()

        nodo = NodoAST(TipoNodo.FOR, token_variable.valor, linea=token_for.linea, columna=token_for.columna)
        nodo.agregar_hijo(rango)
        nodo.agregar_hijo(bloque_cuerpo)

        return nodo

    def bloque(self) -> NodoAST:
        """
        bloque -> { sentencia* }
        """
        token_lbrace = self.consumir(TipoToken.LBRACE, "Se esperaba '{'")
        nodo_bloque = NodoAST(TipoNodo.BLOQUE, "bloque", linea=token_lbrace.linea, columna=token_lbrace.columna)

        while not self.verificar(TipoToken.RBRACE) and not self.verificar(TipoToken.EOF):
            try:
                sentencia = self.sentencia()
                if sentencia:
                    nodo_bloque.agregar_hijo(sentencia)
            except SyntaxError:
                self.sincronizar()

        self.consumir(TipoToken.RBRACE, "Se esperaba '}'")
        return nodo_bloque

    def tipo(self) -> str:
        """
        tipo -> Int | Double | String | Boolean
        """
        if self.verificar(TipoToken.INT_TYPE):
            self.avanzar()
            return "Int"
        elif self.verificar(TipoToken.DOUBLE_TYPE):
            self.avanzar()
            return "Double"
        elif self.verificar(TipoToken.STRING_TYPE):
            self.avanzar()
            return "String"
        elif self.verificar(TipoToken.BOOLEAN_TYPE):
            self.avanzar()
            return "Boolean"
        else:
            error = SyntaxError(
                f"Tipo de dato no válido: {self.token_actual.valor}",
                self.token_actual.linea,
                self.token_actual.columna
            )
            self.error_manager.agregar_error(error)
            raise error

    def expresion(self) -> NodoAST:
        """
        expresion -> termino_logico ((==|!=|<|<=|>|>=) termino_logico)*
        """
        return self.expresion_comparacion()

    def expresion_comparacion(self) -> NodoAST:
        """
        expresion_comparacion -> expresion_suma ((==|!=|<|<=|>|>=) expresion_suma)*
        """
        nodo = self.expresion_suma()

        while self.token_actual.tipo in [TipoToken.EQUAL, TipoToken.NOT_EQUAL,
                                          TipoToken.LESS_THAN, TipoToken.LESS_EQUAL,
                                          TipoToken.GREATER_THAN, TipoToken.GREATER_EQUAL]:
            operador = self.token_actual
            self.avanzar()
            derecha = self.expresion_suma()

            nodo_nuevo = NodoAST(
                TipoNodo.EXPRESION_BINARIA,
                operador.valor,
                linea=operador.linea,
                columna=operador.columna
            )
            nodo_nuevo.agregar_hijo(nodo)
            nodo_nuevo.agregar_hijo(derecha)
            nodo = nodo_nuevo

        return nodo

    def expresion_suma(self) -> NodoAST:
        """
        expresion_suma -> expresion_multiplicacion ((+|-) expresion_multiplicacion)*
        """
        nodo = self.expresion_multiplicacion()

        while self.token_actual.tipo in [TipoToken.PLUS, TipoToken.MINUS]:
            operador = self.token_actual
            self.avanzar()
            derecha = self.expresion_multiplicacion()

            nodo_nuevo = NodoAST(
                TipoNodo.EXPRESION_BINARIA,
                operador.valor,
                linea=operador.linea,
                columna=operador.columna
            )
            nodo_nuevo.agregar_hijo(nodo)
            nodo_nuevo.agregar_hijo(derecha)
            nodo = nodo_nuevo

        return nodo

    def expresion_multiplicacion(self) -> NodoAST:
        """
        expresion_multiplicacion -> expresion_primaria ((*|/|%) expresion_primaria)*
        """
        nodo = self.expresion_primaria()

        while self.token_actual.tipo in [TipoToken.MULTIPLY, TipoToken.DIVIDE, TipoToken.MODULO]:
            operador = self.token_actual
            self.avanzar()
            derecha = self.expresion_primaria()

            nodo_nuevo = NodoAST(
                TipoNodo.EXPRESION_BINARIA,
                operador.valor,
                linea=operador.linea,
                columna=operador.columna
            )
            nodo_nuevo.agregar_hijo(nodo)
            nodo_nuevo.agregar_hijo(derecha)
            nodo = nodo_nuevo

        return nodo

    def expresion_primaria(self) -> NodoAST:
        """
        expresion_primaria -> literal | IDENTIFIER | ( expresion )
        Maneja también rangos después de parsear el valor inicial
        """
        nodo = None

        # Literales
        if self.verificar(TipoToken.INT_LITERAL):
            token = self.token_actual
            self.avanzar()
            nodo = NodoAST(TipoNodo.EXPRESION_LITERAL, token.valor, linea=token.linea, columna=token.columna)

        elif self.verificar(TipoToken.DOUBLE_LITERAL):
            token = self.token_actual
            self.avanzar()
            nodo = NodoAST(TipoNodo.EXPRESION_LITERAL, token.valor, linea=token.linea, columna=token.columna)

        elif self.verificar(TipoToken.STRING_LITERAL):
            token = self.token_actual
            self.avanzar()
            nodo = NodoAST(TipoNodo.EXPRESION_LITERAL, token.valor, linea=token.linea, columna=token.columna)

        elif self.verificar(TipoToken.BOOLEAN_LITERAL):
            token = self.token_actual
            self.avanzar()
            valor_bool = token.valor == 'true'
            nodo = NodoAST(TipoNodo.EXPRESION_LITERAL, valor_bool, linea=token.linea, columna=token.columna)

        # Identificador
        elif self.verificar(TipoToken.IDENTIFIER):
            token = self.token_actual
            self.avanzar()
            nodo = NodoAST(TipoNodo.EXPRESION_VARIABLE, token.valor, linea=token.linea, columna=token.columna)

        # Expresión entre paréntesis
        elif self.verificar(TipoToken.LPAREN):
            self.avanzar()
            nodo = self.expresion()
            self.consumir(TipoToken.RPAREN, "Se esperaba ')' después de la expresión")

        else:
            error = SyntaxError(
                f"Expresión no válida: {self.token_actual.tipo.name}",
                self.token_actual.linea,
                self.token_actual.columna
            )
            self.error_manager.agregar_error(error)
            raise error

        # Verificar si es un rango (.. después del valor)
        if self.verificar(TipoToken.RANGE):
            token_range = self.token_actual
            self.avanzar()
            # Parsear el valor final del rango (solo literal o identificador simple)
            fin = None
            if self.verificar(TipoToken.INT_LITERAL):
                token = self.token_actual
                self.avanzar()
                fin = NodoAST(TipoNodo.EXPRESION_LITERAL, token.valor, linea=token.linea, columna=token.columna)
            elif self.verificar(TipoToken.IDENTIFIER):
                token = self.token_actual
                self.avanzar()
                fin = NodoAST(TipoNodo.EXPRESION_VARIABLE, token.valor, linea=token.linea, columna=token.columna)
            else:
                error = SyntaxError(
                    f"Se esperaba un valor después de '..'",
                    self.token_actual.linea,
                    self.token_actual.columna
                )
                self.error_manager.agregar_error(error)
                raise error

            # Crear nodo de rango
            nodo_rango = NodoAST(
                TipoNodo.EXPRESION_BINARIA,
                "..",
                linea=token_range.linea,
                columna=token_range.columna
            )
            nodo_rango.agregar_hijo(nodo)
            nodo_rango.agregar_hijo(fin)
            return nodo_rango

        return nodo

    def sincronizar(self):
        """
        Sincronización para recuperación de errores.
        Avanza hasta encontrar un punto seguro para continuar.
        """
        self.avanzar()

        while not self.verificar(TipoToken.EOF):
            # Puntos de sincronización: palabras clave que inician sentencias
            if self.token_actual.tipo in [TipoToken.VAR, TipoToken.VAL, TipoToken.IF,
                                           TipoToken.WHILE, TipoToken.FOR, TipoToken.RBRACE]:
                return

            self.avanzar()
