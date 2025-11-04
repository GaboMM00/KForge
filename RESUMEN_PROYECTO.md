# KForge - Resumen del Proyecto

## Información General

**Nombre:** KForge - Compilador Kotlin
**Lenguaje:** Python 3.8+
**Interfaz:** Tkinter
**Tipo:** Compilador modular y extensible

## Estructura Completa del Proyecto

```
KForge/
├── main.py                          # Punto de entrada principal
├── test_compilador.py               # Script de pruebas CLI
├── README.md                        # Documentación principal
├── INSTRUCCIONES.md                 # Guía de uso detallada
├── RESUMEN_PROYECTO.md             # Este archivo
│
├── core/                            # Módulo del compilador
│   ├── __init__.py                  # Inicialización del paquete
│   ├── controller.py                # Controlador principal (coordina fases)
│   ├── lexer.py                     # Analizador léxico (tokenización)
│   ├── parser.py                    # Analizador sintáctico (AST)
│   ├── semantic.py                  # Analizador semántico (tipos/símbolos)
│   ├── codegen.py                   # Generador de código (placeholder)
│   ├── errors.py                    # Manejo centralizado de errores
│   └── utils.py                     # Estructuras de datos y utilidades
│
├── ui/                              # Módulo de interfaz gráfica
│   ├── __init__.py                  # Inicialización del paquete
│   ├── interfaz.py                  # Ventana principal
│   ├── editor.py                    # Editor con numeración de líneas
│   └── consola.py                   # Consola de resultados
│
├── tests/                           # Archivos de prueba
│   ├── ejemplo_kotlin.txt           # Ejemplo completo de código
│   ├── prueba_simple.txt            # Prueba básica
│   └── prueba_errores.txt           # Prueba de detección de errores
│
└── assets/                          # Recursos (opcional)
```

## Módulos Implementados

### 1. Core (Lógica del Compilador)

#### controller.py
- **Clase:** `CompiladorController`
- **Responsabilidad:** Coordinar todas las fases del compilador
- **Métodos principales:**
  - `ejecutar(codigo)` - Compilación completa
  - `ejecutar_lexico(codigo)` - Solo análisis léxico
  - `ejecutar_sintactico(codigo)` - Léxico + Sintáctico
  - `ejecutar_semantico(codigo)` - Léxico + Sintáctico + Semántico
  - `ejecutar_codegen(codigo)` - Todas las fases + código intermedio

#### lexer.py
- **Clase:** `Lexer`
- **Responsabilidad:** Análisis léxico (tokenización)
- **Características:**
  - Usa expresiones regulares
  - Reconoce palabras clave, identificadores, literales
  - Detecta operadores y delimitadores
  - Ignora comentarios y espacios en blanco
- **Método principal:** `tokenizar(codigo) -> List[Token]`

#### parser.py
- **Clase:** `Parser`
- **Responsabilidad:** Análisis sintáctico (generación de AST)
- **Características:**
  - Descendente recursivo
  - Una función por regla gramatical
  - Recuperación de errores
- **Reglas implementadas:**
  - `programa()`
  - `sentencia()`
  - `declaracion_variable()`
  - `asignacion()`
  - `sentencia_if()`
  - `sentencia_while()`
  - `sentencia_for()`
  - `bloque()`
  - `expresion()`
  - Y más...

#### semantic.py
- **Clase:** `AnalizadorSemantico`
- **Responsabilidad:** Verificación semántica
- **Verificaciones:**
  - Variables declaradas antes de usar
  - Tipos compatibles en asignaciones
  - No reasignación de constantes (val)
  - Condiciones booleanas en if/while
  - Gestión de scopes
- **Método principal:** `analizar(ast) -> List[str]`

#### codegen.py
- **Clase:** `CodeGenerator`
- **Responsabilidad:** Generación de código intermedio (FUTURO)
- **Estado:** Placeholder - no implementado
- **Propósito:** Documentado para implementación futura

#### errors.py
- **Clases:**
  - `CompiladorError` - Base
  - `LexicalError` - Errores léxicos
  - `SyntaxError` - Errores sintácticos
  - `SemanticError` - Errores semánticos
  - `ErrorManager` - Gestor centralizado

#### utils.py
- **Estructuras de datos:**
  - `TipoToken` - Enumeración de tipos de tokens
  - `Token` - Dataclass para tokens
  - `TipoNodo` - Enumeración de tipos de nodos AST
  - `NodoAST` - Dataclass para nodos del AST
  - `TipoDato` - Enumeración de tipos de datos
  - `Simbolo` - Dataclass para símbolos
  - `TablaSimbolos` - Gestión de símbolos por scope

### 2. UI (Interfaz Gráfica)

#### interfaz.py
- **Clase:** `InterfazCompilador`
- **Responsabilidad:** Ventana principal de la aplicación
- **Componentes:**
  - Menú completo (Archivo, Compilador, Variable, Ayuda)
  - Editor de código
  - Consola de resultados
- **Atajos de teclado:** F5-F9, Ctrl+N/O/S

#### editor.py
- **Clase:** `EditorConLineas`
- **Responsabilidad:** Editor de texto con numeración
- **Características:**
  - Numeración automática de líneas
  - Fuente monoespaciada
  - Resaltado de sintaxis básico
  - Scrollbars sincronizados

#### consola.py
- **Clase:** `ConsolaSalida`
- **Responsabilidad:** Consola de resultados con colores
- **Características:**
  - Fondo oscuro tipo IDE
  - Colores según tipo de mensaje
  - Auto-scroll
  - Solo lectura

## Funcionalidades Implementadas

### Sintaxis Soportada

1. **Variables:**
   - `var` (mutable)
   - `val` (inmutable)

2. **Tipos de datos:**
   - `Int`
   - `Double`
   - `String`
   - `Boolean`

3. **Operadores:**
   - Aritméticos: `+`, `-`, `*`, `/`, `%`
   - Comparación: `==`, `!=`, `<`, `<=`, `>`, `>=`
   - Asignación: `=`

4. **Estructuras de control:**
   - `if-else`
   - `while`
   - `for-in` con rangos (`1..10`)

5. **Otros:**
   - Comentarios de línea (`//`)
   - Bloques `{}`
   - Expresiones anidadas

### Análisis Implementado

✅ **Léxico:**
- Tokenización completa
- Detección de caracteres inválidos
- Manejo de literales (int, double, string, boolean)

✅ **Sintáctico:**
- Generación de AST
- Validación de estructura gramatical
- Recuperación de errores

✅ **Semántico:**
- Tabla de símbolos
- Verificación de tipos
- Control de scopes
- Detección de redeclaraciones
- Validación de constantes

🔜 **Generación de Código:**
- Preparado pero no implementado
- Documentado para futuro desarrollo

## Arquitectura y Diseño

### Principios Aplicados

1. **Separación de Responsabilidades**
   - UI completamente desacoplada de la lógica
   - Cada fase del compilador es independiente

2. **Modularidad**
   - Cada módulo tiene una responsabilidad clara
   - Fácil de extender y modificar

3. **Manejo Centralizado de Errores**
   - Todos los errores pasan por `ErrorManager`
   - Formato consistente de mensajes

4. **Extensibilidad**
   - Fácil añadir nuevas palabras clave
   - Fácil añadir nuevas reglas gramaticales
   - Estructura preparada para futuras mejoras

### Flujo de Datos

```
Usuario escribe código
        ↓
[Interfaz UI] → obtener_texto()
        ↓
[Controller] → ejecutar()
        ↓
[Lexer] → tokenizar() → Tokens
        ↓
[Parser] → parsear() → AST
        ↓
[Semantic] → analizar() → Validación
        ↓
[Controller] → construir_resultado()
        ↓
[Interfaz UI] → mostrar en consola
```

## Archivos de Prueba

1. **ejemplo_kotlin.txt**
   - Ejemplo completo
   - Todas las características soportadas
   - 181 tokens
   - Sin errores

2. **prueba_simple.txt**
   - Prueba básica
   - Declaraciones y operaciones
   - Para verificación rápida

3. **prueba_errores.txt**
   - Errores intencionales
   - Para probar detección de errores
   - Variable no declarada
   - Reasignación de constante
   - Tipo incompatible
   - Redeclaración

## Comandos de Ejecución

### Interfaz Gráfica
```bash
python main.py
```

### Pruebas CLI
```bash
# Prueba básica
python test_compilador.py

# Compilar archivo
python test_compilador.py tests/ejemplo_kotlin.txt

# Ayuda
python test_compilador.py --help
```

### Uso Programático
```python
from core.controller import CompiladorController

compilador = CompiladorController()
resultado = compilador.ejecutar("var x: Int = 5")

if resultado["exito"]:
    print("OK")
else:
    print(resultado["errores"])
```

## Métricas del Proyecto

- **Total de archivos Python:** 13
- **Total de archivos de prueba:** 3
- **Líneas de código (aprox):**
  - core/: ~2500 líneas
  - ui/: ~800 líneas
  - tests y scripts: ~200 líneas
- **Clases principales:** 10
- **Métodos principales:** ~50
- **Tokens soportados:** 35+
- **Tipos de nodos AST:** 12

## Limitaciones Conocidas

1. No soporta funciones definidas por usuario
2. No soporta arrays o colecciones
3. No soporta clases u objetos
4. No soporta imports
5. No soporta expresiones lambda
6. No soporta `when` (switch)
7. No soporta try-catch
8. Sin optimizaciones
9. Generación de código no implementada

## Mejoras Futuras Planificadas

- [ ] Funciones (`fun`)
- [ ] Arrays y listas
- [ ] Clases y objetos
- [ ] Herencia
- [ ] Interfaces
- [ ] Lambda expressions
- [ ] When expression
- [ ] Try-catch-finally
- [ ] Null safety (`?`)
- [ ] Data classes
- [ ] Extension functions
- [ ] Generación de código intermedio
- [ ] Optimizaciones
- [ ] Mejor manejo de errores con sugerencias
- [ ] Autocompletado
- [ ] Depurador integrado

## Tecnologías Utilizadas

- **Python 3.8+**
- **Tkinter** - Interfaz gráfica
- **re** - Expresiones regulares
- **dataclasses** - Estructuras de datos
- **enum** - Enumeraciones
- **typing** - Type hints

## Conclusión

KForge es un compilador funcional y modular para Kotlin que implementa las fases fundamentales del proceso de compilación. Su arquitectura limpia y extensible permite agregar nuevas características fácilmente, y la separación entre interfaz y lógica facilita su uso tanto en modo gráfico como programático.

El proyecto demuestra los conceptos fundamentales de diseño de compiladores:
- Análisis léxico con expresiones regulares
- Análisis sintáctico descendente recursivo
- Análisis semántico con tabla de símbolos
- Manejo de errores y recuperación
- Arquitectura modular y extensible

---

**Versión:** 1.0
**Fecha:** Noviembre 2024
**Estado:** Funcional - Listo para uso y extensión
