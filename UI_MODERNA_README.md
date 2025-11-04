# KForge - Interfaz Moderna

## Nueva Interfaz Modular

KForge ahora incluye una interfaz moderna completamente refactorizada con diseño tipo JetBrains/VSCode.

## Ejecución

```bash
# Interfaz moderna (recomendada)
python main_modern.py

# Interfaz clásica (legacy)
python main.py
```

## Estructura Modular

```
ui/
├── app_ui.py               # Aplicación principal integrada
├── theme_manager.py        # Gestión de temas y idiomas
├── splash_screen.py        # Pantalla de inicio animada
├── editor_panel.py         # Editor con pestañas y resaltado
├── console_panel.py        # Consola con 4 pestañas
├── sidebar.py              # Barra lateral tipo VSCode
├── phases_panel.py         # Panel de fases del compilador
├── status_bar.py           # Barra de estado inferior
├── editor.py               # Editor clásico (legacy)
├── consola.py              # Consola clásica (legacy)
└── interfaz.py             # Interfaz clásica (legacy)

resources/
├── keywords.json           # Palabras clave y colores compartidos
└── lang.json               # Traducciones ES/EN
```

## Características de la Nueva UI

### 🎨 Temas

- **Tema Oscuro** (Darcula de JetBrains) - Por defecto
- **Tema Claro** (IntelliJ Light)
- Cambio desde menú: `Ver → Tema`

### 🌍 Multilenguaje

- Español (ES) - Por defecto
- Inglés (EN)
- Cambio con clic en barra de estado o menú

### 📝 Editor Avanzado

- **Pestañas** para múltiples archivos
- **Numeración de líneas** sincronizada
- **Resaltado de sintaxis** Kotlin usando `keywords.json`
- **Atajos de teclado**:
  - `Ctrl+N` - Nuevo archivo
  - `Ctrl+O` - Abrir archivo
  - `Ctrl+S` - Guardar archivo

### 🔧 Panel de Fases

Botones animados para cada fase del compilador:

- **Léxico** (F5) - Con icono animado durante ejecución
- **Sintáctico** (F6) - Marca verde ✓ al completar
- **Semántico** (F7) - Marca roja ✗ si hay error
- **Código Intermedio** (F9) - Placeholder

### 📊 Consola Multi-Pestaña

4 pestañas especializadas:

1. **Salida** - Resultados generales
2. **Errores** - Mensajes de error en rojo
3. **Tokens** - Tabla formateada de tokens
4. **AST** - Visualización del árbol sintáctico

### 🎯 Barra Lateral (Sidebar)

Iconos estilo VSCode:

- 📁 **Archivos** - Navegador de archivos (futuro)
- 🔤 **Tokens** - Vista de tokens
- 🌳 **AST** - Vista de árbol
- ⚙ **Configuración** - Preferencias

### 📍 Barra de Estado

Muestra:

- Estado actual (Listo/Analizando/Completado/Error)
- Posición del cursor (Línea, Columna)
- Versión de KForge
- Idioma actual (clic para cambiar)

### ✨ Splash Screen

Pantalla de inicio con:

- Logo de KForge
- Animación de carga
- Efecto de fade-out

## Configuración de Temas

### Personalizar Colores

Editar `ui/theme_manager.py`:

```python
DARK_THEME = ThemeColors(
    bg_primary="#2B2B2B",      # Fondo principal
    accent="#4A88C7",           # Color de acento
    syntax_keyword="#CC7832",   # Palabras clave
    # ... más colores
)
```

### Usar Colores desde keywords.json

Los colores de sintaxis se cargan automáticamente desde `resources/keywords.json`:

```json
{
  "colors": {
    "keyword": "#CC7832",
    "type": "#A9B7C6",
    "string": "#6A8759",
    "number": "#6897BB",
    "comment": "#808080"
  }
}
```

## Personalización de Fuentes

Fuentes disponibles:

- JetBrains Mono
- Fira Code
- Consolas (por defecto)
- Source Code Pro
- Courier New

Cambiar en `theme_manager.py`:

```python
theme = get_theme_manager()
theme.set_font("JetBrains Mono")
theme.font_size = 12
```

## Agregar Nuevas Palabras Clave

1. Editar `resources/keywords.json`:

```json
{
  "keywords": [
    "var", "val", "fun", "when",  // Añadir aquí
  ]
}
```

2. El resaltador las detectará automáticamente

## Agregar Nuevos Idiomas

Editar `resources/lang.json`:

```json
{
  "fr": {
    "app_title": "KForge - Compilateur Kotlin",
    "menu": {
      "file": "Fichier",
      // ...
    }
  }
}
```

Activar en `theme_manager.py`:

```python
lang_manager.set_language("fr")
```

## Integración con el Compilador

La interfaz se comunica con el compilador **únicamente** a través de `CompiladorController`:

```python
from core.controller import CompiladorController

controller = CompiladorController()
resultado = controller.ejecutar(codigo)

# Mostrar en UI
console.show_results(resultado)
phases_panel.set_phase_completed("semantic", resultado["exito"])
```

## Eventos Personalizados

La UI usa eventos de Tkinter para comunicación entre componentes:

```python
# Emitir evento
phases_panel.event_generate("<<RunLexical>>")

# Escuchar evento
phases_panel.bind("<<RunLexical>>", lambda e: run_lexical())
```

## Arquitectura

### Separación de Responsabilidades

```
UI (Presentación)
    ↓
Controller (Coordinación)
    ↓
Core (Lógica del Compilador)
```

### Flujo de Datos

```
Usuario → Editor → Controller → Lexer/Parser/Semantic
                                      ↓
Usuario ← Consola ← Controller ← Resultados
```

## Ventajas de la Nueva UI

1. **Modularidad**: Cada componente es independiente
2. **Extensibilidad**: Fácil agregar nuevos paneles o temas
3. **Mantenibilidad**: Código organizado por responsabilidad
4. **Multilenguaje**: Soporte nativo para i18n
5. **Temas**: Oscuro/claro con colores personalizables
6. **Modernidad**: Diseño similar a IDEs profesionales

## Comparación: Clásica vs Moderna

| Característica | Clásica | Moderna |
|---|---|---|
| Pestañas de editor | ❌ | ✅ |
| Temas | ❌ | ✅ Oscuro/Claro |
| Multilenguaje | ❌ | ✅ ES/EN |
| Splash Screen | ❌ | ✅ Animado |
| Consola multi-pestaña | ❌ | ✅ 4 pestañas |
| Sidebar | ❌ | ✅ Tipo VSCode |
| Panel de fases | ❌ | ✅ Con animaciones |
| Barra de estado | ❌ | ✅ Completa |
| Resaltado sintaxis | Básico | ✅ keywords.json |
| Keywords compartidos | ❌ | ✅ JSON centralizado |

## Próximas Mejoras

- [ ] Split view (editor dividido)
- [ ] Navegador de archivos funcional
- [ ] Autocompletado de código
- [ ] Minimap del código
- [ ] Búsqueda y reemplazo avanzado
- [ ] Vista gráfica del AST
- [ ] Temas personalizados del usuario
- [ ] Plugins y extensiones

## Problemas Conocidos

- El cambio de tema requiere reinicio de la aplicación
- La sidebar es decorativa (funcionalidad limitada)
- No hay soporte para zoom con Ctrl+Mouse

## Contribuir

Para agregar nuevos componentes UI:

1. Crear módulo en `ui/nuevo_componente.py`
2. Heredar de `tk.Frame`
3. Usar `get_theme_manager()` para colores
4. Usar `get_language_manager()` para textos
5. Emitir eventos con `event_generate()`
6. Agregar a `ui/__init__.py`

## Soporte

- Requiere Python 3.8+
- Tkinter (incluido en Python estándar)
- No requiere dependencias adicionales

---

**KForge Compiler Suite v1.0 Alpha**

*Modular Kotlin Compiler Environment*
