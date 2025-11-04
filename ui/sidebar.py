"""
Barra lateral tipo VSCode para KForge.
Permite alternar entre diferentes vistas (archivos, tokens, AST, configuración).
"""

import tkinter as tk
from ui.theme_manager import get_theme_manager


class SidebarButton(tk.Label):
    """Botón de la barra lateral."""

    def __init__(self, parent, icon: str, tooltip: str, command=None, **kwargs):
        self.theme = get_theme_manager()
        colors = self.theme.get_colors()

        super().__init__(
            parent,
            text=icon,
            font=("Segoe UI", 18),
            fg=colors.fg_tertiary,
            bg=colors.bg_secondary,
            cursor="hand2",
            width=3,
            height=1,
            **kwargs
        )

        self.command = command
        self.tooltip = tooltip
        self.is_active = False

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_click(self, event):
        if self.command:
            self.command()

    def _on_enter(self, event):
        if not self.is_active:
            colors = self.theme.get_colors()
            self.config(bg=colors.button_hover)

    def _on_leave(self, event):
        if not self.is_active:
            colors = self.theme.get_colors()
            self.config(bg=colors.bg_secondary)

    def set_active(self, active: bool):
        """Marca el botón como activo/inactivo."""
        self.is_active = active
        colors = self.theme.get_colors()
        if active:
            self.config(fg=colors.accent, bg=colors.bg_tertiary)
        else:
            self.config(fg=colors.fg_tertiary, bg=colors.bg_secondary)


class Sidebar(tk.Frame):
    """Barra lateral con iconos tipo VSCode."""

    def __init__(self, parent, **kwargs):
        self.theme = get_theme_manager()
        colors = self.theme.get_colors()

        super().__init__(
            parent,
            bg=colors.bg_secondary,
            width=50,
            relief=tk.FLAT,
            bd=1,
            **kwargs
        )

        self.pack_propagate(False)
        self.buttons = {}
        self.active_button = None

        self._create_buttons()

    def _create_buttons(self):
        """Crea los botones de la barra lateral."""
        buttons_config = [
            ("files", "📁", "Archivos"),
            ("tokens", "🔤", "Tokens"),
            ("ast", "🌳", "AST"),
            ("settings", "⚙", "Configuración"),
        ]

        for btn_id, icon, tooltip in buttons_config:
            btn = SidebarButton(
                self,
                icon,
                tooltip,
                command=lambda b=btn_id: self._on_button_click(b)
            )
            btn.pack(pady=5)
            self.buttons[btn_id] = btn

    def _on_button_click(self, button_id: str):
        """Maneja el clic en un botón."""
        # Desactivar botón anterior
        if self.active_button and self.active_button in self.buttons:
            self.buttons[self.active_button].set_active(False)

        # Activar nuevo botón
        if button_id in self.buttons:
            self.buttons[button_id].set_active(True)
            self.active_button = button_id

        # Generar evento
        self.event_generate(f"<<Sidebar{button_id.capitalize()}>>")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Sidebar")
    root.geometry("60x400")

    sidebar = Sidebar(root)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    root.mainloop()
