// ============================================================
// TEST FINAL VERSIÓN 1.0 DEL COMPILADOR KFORGE
// Algoritmo: Bubble Sort (Ordenamiento de Burbuja)
// ============================================================
// Basado en el código original propuesto por el usuario
// Adaptado para usar solo las características implementadas
// ============================================================

fun main() {
    var arr: IntArray = intArrayOf(64, 34, 25, 12, 22, 11, 90)
    var n: Int = arr.size
    var swapped: Boolean

    println("=== Bubble Sort - KForge v1.0 ===")
    println("Array original:")

    // Mostrar array antes de ordenar
    for (i in 0 until n) {
        println(arr[i])
    }

    // ============================================================
    // ALGORITMO BUBBLE SORT
    // ============================================================
    for (i in 0 until n - 1) {
        swapped = false

        for (j in 0 until n - i - 1) {
            if (arr[j] > arr[j + 1]) {
                // Intercambio de elementos (swap)
                var temp: Int = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp
                swapped = true
            }
        }

        // Si no hubo intercambios, el array ya está ordenado
        if (!swapped) {
            break
        }
    }

    println("Array ordenado:")

    // Mostrar array después de ordenar
    for (i in 0 until n) {
        println(arr[i])
    }

    println("=== Ordenamiento completado ===")
}
