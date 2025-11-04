"""
Panel de consola con pestañas para KForge.
Muestra resultados, errores, tokens y AST.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from ui.theme_manager import get_theme_manager, get_language_manager


class ConsoleTab(tk.Frame):
    """Pestaña individual de la consola."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.theme = get_theme_manager()
        colors = self.theme.get_colors()

        self.configure(bg=colors.console_bg)

        # Crear área de texto
        self.text = scrolledtext.ScrolledText(
            self,
            font=self.theme.get_font(),
            wrap=tk.WORD,
            bg=colors.console_bg,
            fg=colors.console_fg,
            insertbackground=colors.console_fg,
            selectbackground=colors.editor_selection_bg,
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.text.pack(fill=tk.BOTH, expand=True)

        # Tags de colores
        self.text.tag_config("error", foreground=colors.console_error)
        self.text.tag_config("warning", foreground=colors.console_warning)
        self.text.tag_config("success", foreground=colors.console_success)
        self.text.tag_config("info", foreground=colors.console_info)

    def write(self, text: str, tag: str = None):
        """Escribe texto en la consola."""
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, text + "\n", tag)
        self.text.see(tk.END)
        self.text.config(state=tk.DISABLED)

    def clear(self):
        """Limpia el contenido de la pestaña."""
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.config(state=tk.DISABLED)


class ConsolePanel(ttk.Notebook):
    """Panel de consola con múltiples pestañas."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.theme = get_theme_manager()
        self.lang = get_language_manager()

        # Crear pestañas
        self.output_tab = ConsoleTab(self)
        self.errors_tab = ConsoleTab(self)
        self.tokens_tab = ConsoleTab(self)
        self.ast_tab = ConsoleTab(self)

        # Agregar pestañas
        self.add(self.output_tab, text=self.lang.t("console.output"))
        self.add(self.errors_tab, text=self.lang.t("console.errors"))
        self.add(self.tokens_tab, text=self.lang.t("console.tokens"))
        self.add(self.ast_tab, text=self.lang.t("console.ast"))

    def write_output(self, text: str, tag: str = None):
        """Escribe en la pestaña de salida."""
        self.output_tab.write(text, tag)

    def write_error(self, text: str):
        """Escribe un error."""
        self.errors_tab.write(text, "error")
        self.select(self.errors_tab)

    def show_tokens(self, tokens):
        """Muestra los tokens en formato tabla."""
        self.tokens_tab.clear()
        if tokens:
            header = f"{'#':<5} {'Tipo':<20} {'Valor':<25} {'Línea':<8} {'Columna':<8}\n"
            self.tokens_tab.write(header + "-" * 80)
            for i, token in enumerate(tokens[:-1], 1):  # Excluir EOF
                line = f"{i:<5} {str(token.tipo.name):<20} {str(token.valor):<25} {token.linea:<8} {token.columna:<8}"
                self.tokens_tab.write(line)
        self.select(self.tokens_tab)

    def show_ast(self, ast):
        """Muestra el AST."""
        self.ast_tab.clear()
        if ast:
            self.ast_tab.write(str(ast))
        self.select(self.ast_tab)

    def show_results(self, resultado: dict):
        """Muestra los resultados de la compilación."""
        self.output_tab.clear()

        if resultado.get("exito"):
            self.output_tab.write("=== COMPILACION EXITOSA ===", "success")
            self.output_tab.write(f"\nTokens generados: {len(resultado.get('tokens', []))}", "info")

            for item in resultado.get("semantico", []):
                self.output_tab.write(f"  {item}")
        else:
            self.output_tab.write("=== COMPILACION FALLIDA ===", "error")
            self.errors_tab.clear()
            for error in resultado.get("errores", []):
                self.errors_tab.write(str(error), "error")
            self.select(self.errors_tab)

    def clear_all(self):
        """Limpia todas las pestañas."""
        self.output_tab.clear()
        self.errors_tab.clear()
        self.tokens_tab.clear()
        self.ast_tab.clear()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Console Panel")
    root.geometry("800x300")

    console = ConsolePanel(root)
    console.pack(fill=tk.BOTH, expand=True)

    # Test
    console.write_output("Mensaje de prueba", "info")
    console.write_error("Error de prueba")

    root.mainloop()
