"""
Aplicación principal de KForge.
Integra todos los componentes de la interfaz moderna.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from ui.theme_manager import get_theme_manager, get_language_manager
from ui.splash_screen import show_splash
from ui.editor_panel import EditorPanel
from ui.console_panel import ConsolePanel
from ui.sidebar import Sidebar
from ui.phases_panel import PhasesPanel
from ui.status_bar import StatusBar
from core.controller import CompiladorController


class KForgeApp(tk.Tk):
    """Ventana principal de KForge con interfaz moderna."""

    def __init__(self):
        super().__init__()

        # Mostrar splash screen
        self.withdraw()
        splash = show_splash(self, duration=2000)
        self.after(2000, lambda: [splash.close(), self.deiconify()])

        # Gestores
        self.theme = get_theme_manager()
        self.lang = get_language_manager()
        self.controller = CompiladorController()

        # Configuración de ventana
        self.title(self.lang.t("app_title"))
        self.geometry("1200x800")
        self.minsize(1000, 600)

        # Aplicar tema
        self._apply_theme()

        # Crear interfaz
        self._create_menu()
        self._create_layout()

        # Configurar eventos
        self._bind_events()

        # Archivo actual
        self.current_file = None

    def _apply_theme(self):
        """Aplica el tema actual."""
        colors = self.theme.get_colors()
        self.configure(bg=colors.bg_primary)

    def _create_menu(self):
        """Crea el menú principal."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.lang.t("menu.file"), menu=file_menu)
        file_menu.add_command(label=self.lang.t("menu.new"), command=self._new_file,
                            accelerator="Ctrl+N")
        file_menu.add_command(label=self.lang.t("menu.open"), command=self._open_file,
                            accelerator="Ctrl+O")
        file_menu.add_command(label=self.lang.t("menu.save"), command=self._save_file,
                            accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label=self.lang.t("menu.exit"), command=self.quit)

        # Menú Compilador
        compiler_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.lang.t("menu.compiler"), menu=compiler_menu)
        compiler_menu.add_command(label=self.lang.t("menu.lexical"),
                                command=self._run_lexical, accelerator="F5")
        compiler_menu.add_command(label=self.lang.t("menu.syntactic"),
                                command=self._run_syntactic, accelerator="F6")
        compiler_menu.add_command(label=self.lang.t("menu.semantic"),
                                command=self._run_semantic, accelerator="F7")
        compiler_menu.add_command(label=self.lang.t("menu.compile_all"),
                                command=self._run_complete, accelerator="F8")

        # Menú Ver
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.lang.t("menu.view"), menu=view_menu)
        view_menu.add_command(label=self.lang.t("menu.dark_theme"),
                            command=lambda: self._toggle_theme("dark"))
        view_menu.add_command(label=self.lang.t("menu.light_theme"),
                            command=lambda: self._toggle_theme("light"))

        # Atajos de teclado
        self.bind("<Control-n>", lambda e: self._new_file())
        self.bind("<Control-o>", lambda e: self._open_file())
        self.bind("<Control-s>", lambda e: self._save_file())
        self.bind("<F5>", lambda e: self._run_lexical())
        self.bind("<F6>", lambda e: self._run_syntactic())
        self.bind("<F7>", lambda e: self._run_semantic())
        self.bind("<F8>", lambda e: self._run_complete())

    def _create_layout(self):
        """Crea el layout principal."""
        colors = self.theme.get_colors()

        # Frame principal
        main_frame = tk.Frame(self, bg=colors.bg_primary)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Sidebar (izquierda)
        self.sidebar = Sidebar(main_frame)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Frame central (editor + consola)
        center_frame = tk.Frame(main_frame, bg=colors.bg_primary)
        center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Panel de editor (arriba)
        editor_container = tk.Frame(center_frame, bg=colors.bg_primary)
        editor_container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.editor_panel = EditorPanel(editor_container)
        self.editor_panel.pack(fill=tk.BOTH, expand=True)

        # Panel de fases (medio)
        self.phases_panel = PhasesPanel(center_frame, self.controller)
        self.phases_panel.pack(fill=tk.X, padx=2, pady=2)

        # Panel de consola (abajo)
        console_container = tk.Frame(center_frame, bg=colors.bg_primary)
        console_container.pack(fill=tk.BOTH, expand=False, padx=2, pady=2)
        console_container.configure(height=200)

        self.console_panel = ConsolePanel(console_container)
        self.console_panel.pack(fill=tk.BOTH, expand=True)

        # Barra de estado (inferior)
        self.status_bar = StatusBar(self)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Mensaje de bienvenida
        self.console_panel.write_output(self.lang.t("messages.welcome"), "info")

    def _bind_events(self):
        """Vincula eventos personalizados."""
        self.phases_panel.bind("<<RunLexical>>", lambda e: self._run_lexical())
        self.phases_panel.bind("<<RunSyntactic>>", lambda e: self._run_syntactic())
        self.phases_panel.bind("<<RunSemantic>>", lambda e: self._run_semantic())
        self.phases_panel.bind("<<RunCodeGen>>", lambda e: self._run_codegen())

    # ========== Métodos de archivo ==========

    def _new_file(self):
        """Crea un nuevo archivo."""
        self.editor_panel.new_file()
        self.current_file = None

    def _open_file(self):
        """Abre un archivo."""
        filename = filedialog.askopenfilename(
            title=self.lang.t("menu.open"),
            filetypes=[
                ("Archivos Kotlin", "*.kt"),
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ]
        )

        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()

                self.editor_panel.new_file(filename.split("/")[-1])
                editor = self.editor_panel.get_current_editor()
                editor.set_text(content)

                self.current_file = filename
                self.status_bar.set_status("Archivo abierto", "ready")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

    def _save_file(self):
        """Guarda el archivo actual."""
        if not self.current_file:
            filename = filedialog.asksaveasfilename(
                defaultextension=".kt",
                filetypes=[
                    ("Archivos Kotlin", "*.kt"),
                    ("Archivos de texto", "*.txt")
                ]
            )
            if filename:
                self.current_file = filename

        if self.current_file:
            try:
                content = self.editor_panel.get_current_text()
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.status_bar.set_status("Archivo guardado", "completed")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

    # ========== Métodos de compilación ==========

    def _run_lexical(self):
        """Ejecuta análisis léxico."""
        code = self.editor_panel.get_current_text()
        if not code.strip():
            messagebox.showwarning("Advertencia", "El editor está vacío")
            return

        self.phases_panel.set_phase_running("lexical")
        self.status_bar.set_status(self.lang.t("phases.analyzing"), "analyzing")

        try:
            resultado = self.controller.ejecutar_lexico(code)

            if resultado["exito"]:
                self.console_panel.show_tokens(resultado["tokens"])
                self.phases_panel.set_phase_completed("lexical", True)
                self.status_bar.set_status(self.lang.t("status.completed"), "completed")
            else:
                for error in resultado["errores"]:
                    self.console_panel.write_error(str(error))
                self.phases_panel.set_phase_completed("lexical", False)
                self.status_bar.set_status(self.lang.t("status.error"), "error")
        except Exception as e:
            self.console_panel.write_error(str(e))
            self.phases_panel.set_phase_completed("lexical", False)
            self.status_bar.set_status(self.lang.t("status.error"), "error")

    def _run_syntactic(self):
        """Ejecuta análisis sintáctico."""
        code = self.editor_panel.get_current_text()
        if not code.strip():
            messagebox.showwarning("Advertencia", "El editor está vacío")
            return

        self.phases_panel.reset_all()
        self.phases_panel.set_phase_running("syntactic")
        self.status_bar.set_status(self.lang.t("phases.analyzing"), "analyzing")

        try:
            resultado = self.controller.ejecutar_sintactico(code)

            if resultado["exito"]:
                self.console_panel.show_ast(resultado["arbol"])
                self.phases_panel.set_phase_completed("lexical", True)
                self.phases_panel.set_phase_completed("syntactic", True)
                self.status_bar.set_status(self.lang.t("status.completed"), "completed")
            else:
                for error in resultado["errores"]:
                    self.console_panel.write_error(str(error))
                self.phases_panel.set_phase_completed("syntactic", False)
                self.status_bar.set_status(self.lang.t("status.error"), "error")
        except Exception as e:
            self.console_panel.write_error(str(e))
            self.phases_panel.set_phase_completed("syntactic", False)

    def _run_semantic(self):
        """Ejecuta análisis semántico."""
        code = self.editor_panel.get_current_text()
        if not code.strip():
            messagebox.showwarning("Advertencia", "El editor está vacío")
            return

        self.phases_panel.reset_all()
        self.phases_panel.set_phase_running("semantic")
        self.status_bar.set_status(self.lang.t("phases.analyzing"), "analyzing")

        try:
            resultado = self.controller.ejecutar_semantico(code)
            self.console_panel.show_results(resultado)

            if resultado["exito"]:
                self.phases_panel.set_phase_completed("lexical", True)
                self.phases_panel.set_phase_completed("syntactic", True)
                self.phases_panel.set_phase_completed("semantic", True)
                self.status_bar.set_status(self.lang.t("messages.compilation_success"), "completed")
            else:
                self.phases_panel.set_phase_completed("semantic", False)
                self.status_bar.set_status(self.lang.t("messages.compilation_failed"), "error")
        except Exception as e:
            self.console_panel.write_error(str(e))
            self.phases_panel.set_phase_completed("semantic", False)

    def _run_complete(self):
        """Ejecuta compilación completa."""
        self._run_semantic()

        # Aplicar resaltado de sintaxis
        editor = self.editor_panel.get_current_editor()
        if editor:
            editor.highlight_syntax()

    def _run_codegen(self):
        """Ejecuta generación de código."""
        code = self.editor_panel.get_current_text()
        if not code.strip():
            return

        self.phases_panel.set_phase_running("codegen")
        try:
            resultado = self.controller.ejecutar_codegen(code)
            if resultado.get("codigo_intermedio"):
                self.console_panel.write_output(resultado["codigo_intermedio"])
            self.phases_panel.set_phase_completed("codegen", resultado["exito"])
        except Exception as e:
            self.console_panel.write_error(str(e))
            self.phases_panel.set_phase_completed("codegen", False)

    def _toggle_theme(self, theme: str):
        """Cambia el tema de la aplicación."""
        self.theme.set_theme(theme)
        messagebox.showinfo("Tema", f"Tema cambiado. Reinicie la aplicación para aplicar completamente.")


def run():
    """Ejecuta la aplicación KForge."""
    app = KForgeApp()
    app.mainloop()


if __name__ == "__main__":
    run()
