# 📦 Instalación y Configuración - KForge Compiler

**Guía completa para configurar el entorno de desarrollo de KForge**

---

## 📋 Requisitos Previos

- **Python 3.8 o superior**
- **Git** (para clonar el repositorio)
- **JDK 8+** (opcional, para verificar archivos .class generados con javap)

---

## 🚀 Instalación Rápida

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd KForge
```

### 2. Crear Entorno Virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Nota**: El compilador usa únicamente la biblioteca estándar de Python, por lo que no requiere dependencias externas para funcionar. El archivo `requirements.txt` está preparado para futuras dependencias opcionales.

### 4. Verificar Instalación

```bash
# Ejecutar la interfaz gráfica
python main_modern.py

# O ejecutar tests
python tests/phases/test_fase1_directo.py
python tests/jvm/test_constant_pool.py
```

---

## 🧪 Ejecutar Tests

### Tests Completos

```bash
# Tests de fases del compilador
python tests/phases/test_fase1_directo.py
python tests/phases/test_fase2_directo.py
python tests/phases/test_fase3_directo.py

# Tests de JVM
python tests/jvm/test_constant_pool.py
python tests/jvm/test_classfile.py
python tests/jvm/test_instructions.py
python tests/jvm/test_jvm_generator.py
python tests/jvm/test_jvm_validation.py

# Tests de integración
python tests/integration/test_ui_integration.py
python tests/integration/test_global_statements.py
```

### Ejecutar Todos los Tests

**Windows:**
```bash
# Script para ejecutar todos los tests
for %f in (tests\phases\*.py) do python %f
for %f in (tests\jvm\*.py) do python %f
```

**Linux/macOS:**
```bash
# Ejecutar todos los tests de fases
for test in tests/phases/*.py; do python "$test"; done

# Ejecutar todos los tests JVM
for test in tests/jvm/*.py; do python "$test"; done
```

---

## 🔧 Configuración de Desarrollo

### Estructura del Proyecto

```
KForge/
├── venv/                    # Entorno virtual (creado por ti)
├── core/                    # Núcleo del compilador
│   ├── lexer.py
│   ├── parser.py
│   ├── semantic.py
│   ├── tac.py
│   ├── bytecode.py
│   ├── controller.py
│   └── jvm/                 # Módulo JVM (v2.0)
│       ├── constant_pool.py
│       ├── descriptors.py
│       ├── classfile.py
│       ├── instructions.py
│       └── jvm_generator.py
├── ui/                      # Interfaz gráfica
├── tests/                   # Suite de tests
│   ├── phases/
│   ├── jvm/
│   └── integration/
├── docs/                    # Documentación técnica
├── main_modern.py           # Punto de entrada UI
└── requirements.txt         # Dependencias
```

### Variables de Entorno (Opcional)

Si deseas configurar rutas personalizadas:

```bash
# Windows
set KFORGE_HOME=C:\Dev\Compiladores\ProyectoFinal\KForge

# Linux/macOS
export KFORGE_HOME=/path/to/KForge
```

---

## 🎯 Uso Básico

### Modo Interfaz Gráfica

```bash
# Activar entorno virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# Ejecutar UI
python main_modern.py
```

### Modo Programático

```python
from core.controller import CompiladorController

# Código Kotlin
codigo = """
var x: Int = 10
var y: Int = 20
var suma: Int = x + y
println(suma)
"""

# Compilar
controlador = CompiladorController()
resultado = controlador.compilar(codigo)

# Acceder a resultados
print("Tokens:", resultado.tokens)
print("AST:", resultado.ast)
print("Errores:", resultado.error_manager.get_errores())
print("TAC:", resultado.tac)
print("Bytecode:", resultado.bytecode)
```

---

## 🔍 Verificación de Archivos .class (Opcional)

Si tienes JDK instalado, puedes verificar los archivos .class generados:

### Instalar JDK

**Windows:**
1. Descargar JDK 8+ desde [Oracle](https://www.oracle.com/java/technologies/downloads/) o [OpenJDK](https://adoptium.net/)
2. Instalar y agregar `bin/` al PATH
3. Verificar: `javap -version`

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install openjdk-11-jdk
javap -version
```

**macOS:**
```bash
brew install openjdk@11
javap -version
```

### Usar javap

```bash
# Generar un .class
python tests/jvm/test_classfile.py

# Verificar con javap
javap -v -p tests/jvm/output/HelloWorld.class
```

---

## 🐛 Solución de Problemas

### Error: "No module named 'core'"

**Solución**: Asegúrate de ejecutar los scripts desde el directorio raíz del proyecto:

```bash
cd KForge
python tests/jvm/test_constant_pool.py
```

### Error: "UnicodeEncodeError"

**Solución**: Ya está solucionado en los tests con:

```python
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

Si encuentras este error en otros archivos, agrega las líneas anteriores al inicio.

### Error: "venv\Scripts\activate" no funciona en Windows

**Solución**: Si usas PowerShell, ejecuta primero:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

O usa Command Prompt (cmd) en lugar de PowerShell.

---

## 📚 Documentación Adicional

- **[README.md](README.md)** - Descripción general del proyecto
- **[ROADMAP.md](ROADMAP.md)** - Plan de desarrollo v2.0
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Reglas de contribución
- **[CHANGELOG.md](CHANGELOG.md)** - Historial de cambios
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Arquitectura del compilador
- **[docs/JVM_BYTECODE_GUIDE.md](docs/JVM_BYTECODE_GUIDE.md)** - Guía de JVM bytecode

---

## 🤝 Contribuir

Para contribuir al proyecto, lee [CONTRIBUTING.md](CONTRIBUTING.md) que contiene:

- Reglas de organización de código
- Flujo de trabajo para implementar características
- Convenciones de código
- Formato de mensajes de commit

---

## 📄 Licencia

GPL-3.0 License - Ver [LICENSE](LICENSE) para más detalles.

---

## 👤 Autor

**Gabriel Alejandro Medina Miramontes**

Desarrollado como proyecto educativo para aprender compiladores e implementación de lenguajes de programación.
