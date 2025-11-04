"""
Panel de editor moderno con pestañas y resaltado de sintaxis para KForge.
"""

import tkinter as tk
from tkinter import ttk
import re
from ui.theme_manager import get_theme_manager


class EditorWithLineNumbers(tk.Frame):
    """Editor con numeración de líneas y resaltado de sintaxis."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.theme = get_theme_manager()
        colors = self.theme.get_colors()

        self.configure(bg=colors.editor_bg)

        # Canvas para números de línea
        self.line_numbers = tk.Canvas(
            self,
            width=50,
            bg=colors.editor_line_numbers_bg,
            highlightthickness=0
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Área de texto
        self.text = tk.Text(
            self,
            font=self.theme.get_font(),
            wrap=tk.NONE,
            undo=True,
            bg=colors.editor_bg,
            fg=colors.editor_fg,
            insertbackground=colors.editor_fg,
            selectbackground=colors.editor_selection_bg,
            selectforeground=colors.editor_selection_fg,
            relief=tk.FLAT,
            borderwidth=0
        )
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbars
        self.scrollbar_y = tk.Scrollbar(self, orient=tk.VERTICAL, command=self._scroll_y)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=self._update_scrollbar)

        # Configurar tags de sintaxis
        self._configure_syntax_tags()

        # Eventos
        self.text.bind("<KeyRelease>", self._on_text_change)
        self.text.bind("<MouseWheel>", lambda e: self._update_line_numbers())
        self.text.bind("<Button-1>", lambda e: self.after(10, self._update_line_numbers))

        self._update_line_numbers()

    def _configure_syntax_tags(self):
        """Configura los tags para resaltado de sintaxis."""
        syntax_colors = self.theme.get_syntax_colors()
        font_family, font_size = self.theme.get_font()

        self.text.tag_config("keyword", foreground=syntax_colors.get("keyword", "#CC7832"),
                           font=(font_family, font_size, "bold"))
        self.text.tag_config("type", foreground=syntax_colors.get("type", "#A9B7C6"))
        self.text.tag_config("string", foreground=syntax_colors.get("string", "#6A8759"))
        self.text.tag_config("number", foreground=syntax_colors.get("number", "#6897BB"))
        self.text.tag_config("comment", foreground=syntax_colors.get("comment", "#808080"),
                           font=(font_family, font_size, "italic"))

    def _scroll_y(self, *args):
        """Maneja el scroll vertical."""
        self.text.yview(*args)
        self._update_line_numbers()

    def _update_scrollbar(self, *args):
        """Actualiza la scrollbar."""
        self.scrollbar_y.set(*args)
        self._update_line_numbers()

    def _on_text_change(self, event=None):
        """Maneja cambios en el texto."""
        self._update_line_numbers()
        self.after(500, self.highlight_syntax)

    def _update_line_numbers(self):
        """Actualiza la numeración de líneas."""
        self.line_numbers.delete("all")
        colors = self.theme.get_colors()

        i = self.text.index("@0,0")
        while True:
            dline = self.text.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.line_numbers.create_text(
                45, y + dline[3] // 2,
                text=linenum,
                anchor=tk.E,
                font=self.theme.get_font(),
                fill=colors.editor_line_numbers_fg
            )
            i = self.text.index(f"{i}+1line")

    def highlight_syntax(self):
        """Aplica resaltado de sintaxis."""
        # Remover tags existentes
        for tag in ["keyword", "type", "string", "number", "comment"]:
            self.text.tag_remove(tag, "1.0", tk.END)

        content = self.text.get("1.0", tk.END)
        lines = content.split('\n')

        keywords = set(self.theme.get_keywords())
        types = set(self.theme.get_types())

        for line_num, line in enumerate(lines, 1):
            # Comentarios
            if '//' in line:
                idx = line.index('//')
                start = f"{line_num}.{idx}"
                end = f"{line_num}.{len(line)}"
                self.text.tag_add("comment", start, end)
                line = line[:idx]

            # Strings
            for match in re.finditer(r'"([^"\\]|\\.)*"', line):
                start = f"{line_num}.{match.start()}"
                end = f"{line_num}.{match.end()}"
                self.text.tag_add("string", start, end)

            # Palabras clave y tipos
            for match in re.finditer(r'\b\w+\b', line):
                word = match.group()
                start = f"{line_num}.{match.start()}"
                end = f"{line_num}.{match.end()}"

                if word in keywords:
                    self.text.tag_add("keyword", start, end)
                elif word in types:
                    self.text.tag_add("type", start, end)
                elif word.isdigit():
                    self.text.tag_add("number", start, end)

    def get_text(self):
        """Obtiene el texto del editor."""
        return self.text.get("1.0", tk.END).rstrip()

    def set_text(self, text: str):
        """Establece el texto del editor."""
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", text)
        self.highlight_syntax()
        self._update_line_numbers()

    def clear(self):
        """Limpia el editor."""
        self.text.delete("1.0", tk.END)
        self._update_line_numbers()


class EditorPanel(ttk.Notebook):
    """Panel de editor con soporte de pestañas."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.editors = {}
        self.file_counter = 1

        # Crear editor inicial
        self.new_file()

    def new_file(self, filename: str = None):
        """Crea un nuevo archivo/pestaña."""
        if filename is None:
            filename = f"Sin título-{self.file_counter}"
            self.file_counter += 1

        editor = EditorWithLineNumbers(self)
        self.add(editor, text=filename)
        self.editors[filename] = editor
        self.select(editor)

        return editor

    def get_current_editor(self):
        """Obtiene el editor actualmente activo."""
        try:
            current_tab = self.select()
            return self.nametowidget(current_tab)
        except:
            return None

    def get_current_text(self):
        """Obtiene el texto del editor actual."""
        editor = self.get_current_editor()
        return editor.get_text() if editor else ""

    def close_current_tab(self):
        """Cierra la pestaña actual."""
        try:
            current = self.select()
            self.forget(current)
        except:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Editor Panel")
    root.geometry("800x600")

    editor_panel = EditorPanel(root)
    editor_panel.pack(fill=tk.BOTH, expand=True)

    # Test code
    test_code = """var x: Int = 10
// Este es un comentario
var nombre: String = "KForge"
if (x > 5) {
    x = x + 1
}"""

    editor = editor_panel.get_current_editor()
    editor.set_text(test_code)

    root.mainloop()
