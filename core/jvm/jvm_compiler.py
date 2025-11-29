"""
JVM Compiler - Integrador completo TAC -> JVM .class

Conecta todo el pipeline:
1. TAC generado por el frontend
2. JVM bytecode generation
3. ClassFile creation con debugging info
4. Escritura de archivo .class ejecutable

Este modulo es el punto de entrada principal para compilacion JVM.
"""

from typing import List, Optional
from pathlib import Path

from core.tac import TACInstruction
from core.utils import TipoDato
from core.jvm.jvm_generator import JVMGenerator
from core.jvm.classfile import ClassFileWriter, MethodInfo, CodeAttribute, AccessFlags
from core.jvm.runtime import RuntimeHelper, create_main_method
from core.jvm.attributes import create_line_number_table, create_local_variable_table


class JVMCompiler:
    """
    Compilador JVM completo.

    Toma instrucciones TAC y genera un archivo .class ejecutable.
    """

    def __init__(self, class_name: str = "Main", java_version: int = 6):
        """
        Inicializa el compilador JVM.

        Args:
            class_name: Nombre de la clase a generar
            java_version: Version de Java target (6, 7, 8)
        """
        self.class_name = class_name
        self.java_version = java_version
        self.writer = ClassFileWriter(class_name, java_version=java_version)
        self.runtime_helper = RuntimeHelper(self.writer.constant_pool)

    def compile(self, tac_instructions: List[TACInstruction],
                source_file: str = "Main.kt",
                add_debug_info: bool = True) -> bytes:
        """
        Compila instrucciones TAC a bytecode JVM.

        Args:
            tac_instructions: Lista de instrucciones TAC
            source_file: Nombre del archivo fuente
            add_debug_info: Si agregar LineNumberTable y LocalVariableTable

        Returns:
            Bytecode del archivo .class completo
        """
        # Agregar SourceFile attribute
        self.writer.add_source_file(source_file)

        # Generar bytecode JVM
        generator = JVMGenerator(self.writer.constant_pool)
        bytecode, max_stack, max_locals = generator.generate(tac_instructions)

        # max_stack y max_locals ya vienen del generator
        # Asegurar al menos 1 para args[]
        max_locals = max(max_locals, 1)

        code_name_idx = self.writer.constant_pool.add_utf8("Code")
        code_attr = CodeAttribute(
            code_name_idx,
            max_stack=max_stack,
            max_locals=max_locals,
            code=bytecode
        )

        # Agregar debugging info si se solicita
        if add_debug_info:
            # LineNumberTable - mapeo PC a lineas
            # Por ahora usamos mapeo simple 1:1
            pc_to_line = self._generate_line_mappings(tac_instructions)
            if pc_to_line:
                lnt = create_line_number_table(self.writer.constant_pool, pc_to_line)
                code_attr.add_sub_attribute(lnt)

            # LocalVariableTable - info de variables
            variables = self._generate_variable_info(generator)
            if variables:
                lvt = create_local_variable_table(self.writer.constant_pool, variables)
                code_attr.add_sub_attribute(lvt)

        # Crear metodo main
        name_idx = self.writer.constant_pool.add_utf8("main")
        desc_idx = self.writer.constant_pool.add_utf8("([Ljava/lang/String;)V")

        method = MethodInfo(
            AccessFlags.ACC_PUBLIC | AccessFlags.ACC_STATIC,
            name_idx,
            desc_idx
        )
        method.add_attribute(code_attr)

        # Agregar metodo a la clase
        self.writer.add_method(method)

        # Generar archivo .class completo
        return self.writer.to_bytes()

    def compile_to_file(self, tac_instructions: List[TACInstruction],
                        output_path: str,
                        source_file: str = "Main.kt",
                        add_debug_info: bool = True) -> str:
        """
        Compila TAC y escribe archivo .class.

        Args:
            tac_instructions: Lista de instrucciones TAC
            output_path: Ruta donde escribir el .class
            source_file: Nombre del archivo fuente
            add_debug_info: Si agregar debugging info

        Returns:
            Ruta del archivo .class generado
        """
        # Compilar
        bytecode = self.compile(tac_instructions, source_file, add_debug_info)

        # Asegurar extension .class
        if not output_path.endswith('.class'):
            output_path += '.class'

        # Escribir archivo
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(bytecode)

        return output_path

    def _generate_line_mappings(self, tac_instructions: List[TACInstruction]) -> List[tuple]:
        """
        Genera mapeo de PC offset a lineas de codigo.

        Por ahora implementacion simple: cada instruccion TAC = 1 linea.

        Args:
            tac_instructions: Instrucciones TAC

        Returns:
            Lista de tuplas (pc_offset, line_number)
        """
        mappings = []
        pc = 0
        line = 1

        for instr in tac_instructions:
            # Mapear PC actual a linea
            mappings.append((pc, line))

            # Estimar tamaño aproximado de la instruccion
            # (esto es simplificado, el tamaño real depende de la instruccion)
            pc += 3  # Estimacion promedio

            line += 1

        return mappings

    def _generate_variable_info(self, generator: JVMGenerator) -> List[tuple]:
        """
        Genera informacion de variables locales para debugging.

        Args:
            generator: Generador JVM usado

        Returns:
            Lista de tuplas (start_pc, length, name, descriptor, index)
        """
        variables = []

        # Obtener todas las variables del manager
        for var_name, slot in generator.var_manager.var_to_slot.items():
            var_type = generator.var_manager.var_types.get(var_name, TipoDato.INT)

            # Descriptor del tipo
            if var_type == TipoDato.INT:
                descriptor = "I"
            elif var_type == TipoDato.DOUBLE:
                descriptor = "D"
            elif var_type == TipoDato.STRING:
                descriptor = "Ljava/lang/String;"
            elif var_type == TipoDato.BOOLEAN:
                descriptor = "Z"
            else:
                descriptor = "Ljava/lang/Object;"

            # Por ahora: start_pc=0, length=todo el metodo
            # (esto es simplificado, idealmente calculariamos el scope real)
            variables.append((0, 100, var_name, descriptor, slot))

        return variables

    def get_info(self) -> dict:
        """
        Obtiene informacion del .class generado.

        Returns:
            Diccionario con informacion del class file
        """
        return self.writer.get_class_info()


def compile_kotlin_to_jvm(tac_instructions: List[TACInstruction],
                          class_name: str = "Main",
                          output_path: Optional[str] = None,
                          source_file: str = "Main.kt",
                          java_version: int = 6,
                          add_debug_info: bool = True) -> bytes:
    """
    Helper function para compilar TAC a JVM bytecode.

    Args:
        tac_instructions: Instrucciones TAC generadas
        class_name: Nombre de la clase
        output_path: Si se especifica, escribe el .class a este path
        source_file: Nombre del archivo fuente
        java_version: Version de Java (6, 7, 8)
        add_debug_info: Si agregar LineNumberTable y LocalVariableTable

    Returns:
        Bytecode del archivo .class

    Example:
        >>> from core.tac import TACGenerator
        >>> tac_gen = TACGenerator()
        >>> tac = tac_gen.generate(ast)
        >>> bytecode = compile_kotlin_to_jvm(tac, "MiPrograma")
    """
    compiler = JVMCompiler(class_name, java_version)

    if output_path:
        compiler.compile_to_file(tac_instructions, output_path, source_file, add_debug_info)
        return compiler.writer.to_bytes()
    else:
        return compiler.compile(tac_instructions, source_file, add_debug_info)
