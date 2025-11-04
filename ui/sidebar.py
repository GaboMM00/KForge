"""
Barra lateral funcional para KForge.
Gestiona archivos, configuración y visibilidad de la consola.
"""

import tkinter as tk
from tkinter import ttk
from ui.theme_manager import get_theme_manager


class Tooltip:
    """Tooltip simple para mostrar ayuda al pasar el mouse."""

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None

        self.widget.bind("<Enter>", self._show_tooltip)
        self.widget.bind("<Leave>", self._hide_tooltip)

    def _show_tooltip(self, event=None):
        """Muestra el tooltip."""
        if self.tooltip_window or not self.text:
            return

        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 5
        y = self.widget.winfo_rooty() + self.widget.winfo_height() // 2

        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            background="#2B2B2B",
            foreground="#CCCCCC",
            relief=tk.SOLID,
            borderwidth=1,
            font=("Segoe UI", 9),
            padx=5,
            pady=3
        )
        label.pack()

    def _hide_tooltip(self, event=None):
        """Oculta el tooltip."""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class SidebarButton(tk.Label):
    """Botón de la barra lateral con tooltip."""

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
        self.is_active = False

        # Añadir tooltip
        Tooltip(self, tooltip)

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_click(self, event):
        if self.command:
            self.command()

    def _on_enter(self, event):
        if not self.is_active:
            colors = self.theme.get_colors()
            self.config(bg=colors.button_hover, fg=colors.accent)

    def _on_leave(self, event):
        if not self.is_active:
            colors = self.theme.get_colors()
            self.config(bg=colors.bg_secondary, fg=colors.fg_tertiary)

    def set_active(self, active: bool):
        """Marca el botón como activo/inactivo."""
        self.is_active = active
        colors = self.theme.get_colors()
        if active:
            self.config(fg=colors.accent, bg=colors.bg_tertiary)
        else:
            self.config(fg=colors.fg_tertiary, bg=colors.bg_secondary)


class Sidebar(tk.Frame):
    """Barra lateral funcional con gestión de archivos, configuración y terminal."""

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
        self.is_visible = True

        self._create_buttons()

    def _create_buttons(self):
        """Crea los botones de la barra lateral."""
        # Botones superiores
        buttons_config = [
            ("files", "📁", "Gestión de Archivos (Ctrl+O)"),
            ("settings", "⚙️", "Configuración"),
            ("terminal", "💬", "Mostrar/Ocultar Terminal"),
        ]

        for btn_id, icon, tooltip in buttons_config:
            btn = SidebarButton(
                self,
                icon,
                tooltip,
                command=lambda b=btn_id: self._on_button_click(b)
            )
            btn.pack(pady=8, padx=5)
            self.buttons[btn_id] = btn

        # Separador
        separator = tk.Frame(self, bg=self.theme.get_colors().fg_tertiary, height=1)
        separator.pack(fill=tk.X, padx=10, pady=10)

        # Botón de colapsar en la parte inferior
        collapse_btn = SidebarButton(
            self,
            "◀",
            "Ocultar Barra Lateral",
            command=self._toggle_sidebar
        )
        collapse_btn.pack(side=tk.BOTTOM, pady=8, padx=5)
        self.buttons["collapse"] = collapse_btn

    def _on_button_click(self, button_id: str):
        """Maneja el clic en un botón."""
        # Terminal no mantiene estado activo
        if button_id == "terminal":
            self.event_generate("<<SidebarTerminal>>")
            return

        # Desactivar botón anterior
        if self.active_button and self.active_button in self.buttons:
            self.buttons[self.active_button].set_active(False)

        # Activar nuevo botón
        if button_id in self.buttons:
            self.buttons[button_id].set_active(True)
            self.active_button = button_id

        # Generar evento
        if button_id == "files":
            self.event_generate("<<SidebarFiles>>")
        elif button_id == "settings":
            self.event_generate("<<SidebarSettings>>")

    def _toggle_sidebar(self):
        """Colapsa/expande la barra lateral."""
        if self.is_visible:
            self.config(width=0)
            self.pack_propagate(True)
            self.is_visible = False
        else:
            self.config(width=50)
            self.pack_propagate(False)
            self.is_visible = True

        self.event_generate("<<SidebarToggle>>")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Sidebar")
    root.geometry("60x400")

    sidebar = Sidebar(root)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    root.mainloop()
