"""
Módulo de utilidades generales del compilador.
Contiene estructuras de datos y funciones auxiliares.
"""

from dataclasses import dataclass
from typing import Any, List, Optional
from enum import Enum, auto


class TipoToken(Enum):
    """Enumeración de tipos de tokens."""
    # Palabras clave
    VAR = auto()
    VAL = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    UNTIL = auto()
    BREAK = auto()
    CONTINUE = auto()
    FUN = auto()
    RETURN = auto()

    # Tipos de datos
    INT_TYPE = auto()
    DOUBLE_TYPE = auto()
    STRING_TYPE = auto()
    BOOLEAN_TYPE = auto()

    # Literales
    INT_LITERAL = auto()
    DOUBLE_LITERAL = auto()
    STRING_LITERAL = auto()
    BOOLEAN_LITERAL = auto()

    # Identificadores
    IDENTIFIER = auto()

    # Operadores
    PLUS = auto()          # +
    MINUS = auto()         # -
    MULTIPLY = auto()      # *
    DIVIDE = auto()        # /
    MODULO = auto()        # %
    ASSIGN = auto()        # =
    EQUAL = auto()         # ==
    NOT_EQUAL = auto()     # !=
    LESS_THAN = auto()     # <
    LESS_EQUAL = auto()    # <=
    GREATER_THAN = auto()  # >
    GREATER_EQUAL = auto() # >=
    NOT = auto()           # ! (negación lógica)
    AND = auto()           # && (AND lógico)
    OR = auto()            # || (OR lógico)

    # Delimitadores
    LPAREN = auto()        # (
    RPAREN = auto()        # )
    LBRACE = auto()        # {
    RBRACE = auto()        # }
    LBRACKET = auto()      # [
    RBRACKET = auto()      # ]
    COMMA = auto()         # ,
    COLON = auto()         # :
    SEMICOLON = auto()     # ;
    DOT = auto()           # .
    RANGE = auto()         # ..

    # Especiales
    NEWLINE = auto()
    EOF = auto()
    COMMENT = auto()


@dataclass
class Token:
    """Representa un token del lenguaje."""
    tipo: TipoToken
    valor: Any
    linea: int
    columna: int

    def __repr__(self):
        return f"Token({self.tipo.name}, {repr(self.valor)}, {self.linea}:{self.columna})"


class TipoNodo(Enum):
    """Enumeración de tipos de nodos del AST."""
    PROGRAMA = auto()
    DECLARACION_VARIABLE = auto()
    ASIGNACION = auto()
    EXPRESION_BINARIA = auto()
    EXPRESION_UNARIA = auto()      # Para operadores unarios como ! (NOT)
    EXPRESION_LITERAL = auto()
    EXPRESION_VARIABLE = auto()
    EXPRESION_INDICE = auto()      # Para acceso a arreglos/listas con []
    EXPRESION_PUNTO = auto()       # Para acceso a propiedades con . (obj.property)
    BLOQUE = auto()
    IF = auto()
    WHILE = auto()
    FOR = auto()
    BREAK = auto()
    CONTINUE = auto()
    FUNCION = auto()
    LLAMADA_FUNCION = auto()
    RETURN = auto()


@dataclass
class NodoAST:
    """Nodo base del árbol sintáctico abstracto."""
    tipo: TipoNodo
    valor: Any = None
    hijos: List['NodoAST'] = None
    linea: int = None
    columna: int = None
    metadata: dict = None

    def __post_init__(self):
        if self.hijos is None:
            self.hijos = []
        if self.metadata is None:
            self.metadata = {}

    def agregar_hijo(self, hijo: 'NodoAST'):
        """Agrega un hijo al nodo."""
        self.hijos.append(hijo)

    def __repr__(self, nivel=0):
        indent = "  " * nivel
        resultado = f"{indent}{self.tipo.name}"
        if self.valor is not None:
            resultado += f": {self.valor}"
        if self.metadata:
            resultado += f" {self.metadata}"
        resultado += "\n"
        for hijo in self.hijos:
            if isinstance(hijo, NodoAST):
                resultado += hijo.__repr__(nivel + 1)
            else:
                resultado += f"{indent}  {hijo}\n"
        return resultado


class TipoDato(Enum):
    """Enumeración de tipos de datos."""
    INT = "Int"
    DOUBLE = "Double"
    STRING = "String"
    BOOLEAN = "Boolean"
    VOID = "Unit"
    ARRAY_INT = "IntArray"
    ARRAY_DOUBLE = "DoubleArray"
    ARRAY_STRING = "Array<String>"
    UNKNOWN = "Unknown"

    @staticmethod
    def desde_string(tipo_str: str) -> 'TipoDato':
        """Convierte un string a TipoDato."""
        mapeo = {
            "Int": TipoDato.INT,
            "Double": TipoDato.DOUBLE,
            "String": TipoDato.STRING,
            "Boolean": TipoDato.BOOLEAN,
            "Unit": TipoDato.VOID,
            "IntArray": TipoDato.ARRAY_INT,
            "DoubleArray": TipoDato.ARRAY_DOUBLE,
            "Array<String>": TipoDato.ARRAY_STRING
        }
        return mapeo.get(tipo_str, TipoDato.UNKNOWN)


@dataclass
class Parametro:
    """Representa un parámetro de función."""
    nombre: str
    tipo: TipoDato
    linea: int = None
    columna: int = None

    def __repr__(self):
        return f"{self.nombre}: {self.tipo.value}"


@dataclass
class FuncionInfo:
    """Información sobre una función declarada."""
    nombre: str
    parametros: List[Parametro]
    tipo_retorno: TipoDato
    cuerpo: 'NodoAST' = None
    linea: int = None
    columna: int = None
    es_builtin: bool = False

    def __repr__(self):
        params_str = ", ".join(str(p) for p in self.parametros)
        return f"fun {self.nombre}({params_str}): {self.tipo_retorno.value}"


@dataclass
class Simbolo:
    """Representa un símbolo en la tabla de símbolos."""
    nombre: str
    tipo: TipoDato
    es_constante: bool  # True para val, False para var
    linea: int
    columna: int
    valor: Any = None
    inicializada: bool = False  # True si la variable tiene un valor asignado

    def __repr__(self):
        return f"Simbolo({self.nombre}, {self.tipo.value}, {'val' if self.es_constante else 'var'})"


class TablaSimbolos:
    """Tabla de símbolos para el análisis semántico."""

    def __init__(self, padre: Optional['TablaSimbolos'] = None):
        self.simbolos = {}
        self.padre = padre

    def declarar(self, simbolo: Simbolo):
        """Declara un nuevo símbolo en la tabla."""
        if simbolo.nombre in self.simbolos:
            return False
        self.simbolos[simbolo.nombre] = simbolo
        return True

    def buscar(self, nombre: str) -> Optional[Simbolo]:
        """Busca un símbolo en la tabla o en las tablas padre."""
        if nombre in self.simbolos:
            return self.simbolos[nombre]
        if self.padre:
            return self.padre.buscar(nombre)
        return None

    def existe(self, nombre: str) -> bool:
        """Verifica si un símbolo existe en el scope actual o padres."""
        return self.buscar(nombre) is not None

    def existe_en_scope_actual(self, nombre: str) -> bool:
        """Verifica si un símbolo existe solo en el scope actual."""
        return nombre in self.simbolos
