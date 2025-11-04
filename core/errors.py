"""
Módulo de manejo centralizado de errores del compilador.
Define las excepciones personalizadas para cada fase del análisis.
"""

class CompiladorError(Exception):
    """Clase base para todos los errores del compilador."""
    def __init__(self, mensaje: str, linea: int = None, columna: int = None):
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna
        super().__init__(self.formato_mensaje())

    def formato_mensaje(self) -> str:
        """Formatea el mensaje de error con información de posición."""
        if self.linea is not None and self.columna is not None:
            return f"[Línea {self.linea}, Columna {self.columna}] {self.mensaje}"
        elif self.linea is not None:
            return f"[Línea {self.linea}] {self.mensaje}"
        return self.mensaje


class LexicalError(CompiladorError):
    """Error en la fase de análisis léxico."""
    def formato_mensaje(self) -> str:
        base = super().formato_mensaje()
        return f"Error Léxico: {base}"


class SyntaxError(CompiladorError):
    """Error en la fase de análisis sintáctico."""
    def formato_mensaje(self) -> str:
        base = super().formato_mensaje()
        return f"Error Sintáctico: {base}"


class SemanticError(CompiladorError):
    """Error en la fase de análisis semántico."""
    def formato_mensaje(self) -> str:
        base = super().formato_mensaje()
        return f"Error Semántico: {base}"


class ErrorManager:
    """Gestor centralizado de errores del compilador."""

    def __init__(self):
        self.errores = []

    def agregar_error(self, error: CompiladorError):
        """Agrega un error a la lista de errores."""
        self.errores.append(error)

    def tiene_errores(self) -> bool:
        """Verifica si hay errores registrados."""
        return len(self.errores) > 0

    def obtener_errores(self) -> list:
        """Obtiene la lista de errores."""
        return self.errores

    def limpiar(self):
        """Limpia la lista de errores."""
        self.errores.clear()

    def obtener_resumen(self) -> str:
        """Obtiene un resumen de todos los errores."""
        if not self.tiene_errores():
            return "No se encontraron errores."

        resumen = f"Se encontraron {len(self.errores)} error(es):\n"
        for i, error in enumerate(self.errores, 1):
            resumen += f"{i}. {str(error)}\n"
        return resumen
