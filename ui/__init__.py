"""
Módulo ui del compilador de Kotlin.
Contiene todos los componentes de la interfaz gráfica moderna.
"""

# Interfaz moderna
from ui.app_ui import KForgeApp, run as ejecutar_app
from ui.theme_manager import ThemeManager, LanguageManager, get_theme_manager, get_language_manager
from ui.editor_panel import EditorPanel, EditorWithLineNumbers
from ui.console_panel import ConsolePanel
from ui.sidebar import Sidebar
from ui.phases_panel import PhasesPanel
from ui.status_bar import StatusBar
from ui.splash_screen import SplashScreen, show_splash

__all__ = [
    'KForgeApp',
    'ejecutar_app',
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
