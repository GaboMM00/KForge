"""
Módulo core del compilador de Kotlin.
Contiene todas las fases del análisis: léxico, sintáctico, semántico y generación de código.
"""

from core.lexer import Lexer
from core.parser import Parser
from core.semantic import AnalizadorSemantico
from core.codegen import CodeGenerator
from core.controller import CompiladorController
from core.errors import (
    CompiladorError,
    LexicalError,
    SyntaxError,
    SemanticError,
    ErrorManager
)
from core.utils import (
    Token,
    TipoToken,
    NodoAST,
    TipoNodo,
    TipoDato,
    Simbolo,
    TablaSimbolos
)

__all__ = [
    'Lexer',
    'Parser',
    'AnalizadorSemantico',
    'CodeGenerator',
    'CompiladorController',
    'CompiladorError',
    'LexicalError',
    'SyntaxError',
    'SemanticError',
    'ErrorManager',
    'Token',
    'TipoToken',
    'NodoAST',
    'TipoNodo',
    'TipoDato',
    'Simbolo',
    'TablaSimbolos'
]
