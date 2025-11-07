"""
Aplicación principal de KForge.
Integra todos los componentes de la interfaz moderna.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
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
        self.phases_panel.bind("<<ClearConsole>>", lambda e: self.console_panel.clear_all())

        # Sidebar events
        self.sidebar.bind("<<SidebarFiles>>", lambda e: self._sidebar_files())
        self.sidebar.bind("<<SidebarSettings>>", lambda e: self._sidebar_settings())
        self.sidebar.bind("<<SidebarTerminal>>", lambda e: self._sidebar_terminal())
        self.sidebar.bind("<<SidebarToggle>>", lambda e: self._sidebar_toggle())

    # ========== Métodos de sidebar ==========

    def _sidebar_files(self):
        """Abre el diálogo de gestión de archivos."""
        # Crear menú contextual de archivos
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Nuevo archivo (Ctrl+N)", command=self._new_file)
        menu.add_command(label="Abrir archivo (Ctrl+O)", command=self._open_file)
        menu.add_command(label="Guardar (Ctrl+S)", command=self._save_file)
        menu.add_separator()
        menu.add_command(label="Información del archivo", command=self._show_file_info)

        # Mostrar el menú en la posición del sidebar
        x = self.sidebar.winfo_rootx() + self.sidebar.winfo_width()
        y = self.sidebar.winfo_rooty() + 50
        menu.tk_popup(x, y)

    def _show_file_info(self):
        """Muestra información del archivo actual."""
        filename = self.editor_panel.get_current_filename()
        filepath = self.editor_panel.get_current_filepath()
        text = self.editor_panel.get_current_text()
        lines = text.count('\n') + 1 if text else 0
        chars = len(text)

        info_text = f"""Archivo: {filename}
Ruta: {filepath if filepath else '(sin guardar)'}
Líneas: {lines}
Caracteres: {chars}"""

        messagebox.showinfo("Información del Archivo", info_text)

    def _sidebar_settings(self):
        """Abre ventana de configuración funcional."""
        settings_window = tk.Toplevel(self)
        settings_window.title("Configuración de KForge")
        settings_window.geometry("450x400")
        settings_window.resizable(False, False)

        colors = self.theme.get_colors()
        settings_window.configure(bg=colors.bg_primary)

        # Frame principal
        main_frame = tk.Frame(settings_window, bg=colors.bg_primary, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title = tk.Label(
            main_frame,
            text="⚙️ Configuración",
            font=("Segoe UI", 14, "bold"),
            fg=colors.fg_primary,
            bg=colors.bg_primary
        )
        title.pack(pady=(0, 20))

        # === TEMA ===
        theme_frame = tk.Frame(main_frame, bg=colors.bg_primary)
        theme_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            theme_frame,
            text="Tema:",
            font=("Segoe UI", 10, "bold"),
            fg=colors.fg_primary,
            bg=colors.bg_primary,
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT)

        theme_var = tk.StringVar(value=self.theme.current_theme)
        theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=theme_var,
            values=["dark", "light"],
            state="readonly",
            width=18
        )
        theme_combo.pack(side=tk.LEFT, padx=10)

        def apply_theme(event=None):
            new_theme = theme_var.get()
            self.theme.set_theme(new_theme)
            self.theme.save_config()  # Guardar configuración
            self._apply_theme_to_all()
            update_info()
            self.status_bar.set_status(f"Tema '{new_theme}' aplicado", "ready")

        theme_combo.bind("<<ComboboxSelected>>", apply_theme)

        # === TIPOGRAFÍA ===
        font_family_frame = tk.Frame(main_frame, bg=colors.bg_primary)
        font_family_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            font_family_frame,
            text="Tipografía:",
            font=("Segoe UI", 10, "bold"),
            fg=colors.fg_primary,
            bg=colors.bg_primary,
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT)

        font_family_var = tk.StringVar(value=self.theme.current_font)
        font_family_combo = ttk.Combobox(
            font_family_frame,
            textvariable=font_family_var,
            values=["JetBrains Mono", "Fira Code", "Consolas", "Source Code Pro"],
            state="readonly",
            width=18
        )
        font_family_combo.pack(side=tk.LEFT, padx=10)

        def apply_font_family(event=None):
            new_font = font_family_var.get()
            self.theme.set_font(new_font)
            self.theme.save_config()  # Guardar configuración
            self._apply_font_to_editors()
            # Actualizar la información mostrada
            update_info()
            self.status_bar.set_status(f"Fuente '{new_font}' aplicada", "ready")

        font_family_combo.bind("<<ComboboxSelected>>", apply_font_family)

        # === TAMAÑO DE FUENTE ===
        font_size_frame = tk.Frame(main_frame, bg=colors.bg_primary)
        font_size_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            font_size_frame,
            text="Tamaño fuente:",
            font=("Segoe UI", 10, "bold"),
            fg=colors.fg_primary,
            bg=colors.bg_primary,
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT)

        font_size_var = tk.IntVar(value=self.theme.font_size)

        def apply_font_size_change():
            new_size = font_size_var.get()
            self.theme.font_size = new_size
            self.theme.save_config()  # Guardar configuración
            self._apply_font_to_editors()
            update_info()
            self.status_bar.set_status(f"Tamaño de fuente: {new_size}pt", "ready")

        font_spinbox = tk.Spinbox(
            font_size_frame,
            from_=8,
            to=24,
            textvariable=font_size_var,
            width=10,
            command=apply_font_size_change
        )
        font_spinbox.pack(side=tk.LEFT, padx=10)

        # === IDIOMA ===
        lang_frame = tk.Frame(main_frame, bg=colors.bg_primary)
        lang_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            lang_frame,
            text="Idioma:",
            font=("Segoe UI", 10, "bold"),
            fg=colors.fg_primary,
            bg=colors.bg_primary,
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT)

        lang_var = tk.StringVar(value=self.lang.current_language)
        lang_combo = ttk.Combobox(
            lang_frame,
            textvariable=lang_var,
            values=["es", "en"],
            state="readonly",
            width=18
        )
        lang_combo.pack(side=tk.LEFT, padx=10)

        def apply_language(event=None):
            new_lang = lang_var.get()
            self.lang.set_language(new_lang)
            self.lang.save_config()  # Guardar configuración
            update_info()
            self.status_bar.set_status(f"Idioma cambiado a '{new_lang}'", "ready")
            messagebox.showinfo(
                "Cambio de idioma",
                "El idioma se ha cambiado. Algunos cambios requieren reiniciar la aplicación para aplicarse completamente."
            )

        lang_combo.bind("<<ComboboxSelected>>", apply_language)

        # Separador
        separator = tk.Frame(main_frame, bg=colors.fg_tertiary, height=1)
        separator.pack(fill=tk.X, pady=15)

        # === INFORMACIÓN DINÁMICA ===
        info_frame = tk.Frame(main_frame, bg=colors.bg_secondary, relief=tk.FLAT, padx=10, pady=10)
        info_frame.pack(fill=tk.X, pady=10)

        info_label = tk.Label(
            info_frame,
            text="",
            font=("Consolas", 9),
            fg=colors.fg_secondary,
            bg=colors.bg_secondary,
            justify=tk.LEFT,
            anchor="w"
        )
        info_label.pack(fill=tk.X)

        def update_info():
            """Actualiza la información mostrada."""
            info_text = f"""📌 Configuración actual:
  • Versión: {self.lang.t('app_version')}
  • Tema: {self.theme.current_theme}
  • Fuente: {self.theme.current_font} {self.theme.font_size}pt
  • Idioma: {self.lang.current_language}"""
            info_label.config(text=info_text)

        # Mostrar información inicial
        update_info()

        # Botón cerrar
        close_btn = tk.Button(
            main_frame,
            text="Cerrar",
            command=settings_window.destroy,
            bg=colors.accent,
            fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=30,
            pady=8,
            cursor="hand2"
        )
        close_btn.pack(pady=15)

    def _sidebar_terminal(self):
        """Alterna la visibilidad de la consola."""
        if self.console_panel.winfo_viewable():
            self.console_panel.pack_forget()
            self.status_bar.set_status("Terminal ocultada", "ready")
        else:
            self.console_panel.pack(fill=tk.BOTH, expand=False, padx=2, pady=2)
            self.status_bar.set_status("Terminal visible", "ready")

    def _sidebar_toggle(self):
        """Maneja el toggle de la sidebar (ya gestionado por la propia sidebar)."""
        pass

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

        # LIMPIAR RESULTADOS PREVIOS
        self.console_panel.clear_all()
        self.phases_panel.reset_all()

        self.phases_panel.set_phase_running("lexical")
        self.status_bar.set_status(self.lang.t("phases.analyzing"), "analyzing")

        try:
            resultado = self.controller.ejecutar_lexico(code)

            if resultado["exito"]:
                self.console_panel.show_tokens(resultado["tokens"])
                # Cambiar a la pestaña de Tokens
                self.console_panel.select(self.console_panel.tokens_tab)
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

        # LIMPIAR RESULTADOS PREVIOS
        self.console_panel.clear_all()
        self.phases_panel.reset_all()

        self.phases_panel.set_phase_running("syntactic")
        self.status_bar.set_status(self.lang.t("phases.analyzing"), "analyzing")

        try:
            # Primero ejecutar análisis léxico para mostrar tokens
            resultado_lexico = self.controller.ejecutar_lexico(code)
            if resultado_lexico["exito"]:
                self.console_panel.show_tokens(resultado_lexico["tokens"])
                self.phases_panel.set_phase_completed("lexical", True)

            # Luego ejecutar análisis sintáctico
            resultado = self.controller.ejecutar_sintactico(code)

            if resultado["exito"]:
                self.console_panel.show_ast(resultado["arbol"])
                # Cambiar a la pestaña de AST
                self.console_panel.select(self.console_panel.ast_tab)
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

        # LIMPIAR RESULTADOS PREVIOS
        self.console_panel.clear_all()
        self.phases_panel.reset_all()

        self.phases_panel.set_phase_running("semantic")
        self.status_bar.set_status(self.lang.t("phases.analyzing"), "analyzing")

        try:
            # 1. Ejecutar análisis léxico
            resultado_lexico = self.controller.ejecutar_lexico(code)
            if resultado_lexico["exito"]:
                self.console_panel.show_tokens(resultado_lexico["tokens"])
                self.phases_panel.set_phase_completed("lexical", True)

            # 2. Ejecutar análisis sintáctico
            resultado_sintactico = self.controller.ejecutar_sintactico(code)
            if resultado_sintactico["exito"]:
                self.console_panel.show_ast(resultado_sintactico["arbol"])
                self.phases_panel.set_phase_completed("syntactic", True)

            # 3. Ejecutar análisis semántico
            resultado = self.controller.ejecutar_semantico(code)
            self.console_panel.show_results(resultado)
            # Cambiar a la pestaña de Salida
            self.console_panel.select(self.console_panel.output_tab)

            if resultado["exito"]:
                self.phases_panel.set_phase_completed("semantic", True)
                self.status_bar.set_status(self.lang.t("messages.compilation_success"), "completed")
            else:
                self.phases_panel.set_phase_completed("semantic", False)
                self.status_bar.set_status(self.lang.t("messages.compilation_failed"), "error")
        except Exception as e:
            self.console_panel.write_error(str(e))
            self.phases_panel.set_phase_completed("semantic", False)

    def _run_complete(self):
        """Ejecuta compilación completa (semántica + resaltado)."""
        self._run_semantic()

        # Aplicar resaltado de sintaxis
        editor = self.editor_panel.get_current_editor()
        if editor:
            editor.highlight_syntax()

    def _run_codegen(self):
        """Ejecuta generación de código."""
        code = self.editor_panel.get_current_text()
        if not code.strip():
            messagebox.showwarning("Advertencia", "El editor está vacío")
            return

        # LIMPIAR RESULTADOS PREVIOS
        self.console_panel.clear_all()
        self.phases_panel.reset_all()

        self.phases_panel.set_phase_running("codegen")
        self.status_bar.set_status("Generando código...", "analyzing")

        try:
            # 1. Ejecutar análisis léxico
            resultado_lexico = self.controller.ejecutar_lexico(code)
            if resultado_lexico["exito"]:
                self.console_panel.show_tokens(resultado_lexico["tokens"])
                self.phases_panel.set_phase_completed("lexical", True)

            # 2. Ejecutar análisis sintáctico
            resultado_sintactico = self.controller.ejecutar_sintactico(code)
            if resultado_sintactico["exito"]:
                self.console_panel.show_ast(resultado_sintactico["arbol"])
                self.phases_panel.set_phase_completed("syntactic", True)

            # 3. Ejecutar análisis semántico
            resultado_semantico = self.controller.ejecutar_semantico(code)
            self.console_panel.show_results(resultado_semantico)
            if resultado_semantico["exito"]:
                self.phases_panel.set_phase_completed("semantic", True)

            # 4. Ejecutar generación de código
            resultado = self.controller.ejecutar_codegen(code)
            if resultado.get("codigo_intermedio"):
                self.console_panel.write_output("\n=== Código Intermedio ===", "info")
                self.console_panel.write_output(resultado["codigo_intermedio"])
            # Cambiar a la pestaña de Salida
            self.console_panel.select(self.console_panel.output_tab)

            self.phases_panel.set_phase_completed("codegen", resultado.get("exito", False))
            self.status_bar.set_status("Generación de código completada", "completed")
        except Exception as e:
            self.console_panel.write_error(str(e))
            self.phases_panel.set_phase_completed("codegen", False)
            self.status_bar.set_status("Error en generación de código", "error")

    def _apply_theme_to_all(self):
        """Aplica el tema actual a todos los componentes."""
        colors = self.theme.get_colors()

        # Aplicar a ventana principal
        self.configure(bg=colors.bg_primary)

        # Aplicar a todos los componentes principales
        self._apply_theme()

        # Actualizar status bar
        if hasattr(self, 'status_bar'):
            self.status_bar.update_theme()

        # Actualizar sidebar
        if hasattr(self, 'sidebar'):
            self.sidebar.configure(bg=colors.bg_secondary)

        # Actualizar phases panel
        if hasattr(self, 'phases_panel'):
            self.phases_panel.configure(bg=colors.bg_primary)

        # Actualizar editor panel
        self._apply_theme_to_editors()

        # Actualizar consola
        self._apply_theme_to_console()

    def _apply_theme_to_editors(self):
        """Aplica el tema a todos los editores abiertos."""
        colors = self.theme.get_colors()
        if hasattr(self, 'editor_panel'):
            for filename, editor in self.editor_panel.editors.items():
                editor.text.config(
                    bg=colors.editor_bg,
                    fg=colors.editor_fg,
                    insertbackground=colors.editor_fg,
                    selectbackground=colors.editor_selection_bg
                )
                editor.line_numbers.config(
                    bg=colors.editor_line_numbers_bg,
                    fg=colors.editor_line_numbers_fg
                )

    def _apply_theme_to_console(self):
        """Aplica el tema a la consola."""
        colors = self.theme.get_colors()
        if hasattr(self, 'console_panel'):
            for tab in [self.console_panel.output_tab, self.console_panel.errors_tab,
                        self.console_panel.tokens_tab, self.console_panel.ast_tab]:
                tab.text.config(
                    bg=colors.console_bg,
                    fg=colors.console_fg,
                    insertbackground=colors.console_fg,
                    selectbackground=colors.editor_selection_bg
                )

    def _apply_font_to_editors(self):
        """Aplica la fuente seleccionada a todos los editores."""
        font = self.theme.get_font()
        if hasattr(self, 'editor_panel'):
            for filename, editor in self.editor_panel.editors.items():
                editor.text.config(font=font)
                # Reconfigurar tags de sintaxis con nueva fuente
                editor._configure_syntax_tags()
                # Redibujar números de línea con nueva fuente (Canvas no soporta config font)
                editor._update_line_numbers()

    def _apply_font_size(self, size):
        """Aplica el tamaño de fuente a los editores."""
        self.theme.font_size = size
        self._apply_font_to_editors()

    def _toggle_theme(self, theme: str):
        """Cambia el tema de la aplicación."""
        self.theme.set_theme(theme)
        self._apply_theme_to_all()
        messagebox.showinfo("Tema", f"Tema '{theme}' aplicado correctamente")


def run():
    """Ejecuta la aplicación KForge."""
    app = KForgeApp()
    app.mainloop()


if __name__ == "__main__":
    run()
