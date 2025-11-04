"""
Editor de código con numeración de líneas para la interfaz del compilador.
"""

import tkinter as tk
from tkinter import font


class EditorConLineas(tk.Frame):
    """
    Widget de editor de texto con numeración de líneas.

    Componentes:
    - Panel de números de línea (izquierda)
    - Área de texto principal (derecha)
    - Sincronización de scroll entre ambos
    """

    def __init__(self, parent, *args, **kwargs):
        """
        Inicializa el editor con numeración de líneas.

        Args:
            parent: Widget padre.
        """
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Configurar fuente monoespaciada
        self.fuente = font.Font(family="Consolas", size=12)

        # Crear canvas para números de línea
        self.canvas_lineas = tk.Canvas(
            self,
            width=50,
            bg="#f0f0f0",
            highlightthickness=0
        )
        self.canvas_lineas.pack(side=tk.LEFT, fill=tk.Y)

        # Crear área de texto principal
        self.texto = tk.Text(
            self,
            font=self.fuente,
            wrap=tk.NONE,
            undo=True,
            maxundo=-1,
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
            selectbackground="#0078d7",
            selectforeground="#ffffff",
            relief=tk.FLAT,
            borderwidth=0
        )
        self.texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configurar scrollbar vertical
        self.scrollbar_y = tk.Scrollbar(self, orient=tk.VERTICAL, command=self._scroll_vertical)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar scrollbar horizontal
        self.scrollbar_x = tk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.texto.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Vincular texto con scrollbars
        self.texto.config(
            yscrollcommand=self._actualizar_scrollbar_y,
            xscrollcommand=self.scrollbar_x.set
        )

        # Configurar eventos para actualizar numeración
        self.texto.bind("<KeyRelease>", self._actualizar_lineas)
        self.texto.bind("<MouseWheel>", self._actualizar_lineas)
        self.texto.bind("<Button-1>", self._actualizar_lineas)
        self.texto.bind("<Configure>", self._actualizar_lineas)

        # Configurar resaltado de sintaxis básico
        self._configurar_tags()

        # Actualizar numeración inicial
        self.after(10, self._actualizar_lineas)

    def _configurar_tags(self):
        """Configura tags para resaltado de sintaxis básico."""
        # Palabras clave
        self.texto.tag_config("keyword", foreground="#0000FF", font=(self.fuente.actual()["family"],
                                                                     self.fuente.actual()["size"], "bold"))
        # Comentarios
        self.texto.tag_config("comment", foreground="#008000", font=(self.fuente.actual()["family"],
                                                                      self.fuente.actual()["size"], "italic"))
        # Strings
        self.texto.tag_config("string", foreground="#A31515")
        # Números
        self.texto.tag_config("number", foreground="#098658")
        # Tipos
        self.texto.tag_config("type", foreground="#2B91AF")

    def _scroll_vertical(self, *args):
        """Maneja el scroll vertical sincronizado."""
        self.texto.yview(*args)
        self._actualizar_lineas()

    def _actualizar_scrollbar_y(self, *args):
        """Actualiza la scrollbar vertical."""
        self.scrollbar_y.set(*args)
        self._actualizar_lineas()

    def _actualizar_lineas(self, event=None):
        """Actualiza la numeración de líneas."""
        # Limpiar canvas
        self.canvas_lineas.delete("all")

        # Obtener rango visible
        primera_linea = self.texto.index("@0,0")
        ultima_linea = self.texto.index(f"@0,{self.texto.winfo_height()}")

        # Extraer números de línea
        inicio = int(primera_linea.split('.')[0])
        fin = int(ultima_linea.split('.')[0]) + 1

        # Dibujar números de línea
        for i in range(inicio, fin + 1):
            # Obtener coordenadas Y de la línea
            dlineinfo = self.texto.dlineinfo(f"{i}.0")
            if dlineinfo is None:
                continue

            y = dlineinfo[1]
            altura = dlineinfo[3]

            # Dibujar número de línea
            self.canvas_lineas.create_text(
                45,  # Posición X (derecha del canvas)
                y + altura // 2,  # Posición Y (centro vertical)
                text=str(i),
                anchor=tk.E,
                font=self.fuente,
                fill="#888888"
            )

    def get(self, inicio, fin=None):
        """
        Obtiene el texto del editor.

        Args:
            inicio: Posición inicial.
            fin: Posición final (opcional).

        Returns:
            Texto del editor.
        """
        if fin is None:
            return self.texto.get(inicio)
        return self.texto.get(inicio, fin)

    def insert(self, posicion, texto):
        """
        Inserta texto en el editor.

        Args:
            posicion: Posición donde insertar.
            texto: Texto a insertar.
        """
        self.texto.insert(posicion, texto)
        self._actualizar_lineas()

    def delete(self, inicio, fin=None):
        """
        Elimina texto del editor.

        Args:
            inicio: Posición inicial.
            fin: Posición final (opcional).
        """
        if fin is None:
            self.texto.delete(inicio)
        else:
            self.texto.delete(inicio, fin)
        self._actualizar_lineas()

    def limpiar(self):
        """Limpia todo el contenido del editor."""
        self.texto.delete("1.0", tk.END)
        self._actualizar_lineas()

    def obtener_texto(self) -> str:
        """
        Obtiene todo el texto del editor.

        Returns:
            Contenido completo del editor.
        """
        return self.texto.get("1.0", tk.END).rstrip()

    def establecer_texto(self, texto: str):
        """
        Establece el texto del editor.

        Args:
            texto: Texto a establecer.
        """
        self.limpiar()
        self.insert("1.0", texto)

    def aplicar_resaltado_basico(self):
        """Aplica resaltado de sintaxis básico al texto actual."""
        # Remover tags existentes
        for tag in ["keyword", "comment", "string", "number", "type"]:
            self.texto.tag_remove(tag, "1.0", tk.END)

        contenido = self.obtener_texto()
        lineas = contenido.split('\n')

        # Palabras clave de Kotlin
        palabras_clave = {'var', 'val', 'if', 'else', 'while', 'for', 'in', 'fun', 'return',
                          'when', 'class', 'object', 'interface', 'true', 'false'}
        tipos = {'Int', 'Double', 'String', 'Boolean', 'Unit'}

        for num_linea, linea in enumerate(lineas, 1):
            # Comentarios
            if '//' in linea:
                indice_comentario = linea.index('//')
                inicio = f"{num_linea}.{indice_comentario}"
                fin = f"{num_linea}.{len(linea)}"
                self.texto.tag_add("comment", inicio, fin)
                linea = linea[:indice_comentario]  # Procesar solo antes del comentario

            # Strings
            en_string = False
            inicio_string = 0
            for i, char in enumerate(linea):
                if char == '"' and (i == 0 or linea[i-1] != '\\'):
                    if not en_string:
                        inicio_string = i
                        en_string = True
                    else:
                        inicio = f"{num_linea}.{inicio_string}"
                        fin = f"{num_linea}.{i+1}"
                        self.texto.tag_add("string", inicio, fin)
                        en_string = False

            # Palabras clave y tipos
            palabras = linea.split()
            col_actual = 0
            for palabra in palabras:
                # Encontrar la posición exacta
                col_actual = linea.find(palabra, col_actual)
                if col_actual == -1:
                    continue

                palabra_limpia = palabra.strip('(){}[],:;')
                if palabra_limpia in palabras_clave:
                    inicio = f"{num_linea}.{col_actual}"
                    fin = f"{num_linea}.{col_actual + len(palabra_limpia)}"
                    self.texto.tag_add("keyword", inicio, fin)
                elif palabra_limpia in tipos:
                    inicio = f"{num_linea}.{col_actual}"
                    fin = f"{num_linea}.{col_actual + len(palabra_limpia)}"
                    self.texto.tag_add("type", inicio, fin)
                elif palabra_limpia.isdigit() or self._es_numero(palabra_limpia):
                    inicio = f"{num_linea}.{col_actual}"
                    fin = f"{num_linea}.{col_actual + len(palabra_limpia)}"
                    self.texto.tag_add("number", inicio, fin)

                col_actual += len(palabra)

    def _es_numero(self, texto: str) -> bool:
        """Verifica si el texto es un número (int o double)."""
        try:
            float(texto)
            return True
        except ValueError:
            return False
