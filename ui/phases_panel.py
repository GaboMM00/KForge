"""
Panel de fases del compilador para KForge.
Muestra botones para ejecutar cada fase con animaciones.
"""

import tkinter as tk
from tkinter import ttk
from ui.theme_manager import get_theme_manager, get_language_manager


class PhaseButton(tk.Frame):
    """Botón animado para una fase del compilador."""

    def __init__(self, parent, phase_name: str, command=None, **kwargs):
        """
        Inicializa el botón de fase.

        Args:
            parent: Widget padre
            phase_name: Nombre de la fase
            command: Función a ejecutar al hacer clic
        """
        super().__init__(parent, **kwargs)

        self.theme = get_theme_manager()
        self.lang = get_language_manager()
        self.phase_name = phase_name
        self.command = command
        self.is_running = False
        self.is_completed = False

        colors = self.theme.get_colors()
        self.configure(bg=colors.bg_secondary)

        self._create_ui(colors)

    def _create_ui(self, colors):
        """Crea la interfaz del botón."""
        # Frame principal con hover effect
        self.button_frame = tk.Frame(
            self,
            bg=colors.button_bg,
            relief=tk.RAISED,
            bd=1,
            cursor="hand2"
        )
        self.button_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Ícono de estado
        self.status_icon = tk.Label(
            self.button_frame,
            text="○",
            font=("Segoe UI", 14),
            fg=colors.fg_tertiary,
            bg=colors.button_bg
        )
        self.status_icon.pack(side=tk.LEFT, padx=(10, 5))

        # Texto del botón
        phase_text = self.lang.t(f"phases.{self.phase_name.lower()}")
        self.label = tk.Label(
            self.button_frame,
            text=phase_text,
            font=("Segoe UI", 10, "bold"),
            fg=colors.button_fg,
            bg=colors.button_bg
        )
        self.label.pack(side=tk.LEFT, padx=5)

        # Bind events
        self.button_frame.bind("<Button-1>", self._on_click)
        self.button_frame.bind("<Enter>", self._on_enter)
        self.button_frame.bind("<Leave>", self._on_leave)
        self.label.bind("<Button-1>", self._on_click)
        self.status_icon.bind("<Button-1>", self._on_click)

    def _on_click(self, event=None):
        """Maneja el clic en el botón."""
        if self.command and not self.is_running:
            self.command()

    def _on_enter(self, event=None):
        """Maneja el hover sobre el botón."""
        if not self.is_running:
            colors = self.theme.get_colors()
            self.button_frame.config(bg=colors.button_hover)
            self.label.config(bg=colors.button_hover)
            self.status_icon.config(bg=colors.button_hover)

    def _on_leave(self, event=None):
        """Maneja cuando el cursor sale del botón."""
        colors = self.theme.get_colors()
        self.button_frame.config(bg=colors.button_bg)
        self.label.config(bg=colors.button_bg)
        self.status_icon.config(bg=colors.button_bg)

    def start_animation(self):
        """Inicia la animación de procesamiento."""
        self.is_running = True
        self.is_completed = False
        colors = self.theme.get_colors()

        # Cambiar ícono a "procesando"
        self.status_icon.config(text="⟳", fg=colors.console_info)
        self._animate_rotation()

    def _animate_rotation(self):
        """Anima el ícono de rotación."""
        if self.is_running:
            # Rotar ícono (simulado con diferentes caracteres)
            icons = ["⟳", "⟲", "⟳", "⟲"]
            current_text = self.status_icon.cget("text")

            if current_text in icons:
                current_idx = icons.index(current_text)
                next_idx = (current_idx + 1) % len(icons)
                self.status_icon.config(text=icons[next_idx])

            self.after(200, self._animate_rotation)

    def complete(self, success: bool = True):
        """
        Marca la fase como completada.

        Args:
            success: True si fue exitosa, False si hubo error
        """
        self.is_running = False
        self.is_completed = True
        colors = self.theme.get_colors()

        if success:
            self.status_icon.config(text="✓", fg=colors.console_success)
        else:
            self.status_icon.config(text="✗", fg=colors.console_error)

    def reset(self):
        """Resetea el estado del botón."""
        self.is_running = False
        self.is_completed = False
        colors = self.theme.get_colors()
        self.status_icon.config(text="○", fg=colors.fg_tertiary)


class PhasesPanel(tk.Frame):
    """Panel con botones para todas las fases del compilador."""

    def __init__(self, parent, controller=None, **kwargs):
        """
        Inicializa el panel de fases.

        Args:
            parent: Widget padre
            controller: Instancia del CompiladorController
        """
        super().__init__(parent, **kwargs)

        self.theme = get_theme_manager()
        self.lang = get_language_manager()
        self.controller = controller

        colors = self.theme.get_colors()
        self.configure(bg=colors.bg_secondary, relief=tk.FLAT, bd=1)

        # Crear botones de fases
        self.phase_buttons = {}
        self._create_ui(colors)

    def _create_ui(self, colors):
        """Crea la interfaz del panel."""
        # Título del panel
        title_frame = tk.Frame(self, bg=colors.bg_secondary)
        title_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=(5, 0))

        title_label = tk.Label(
            title_frame,
            text=self.lang.t("menu.compiler"),
            font=("Segoe UI", 10, "bold"),
            fg=colors.fg_primary,
            bg=colors.bg_secondary
        )
        title_label.pack(side=tk.LEFT, padx=5)

        # Botón de reset
        reset_btn = tk.Label(
            title_frame,
            text="↻",
            font=("Segoe UI", 12),
            fg=colors.fg_tertiary,
            bg=colors.bg_secondary,
            cursor="hand2"
        )
        reset_btn.pack(side=tk.RIGHT, padx=5)
        reset_btn.bind("<Button-1>", lambda e: self.reset_all())

        # Frame para los botones
        buttons_frame = tk.Frame(self, bg=colors.bg_secondary)
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Crear botones para cada fase
        phases = [
            ("lexical", self._run_lexical),
            ("syntactic", self._run_syntactic),
            ("semantic", self._run_semantic),
            ("codegen", self._run_codegen)
        ]

        for i, (phase, command) in enumerate(phases):
            btn = PhaseButton(buttons_frame, phase, command=command)
            btn.grid(row=0, column=i, sticky="nsew", padx=2)
            buttons_frame.grid_columnconfigure(i, weight=1)
            self.phase_buttons[phase] = btn

    def _run_lexical(self):
        """Ejecuta el análisis léxico."""
        self.event_generate("<<RunLexical>>")

    def _run_syntactic(self):
        """Ejecuta el análisis sintáctico."""
        self.event_generate("<<RunSyntactic>>")

    def _run_semantic(self):
        """Ejecuta el análisis semántico."""
        self.event_generate("<<RunSemantic>>")

    def _run_codegen(self):
        """Ejecuta la generación de código."""
        self.event_generate("<<RunCodeGen>>")

    def set_phase_running(self, phase: str):
        """
        Marca una fase como en ejecución.

        Args:
            phase: Nombre de la fase
        """
        if phase in self.phase_buttons:
            self.phase_buttons[phase].start_animation()

    def set_phase_completed(self, phase: str, success: bool = True):
        """
        Marca una fase como completada.

        Args:
            phase: Nombre de la fase
            success: True si fue exitosa
        """
        if phase in self.phase_buttons:
            self.phase_buttons[phase].complete(success)

    def reset_all(self):
        """Resetea todos los botones de fase."""
        for button in self.phase_buttons.values():
            button.reset()

    def reset_phase(self, phase: str):
        """
        Resetea una fase específica.

        Args:
            phase: Nombre de la fase
        """
        if phase in self.phase_buttons:
            self.phase_buttons[phase].reset()


if __name__ == "__main__":
    # Prueba del panel de fases
    root = tk.Tk()
    root.title("Test Phases Panel")
    root.geometry("800x100")

    panel = PhasesPanel(root)
    panel.pack(fill=tk.BOTH, expand=True)

    # Simular ejecución de fases
    def test_phases():
        panel.reset_all()

        # Lexical
        root.after(1000, lambda: panel.set_phase_running("lexical"))
        root.after(2000, lambda: panel.set_phase_completed("lexical", True))

        # Syntactic
        root.after(2500, lambda: panel.set_phase_running("syntactic"))
        root.after(3500, lambda: panel.set_phase_completed("syntactic", True))

        # Semantic
        root.after(4000, lambda: panel.set_phase_running("semantic"))
        root.after(5000, lambda: panel.set_phase_completed("semantic", False))

        # Repetir
        root.after(7000, test_phases)

    test_phases()

    root.mainloop()
