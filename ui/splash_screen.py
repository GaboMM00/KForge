"""
Pantalla de inicio (Splash Screen) para KForge.
Muestra el logo y nombre de la aplicación durante la carga.
"""

import tkinter as tk
from tkinter import ttk
from ui.theme_manager import get_theme_manager


class SplashScreen(tk.Toplevel):
    """Pantalla de inicio de KForge."""

    def __init__(self, parent=None):
        """
        Inicializa la pantalla de inicio.

        Args:
            parent: Ventana padre (None para ventana independiente)
        """
        super().__init__(parent)

        # Configuración de la ventana
        self.title("")
        self.overrideredirect(True)  # Sin bordes ni barra de título

        # Dimensiones
        width = 600
        height = 400

        # Centrar en pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")

        # Tema
        self.theme = get_theme_manager()
        colors = self.theme.get_colors()

        # Configurar fondo
        self.configure(bg=colors.bg_primary)

        # Crear interfaz
        self._create_ui(colors)

        # Hacer la ventana modal
        self.transient(parent)
        if parent:
            self.grab_set()

    def _create_ui(self, colors):
        """Crea la interfaz de la splash screen."""
        # Frame principal
        main_frame = tk.Frame(self, bg=colors.bg_primary)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        # Logo (espacio reservado para futuro logo)
        logo_frame = tk.Frame(main_frame, bg=colors.bg_primary, height=150)
        logo_frame.pack(fill=tk.X, pady=(0, 20))

        # Círculo simulado como logo (mientras se crea el logo real)
        canvas = tk.Canvas(
            logo_frame,
            width=120,
            height=120,
            bg=colors.bg_primary,
            highlightthickness=0
        )
        canvas.pack()

        # Dibujar logo circular con gradiente simulado
        self._draw_logo(canvas, colors)

        # Nombre de la aplicación
        title_label = tk.Label(
            main_frame,
            text="KForge",
            font=("Segoe UI", 48, "bold"),
            fg=colors.accent,
            bg=colors.bg_primary
        )
        title_label.pack(pady=(10, 5))

        # Subtítulo
        subtitle_label = tk.Label(
            main_frame,
            text="Compiler Suite",
            font=("Segoe UI", 18),
            fg=colors.fg_secondary,
            bg=colors.bg_primary
        )
        subtitle_label.pack(pady=(0, 5))

        # Descripción
        desc_label = tk.Label(
            main_frame,
            text="Modular Kotlin Compiler Environment",
            font=("Segoe UI", 11),
            fg=colors.fg_tertiary,
            bg=colors.bg_primary
        )
        desc_label.pack(pady=(0, 30))

        # Barra de progreso
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=400
        )
        self.progress.pack(pady=(0, 10))
        self.progress.start(10)

        # Mensaje de carga
        self.status_label = tk.Label(
            main_frame,
            text="Iniciando...",
            font=("Segoe UI", 9),
            fg=colors.fg_tertiary,
            bg=colors.bg_primary
        )
        self.status_label.pack()

        # Versión en la esquina inferior
        version_label = tk.Label(
            main_frame,
            text="v1.0 Alpha",
            font=("Segoe UI", 8),
            fg=colors.fg_tertiary,
            bg=colors.bg_primary
        )
        version_label.pack(side=tk.BOTTOM, anchor=tk.E)

    def _draw_logo(self, canvas, colors):
        """
        Dibuja un logo temporal en el canvas.

        Args:
            canvas: Canvas donde dibujar
            colors: Colores del tema
        """
        center_x, center_y = 60, 60
        radius = 50

        # Círculo exterior
        canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            outline=colors.accent,
            width=3,
            fill=colors.bg_secondary
        )

        # Círculo interior (más pequeño)
        inner_radius = 35
        canvas.create_oval(
            center_x - inner_radius, center_y - inner_radius,
            center_x + inner_radius, center_y + inner_radius,
            outline=colors.accent,
            width=2,
            fill=colors.bg_tertiary
        )

        # Letra "K" estilizada en el centro
        canvas.create_text(
            center_x, center_y,
            text="K",
            font=("Segoe UI", 36, "bold"),
            fill=colors.accent
        )

        # Líneas decorativas
        canvas.create_line(
            center_x - 30, center_y - 30,
            center_x + 30, center_y + 30,
            fill=colors.accent,
            width=2
        )
        canvas.create_line(
            center_x - 30, center_y + 30,
            center_x + 30, center_y - 30,
            fill=colors.accent,
            width=2
        )

    def update_status(self, message: str):
        """
        Actualiza el mensaje de estado.

        Args:
            message: Nuevo mensaje a mostrar
        """
        self.status_label.config(text=message)
        self.update()

    def close_with_fade(self, duration: int = 500):
        """
        Cierra la splash screen con efecto de desvanecimiento.

        Args:
            duration: Duración del fade en milisegundos
        """
        steps = 20
        delay = duration // steps

        def fade_step(alpha):
            if alpha > 0:
                self.attributes('-alpha', alpha)
                self.after(delay, lambda: fade_step(alpha - 0.05))
            else:
                self.destroy()

        # Iniciar fade
        self.attributes('-alpha', 1.0)
        fade_step(1.0)

    def close(self):
        """Cierra la splash screen inmediatamente."""
        self.progress.stop()
        self.destroy()


def show_splash(parent=None, duration: int = 2000):
    """
    Muestra la splash screen durante un tiempo determinado.

    Args:
        parent: Ventana padre
        duration: Duración en milisegundos

    Returns:
        Instancia de SplashScreen
    """
    splash = SplashScreen(parent)

    # Cerrar automáticamente después del tiempo especificado
    def auto_close():
        splash.close_with_fade()

    splash.after(duration, auto_close)

    return splash


if __name__ == "__main__":
    # Prueba de la splash screen
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal

    splash = show_splash(root, duration=3000)

    root.mainloop()
