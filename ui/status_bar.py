"""
Barra de estado para KForge.
Muestra versión, idioma y estado actual de la compilación.
"""

import tkinter as tk
from tkinter import ttk
from ui.theme_manager import get_theme_manager, get_language_manager


class StatusBar(tk.Frame):
    """Barra de estado inferior de la aplicación."""

    VERSION = "v1.0 Alpha"

    def __init__(self, parent, **kwargs):
        """
        Inicializa la barra de estado.

        Args:
            parent: Widget padre
        """
        super().__init__(parent, **kwargs)

        # Gestores
        self.theme = get_theme_manager()
        self.lang = get_language_manager()
        colors = self.theme.get_colors()

        # Configurar estilo
        self.configure(
            bg=colors.bg_secondary,
            relief=tk.FLAT,
            bd=1,
            highlightthickness=1,
            highlightbackground=colors.border
        )

        # Crear widgets
        self._create_widgets(colors)

    def _create_widgets(self, colors):
        """Crea los widgets de la barra de estado."""
        # Frame izquierdo (estado)
        left_frame = tk.Frame(self, bg=colors.bg_secondary)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)

        # Ícono de estado
        self.status_icon = tk.Label(
            left_frame,
            text="●",
            font=("Segoe UI", 10),
            fg=colors.console_success,
            bg=colors.bg_secondary
        )
        self.status_icon.pack(side=tk.LEFT, padx=(5, 2))

        # Texto de estado
        self.status_label = tk.Label(
            left_frame,
            text=self.lang.t("status.ready"),
            font=("Segoe UI", 9),
            fg=colors.fg_secondary,
            bg=colors.bg_secondary
        )
        self.status_label.pack(side=tk.LEFT, padx=(0, 10))

        # Separador
        sep1 = tk.Label(
            left_frame,
            text="|",
            font=("Segoe UI", 9),
            fg=colors.border,
            bg=colors.bg_secondary
        )
        sep1.pack(side=tk.LEFT, padx=5)

        # Información adicional (línea, columna, etc.)
        self.info_label = tk.Label(
            left_frame,
            text="",
            font=("Segoe UI", 9),
            fg=colors.fg_tertiary,
            bg=colors.bg_secondary
        )
        self.info_label.pack(side=tk.LEFT, padx=5)

        # Frame derecho (versión, idioma)
        right_frame = tk.Frame(self, bg=colors.bg_secondary)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=2)

        # Botón de idioma
        lang_text = "ES" if self.lang.get_current_language() == "es" else "EN"
        self.lang_button = tk.Label(
            right_frame,
            text=f"🌐 {lang_text}",
            font=("Segoe UI", 9),
            fg=colors.fg_secondary,
            bg=colors.bg_secondary,
            cursor="hand2"
        )
        self.lang_button.pack(side=tk.RIGHT, padx=5)
        self.lang_button.bind("<Button-1>", self._toggle_language)

        # Separador
        sep2 = tk.Label(
            right_frame,
            text="|",
            font=("Segoe UI", 9),
            fg=colors.border,
            bg=colors.bg_secondary
        )
        sep2.pack(side=tk.RIGHT, padx=5)

        # Versión
        self.version_label = tk.Label(
            right_frame,
            text=f"{self.lang.t('status.version')}: {self.VERSION}",
            font=("Segoe UI", 9),
            fg=colors.fg_tertiary,
            bg=colors.bg_secondary
        )
        self.version_label.pack(side=tk.RIGHT, padx=5)

    def set_status(self, status: str, status_type: str = "ready"):
        """
        Establece el estado actual.

        Args:
            status: Texto del estado
            status_type: Tipo de estado ("ready", "analyzing", "completed", "error")
        """
        colors = self.theme.get_colors()

        # Cambiar ícono y color según el tipo
        icon_colors = {
            "ready": colors.console_success,
            "analyzing": colors.console_info,
            "completed": colors.console_success,
            "error": colors.console_error
        }

        self.status_icon.config(fg=icon_colors.get(status_type, colors.fg_secondary))
        self.status_label.config(text=status)

        # Animar ícono si está analizando
        if status_type == "analyzing":
            self._animate_status_icon()

    def _animate_status_icon(self):
        """Anima el ícono de estado (parpadeo)."""
        current_fg = self.status_icon.cget("fg")
        colors = self.theme.get_colors()

        # Alternar entre color normal y transparente
        if current_fg == colors.console_info:
            self.status_icon.config(fg=colors.bg_secondary)
        else:
            self.status_icon.config(fg=colors.console_info)

        # Continuar animación si aún está analizando
        if "analiz" in self.status_label.cget("text").lower():
            self.after(500, self._animate_status_icon)

    def set_info(self, info: str):
        """
        Establece la información adicional.

        Args:
            info: Texto de información (ej: "Ln 10, Col 5")
        """
        self.info_label.config(text=info)

    def set_position(self, line: int, column: int):
        """
        Establece la posición del cursor.

        Args:
            line: Número de línea
            column: Número de columna
        """
        self.set_info(f"Ln {line}, Col {column}")

    def _toggle_language(self, event=None):
        """Cambia el idioma de la aplicación."""
        self.lang.toggle_language()

        # Actualizar texto del botón
        lang_text = "ES" if self.lang.get_current_language() == "es" else "EN"
        self.lang_button.config(text=f"🌐 {lang_text}")

        # Actualizar textos de la barra
        self.version_label.config(text=f"{self.lang.t('status.version')}: {self.VERSION}")

        # Notificar cambio de idioma (el evento se propagará)
        self.event_generate("<<LanguageChanged>>")

    def update_theme(self):
        """Actualiza los colores según el tema actual."""
        colors = self.theme.get_colors()

        # Actualizar fondo y bordes
        self.configure(
            bg=colors.bg_secondary,
            highlightbackground=colors.border
        )

        # Actualizar todos los widgets
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=colors.bg_secondary)
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.configure(
                            bg=colors.bg_secondary,
                            fg=colors.fg_secondary
                        )
            elif isinstance(widget, tk.Label):
                widget.configure(
                    bg=colors.bg_secondary,
                    fg=colors.fg_secondary
                )


if __name__ == "__main__":
    # Prueba de la barra de estado
    root = tk.Tk()
    root.title("Test StatusBar")
    root.geometry("800x100")

    # Crear barra de estado
    status_bar = StatusBar(root)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # Probar diferentes estados
    def test_states():
        status_bar.set_status("Listo", "ready")
        status_bar.set_position(1, 1)

        root.after(2000, lambda: status_bar.set_status("Analizando...", "analyzing"))
        root.after(4000, lambda: status_bar.set_status("Completado", "completed"))
        root.after(6000, lambda: status_bar.set_status("Error detectado", "error"))
        root.after(8000, test_states)

    test_states()

    root.mainloop()
