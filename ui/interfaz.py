"""
Interfaz gráfica principal del compilador de Kotlin.
Proporciona un editor tipo IDE con menú y consola de resultados.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from ui.editor import EditorConLineas
from ui.consola import ConsolaSalida
from core.controller import CompiladorController


class InterfazCompilador(tk.Tk):
    """
    Ventana principal del compilador de Kotlin.

    Componentes:
    - Menú superior
    - Editor de código con numeración
    - Consola de resultados
    """

    def __init__(self):
        """Inicializa la interfaz gráfica."""
        super().__init__()

        # Configuración de la ventana
        self.title("KForge - Compilador Kotlin")
        self.geometry("1000x700")
        self.minsize(800, 600)

        # Controlador del compilador (desacoplado de la UI)
        self.controlador = CompiladorController()

        # Ruta del archivo actual
        self.archivo_actual = None

        # Crear interfaz
        self._crear_menu()
        self._crear_editor()
        self._crear_consola()

        # Mensaje de bienvenida
        self.consola.mostrar_mensaje_bienvenida()

        # Configurar cierre de ventana
        self.protocol("WM_DELETE_WINDOW", self._salir)

    def _crear_menu(self):
        """Crea el menú superior."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Menú Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Nuevo", command=self._nuevo, accelerator="Ctrl+N")
        menu_archivo.add_command(label="Abrir...", command=self._abrir, accelerator="Ctrl+O")
        menu_archivo.add_command(label="Guardar", command=self._guardar, accelerator="Ctrl+S")
        menu_archivo.add_command(label="Guardar como...", command=self._guardar_como, accelerator="Ctrl+Shift+S")
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Limpiar Editor", command=self._limpiar_editor)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self._salir, accelerator="Alt+F4")

        # Menú Compilador
        menu_compilador = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Compilador", menu=menu_compilador)
        menu_compilador.add_command(
            label="Análisis Léxico",
            command=self._ejecutar_lexico,
            accelerator="F5"
        )
        menu_compilador.add_command(
            label="Análisis Sintáctico",
            command=self._ejecutar_sintactico,
            accelerator="F6"
        )
        menu_compilador.add_command(
            label="Análisis Semántico",
            command=self._ejecutar_semantico,
            accelerator="F7"
        )
        menu_compilador.add_command(
            label="Compilación Completa",
            command=self._ejecutar_completo,
            accelerator="F8"
        )
        menu_compilador.add_separator()
        menu_compilador.add_command(
            label="Código Intermedio",
            command=self._ejecutar_codegen,
            accelerator="F9"
        )
        menu_compilador.add_separator()
        menu_compilador.add_command(label="Limpiar Consola", command=self._limpiar_consola)

        # Menú Variable
        menu_variable = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Variable", menu=menu_variable)
        menu_variable.add_command(label="Int - Entero", command=lambda: self._insertar_tipo("Int"))
        menu_variable.add_command(label="Double - Decimal", command=lambda: self._insertar_tipo("Double"))
        menu_variable.add_command(label="String - Cadena", command=lambda: self._insertar_tipo("String"))
        menu_variable.add_command(label="Boolean - Lógico", command=lambda: self._insertar_tipo("Boolean"))
        menu_variable.add_separator()
        menu_variable.add_command(label="var - Variable mutable", command=lambda: self._insertar_declaracion("var"))
        menu_variable.add_command(label="val - Variable inmutable", command=lambda: self._insertar_declaracion("val"))

        # Menú Ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Librerías Estándar", command=self._mostrar_librerias)
        menu_ayuda.add_command(label="Sintaxis Soportada", command=self._mostrar_sintaxis)
        menu_ayuda.add_separator()
        menu_ayuda.add_command(label="Acerca de", command=self._acerca_de)

        # Atajos de teclado
        self.bind("<Control-n>", lambda e: self._nuevo())
        self.bind("<Control-o>", lambda e: self._abrir())
        self.bind("<Control-s>", lambda e: self._guardar())
        self.bind("<Control-Shift-S>", lambda e: self._guardar_como())
        self.bind("<F5>", lambda e: self._ejecutar_lexico())
        self.bind("<F6>", lambda e: self._ejecutar_sintactico())
        self.bind("<F7>", lambda e: self._ejecutar_semantico())
        self.bind("<F8>", lambda e: self._ejecutar_completo())
        self.bind("<F9>", lambda e: self._ejecutar_codegen())

    def _crear_editor(self):
        """Crea el editor de código."""
        # Frame para el editor
        frame_editor = tk.Frame(self, bg="#ffffff")
        frame_editor.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Etiqueta
        label_editor = tk.Label(frame_editor, text="Editor de Código", font=("Segoe UI", 10, "bold"),
                                bg="#f0f0f0", anchor=tk.W, padx=10, pady=5)
        label_editor.pack(side=tk.TOP, fill=tk.X)

        # Editor
        self.editor = EditorConLineas(frame_editor)
        self.editor.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def _crear_consola(self):
        """Crea la consola de resultados."""
        # Frame para la consola
        frame_consola = tk.Frame(self)
        frame_consola.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False, padx=5, pady=5)

        # Etiqueta
        label_consola = tk.Label(frame_consola, text="Consola de Resultados", font=("Segoe UI", 10, "bold"),
                                 bg="#1e1e1e", fg="#ffffff", anchor=tk.W, padx=10, pady=5)
        label_consola.pack(side=tk.TOP, fill=tk.X)

        # Consola
        self.consola = ConsolaSalida(frame_consola, height=15)
        self.consola.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # ========== Métodos del Menú Archivo ==========

    def _nuevo(self):
        """Crea un nuevo archivo."""
        if messagebox.askyesno("Nuevo", "¿Desea limpiar el editor?"):
            self.editor.limpiar()
            self.archivo_actual = None
            self.title("KForge - Compilador Kotlin")
            self._limpiar_consola()

    def _abrir(self):
        """Abre un archivo existente."""
        archivo = filedialog.askopenfilename(
            title="Abrir archivo",
            filetypes=[
                ("Archivos Kotlin", "*.kt"),
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ]
        )

        if archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                self.editor.establecer_texto(contenido)
                self.editor.aplicar_resaltado_basico()
                self.archivo_actual = archivo
                self.title(f"KForge - {archivo}")
                self.consola.escribir_exito(f"Archivo abierto: {archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{str(e)}")

    def _guardar(self):
        """Guarda el archivo actual."""
        if self.archivo_actual:
            self._guardar_archivo(self.archivo_actual)
        else:
            self._guardar_como()

    def _guardar_como(self):
        """Guarda el archivo con un nuevo nombre."""
        archivo = filedialog.asksaveasfilename(
            title="Guardar como",
            defaultextension=".kt",
            filetypes=[
                ("Archivos Kotlin", "*.kt"),
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ]
        )

        if archivo:
            self._guardar_archivo(archivo)

    def _guardar_archivo(self, ruta: str):
        """Guarda el contenido del editor en un archivo."""
        try:
            contenido = self.editor.obtener_texto()
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(contenido)
            self.archivo_actual = ruta
            self.title(f"KForge - {ruta}")
            self.consola.escribir_exito(f"Archivo guardado: {ruta}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")

    def _limpiar_editor(self):
        """Limpia el contenido del editor."""
        if messagebox.askyesno("Limpiar", "¿Está seguro de limpiar el editor?"):
            self.editor.limpiar()

    def _salir(self):
        """Sale de la aplicación."""
        if messagebox.askyesno("Salir", "¿Desea salir del compilador?"):
            self.quit()

    # ========== Métodos del Menú Compilador ==========

    def _ejecutar_lexico(self):
        """Ejecuta solo el análisis léxico."""
        codigo = self.editor.obtener_texto()
        if not codigo.strip():
            messagebox.showwarning("Advertencia", "El editor está vacío")
            return

        resultado = self.controlador.ejecutar_lexico(codigo)
        self.consola.mostrar_tokens(resultado)

    def _ejecutar_sintactico(self):
        """Ejecuta análisis léxico y sintáctico."""
        codigo = self.editor.obtener_texto()
        if not codigo.strip():
            messagebox.showwarning("Advertencia", "El editor está vacío")
            return

        resultado = self.controlador.ejecutar_sintactico(codigo)
        self.consola.mostrar_ast(resultado)

    def _ejecutar_semantico(self):
        """Ejecuta análisis completo (léxico, sintáctico y semántico)."""
        codigo = self.editor.obtener_texto()
        if not codigo.strip():
            messagebox.showwarning("Advertencia", "El editor está vacío")
            return

        resultado = self.controlador.ejecutar_semantico(codigo)
        self.consola.mostrar_resultado_compilacion(resultado)

    def _ejecutar_completo(self):
        """Ejecuta compilación completa."""
        self._ejecutar_semantico()
        # Aplicar resaltado de sintaxis
        self.editor.aplicar_resaltado_basico()

    def _ejecutar_codegen(self):
        """Ejecuta generación de código intermedio."""
        codigo = self.editor.obtener_texto()
        if not codigo.strip():
            messagebox.showwarning("Advertencia", "El editor está vacío")
            return

        resultado = self.controlador.ejecutar_codegen(codigo)
        self.consola.mostrar_resultado_compilacion(resultado)

    def _limpiar_consola(self):
        """Limpia la consola de resultados."""
        self.consola.limpiar()

    # ========== Métodos del Menú Variable ==========

    def _insertar_tipo(self, tipo: str):
        """Inserta un tipo de dato en el editor."""
        self.editor.insert(tk.INSERT, tipo)

    def _insertar_declaracion(self, declaracion: str):
        """Inserta una declaración en el editor."""
        self.editor.insert(tk.INSERT, f"{declaracion} nombre: Tipo = valor")

    # ========== Métodos del Menú Ayuda ==========

    def _mostrar_librerias(self):
        """Muestra información sobre librerías estándar."""
        self.consola.limpiar()
        self.consola.escribir_titulo("LIBRERÍAS ESTÁNDAR DE KOTLIN")
        self.consola.escribir_separador()
        self.consola.escribir_linea()
        self.consola.escribir_info("Principales paquetes de Kotlin:")
        self.consola.escribir_linea()
        self.consola.escribir("  • kotlin.collections - Colecciones (List, Set, Map)")
        self.consola.escribir("  • kotlin.io - Entrada/Salida")
        self.consola.escribir("  • kotlin.math - Funciones matemáticas")
        self.consola.escribir("  • kotlin.text - Manipulación de texto")
        self.consola.escribir("  • kotlin.ranges - Rangos y progresiones")
        self.consola.escribir_linea()
        self.consola.escribir_comentario("Nota: Este compilador soporta un subconjunto básico de Kotlin")
        self.consola.escribir_separador()

    def _mostrar_sintaxis(self):
        """Muestra la sintaxis soportada."""
        self.consola.limpiar()
        self.consola.escribir_titulo("SINTAXIS SOPORTADA")
        self.consola.escribir_separador()
        self.consola.escribir_linea()

        self.consola.escribir_subtitulo("1. Declaración de Variables:")
        self.consola.escribir("  var nombre: Int = 10        // Variable mutable")
        self.consola.escribir("  val PI: Double = 3.14       // Variable inmutable")
        self.consola.escribir_linea()

        self.consola.escribir_subtitulo("2. Tipos de Datos:")
        self.consola.escribir("  Int, Double, String, Boolean")
        self.consola.escribir_linea()

        self.consola.escribir_subtitulo("3. Operadores:")
        self.consola.escribir("  Aritméticos: +, -, *, /, %")
        self.consola.escribir("  Comparación: ==, !=, <, <=, >, >=")
        self.consola.escribir_linea()

        self.consola.escribir_subtitulo("4. Estructuras de Control:")
        self.consola.escribir("  if (condicion) { ... } else { ... }")
        self.consola.escribir("  while (condicion) { ... }")
        self.consola.escribir("  for (i in 1..10) { ... }")
        self.consola.escribir_linea()

        self.consola.escribir_subtitulo("5. Comentarios:")
        self.consola.escribir("  // Comentario de una línea")
        self.consola.escribir_linea()

        self.consola.escribir_separador()

    def _acerca_de(self):
        """Muestra información sobre el compilador."""
        mensaje = """
KForge - Compilador Kotlin
Versión 1.0

Compilador modular y extensible para el lenguaje Kotlin,
desarrollado en Python con interfaz Tkinter.

Características:
• Análisis Léxico
• Análisis Sintáctico
• Análisis Semántico
• Generación de Código Intermedio (próximamente)

Arquitectura modular y extensible que permite añadir
nuevas reglas y funcionalidades fácilmente.

Desarrollado como proyecto académico.
        """
        messagebox.showinfo("Acerca de KForge", mensaje)


def ejecutar_interfaz():
    """Función para ejecutar la interfaz gráfica."""
    app = InterfazCompilador()
    app.mainloop()
