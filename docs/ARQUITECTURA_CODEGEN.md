# 🏗️ Arquitectura de Generación de Código Intermedio

**Versión**: 1.1+ (Planeada)
**Objetivo**: Backend profesional con código intermedio de 3 direcciones y bytecode

---

## 📐 Diseño de Arquitectura

### **Pipeline Completo del Compilador**

```
┌────────────────────────────────────────────────────────────────┐
│                     CÓDIGO FUENTE KOTLIN                        │
└──────────────────────┬─────────────────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────────────────┐
│  FRONTEND (Ya implementado - v1.0.1)                           │
├────────────────────────────────────────────────────────────────┤
│  • Lexer     → Tokens                                          │
│  • Parser    → AST                                             │
│  • Semantic  → AST Validado + Tabla de Símbolos               │
└──────────────────────┬─────────────────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────────────────┐
│  INTERMEDIATE REPRESENTATION (v1.1 - v1.2)                     │
├────────────────────────────────────────────────────────────────┤
│  • TACGenerator  → Código de 3 Direcciones (TAC)              │
│  • Optimizer     → TAC Optimizado (v1.2)                       │
└──────────────────────┬─────────────────────────────────────────┘
                       │
                       ├──────────────┬──────────────┐
                       ▼              ▼              ▼
         ┌─────────────────┐  ┌─────────────┐  ┌──────────────┐
         │   BYTECODE      │  │  C CODE     │  │  LLVM IR     │
         │   (v1.1)        │  │  (v1.3)     │  │  (v2.0)      │
         └────────┬────────┘  └──────┬──────┘  └──────┬───────┘
                  │                  │                 │
                  ▼                  ▼                 ▼
         ┌─────────────────┐  ┌─────────────┐  ┌──────────────┐
         │   Intérprete    │  │     gcc     │  │   llc/opt    │
         │   de Stack      │  │  Ejecutable │  │  Ejecutable  │
         └─────────────────┘  └─────────────┘  └──────────────┘
```

---

## 🎯 Módulos a Implementar

### **1. core/tac.py** - Código de 3 Direcciones (TAC)

**Responsabilidad**: Representación Intermedia profesional

```python
@dataclass
class TACInstruction:
    """Instrucción de código de tres direcciones"""
    op: str                    # Operación
    arg1: Optional[str] = None # Primer operando
    arg2: Optional[str] = None # Segundo operando
    result: Optional[str] = None # Resultado
    label: Optional[str] = None  # Etiqueta (para saltos)

class TACGenerator:
    """Genera código TAC desde el AST validado"""
    def __init__(self):
        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0

    def generate(self, ast: NodoAST) -> List[TACInstruction]:
        """Genera TAC completo desde el AST"""
        pass
```

**Operaciones TAC**:
- `ASSIGN` - Asignación simple: `x = 5`
- `ADD, SUB, MUL, DIV, MOD` - Aritmética: `t1 = a + b`
- `LT, GT, LE, GE, EQ, NE` - Comparación: `t2 = a < b`
- `AND, OR, NOT` - Lógicos: `t3 = a && b`
- `LABEL` - Etiquetas: `L1:`
- `GOTO` - Salto incondicional: `GOTO L1`
- `IF_FALSE` - Salto condicional: `IF_FALSE t1 GOTO L2`
- `PARAM` - Paso de parámetros: `PARAM x`
- `CALL` - Llamada a función: `CALL foo, 2`
- `RETURN` - Retorno: `RETURN t5`
- `ARRAY_LOAD` - Carga de array: `t1 = arr[i]`
- `ARRAY_STORE` - Escritura en array: `arr[i] = t2`

---

### **2. core/bytecode.py** - Generador de Bytecode Assembly

**Responsabilidad**: Formatear TAC como "Assembly" para presentación

```python
class BytecodeGenerator:
    """Traduce TAC a bytecode stack-based"""

    def generate(self, tac: List[TACInstruction]) -> List[str]:
        """Genera bytecode desde TAC"""
        pass

    def format_output(self, bytecode: List[str]) -> str:
        """Formatea bytecode para mostrar en UI"""
        pass
```

**Instrucciones Bytecode**:
```asm
PUSH <valor>     ; Push literal al stack
LOAD <var>       ; Push variable al stack
STORE <var>      ; Pop y guardar en variable
ADD              ; Pop 2, sumar, push resultado
SUB, MUL, DIV    ; Operaciones aritméticas
EQ, LT, GT       ; Comparaciones
AND, OR, NOT     ; Lógicas
JUMP <label>     ; Salto incondicional
JUMPF <label>    ; Salto si falso
CALL <func>      ; Llamar función
RET              ; Retornar de función
HALT             ; Fin de programa
```

---

### **3. core/optimizer.py** - Optimizador de TAC (v1.2+)

**Responsabilidad**: Optimizaciones sobre código TAC

```python
class TACOptimizer:
    """Optimiza código TAC"""

    def optimize(self, tac: List[TACInstruction]) -> List[TACInstruction]:
        """Aplica todas las optimizaciones"""
        tac = self.constant_folding(tac)
        tac = self.dead_code_elimination(tac)
        tac = self.copy_propagation(tac)
        return tac

    def constant_folding(self, tac):
        """Plegado de constantes: 2 + 3 → 5"""
        pass

    def dead_code_elimination(self, tac):
        """Elimina código muerto"""
        pass
```

---

### **4. core/backends/** - Backends Múltiples (v1.3+)

```
core/backends/
├── __init__.py
├── c_backend.py         # Generador de C (v1.3)
├── llvm_backend.py      # Generador de LLVM IR (v2.0)
└── interpreter.py       # Intérprete de bytecode (v1.1)
```

---

## 🔄 Integración con el Sistema Actual

### **Modificación en core/controller.py**

```python
class CompiladorController:
    def __init__(self):
        self.error_manager = ErrorManager()
        self.lexer = None
        self.parser = None
        self.semantic_analyzer = None

        # NUEVO: Generadores de código
        self.tac_generator = None      # v1.1
        self.bytecode_generator = None # v1.1
        self.optimizer = None          # v1.2

        # Resultados
        self.tokens = []
        self.ast = None
        self.tac_code = []      # NUEVO
        self.bytecode = []      # NUEVO

    def ejecutar(self, codigo: str) -> Dict[str, Any]:
        """Ejecuta todas las fases incluyendo generación de código"""

        # Frontend (ya existe)
        self.lexer = Lexer(self.error_manager)
        self.tokens = self.lexer.tokenizar(codigo)

        self.parser = Parser(self.tokens, self.error_manager)
        self.ast = self.parser.parsear()

        self.semantic_analyzer = AnalizadorSemantico(self.error_manager)
        resultados_semanticos = self.semantic_analyzer.analizar(self.ast)

        # NUEVO: Backend
        if not self.error_manager.tiene_errores():
            # Generar TAC
            from core.tac import TACGenerator
            self.tac_generator = TACGenerator()
            self.tac_code = self.tac_generator.generate(self.ast)

            # Generar Bytecode
            from core.bytecode import BytecodeGenerator
            self.bytecode_generator = BytecodeGenerator()
            self.bytecode = self.bytecode_generator.generate(self.tac_code)

        return {
            "tokens": self.tokens,
            "ast": self.ast,
            "semantico": resultados_semanticos,
            "tac": self.tac_code,         # NUEVO
            "bytecode": self.bytecode,     # NUEVO
            "errores": self.error_manager.errores,
            "exito": not self.error_manager.tiene_errores()
        }
```

---

## 🎨 Modificación en la Interfaz UI

### **ui/console_panel.py** - Agregar pestaña de Código

```python
class ConsolePanel:
    def _setup_tabs(self):
        # Pestañas existentes
        self.output_tab = ...
        self.error_tab = ...
        self.ast_tab = ...
        self.tokens_tab = ...

        # NUEVA: Pestaña de Código Intermedio
        self.code_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.code_tab, text="Código")

        # Text widget para mostrar código
        self.code_text = scrolledtext.ScrolledText(
            self.code_tab,
            wrap=tk.NONE,
            font=self.theme.get_font()
        )
        self.code_text.pack(fill="both", expand=True)

        # Botones para cambiar entre TAC y Bytecode
        button_frame = ttk.Frame(self.code_tab)
        button_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            button_frame,
            text="Ver TAC",
            command=lambda: self.show_code("tac")
        ).pack(side="left", padx=2)

        ttk.Button(
            button_frame,
            text="Ver Bytecode",
            command=lambda: self.show_code("bytecode")
        ).pack(side="left", padx=2)

        ttk.Button(
            button_frame,
            text="Guardar Código",
            command=self.save_code
        ).pack(side="right", padx=2)
```

---

## 📂 Exportación de Código

### **Nueva funcionalidad**: Guardar código generado

```python
def save_code(self, code_type="bytecode"):
    """Guarda el código generado a archivo"""
    from tkinter import filedialog

    filename = filedialog.asksaveasfilename(
        defaultextension=".asm" if code_type == "bytecode" else ".tac",
        filetypes=[
            ("Assembly", "*.asm"),
            ("TAC Code", "*.tac"),
            ("Todos", "*.*")
        ]
    )

    if filename:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.current_code)

        messagebox.showinfo("Éxito", f"Código guardado en {filename}")
```

---

## ✅ Compatibilidad con Sistema Actual

**NO se modifica**:
- ✅ Lexer
- ✅ Parser
- ✅ Semantic Analyzer
- ✅ Sistema de errores
- ✅ Tests existentes

**SE agrega**:
- ✅ Nuevos módulos en `core/`
- ✅ Nueva pestaña en UI
- ✅ Nuevos resultados en `controller.ejecutar()`

**Principio**: Extensión sin modificación (Open/Closed Principle)

---

## 🧪 Estrategia de Testing

```
tests/
├── test_tac_generator.py       # Tests de generación TAC
├── test_bytecode_generator.py  # Tests de bytecode
├── test_optimizer.py           # Tests de optimizaciones (v1.2)
└── test_codegen_integration.py # Tests de integración completa
```

**Ejemplo de test**:
```python
def test_simple_assignment():
    codigo = "var x: Int = 5"
    tac = generar_tac(codigo)

    assert len(tac) == 1
    assert tac[0].op == 'ASSIGN'
    assert tac[0].arg1 == '5'
    assert tac[0].result == 'x'
```

---

## 📊 Métricas de Éxito

**v1.1 (Bytecode)**:
- ✅ Genera TAC desde AST
- ✅ Genera Bytecode desde TAC
- ✅ UI muestra código generado
- ✅ Puede guardar a archivo
- ✅ Todos los tests v1.0 siguen pasando

**v1.2 (Optimizaciones)**:
- ✅ Constant folding funciona
- ✅ Dead code elimination funciona
- ✅ Código optimizado < código original

**v1.3 (Backend C)**:
- ✅ Genera C ejecutable
- ✅ Compila con gcc
- ✅ Ejecuta correctamente

---

**Autor**: Gabriel Alejandro Medina Miramontes
**Fecha**: 2025-11-22
**Versión Documento**: 1.0
