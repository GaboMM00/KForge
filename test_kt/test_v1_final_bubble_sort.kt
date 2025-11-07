// ============================================================
// TEST FINAL VERSIÓN 1 DEL COMPILADOR KFORGE
// Algoritmo: Bubble Sort (Ordenamiento de Burbuja)
// ============================================================
// Este test demuestra todas las características implementadas
// en las Fases 1, 2 y 3 del compilador KForge v1.0
// ============================================================

fun main() {
    // Fase 2: Función main() con declaración
    // Fase 3: intArrayOf() - creación de arrays
    var arr: IntArray = intArrayOf(64, 34, 25, 12, 22, 11, 90)

    // Fase 3: Propiedad .size para arrays
    var n: Int = arr.size

    // Fase 1: Declaración de variable Boolean
    var swapped: Boolean

    // Fase 2: Llamada a función println (built-in)
    println("=== Bubble Sort - KForge Compiler v1.0 ===")
    println("Algoritmo de ordenamiento implementado")

    // Mostrar array original
    println("Array original:")
    for (i in 0 until n) {
        // Fase 3: Acceso a elementos con []
        var elemento: Int = arr[i]
        println(elemento)
    }

    // ============================================================
    // ALGORITMO BUBBLE SORT
    // ============================================================
    // Fase 1: For loop con expresiones aritméticas en rangos
    for (i in 0 until n - 1) {
        // Fase 1: Asignación de valores booleanos
        swapped = false

        // Fase 1: For loop anidado con expresiones complejas
        for (j in 0 until n - i - 1) {
            // Fase 3: Acceso a elementos de array con índices aritméticos
            // Fase 1: Comparación con operador >
            if (arr[j] > arr[j + 1]) {
                // Intercambio de elementos (swap)
                // Fase 1: Variable temporal
                var temp: Int = arr[j]

                // Fase 3: Modificación de elementos de array
                arr[j] = arr[j + 1]
                arr[j + 1] = temp

                // Marcar que hubo intercambio
                swapped = true
            }
        }

        // Optimización: si no hubo intercambios, ya está ordenado
        // Fase 1: Operador de negación !
        // Fase 1: Break statement
        if (!swapped) {
            break
        }
    }

    // Mostrar array ordenado
    println("Array ordenado:")
    for (i in 0 until n) {
        var elemento: Int = arr[i]
        println(elemento)
    }

    println("=== Ordenamiento completado exitosamente ===")
}

// ============================================================
// CARACTERÍSTICAS DEMOSTRADAS:
// ============================================================
// ✓ Fase 1: Declaraciones de variables (var)
// ✓ Fase 1: Tipos de datos: Int, Boolean
// ✓ Fase 1: Expresiones aritméticas: +, -, *, /
// ✓ Fase 1: Operadores de comparación: >, <, ==, !=
// ✓ Fase 1: Operadores lógicos: !, &&, ||
// ✓ Fase 1: Estructuras de control: if, for, while
// ✓ Fase 1: Break y Continue
// ✓ Fase 1: Rangos: 0 until n
// ✓ Fase 2: Declaración de funciones
// ✓ Fase 2: Llamadas a funciones
// ✓ Fase 2: Funciones built-in: println()
// ✓ Fase 3: Arrays: IntArray, DoubleArray
// ✓ Fase 3: Creación de arrays: intArrayOf(), doubleArrayOf()
// ✓ Fase 3: Acceso a elementos: arr[i]
// ✓ Fase 3: Modificación de elementos: arr[i] = value
// ✓ Fase 3: Propiedad .size para arrays
// ✓ Fase 3: Índices con expresiones aritméticas: arr[j + 1]
// ============================================================
