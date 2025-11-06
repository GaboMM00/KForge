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
        programa -> (declaracion_funcion | sentencia)*
        """
        nodo_programa = NodoAST(TipoNodo.PROGRAMA, "programa")

        while not self.verificar(TipoToken.EOF):
            try:
                # Verificar si es una declaración de función
                if self.verificar(TipoToken.FUN):
                    funcion = self.declaracion_funcion()
                    if funcion:
                        nodo_programa.agregar_hijo(funcion)
                else:
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
                  | break
                  | continue
                  | return
                  | llamada_funcion
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
        elif self.verificar(TipoToken.BREAK):
            return self.sentencia_break()
        elif self.verificar(TipoToken.CONTINUE):
            return self.sentencia_continue()
        elif self.verificar(TipoToken.RETURN):
            return self.sentencia_return()
        elif self.verificar(TipoToken.LBRACE):
            return self.bloque()
        elif self.verificar(TipoToken.IDENTIFIER):
            # Puede ser asignación o llamada a función
            # Mirar adelante para decidir
            if self.posicion + 1 < len(self.tokens) and self.tokens[self.posicion + 1].tipo == TipoToken.LPAREN:
                # Es una llamada a función
                expr = self.expresion()
                return expr
            else:
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
        asignacion -> IDENTIFIER [indice]* = expresion
        Soporta asignaciones a variables simples y elementos de arreglos
        """
        token_id = self.consumir(TipoToken.IDENTIFIER)

        # Construir expresión del lado izquierdo (puede tener índices)
        nodo_izq = NodoAST(TipoNodo.EXPRESION_VARIABLE, token_id.valor, linea=token_id.linea, columna=token_id.columna)

        # Verificar si hay acceso a índices (array[0][1] = valor)
        while self.verificar(TipoToken.LBRACKET):
            bracket_token = self.token_actual
            self.avanzar()
            indice = self.expresion()
            self.consumir(TipoToken.RBRACKET, "Se esperaba ']' después del índice")

            # Crear nodo de acceso a índice
            nodo_indice = NodoAST(
                TipoNodo.EXPRESION_INDICE,
                "[]",
                linea=bracket_token.linea,
                columna=bracket_token.columna
            )
            nodo_indice.agregar_hijo(nodo_izq)
            nodo_indice.agregar_hijo(indice)
            nodo_izq = nodo_indice

        self.consumir(TipoToken.ASSIGN, "Se esperaba '=' en la asignación")
        valor = self.expresion()

        nodo = NodoAST(
            TipoNodo.ASIGNACION,
            token_id.valor,
            linea=token_id.linea,
            columna=token_id.columna
        )
        nodo.agregar_hijo(nodo_izq)  # Lado izquierdo (puede ser variable o acceso a índice)
        nodo.agregar_hijo(valor)      # Lado derecho (valor a asignar)
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

    def sentencia_break(self) -> NodoAST:
        """
        sentencia_break -> break
        """
        token_break = self.consumir(TipoToken.BREAK)
        nodo = NodoAST(TipoNodo.BREAK, "break", linea=token_break.linea, columna=token_break.columna)
        return nodo

    def sentencia_continue(self) -> NodoAST:
        """
        sentencia_continue -> continue
        """
        token_continue = self.consumir(TipoToken.CONTINUE)
        nodo = NodoAST(TipoNodo.CONTINUE, "continue", linea=token_continue.linea, columna=token_continue.columna)
        return nodo

    def sentencia_return(self) -> NodoAST:
        """
        sentencia_return -> return expresion?
        """
        token_return = self.consumir(TipoToken.RETURN)

        # El return puede tener una expresión opcional
        valor_return = None
        if not self.verificar(TipoToken.RBRACE) and not self.verificar(TipoToken.EOF):
            # Intentar parsear expresión
            try:
                valor_return = self.expresion()
            except:
                pass  # Return sin valor

        nodo = NodoAST(TipoNodo.RETURN, "return", linea=token_return.linea, columna=token_return.columna)
        if valor_return:
            nodo.agregar_hijo(valor_return)
        return nodo

    def declaracion_funcion(self) -> NodoAST:
        """
        declaracion_funcion -> fun IDENTIFIER ( parametros? ) : TIPO bloque
        parametros -> IDENTIFIER : TIPO (, IDENTIFIER : TIPO)*
        """
        token_fun = self.consumir(TipoToken.FUN)
        token_nombre = self.consumir(TipoToken.IDENTIFIER, "Se esperaba nombre de función")

        self.consumir(TipoToken.LPAREN, "Se esperaba '(' después del nombre de función")

        # Parsear parámetros
        parametros = []
        if not self.verificar(TipoToken.RPAREN):
            # Primer parámetro
            param_nombre = self.consumir(TipoToken.IDENTIFIER, "Se esperaba nombre de parámetro")
            self.consumir(TipoToken.COLON, "Se esperaba ':' después del nombre del parámetro")
            param_tipo = self.tipo()
            parametros.append({
                'nombre': param_nombre.valor,
                'tipo': param_tipo,
                'linea': param_nombre.linea,
                'columna': param_nombre.columna
            })

            # Parámetros adicionales
            while self.verificar(TipoToken.COMMA):
                self.avanzar()  # Consumir coma
                param_nombre = self.consumir(TipoToken.IDENTIFIER, "Se esperaba nombre de parámetro")
                self.consumir(TipoToken.COLON, "Se esperaba ':' después del nombre del parámetro")
                param_tipo = self.tipo()
                parametros.append({
                    'nombre': param_nombre.valor,
                    'tipo': param_tipo,
                    'linea': param_nombre.linea,
                    'columna': param_nombre.columna
                })

        self.consumir(TipoToken.RPAREN, "Se esperaba ')' después de los parámetros")
        self.consumir(TipoToken.COLON, "Se esperaba ':' antes del tipo de retorno")

        tipo_retorno = self.tipo()

        # Parsear cuerpo de la función
        cuerpo = self.bloque()

        # Crear nodo de función
        nodo = NodoAST(
            TipoNodo.FUNCION,
            token_nombre.valor,
            linea=token_fun.linea,
            columna=token_fun.columna
        )
        nodo.metadata = {
            'parametros': parametros,
            'tipo_retorno': tipo_retorno
        }
        nodo.agregar_hijo(cuerpo)

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
        tipo -> Int | Double | String | Boolean | IntArray | DoubleArray | Unit
        """
        if self.verificar(TipoToken.IDENTIFIER):
            # Puede ser IntArray, DoubleArray, Unit, etc.
            tipo_valor = self.token_actual.valor
            if tipo_valor in ['IntArray', 'DoubleArray', 'Unit']:
                self.avanzar()
                return tipo_valor

        if self.verificar(TipoToken.INT_TYPE):
            tipo_valor = self.token_actual.valor
            self.avanzar()
            return tipo_valor if tipo_valor in ['IntArray', 'DoubleArray'] else "Int"
        elif self.verificar(TipoToken.DOUBLE_TYPE):
            tipo_valor = self.token_actual.valor
            self.avanzar()
            return tipo_valor if tipo_valor == 'DoubleArray' else "Double"
        elif self.verificar(TipoToken.STRING_TYPE):
            self.avanzar()
            return "String"
        elif self.verificar(TipoToken.BOOLEAN_TYPE):
            tipo_valor = self.token_actual.valor
            self.avanzar()
            return tipo_valor if tipo_valor == 'Unit' else "Boolean"
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
        expresion -> expresion_or
        Jerarquía: OR -> AND -> comparación -> suma -> multiplicación -> unaria -> primaria
        """
        return self.expresion_or()

    def expresion_or(self) -> NodoAST:
        """
        expresion_or -> expresion_and (|| expresion_and)*
        OR lógico tiene la menor precedencia
        """
        nodo = self.expresion_and()

        while self.verificar(TipoToken.OR):
            operador = self.token_actual
            self.avanzar()
            derecha = self.expresion_and()

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

    def expresion_and(self) -> NodoAST:
        """
        expresion_and -> expresion_comparacion (&& expresion_comparacion)*
        AND lógico tiene mayor precedencia que OR
        """
        nodo = self.expresion_comparacion()

        while self.verificar(TipoToken.AND):
            operador = self.token_actual
            self.avanzar()
            derecha = self.expresion_comparacion()

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
        expresion_multiplicacion -> expresion_unaria ((*|/|%) expresion_unaria)*
        """
        nodo = self.expresion_unaria()

        while self.token_actual.tipo in [TipoToken.MULTIPLY, TipoToken.DIVIDE, TipoToken.MODULO]:
            operador = self.token_actual
            self.avanzar()
            derecha = self.expresion_unaria()

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

    def expresion_unaria(self) -> NodoAST:
        """
        expresion_unaria -> (! | -) expresion_unaria | expresion_primaria
        Soporta operadores unarios: ! (NOT lógico) y - (negativo)
        """
        # Verificar si hay operador unario
        if self.token_actual.tipo in [TipoToken.NOT, TipoToken.MINUS]:
            operador = self.token_actual
            self.avanzar()
            # Recursivo para soportar múltiples operadores unarios: !!x, -(-x)
            operando = self.expresion_unaria()

            nodo = NodoAST(
                TipoNodo.EXPRESION_UNARIA,
                operador.valor,
                linea=operador.linea,
                columna=operador.columna
            )
            nodo.agregar_hijo(operando)
            return nodo

        # Si no hay operador unario, parsear expresión primaria
        return self.expresion_primaria()

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

        # Identificador (puede ser variable o llamada a función)
        elif self.verificar(TipoToken.IDENTIFIER):
            token = self.token_actual
            self.avanzar()

            # Verificar si es una llamada a función
            if self.verificar(TipoToken.LPAREN):
                # Es una llamada a función
                self.avanzar()  # Consumir (

                # Parsear argumentos
                argumentos = []
                if not self.verificar(TipoToken.RPAREN):
                    # Primer argumento
                    argumentos.append(self.expresion())

                    # Argumentos adicionales
                    while self.verificar(TipoToken.COMMA):
                        self.avanzar()  # Consumir coma
                        argumentos.append(self.expresion())

                self.consumir(TipoToken.RPAREN, "Se esperaba ')' después de los argumentos")

                # Crear nodo de llamada a función
                nodo = NodoAST(TipoNodo.LLAMADA_FUNCION, token.valor, linea=token.linea, columna=token.columna)
                for arg in argumentos:
                    nodo.agregar_hijo(arg)
            else:
                # Es una variable
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

        # Verificar si hay acceso a índices o propiedades (soporta n dimensiones y encadenamiento)
        # Ejemplos: array[0], array[0].size, obj.property, obj.property[0]
        while self.verificar(TipoToken.LBRACKET) or self.verificar(TipoToken.DOT):
            if self.verificar(TipoToken.LBRACKET):
                # Acceso a índice: array[0]
                bracket_token = self.token_actual
                self.avanzar()
                # Parsear la expresión del índice
                indice = self.expresion()
                self.consumir(TipoToken.RBRACKET, "Se esperaba ']' después del índice")

                # Crear nodo de acceso a índice
                nodo_indice = NodoAST(
                    TipoNodo.EXPRESION_INDICE,
                    "[]",
                    linea=bracket_token.linea,
                    columna=bracket_token.columna
                )
                nodo_indice.agregar_hijo(nodo)      # El arreglo/lista
                nodo_indice.agregar_hijo(indice)    # El índice
                nodo = nodo_indice                  # Actualizar para soportar múltiples []

            elif self.verificar(TipoToken.DOT):
                # Acceso a propiedad: obj.property
                dot_token = self.token_actual
                self.avanzar()  # Consumir el punto

                # El siguiente token debe ser un identificador (nombre de propiedad)
                propiedad = self.consumir(TipoToken.IDENTIFIER, "Se esperaba nombre de propiedad después de '.'")

                # Crear nodo de acceso a propiedad
                nodo_punto = NodoAST(
                    TipoNodo.EXPRESION_PUNTO,
                    propiedad.valor,  # El nombre de la propiedad
                    linea=dot_token.linea,
                    columna=dot_token.columna
                )
                nodo_punto.agregar_hijo(nodo)  # El objeto base
                nodo = nodo_punto              # Actualizar para soportar encadenamiento

        # Verificar si es un rango (.. o until después del valor)
        if self.verificar(TipoToken.RANGE) or self.verificar(TipoToken.UNTIL):
            token_range = self.token_actual
            operador = ".." if self.verificar(TipoToken.RANGE) else "until"
            self.avanzar()
            # Parsear el valor final del rango (solo literal o identificador simple o expresión)
            fin = None
            if self.verificar(TipoToken.INT_LITERAL):
                token = self.token_actual
                self.avanzar()
                fin = NodoAST(TipoNodo.EXPRESION_LITERAL, token.valor, linea=token.linea, columna=token.columna)
            elif self.verificar(TipoToken.IDENTIFIER):
                token = self.token_actual
                self.avanzar()
                # Puede seguir con operaciones: n - 1, o con propiedades: arr.size
                fin = NodoAST(TipoNodo.EXPRESION_VARIABLE, token.valor, linea=token.linea, columna=token.columna)

                # Verificar si hay acceso a propiedades (.size, .length)
                if self.verificar(TipoToken.DOT):
                    dot_token = self.token_actual
                    self.avanzar()  # Consumir el punto
                    propiedad = self.consumir(TipoToken.IDENTIFIER, "Se esperaba nombre de propiedad después de '.'")
                    nodo_punto = NodoAST(
                        TipoNodo.EXPRESION_PUNTO,
                        propiedad.valor,
                        linea=dot_token.linea,
                        columna=dot_token.columna
                    )
                    nodo_punto.agregar_hijo(fin)
                    fin = nodo_punto

                # Verificar si hay operadores después (para soportar "n - 1" o "arr.size - 1")
                if self.token_actual.tipo in [TipoToken.PLUS, TipoToken.MINUS, TipoToken.MULTIPLY, TipoToken.DIVIDE]:
                    # Convertir a expresión completa retrocediendo
                    self.posicion -= 1
                    self.token_actual = self.tokens[self.posicion]
                    fin = self.expresion_suma()
            elif self.verificar(TipoToken.LPAREN):
                # Expresión entre paréntesis
                fin = self.expresion_primaria()
            else:
                error = SyntaxError(
                    f"Se esperaba un valor después de '{operador}'",
                    self.token_actual.linea,
                    self.token_actual.columna
                )
                self.error_manager.agregar_error(error)
                raise error

            # Crear nodo de rango
            # Nota: "until" se marca en metadata para que el semántico lo maneje diferente
            nodo_rango = NodoAST(
                TipoNodo.EXPRESION_BINARIA,
                operador,
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
