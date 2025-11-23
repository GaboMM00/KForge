"""
Panel de consola con pestañas para KForge.
Muestra resultados, errores, tokens y AST.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
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


class CodeTab(tk.Frame):
    """Pestaña para visualizar código TAC y Bytecode."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.theme = get_theme_manager()
        colors = self.theme.get_colors()

        self.configure(bg=colors.console_bg)

        # Almacenar código actual
        self.current_tac = ""
        self.current_bytecode = ""
        self.current_mode = "tac"  # 'tac' o 'bytecode'

        # Frame superior para botones
        button_frame = tk.Frame(self, bg=colors.console_bg)
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Botones
        btn_style = {
            'bg': colors.button_bg,
            'fg': colors.button_fg,
            'activebackground': colors.button_hover,
            'activeforeground': colors.button_fg,
            'relief': tk.FLAT,
            'padx': 10,
            'pady': 5,
            'cursor': 'hand2'
        }

        self.btn_tac = tk.Button(
            button_frame,
            text="Ver TAC",
            command=self._show_tac,
            **btn_style
        )
        self.btn_tac.pack(side=tk.LEFT, padx=2)

        self.btn_bytecode = tk.Button(
            button_frame,
            text="Ver Bytecode",
            command=self._show_bytecode,
            **btn_style
        )
        self.btn_bytecode.pack(side=tk.LEFT, padx=2)

        self.btn_save = tk.Button(
            button_frame,
            text="Guardar Código",
            command=self._save_code,
            **btn_style
        )
        self.btn_save.pack(side=tk.LEFT, padx=2)

        # Label para indicar modo actual
        self.mode_label = tk.Label(
            button_frame,
            text="TAC",
            font=self.theme.get_font(),
            bg=colors.console_bg,
            fg=colors.console_info
        )
        self.mode_label.pack(side=tk.RIGHT, padx=10)

        # Área de texto para código
        self.text = scrolledtext.ScrolledText(
            self,
            font=('Consolas', 10),  # Fuente monoespaciada para código
            wrap=tk.NONE,  # Sin wrap para código
            bg=colors.console_bg,
            fg=colors.console_fg,
            insertbackground=colors.console_fg,
            selectbackground=colors.editor_selection_bg,
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Tags para syntax highlighting
        self.text.tag_config("keyword", foreground=colors.syntax_keyword)
        self.text.tag_config("comment", foreground=colors.syntax_comment)
        self.text.tag_config("label", foreground=colors.syntax_string)
        self.text.tag_config("instruction", foreground=colors.syntax_function)

    def set_code(self, tac_code: str, bytecode_code: str):
        """Establece el código TAC y Bytecode."""
        self.current_tac = tac_code
        self.current_bytecode = bytecode_code
        # Mostrar TAC por defecto
        self._show_tac()

    def _show_tac(self):
        """Muestra el código TAC."""
        self.current_mode = "tac"
        self.mode_label.config(text="TAC")
        self._display_code(self.current_tac)

    def _show_bytecode(self):
        """Muestra el código Bytecode."""
        self.current_mode = "bytecode"
        self.mode_label.config(text="Bytecode Assembly")
        self._display_code(self.current_bytecode)

    def _display_code(self, code: str):
        """Muestra código con syntax highlighting básico."""
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)

        if not code:
            self.text.insert(tk.END, "No hay código generado aún.")
        else:
            # Insertar código línea por línea con highlighting
            for line in code.split('\n'):
                self._highlight_line(line)
                self.text.insert(tk.END, "\n")

        self.text.config(state=tk.DISABLED)

    def _highlight_line(self, line: str):
        """Aplica syntax highlighting a una línea."""
        if not line.strip():
            self.text.insert(tk.END, line)
            return

        # Comentarios (;)
        if line.strip().startswith(';'):
            self.text.insert(tk.END, line, "comment")
        # Labels (terminan en :)
        elif ':' in line and not line.strip().startswith(';'):
            parts = line.split(':', 1)
            self.text.insert(tk.END, parts[0], "label")
            self.text.insert(tk.END, ':')
            if len(parts) > 1:
                # Resto de la línea después del label
                rest = parts[1]
                if ';' in rest:
                    code_part, comment_part = rest.split(';', 1)
                    self.text.insert(tk.END, code_part)
                    self.text.insert(tk.END, ';' + comment_part, "comment")
                else:
                    self.text.insert(tk.END, rest)
        # Líneas con comentarios al final
        elif ';' in line:
            parts = line.split(';', 1)
            # Parte de código
            code_part = parts[0]
            self._highlight_instruction(code_part)
            # Parte de comentario
            self.text.insert(tk.END, ';' + parts[1], "comment")
        else:
            # Solo código
            self._highlight_instruction(line)

    def _highlight_instruction(self, line: str):
        """Aplica highlighting a instrucciones."""
        # Lista de instrucciones conocidas
        tac_ops = ['ASSIGN', 'ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'LT', 'GT', 'LE', 'GE',
                   'EQ', 'NE', 'AND', 'OR', 'NOT', 'NEG', 'LABEL', 'GOTO', 'IF_FALSE',
                   'PARAM', 'CALL', 'RETURN', 'ARRAY_LOAD', 'ARRAY_STORE']

        bytecode_ops = ['PUSH', 'LOAD', 'STORE', 'ADD', 'SUB', 'MUL', 'DIV', 'MOD',
                        'LT', 'GT', 'LE', 'GE', 'EQ', 'NE', 'AND', 'OR', 'NOT', 'NEG',
                        'LABEL', 'JUMP', 'JUMPF', 'CALL', 'RET', 'HALT', 'ALOAD', 'ASTORE']

        all_ops = set(tac_ops + bytecode_ops)

        # Dividir la línea en palabras
        words = line.split()
        for i, word in enumerate(words):
            if word.upper() in all_ops:
                self.text.insert(tk.END, word, "instruction")
            else:
                self.text.insert(tk.END, word)

            # Agregar espacio entre palabras (excepto la última)
            if i < len(words) - 1:
                self.text.insert(tk.END, " ")

    def _save_code(self):
        """Guarda el código actual a un archivo."""
        if self.current_mode == "tac":
            code = self.current_tac
            default_ext = ".tac"
            filetypes = [("TAC files", "*.tac"), ("Text files", "*.txt"), ("All files", "*.*")]
        else:
            code = self.current_bytecode
            default_ext = ".asm"
            filetypes = [("Assembly files", "*.asm"), ("Text files", "*.txt"), ("All files", "*.*")]

        if not code:
            messagebox.showwarning("Sin código", "No hay código para guardar.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=default_ext,
            filetypes=filetypes,
            title=f"Guardar código {self.current_mode.upper()}"
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(code)
                messagebox.showinfo("Éxito", f"Código guardado en:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")

    def clear(self):
        """Limpia el contenido de la pestaña."""
        self.current_tac = ""
        self.current_bytecode = ""
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
        self.code_tab = CodeTab(self)  # Nueva pestaña de código

        # Agregar pestañas
        self.add(self.output_tab, text=self.lang.t("console.output"))
        self.add(self.errors_tab, text=self.lang.t("console.errors"))
        self.add(self.tokens_tab, text=self.lang.t("console.tokens"))
        self.add(self.ast_tab, text=self.lang.t("console.ast"))
        self.add(self.code_tab, text="Código")  # Nueva pestaña

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

    def show_code(self, tac_code: str, bytecode_code: str):
        """Muestra el código TAC y Bytecode."""
        self.code_tab.set_code(tac_code, bytecode_code)
        self.select(self.code_tab)

    def show_results(self, resultado: dict):
        """Muestra los resultados de la compilación."""
        self.output_tab.clear()

        if resultado.get("exito"):
            self.output_tab.write("=== COMPILACION EXITOSA ===", "success")
            self.output_tab.write(f"\nTokens generados: {len(resultado.get('tokens', []))}", "info")

            for item in resultado.get("semantico", []):
                self.output_tab.write(f"  {item}")

            # Mostrar información sobre código generado
            if resultado.get("codigo_intermedio"):
                tac_lines = len(resultado.get("codigo_intermedio", "").split('\n'))
                self.output_tab.write(f"\nCódigo TAC generado: {tac_lines} líneas", "info")

            if resultado.get("bytecode"):
                bc_instructions = len(resultado.get("bytecode_instructions", []))
                self.output_tab.write(f"Bytecode generado: {bc_instructions} instrucciones", "info")
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
        self.code_tab.clear()


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
