"""
Gestor de temas para KForge.
Maneja temas oscuro/claro, fuentes y colores de la interfaz.
"""

import json
import os
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class ThemeColors:
    """Colores del tema."""
    # Colores principales
    bg_primary: str
    bg_secondary: str
    bg_tertiary: str
    fg_primary: str
    fg_secondary: str
    fg_tertiary: str

    # Colores de acento
    accent: str
    accent_hover: str
    accent_active: str

    # Colores del editor
    editor_bg: str
    editor_fg: str
    editor_line_numbers_bg: str
    editor_line_numbers_fg: str
    editor_current_line: str
    editor_selection_bg: str
    editor_selection_fg: str

    # Colores de la consola
    console_bg: str
    console_fg: str
    console_error: str
    console_warning: str
    console_success: str
    console_info: str

    # Colores de sintaxis (cargados desde keywords.json)
    syntax_keyword: str
    syntax_type: str
    syntax_string: str
    syntax_number: str
    syntax_comment: str
    syntax_operator: str
    syntax_function: str

    # Colores de UI
    border: str
    button_bg: str
    button_fg: str
    button_hover: str
    scrollbar_bg: str
    scrollbar_fg: str


class ThemeManager:
    """Gestor centralizado de temas de la aplicación."""

    # Tema oscuro (JetBrains Darcula)
    DARK_THEME = ThemeColors(
        # Principales
        bg_primary="#2B2B2B",
        bg_secondary="#3C3F41",
        bg_tertiary="#313335",
        fg_primary="#A9B7C6",
        fg_secondary="#787878",
        fg_tertiary="#6C6C6C",

        # Acentos
        accent="#4A88C7",
        accent_hover="#5394D1",
        accent_active="#3D7AB8",

        # Editor
        editor_bg="#2B2B2B",
        editor_fg="#A9B7C6",
        editor_line_numbers_bg="#313335",
        editor_line_numbers_fg="#606366",
        editor_current_line="#323232",
        editor_selection_bg="#214283",
        editor_selection_fg="#FFFFFF",

        # Consola
        console_bg="#1E1E1E",
        console_fg="#CCCCCC",
        console_error="#F48771",
        console_warning="#D8A657",
        console_success="#629755",
        console_info="#6897BB",

        # Sintaxis (JetBrains)
        syntax_keyword="#CC7832",
        syntax_type="#A9B7C6",
        syntax_string="#6A8759",
        syntax_number="#6897BB",
        syntax_comment="#808080",
        syntax_operator="#A9B7C6",
        syntax_function="#FFC66D",

        # UI
        border="#323232",
        button_bg="#3C3F41",
        button_fg="#A9B7C6",
        button_hover="#4C5052",
        scrollbar_bg="#3C3F41",
        scrollbar_fg="#5A5A5A"
    )

    # Tema claro (JetBrains Light)
    LIGHT_THEME = ThemeColors(
        # Principales
        bg_primary="#FFFFFF",
        bg_secondary="#F5F5F5",
        bg_tertiary="#EEEEEE",
        fg_primary="#000000",
        fg_secondary="#555555",
        fg_tertiary="#888888",

        # Acentos
        accent="#2470B3",
        accent_hover="#1E5C8F",
        accent_active="#1A4F7F",

        # Editor
        editor_bg="#FFFFFF",
        editor_fg="#000000",
        editor_line_numbers_bg="#F0F0F0",
        editor_line_numbers_fg="#999999",
        editor_current_line="#F0F8FF",
        editor_selection_bg="#D5E8FF",
        editor_selection_fg="#000000",

        # Consola
        console_bg="#FFFFFF",
        console_fg="#000000",
        console_error="#BC3F3C",
        console_warning="#B58900",
        console_success="#2B7A0B",
        console_info="#1764A0",

        # Sintaxis (Light)
        syntax_keyword="#0033B3",
        syntax_type="#000000",
        syntax_string="#067D17",
        syntax_number="#1750EB",
        syntax_comment="#8C8C8C",
        syntax_operator="#000000",
        syntax_function="#00627A",

        # UI
        border="#D0D0D0",
        button_bg="#F5F5F5",
        button_fg="#000000",
        button_hover="#E5E5E5",
        scrollbar_bg="#F5F5F5",
        scrollbar_fg="#AAAAAA"
    )

    # Fuentes disponibles
    FONTS = {
        "JetBrains Mono": "JetBrains Mono",
        "Fira Code": "Fira Code",
        "Consolas": "Consolas",
        "Source Code Pro": "Source Code Pro",
        "Courier New": "Courier New"
    }

    def __init__(self):
        """Inicializa el gestor de temas."""
        self.current_theme = "dark"
        self.current_font = "Consolas"
        self.font_size = 11
        self.keywords = self._load_keywords()

    def _load_keywords(self) -> Dict[str, Any]:
        """Carga las palabras clave desde keywords.json."""
        try:
            keywords_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "resources",
                "keywords.json"
            )
            with open(keywords_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error al cargar keywords.json: {e}")
            return {
                "keywords": [],
                "types": [],
                "operators": [],
                "colors": {}
            }

    def get_colors(self) -> ThemeColors:
        """Obtiene los colores del tema actual."""
        if self.current_theme == "dark":
            return self.DARK_THEME
        else:
            return self.LIGHT_THEME

    def set_theme(self, theme: str):
        """
        Cambia el tema actual.

        Args:
            theme: "dark" o "light"
        """
        if theme in ["dark", "light"]:
            self.current_theme = theme

    def toggle_theme(self):
        """Alterna entre tema oscuro y claro."""
        self.current_theme = "light" if self.current_theme == "dark" else "dark"

    def get_font(self) -> tuple:
        """Obtiene la fuente actual como tupla (nombre, tamaño)."""
        return (self.current_font, self.font_size)

    def set_font(self, font_name: str):
        """
        Cambia la fuente actual.

        Args:
            font_name: Nombre de la fuente (debe estar en FONTS)
        """
        if font_name in self.FONTS.values():
            self.current_font = font_name

    def increase_font_size(self):
        """Aumenta el tamaño de fuente."""
        if self.font_size < 24:
            self.font_size += 1

    def decrease_font_size(self):
        """Disminuye el tamaño de fuente."""
        if self.font_size > 8:
            self.font_size -= 1

    def reset_font_size(self):
        """Restablece el tamaño de fuente por defecto."""
        self.font_size = 11

    def get_keywords(self) -> list:
        """Obtiene la lista de palabras clave."""
        return self.keywords.get("keywords", [])

    def get_types(self) -> list:
        """Obtiene la lista de tipos."""
        return self.keywords.get("types", [])

    def get_operators(self) -> list:
        """Obtiene la lista de operadores."""
        return self.keywords.get("operators", [])

    def get_modifiers(self) -> list:
        """Obtiene la lista de modificadores."""
        return self.keywords.get("modifiers", [])

    def get_syntax_colors(self) -> Dict[str, str]:
        """Obtiene los colores de sintaxis desde keywords.json o tema."""
        # Preferir colores de keywords.json si existen
        if "colors" in self.keywords:
            return self.keywords["colors"]

        # Fallback a colores del tema
        colors = self.get_colors()
        return {
            "keyword": colors.syntax_keyword,
            "type": colors.syntax_type,
            "string": colors.syntax_string,
            "number": colors.syntax_number,
            "comment": colors.syntax_comment,
            "operator": colors.syntax_operator,
            "function": colors.syntax_function
        }


class LanguageManager:
    """Gestor de traducciones."""

    def __init__(self, language: str = "es"):
        """
        Inicializa el gestor de idiomas.

        Args:
            language: Código de idioma ("es" o "en")
        """
        self.current_language = language
        self.translations = self._load_translations()

    def _load_translations(self) -> Dict[str, Any]:
        """Carga las traducciones desde lang.json."""
        try:
            lang_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "resources",
                "lang.json"
            )
            with open(lang_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error al cargar lang.json: {e}")
            return {"es": {}, "en": {}}

    def get_text(self, key_path: str) -> str:
        """
        Obtiene un texto traducido.

        Args:
            key_path: Ruta de la clave separada por puntos (ej: "menu.file")

        Returns:
            Texto traducido o la clave si no se encuentra.
        """
        keys = key_path.split('.')
        current = self.translations.get(self.current_language, {})

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return key_path

        return str(current)

    def t(self, key_path: str) -> str:
        """Alias corto para get_text."""
        return self.get_text(key_path)

    def set_language(self, language: str):
        """
        Cambia el idioma actual.

        Args:
            language: Código de idioma ("es" o "en")
        """
        if language in self.translations:
            self.current_language = language

    def toggle_language(self):
        """Alterna entre español e inglés."""
        self.current_language = "en" if self.current_language == "es" else "es"

    def get_current_language(self) -> str:
        """Obtiene el código del idioma actual."""
        return self.current_language


# Instancias globales (singleton)
_theme_manager = None
_language_manager = None


def get_theme_manager() -> ThemeManager:
    """Obtiene la instancia global del gestor de temas."""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager


def get_language_manager() -> LanguageManager:
    """Obtiene la instancia global del gestor de idiomas."""
    global _language_manager
    if _language_manager is None:
        _language_manager = LanguageManager()
    return _language_manager
