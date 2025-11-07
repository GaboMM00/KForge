// Análisis de características necesarias para Bubble Sort

fun main() {
    // ✓ Fase 2: Funciones (main declarada)

    // ❌ NO IMPLEMENTADO: val (inmutabilidad)
    val arr = intArrayOf(64, 34, 25, 12, 22, 11, 90)

    // ✓ Fase 3: .size property
    val n = arr.size

    // ✓ Fase 1: var declaration con Boolean
    var swapped: Boolean

    // ❌ NO IMPLEMENTADO: String templates con ${}
    println("Antes de ordenar: ${arr.joinToString(", ")}")

    // ✓ Fase 1: for loops con rangos
    for (i in 0 until n - 1) {
        // ✓ Fase 1: asignación booleana
        swapped = false

        // ✓ Fase 1: nested for loops
        for (j in 0 until n - i - 1) {
            // ✓ Fase 3: array access con []
            // ✓ Fase 1: comparación con >
            if (arr[j] > arr[j + 1]) {
                // ✓ Fase 1: var declaration
                val temp = arr[j]

                // ✓ Fase 3: array element assignment
                arr[j] = arr[j + 1]
                arr[j + 1] = temp

                // ✓ Fase 1: boolean assignment
                swapped = true
            }
        }

        // ✓ Fase 1: negation operator !
        // ✓ Fase 1: break statement
        if (!swapped) break
    }

    // ❌ NO IMPLEMENTADO: String templates
    println("Después de ordenar: ${arr.joinToString(", ")}")
}
