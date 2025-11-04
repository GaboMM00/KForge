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


class EditorPanel(tk.Frame):
    """Panel de editor con soporte de pestañas y botones de cierre."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.theme = get_theme_manager()
        self.editors = {}
        self.file_counter = 1
        self.file_paths = {}  # Mapea nombres de pestañas a rutas de archivo
        self.modified_files = set()  # Pestañas con cambios no guardados

        # Crear notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Frame de controles (para botón +)
        colors = self.theme.get_colors()
        control_frame = tk.Frame(self, bg=colors.bg_secondary, height=30)
        control_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Botón para nueva pestaña
        new_tab_btn = tk.Label(
            control_frame,
            text="+ Nueva pestaña",
            font=("Segoe UI", 9),
            fg=colors.accent,
            bg=colors.bg_secondary,
            cursor="hand2",
            padx=10,
            pady=5
        )
        new_tab_btn.pack(side=tk.LEFT, padx=5)
        new_tab_btn.bind("<Button-1>", lambda e: self.new_file())

        # Crear editor inicial
        self.new_file()

        # Bind evento de cierre de pestaña
        self.notebook.bind("<Button-3>", self._on_right_click)

    def new_file(self, filename: str = None, file_path: str = None):
        """Crea un nuevo archivo/pestaña."""
        if filename is None:
            filename = f"Sin título-{self.file_counter}"
            self.file_counter += 1

        # Crear frame para la pestaña con botón de cierre
        tab_frame = tk.Frame(self.notebook)

        # Crear editor
        editor = EditorWithLineNumbers(tab_frame)
        editor.pack(fill=tk.BOTH, expand=True)

        # Vincular eventos de modificación
        editor.text.bind("<<Modified>>", lambda e: self._on_text_modified(filename))

        # Agregar pestaña
        self.notebook.add(tab_frame, text=filename)
        self.editors[filename] = editor
        self.file_paths[filename] = file_path
        self.notebook.select(tab_frame)

        # Crear botón de cierre personalizado
        self._update_tab_text(filename)

        return editor

    def _update_tab_text(self, filename: str):
        """Actualiza el texto de la pestaña con indicador de modificación."""
        tab_id = None
        for i, (name, editor) in enumerate(self.editors.items()):
            if name == filename:
                tab_id = i
                break

        if tab_id is not None:
            if filename in self.modified_files:
                self.notebook.tab(tab_id, text=f"● {filename}")
            else:
                self.notebook.tab(tab_id, text=filename)

    def _on_text_modified(self, filename: str):
        """Maneja cambios en el texto."""
        if filename in self.editors:
            editor = self.editors[filename]
            if editor.text.edit_modified():
                self.modified_files.add(filename)
                self._update_tab_text(filename)
                editor.text.edit_modified(False)

    def _on_right_click(self, event):
        """Maneja clic derecho en pestaña."""
        try:
            clicked_tab = self.notebook.tk.call(self.notebook._w, "identify", "tab", event.x, event.y)
            if clicked_tab != '':
                self.close_tab(clicked_tab)
        except:
            pass

    def close_tab(self, tab_index):
        """Cierra una pestaña con confirmación si hay cambios."""
        # Obtener nombre de la pestaña
        filename = self.notebook.tab(tab_index, "text").replace("● ", "")

        # Verificar si hay cambios no guardados
        if filename in self.modified_files:
            from tkinter import messagebox
            response = messagebox.askyesnocancel(
                "Guardar cambios",
                f"¿Desea guardar los cambios en '{filename}'?"
            )

            if response is None:  # Cancelar
                return
            elif response:  # Sí, guardar
                self.event_generate("<<SaveFile>>")
                # Esperar un poco para que se guarde
                self.after(100, lambda: self._do_close_tab(tab_index, filename))
                return

        self._do_close_tab(tab_index, filename)

    def _do_close_tab(self, tab_index, filename):
        """Cierra la pestaña sin preguntar."""
        # No cerrar si es la única pestaña
        if self.notebook.index("end") <= 1:
            return

        # Limpiar referencias
        if filename in self.editors:
            del self.editors[filename]
        if filename in self.file_paths:
            del self.file_paths[filename]
        if filename in self.modified_files:
            self.modified_files.remove(filename)

        # Cerrar pestaña
        self.notebook.forget(tab_index)

    def close_current_tab(self):
        """Cierra la pestaña actual."""
        try:
            current = self.notebook.index(self.notebook.select())
            self.close_tab(current)
        except:
            pass

    def get_current_editor(self):
        """Obtiene el editor actualmente activo."""
        try:
            current_tab = self.notebook.select()
            tab_frame = self.nametowidget(current_tab)
            # El editor es el primer hijo del frame
            for child in tab_frame.winfo_children():
                if isinstance(child, EditorWithLineNumbers):
                    return child
            return None
        except:
            return None

    def get_current_text(self):
        """Obtiene el texto del editor actual."""
        editor = self.get_current_editor()
        return editor.get_text() if editor else ""

    def get_current_filename(self):
        """Obtiene el nombre de archivo de la pestaña actual."""
        try:
            current = self.notebook.index(self.notebook.select())
            filename = self.notebook.tab(current, "text").replace("● ", "")
            return filename
        except:
            return None

    def get_current_filepath(self):
        """Obtiene la ruta del archivo actual."""
        filename = self.get_current_filename()
        return self.file_paths.get(filename)

    def mark_saved(self, filename: str = None):
        """Marca un archivo como guardado."""
        if filename is None:
            filename = self.get_current_filename()

        if filename in self.modified_files:
            self.modified_files.remove(filename)
            self._update_tab_text(filename)


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
