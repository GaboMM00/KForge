"""
Módulo ui del compilador de Kotlin.
Contiene todos los componentes de la interfaz gráfica.
"""

# Interfaz clásica (legacy)
from ui.editor import EditorConLineas
from ui.consola import ConsolaSalida
from ui.interfaz import InterfazCompilador, ejecutar_interfaz

# Interfaz moderna
from ui.app_ui import KForgeApp, run as ejecutar_moderna
from ui.theme_manager import ThemeManager, LanguageManager, get_theme_manager, get_language_manager
from ui.editor_panel import EditorPanel, EditorWithLineNumbers
from ui.console_panel import ConsolePanel
from ui.sidebar import Sidebar
from ui.phases_panel import PhasesPanel
from ui.status_bar import StatusBar
from ui.splash_screen import SplashScreen, show_splash

__all__ = [
    # Legacy
    'EditorConLineas',
    'ConsolaSalida',
    'InterfazCompilador',
    'ejecutar_interfaz',
    # Moderna
    'KForgeApp',
    'ejecutar_moderna',
    'ThemeManager',
    'LanguageManager',
    'get_theme_manager',
    'get_language_manager',
    'EditorPanel',
    'EditorWithLineNumbers',
    'ConsolePanel',
    'Sidebar',
    'PhasesPanel',
    'StatusBar',
    'SplashScreen',
    'show_splash'
]
