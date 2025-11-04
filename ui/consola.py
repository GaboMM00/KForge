"""
Consola de salida para mostrar resultados del compilador.
"""

import tkinter as tk
from tkinter import scrolledtext, font


class ConsolaSalida(tk.Frame):
    """
    Widget de consola para mostrar resultados de la compilación.

    Características:
    - Fondo oscuro (negro)
    - Texto claro (blanco/verde)
    - Soporte para colores según tipo de mensaje
    - Auto-scroll
    """

    def __init__(self, parent, *args, **kwargs):
        """
        Inicializa la consola de salida.

        Args:
            parent: Widget padre.
        """
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Configurar fuente monoespaciada
        self.fuente = font.Font(family="Consolas", size=10)

        # Crear área de texto con scroll
        self.texto = scrolledtext.ScrolledText(
            self,
            font=self.fuente,
            wrap=tk.WORD,
            bg="#1e1e1e",  # Fondo oscuro tipo VS Code
            fg="#d4d4d4",  # Texto gris claro
            insertbackground="#ffffff",
            selectbackground="#264f78",
            selectforeground="#ffffff",
            relief=tk.FLAT,
            borderwidth=0,
            state=tk.DISABLED  # Solo lectura por defecto
        )
        self.texto.pack(fill=tk.BOTH, expand=True)

        # Configurar tags para colores
        self._configurar_tags()

    def _configurar_tags(self):
        """Configura tags para diferentes tipos de mensajes."""
        # Éxito (verde)
        self.texto.tag_config("exito", foreground="#4ec9b0")

        # Error (rojo)
        self.texto.tag_config("error", foreground="#f48771")

        # Advertencia (amarillo)
        self.texto.tag_config("advertencia", foreground="#dcdcaa")

        # Info (azul claro)
        self.texto.tag_config("info", foreground="#569cd6")

        # Título (blanco brillante)
        self.texto.tag_config("titulo", foreground="#ffffff", font=(self.fuente.actual()["family"],
                                                                     self.fuente.actual()["size"], "bold"))

        # Subtítulo (cyan)
        self.texto.tag_config("subtitulo", foreground="#4fc1ff")

        # Comentario (gris)
        self.texto.tag_config("comentario", foreground="#6a9955")

        # Normal (gris claro - por defecto)
        self.texto.tag_config("normal", foreground="#d4d4d4")

    def escribir(self, mensaje: str, tipo: str = "normal"):
        """
        Escribe un mensaje en la consola.

        Args:
            mensaje: Mensaje a escribir.
            tipo: Tipo de mensaje (normal, exito, error, advertencia, info, titulo, subtitulo, comentario).
        """
        self.texto.config(state=tk.NORMAL)
        self.texto.insert(tk.END, mensaje + "\n", tipo)
        self.texto.see(tk.END)  # Auto-scroll
        self.texto.config(state=tk.DISABLED)

    def escribir_linea(self, mensaje: str = ""):
        """
        Escribe una línea en la consola.

        Args:
            mensaje: Mensaje a escribir (vacío para línea en blanco).
        """
        self.escribir(mensaje, "normal")

    def escribir_exito(self, mensaje: str):
        """Escribe un mensaje de éxito."""
        self.escribir(mensaje, "exito")

    def escribir_error(self, mensaje: str):
        """Escribe un mensaje de error."""
        self.escribir(mensaje, "error")

    def escribir_advertencia(self, mensaje: str):
        """Escribe un mensaje de advertencia."""
        self.escribir(mensaje, "advertencia")

    def escribir_info(self, mensaje: str):
        """Escribe un mensaje de información."""
        self.escribir(mensaje, "info")

    def escribir_titulo(self, mensaje: str):
        """Escribe un título."""
        self.escribir(mensaje, "titulo")

    def escribir_subtitulo(self, mensaje: str):
        """Escribe un subtítulo."""
        self.escribir(mensaje, "subtitulo")

    def escribir_comentario(self, mensaje: str):
        """Escribe un comentario."""
        self.escribir(mensaje, "comentario")

    def escribir_separador(self, caracter: str = "=", longitud: int = 70):
        """
        Escribe una línea separadora.

        Args:
            caracter: Carácter a usar para el separador.
            longitud: Longitud del separador.
        """
        self.escribir(caracter * longitud, "comentario")

    def limpiar(self):
        """Limpia el contenido de la consola."""
        self.texto.config(state=tk.NORMAL)
        self.texto.delete("1.0", tk.END)
        self.texto.config(state=tk.DISABLED)

    def mostrar_resultado_compilacion(self, resultado: dict):
        """
        Muestra el resultado de una compilación completa.

        Args:
            resultado: Diccionario con los resultados de la compilación.
        """
        self.limpiar()

        # Título
        self.escribir_separador()
        self.escribir_titulo("RESULTADO DE COMPILACIÓN")
        self.escribir_separador()
        self.escribir_linea()

        # Verificar éxito
        if resultado.get("exito", False):
            self.escribir_exito("✓ COMPILACIÓN EXITOSA")
        else:
            self.escribir_error("✗ COMPILACIÓN FALLIDA")

        self.escribir_linea()

        # Mostrar errores si existen
        errores = resultado.get("errores", [])
        if errores:
            self.escribir_subtitulo(f"Errores encontrados ({len(errores)}):")
            self.escribir_linea()
            for i, error in enumerate(errores, 1):
                self.escribir_error(f"  {i}. {error}")
            self.escribir_linea()

        # Mostrar análisis semántico
        semantico = resultado.get("semantico", [])
        if semantico:
            self.escribir_subtitulo("Análisis Semántico:")
            self.escribir_linea()
            for item in semantico:
                if "Error" in str(item):
                    self.escribir_error(f"  {item}")
                else:
                    self.escribir_info(f"  {item}")
            self.escribir_linea()

        # Mostrar código intermedio si existe
        codigo_intermedio = resultado.get("codigo_intermedio", "")
        if codigo_intermedio:
            self.escribir_subtitulo("Código Intermedio:")
            self.escribir_linea()
            self.escribir(codigo_intermedio, "normal")

        self.escribir_separador()

    def mostrar_tokens(self, resultado: dict):
        """
        Muestra el resultado del análisis léxico.

        Args:
            resultado: Diccionario con tokens y errores.
        """
        self.limpiar()

        self.escribir_separador()
        self.escribir_titulo("ANÁLISIS LÉXICO")
        self.escribir_separador()
        self.escribir_linea()

        if resultado.get("exito", False):
            self.escribir_exito("✓ Análisis léxico completado exitosamente")
            self.escribir_linea()
            resumen = resultado.get("resumen", "")
            if resumen:
                self.escribir(resumen, "normal")
        else:
            self.escribir_error("✗ Errores en análisis léxico")
            self.escribir_linea()
            for error in resultado.get("errores", []):
                self.escribir_error(f"  {error}")

        self.escribir_separador()

    def mostrar_ast(self, resultado: dict):
        """
        Muestra el resultado del análisis sintáctico.

        Args:
            resultado: Diccionario con el AST y errores.
        """
        self.limpiar()

        self.escribir_separador()
        self.escribir_titulo("ANÁLISIS SINTÁCTICO")
        self.escribir_separador()
        self.escribir_linea()

        if resultado.get("exito", False):
            self.escribir_exito("✓ Análisis sintáctico completado exitosamente")
            self.escribir_linea()
            resumen = resultado.get("resumen", "")
            if resumen:
                self.escribir(resumen, "normal")
        else:
            self.escribir_error("✗ Errores en análisis sintáctico")
            self.escribir_linea()
            for error in resultado.get("errores", []):
                self.escribir_error(f"  {error}")

        self.escribir_separador()

    def mostrar_mensaje_bienvenida(self):
        """Muestra un mensaje de bienvenida al iniciar."""
        self.limpiar()

        self.escribir_separador("=")
        self.escribir_titulo("    COMPILADOR KOTLIN - KFORGE    ")
        self.escribir_separador("=")
        self.escribir_linea()
        self.escribir_info("Bienvenido al compilador modular de Kotlin")
        self.escribir_linea()
        self.escribir_comentario("Características:")
        self.escribir_comentario("  • Análisis Léxico")
        self.escribir_comentario("  • Análisis Sintáctico")
        self.escribir_comentario("  • Análisis Semántico")
        self.escribir_comentario("  • Generación de Código Intermedio (próximamente)")
        self.escribir_linea()
        self.escribir_info("Escriba su código Kotlin en el editor superior")
        self.escribir_info("y use el menú 'Compilador' para analizarlo.")
        self.escribir_linea()
        self.escribir_separador("=")
