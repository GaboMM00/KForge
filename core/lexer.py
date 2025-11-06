"""
Analizador Léxico (Lexer) para el compilador de Kotlin.
Convierte el código fuente en una secuencia de tokens.
"""

import re
from typing import List
from core.utils import Token, TipoToken
from core.errors import LexicalError, ErrorManager


class Lexer:
    """Analizador léxico que tokeniza el código fuente de Kotlin."""

    # Palabras clave del lenguaje
    PALABRAS_CLAVE = {
        'var': TipoToken.VAR,
        'val': TipoToken.VAL,
        'if': TipoToken.IF,
        'else': TipoToken.ELSE,
        'while': TipoToken.WHILE,
        'for': TipoToken.FOR,
        'in': TipoToken.IN,
        'until': TipoToken.UNTIL,
        'break': TipoToken.BREAK,
        'continue': TipoToken.CONTINUE,
        'fun': TipoToken.FUN,
        'return': TipoToken.RETURN,
        'Int': TipoToken.INT_TYPE,
        'Double': TipoToken.DOUBLE_TYPE,
        'String': TipoToken.STRING_TYPE,
        'Boolean': TipoToken.BOOLEAN_TYPE,
        'IntArray': TipoToken.INT_TYPE,  # IntArray se maneja como tipo
        'DoubleArray': TipoToken.DOUBLE_TYPE,  # DoubleArray se maneja como tipo
        'Unit': TipoToken.BOOLEAN_TYPE,  # Unit para funciones void
        'true': TipoToken.BOOLEAN_LITERAL,
        'false': TipoToken.BOOLEAN_LITERAL,
    }

    # Especificación de tokens mediante expresiones regulares
    ESPECIFICACION_TOKENS = [
        # Comentarios (se ignoran)
        ('COMMENT', r'//.*'),

        # Literales
        ('DOUBLE_LITERAL', r'\d+\.\d+'),
        ('INT_LITERAL', r'\d+'),
        ('STRING_LITERAL', r'"([^"\\]|\\.)*"'),

        # Operadores lógicos (antes que operadores simples)
        ('AND', r'&&'),
        ('OR', r'\|\|'),

        # Operadores de comparación (antes que operadores simples)
        ('EQUAL', r'=='),
        ('NOT_EQUAL', r'!='),
        ('LESS_EQUAL', r'<='),
        ('GREATER_EQUAL', r'>='),
        ('LESS_THAN', r'<'),
        ('GREATER_THAN', r'>'),

        # Operadores aritméticos y asignación
        ('PLUS', r'\+'),
        ('MINUS', r'-'),
        ('MULTIPLY', r'\*'),
        ('DIVIDE', r'/'),
        ('MODULO', r'%'),
        ('ASSIGN', r'='),
        ('NOT', r'!'),

        # Rango
        ('RANGE', r'\.\.'),

        # Delimitadores
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}'),
        ('LBRACKET', r'\['),
        ('RBRACKET', r'\]'),
        ('COMMA', r','),
        ('COLON', r':'),
        ('SEMICOLON', r';'),
        ('DOT', r'\.'),

        # Identificadores y palabras clave
        ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),

        # Espacios en blanco (se ignoran)
        ('WHITESPACE', r'[ \t]+'),

        # Nuevas líneas
        ('NEWLINE', r'\n'),

        # Caracteres no reconocidos
        ('MISMATCH', r'.'),
    ]

    def __init__(self, error_manager: ErrorManager = None):
        """
        Inicializa el analizador léxico.

        Args:
            error_manager: Gestor de errores para registrar errores léxicos.
        """
        self.error_manager = error_manager or ErrorManager()
        self.tokens = []
        self.codigo = ""
        self.linea_actual = 1
        self.columna_actual = 1

        # Compila las expresiones regulares
        partes = []
        for nombre, patron in self.ESPECIFICACION_TOKENS:
            partes.append(f'(?P<{nombre}>{patron})')
        self.patron_maestro = re.compile('|'.join(partes))

    def tokenizar(self, codigo: str) -> List[Token]:
        """
        Tokeniza el código fuente.

        Args:
            codigo: Código fuente a analizar.

        Returns:
            Lista de tokens generados.
        """
        self.codigo = codigo
        self.tokens = []
        self.linea_actual = 1
        self.columna_actual = 1

        # Itera sobre todas las coincidencias
        for coincidencia in self.patron_maestro.finditer(codigo):
            tipo = coincidencia.lastgroup
            valor = coincidencia.group()
            columna = coincidencia.start() - codigo.rfind('\n', 0, coincidencia.start())

            # Procesa el token según su tipo
            if tipo == 'COMMENT' or tipo == 'WHITESPACE':
                # Ignorar comentarios y espacios en blanco
                continue

            elif tipo == 'NEWLINE':
                # Incrementar contador de líneas
                self.linea_actual += 1
                self.columna_actual = 1
                continue

            elif tipo == 'MISMATCH':
                # Carácter no reconocido
                error = LexicalError(
                    f"Carácter no reconocido: '{valor}'",
                    self.linea_actual,
                    columna
                )
                self.error_manager.agregar_error(error)
                continue

            elif tipo == 'IDENTIFIER':
                # Verificar si es palabra clave
                if valor in self.PALABRAS_CLAVE:
                    tipo_token = self.PALABRAS_CLAVE[valor]
                else:
                    tipo_token = TipoToken.IDENTIFIER
                token = Token(tipo_token, valor, self.linea_actual, columna)

            elif tipo == 'INT_LITERAL':
                token = Token(TipoToken.INT_LITERAL, int(valor), self.linea_actual, columna)

            elif tipo == 'DOUBLE_LITERAL':
                token = Token(TipoToken.DOUBLE_LITERAL, float(valor), self.linea_actual, columna)

            elif tipo == 'STRING_LITERAL':
                # Remover comillas
                valor_string = valor[1:-1]
                token = Token(TipoToken.STRING_LITERAL, valor_string, self.linea_actual, columna)

            else:
                # Otros tokens
                tipo_token = TipoToken[tipo]
                token = Token(tipo_token, valor, self.linea_actual, columna)

            self.tokens.append(token)

        # Agregar token EOF al final
        token_eof = Token(TipoToken.EOF, None, self.linea_actual, self.columna_actual)
        self.tokens.append(token_eof)

        return self.tokens

    def obtener_tokens(self) -> List[Token]:
        """Obtiene la lista de tokens generados."""
        return self.tokens

    def obtener_resumen(self) -> str:
        """Genera un resumen de los tokens encontrados."""
        if not self.tokens:
            return "No se han generado tokens."

        resumen = f"Total de tokens: {len(self.tokens) - 1}\n\n"  # -1 por EOF
        resumen += "Tokens generados:\n"
        resumen += "-" * 60 + "\n"

        for i, token in enumerate(self.tokens[:-1], 1):  # Excluir EOF del resumen
            resumen += f"{i:3d}. {token.tipo.name:20s} | {str(token.valor):20s} | Línea {token.linea:3d}, Col {token.columna:3d}\n"

        return resumen
