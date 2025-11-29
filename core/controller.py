"""
Controlador del compilador de Kotlin.
Coordina todas las fases del análisis: léxico, sintáctico, semántico y generación de código.
"""

from typing import Dict, Any, List
from core.lexer import Lexer
from core.parser import Parser
from core.semantic import AnalizadorSemantico
# from core.codegen import CodeGenerator  # Obsoleto - ver tac.py y bytecode.py
from core.tac import TACGenerator, TACInstruction
from core.bytecode import BytecodeGenerator, BytecodeInstruction
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
        self.tac_generator = None  # Generador de código TAC (v1.1)
        self.bytecode_generator = None  # Generador de bytecode (v1.1)

        # Resultados de cada fase
        self.tokens = []
        self.ast = None
        self.resultados_semanticos = []
        self.tac_instructions: List[TACInstruction] = []  # Código TAC generado
        self.bytecode_instructions: List[BytecodeInstruction] = []  # Bytecode generado

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

        # Fase 4: Generación de Código TAC (v1.1)
        # Solo si no hay errores semánticos
        if not self.error_manager.tiene_errores():
            try:
                self.tac_generator = TACGenerator()
                self.tac_instructions = self.tac_generator.generate(self.ast)
            except Exception as e:
                self.error_manager.agregar_error(Exception(f"Error en generación de TAC: {str(e)}"))

        # Fase 5: Generación de Bytecode (v1.1)
        # Solo si TAC fue generado exitosamente
        if not self.error_manager.tiene_errores() and self.tac_instructions:
            try:
                self.bytecode_generator = BytecodeGenerator()
                self.bytecode_instructions = self.bytecode_generator.generate(self.tac_instructions)
            except Exception as e:
                self.error_manager.agregar_error(Exception(f"Error en generación de bytecode: {str(e)}"))

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

        # Nota: La generación de código intermedio se hace en ejecutar_semantico()
        # que usa TAC y Bytecode generators (v1.1)

        return resultado

    def _construir_resultado(self) -> Dict[str, Any]:
        """Construye el diccionario de resultados."""
        # Formatear código TAC si existe
        tac_code = ""
        if self.tac_generator and self.tac_instructions:
            tac_code = self.tac_generator.format_output()

        # Formatear bytecode si existe
        bytecode_assembly = ""
        if self.bytecode_generator and self.bytecode_instructions:
            bytecode_assembly = self.bytecode_generator.format_output(show_comments=True)

        return {
            "tokens": self.tokens,
            "arbol": self.ast,
            "semantico": self.resultados_semanticos,
            "codigo_intermedio": tac_code,      # Código TAC formateado
            "bytecode": bytecode_assembly,       # Bytecode assembly formateado
            "tac": self.tac_instructions,        # Lista de instrucciones TAC
            "bytecode_instructions": self.bytecode_instructions,  # Lista de instrucciones bytecode
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
        self.tac_instructions = []
        self.bytecode_instructions = []
        self.lexer = None
        self.parser = None
        self.semantic_analyzer = None
        self.code_generator = None
        self.tac_generator = None
        self.bytecode_generator = None

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

    def ejecutar_jvm(self, codigo: str, class_name: str = "Main",
                     output_path: str = None, java_version: int = 6) -> Dict[str, Any]:
        """
        Ejecuta compilacion completa a JVM bytecode (.class file).

        Este metodo ejecuta todas las fases del frontend (lexico, sintactico,
        semantico, TAC) y luego genera un archivo .class ejecutable.

        Args:
            codigo: Codigo fuente Kotlin
            class_name: Nombre de la clase a generar
            output_path: Ruta donde guardar el .class (None = no guardar)
            java_version: Version de Java target (6, 7, 8)

        Returns:
            Diccionario con resultados:
            {
                "exito": bool,
                "errores": List[str],
                "bytecode_jvm": bytes,
                "output_path": str,
                "class_info": dict,
                "tac_instructions": List[TACInstruction],
                "resumen": str
            }
        """
        from core.jvm import compile_kotlin_to_jvm

        # Ejecutar frontend completo
        resultado = self.ejecutar(codigo)

        if not resultado["exito"]:
            return {
                "exito": False,
                "errores": resultado["errores"],
                "bytecode_jvm": None,
                "output_path": None,
                "class_info": None,
                "tac_instructions": [],
                "resumen": "Error en frontend - no se puede generar bytecode JVM"
            }

        # Verificar que se generaron instrucciones TAC
        if not self.tac_instructions:
            return {
                "exito": False,
                "errores": ["No se generaron instrucciones TAC"],
                "bytecode_jvm": None,
                "output_path": None,
                "class_info": None,
                "tac_instructions": [],
                "resumen": "Error: No hay codigo intermedio TAC para compilar"
            }

        # Compilar TAC a JVM bytecode
        try:
            bytecode_jvm = compile_kotlin_to_jvm(
                self.tac_instructions,
                class_name=class_name,
                output_path=output_path,
                source_file=f"{class_name}.kt",
                java_version=java_version,
                add_debug_info=True
            )

            # Generar resumen
            resumen = self._generar_resumen_jvm(class_name, bytecode_jvm, output_path)

            return {
                "exito": True,
                "errores": [],
                "bytecode_jvm": bytecode_jvm,
                "output_path": output_path,
                "class_info": {
                    "class_name": class_name,
                    "java_version": java_version,
                    "bytecode_size": len(bytecode_jvm),
                    "tac_instructions": len(self.tac_instructions)
                },
                "tac_instructions": self.tac_instructions,
                "resumen": resumen
            }

        except Exception as e:
            return {
                "exito": False,
                "errores": [f"Error en compilacion JVM: {str(e)}"],
                "bytecode_jvm": None,
                "output_path": None,
                "class_info": None,
                "tac_instructions": self.tac_instructions,
                "resumen": f"Error durante la generacion de bytecode JVM: {str(e)}"
            }

    def _generar_resumen_jvm(self, class_name: str, bytecode: bytes, output_path: str = None) -> str:
        """
        Genera resumen de la compilacion JVM.

        Args:
            class_name: Nombre de la clase generada
            bytecode: Bytecode JVM generado
            output_path: Ruta del archivo .class (si se guardo)

        Returns:
            String con resumen de la compilacion JVM
        """
        resumen = "=" * 70 + "\n"
        resumen += "COMPILACION JVM EXITOSA\n"
        resumen += "=" * 70 + "\n\n"

        resumen += f"Clase generada: {class_name}\n"
        resumen += f"Bytecode size: {len(bytecode)} bytes\n"
        resumen += f"Instrucciones TAC: {len(self.tac_instructions)}\n"

        if output_path:
            resumen += f"Archivo .class: {output_path}\n"
            resumen += "\nPara ejecutar:\n"
            resumen += f"  java {class_name}\n"
        else:
            resumen += "\n(Archivo .class no guardado - solo en memoria)\n"

        resumen += "\n" + "=" * 70 + "\n"
        return resumen
