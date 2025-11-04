"""
Controlador del compilador de Kotlin.
Coordina todas las fases del análisis: léxico, sintáctico, semántico y generación de código.
"""

from typing import Dict, Any
from core.lexer import Lexer
from core.parser import Parser
from core.semantic import AnalizadorSemantico
from core.codegen import CodeGenerator
from core.errors import ErrorManager


class CompiladorController:
    """
    Controlador principal del compilador.

    Coordina todas las fases del análisis y proporciona una interfaz
    unificada para ejecutar el compilador.
    """

    def __init__(self):
        """Inicializa el controlador del compilador."""
        self.error_manager = ErrorManager()
        self.lexer = None
        self.parser = None
        self.semantic_analyzer = None
        self.code_generator = None

        # Resultados de cada fase
        self.tokens = []
        self.ast = None
        self.resultados_semanticos = []

    def ejecutar(self, codigo: str) -> Dict[str, Any]:
        """
        Ejecuta todas las fases del compilador sobre el código fuente.

        Args:
            codigo: Código fuente a compilar.

        Returns:
            Diccionario con los resultados de cada fase:
            {
                "tokens": [...],
                "arbol": ...,
                "semantico": [...],
                "codigo_intermedio": "...",
                "errores": [...],
                "exito": bool
            }
        """
        # Limpiar estado previo
        self.limpiar()

        # Verificar que el código no esté vacío
        if not codigo or codigo.strip() == "":
            return {
                "tokens": [],
                "arbol": None,
                "semantico": [],
                "codigo_intermedio": "",
                "errores": ["El código fuente está vacío"],
                "exito": False
            }

        # Fase 1: Análisis Léxico
        try:
            self.lexer = Lexer(self.error_manager)
            self.tokens = self.lexer.tokenizar(codigo)
        except Exception as e:
            self.error_manager.agregar_error(Exception(f"Error en análisis léxico: {str(e)}"))

        # Si hay errores léxicos, detener
        if self.error_manager.tiene_errores():
            return self._construir_resultado()

        # Fase 2: Análisis Sintáctico
        try:
            self.parser = Parser(self.tokens, self.error_manager)
            self.ast = self.parser.parsear()
        except Exception as e:
            self.error_manager.agregar_error(Exception(f"Error en análisis sintáctico: {str(e)}"))

        # Si hay errores sintácticos, detener
        if self.error_manager.tiene_errores() or self.ast is None:
            return self._construir_resultado()

        # Fase 3: Análisis Semántico
        try:
            self.semantic_analyzer = AnalizadorSemantico(self.error_manager)
            self.resultados_semanticos = self.semantic_analyzer.analizar(self.ast)
        except Exception as e:
            self.error_manager.agregar_error(Exception(f"Error en análisis semántico: {str(e)}"))

        # Retornar resultados
        return self._construir_resultado()

    def ejecutar_lexico(self, codigo: str) -> Dict[str, Any]:
        """
        Ejecuta solo el análisis léxico.

        Args:
            codigo: Código fuente a analizar.

        Returns:
            Diccionario con tokens y errores léxicos.
        """
        self.limpiar()

        if not codigo or codigo.strip() == "":
            return {
                "tokens": [],
                "errores": ["El código fuente está vacío"],
                "exito": False,
                "resumen": ""
            }

        try:
            self.lexer = Lexer(self.error_manager)
            self.tokens = self.lexer.tokenizar(codigo)
            resumen = self.lexer.obtener_resumen()
        except Exception as e:
            self.error_manager.agregar_error(Exception(f"Error en análisis léxico: {str(e)}"))
            resumen = ""

        return {
            "tokens": self.tokens,
            "errores": [str(e) for e in self.error_manager.obtener_errores()],
            "exito": not self.error_manager.tiene_errores(),
            "resumen": resumen
        }

    def ejecutar_sintactico(self, codigo: str) -> Dict[str, Any]:
        """
        Ejecuta análisis léxico y sintáctico.

        Args:
            codigo: Código fuente a analizar.

        Returns:
            Diccionario con tokens, AST y errores.
        """
        self.limpiar()

        # Primero ejecutar análisis léxico
        resultado_lexico = self.ejecutar_lexico(codigo)
        if not resultado_lexico["exito"]:
            return {
                "tokens": resultado_lexico["tokens"],
                "arbol": None,
                "errores": resultado_lexico["errores"],
                "exito": False,
                "resumen": ""
            }

        # Ejecutar análisis sintáctico
        try:
            self.parser = Parser(self.tokens, self.error_manager)
            self.ast = self.parser.parsear()
            resumen = self._generar_resumen_ast()
        except Exception as e:
            self.error_manager.agregar_error(Exception(f"Error en análisis sintáctico: {str(e)}"))
            resumen = ""

        return {
            "tokens": self.tokens,
            "arbol": self.ast,
            "errores": [str(e) for e in self.error_manager.obtener_errores()],
            "exito": not self.error_manager.tiene_errores() and self.ast is not None,
            "resumen": resumen
        }

    def ejecutar_semantico(self, codigo: str) -> Dict[str, Any]:
        """
        Ejecuta análisis léxico, sintáctico y semántico.

        Args:
            codigo: Código fuente a analizar.

        Returns:
            Diccionario con resultados completos del análisis.
        """
        return self.ejecutar(codigo)

    def ejecutar_codegen(self, codigo: str) -> Dict[str, Any]:
        """
        Ejecuta todas las fases incluyendo generación de código.

        Args:
            codigo: Código fuente a compilar.

        Returns:
            Diccionario con todos los resultados incluyendo código intermedio.
        """
        # Ejecutar análisis completo
        resultado = self.ejecutar(codigo)

        # Si no hay errores, generar código intermedio
        if resultado["exito"]:
            try:
                self.code_generator = CodeGenerator()
                codigo_intermedio = self.code_generator.generar(self.ast)
                resultado["codigo_intermedio"] = codigo_intermedio
            except Exception as e:
                resultado["errores"].append(f"Error en generación de código: {str(e)}")
                resultado["exito"] = False

        return resultado

    def _construir_resultado(self) -> Dict[str, Any]:
        """Construye el diccionario de resultados."""
        return {
            "tokens": self.tokens,
            "arbol": self.ast,
            "semantico": self.resultados_semanticos,
            "codigo_intermedio": "",
            "errores": [str(e) for e in self.error_manager.obtener_errores()],
            "exito": not self.error_manager.tiene_errores()
        }

    def _generar_resumen_ast(self) -> str:
        """Genera un resumen del AST."""
        if not self.ast:
            return "No se genero un arbol sintactico."

        resumen = "=== Arbol Sintactico Abstracto (AST) ===\n\n"
        resumen += str(self.ast)
        return resumen

    def limpiar(self):
        """Limpia el estado del controlador."""
        self.error_manager.limpiar()
        self.tokens = []
        self.ast = None
        self.resultados_semanticos = []
        self.lexer = None
        self.parser = None
        self.semantic_analyzer = None
        self.code_generator = None

    def obtener_resumen_completo(self) -> str:
        """
        Genera un resumen completo de todas las fases.

        Returns:
            String con el resumen completo del análisis.
        """
        resumen = "=" * 70 + "\n"
        resumen += "RESUMEN DE COMPILACION\n"
        resumen += "=" * 70 + "\n\n"

        # Resumen léxico
        if self.lexer:
            resumen += self.lexer.obtener_resumen() + "\n\n"

        # Resumen sintáctico
        if self.ast:
            resumen += self._generar_resumen_ast() + "\n\n"

        # Resumen semántico
        if self.semantic_analyzer:
            resumen += self.semantic_analyzer.obtener_resumen() + "\n\n"

        # Errores
        if self.error_manager.tiene_errores():
            resumen += "=" * 70 + "\n"
            resumen += self.error_manager.obtener_resumen()
        else:
            resumen += "=" * 70 + "\n"
            resumen += "[OK] COMPILACION EXITOSA - Sin errores detectados\n"
            resumen += "=" * 70 + "\n"

        return resumen
