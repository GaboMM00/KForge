// ============================================
// TEST DE ERRORES SEMÁNTICOS
// ============================================
// Este archivo contiene errores semánticos que el analizador
// semántico de KForge debe detectar.

// ERROR 1: Variable no declarada
fun test1() {
    var x: Int = 10
    var y: Int = z + 5
}

// ERROR 2: Tipos incompatibles en asignación
fun test2() {
    var x: Int = "Hola"
}

// ERROR 3: Operación aritmética con tipos incompatibles
fun test3() {
    var x: Int = 10
    var y: String = "5"
    var z: Int = x + y
}

// ERROR 4: Uso de variable antes de inicialización
fun test4() {
    var x: Int
    var y: Int = x + 5
}

// ERROR 5: Función no declarada
fun test5() {
    var x: Int = sumar(10, 20)
}

// ERROR 6: Número incorrecto de argumentos
fun suma(a: Int, b: Int): Int {
    return a + b
}

fun test6() {
    var x: Int = suma(10)
}

// ERROR 7: Tipo de argumento incorrecto
fun test7() {
    var x: Int = suma("10", "20")
}

// ERROR 8: Return en función sin tipo de retorno
fun test8() {
    var x: Int = 10
    return x
}

// ERROR 9: Tipo de retorno incorrecto
fun multiplicar(a: Int, b: Int): Int {
    return "resultado"
}

// ERROR 10: Operador lógico en tipos no booleanos
fun test10() {
    var x: Int = 10
    var y: Int = 20
    var z: Boolean = x && y
}

// ERROR 11: Comparación de tipos incompatibles
fun test11() {
    var x: Int = 10
    var y: String = "10"
    var z: Boolean = x == y
}

// ERROR 12: Índice de array no Int
fun test12() {
    var arr: IntArray = intArrayOf(1, 2, 3)
    var x: Int = arr["0"]
}

// ERROR 13: Acceso a índice de variable que no es array
fun test13() {
    var x: Int = 10
    var y: Int = x[0]
}

// ERROR 14: Propiedad .size en tipo no soportado
fun test14() {
    var x: Int = 10
    var y: Int = x.size
}

// ERROR 15: Operador de negación en tipo no booleano
fun test15() {
    var x: Int = 10
    var y: Boolean = !x
}

// ERROR 16: Variable declarada dos veces en mismo scope
fun test16() {
    var x: Int = 10
    var x: Double = 20.5
}

// ERROR 17: Función declarada dos veces
fun duplicada(a: Int): Int {
    return a * 2
}

fun duplicada(a: Int): Int {
    return a * 3
}

// ERROR 18: Operación de módulo con Double
fun test18() {
    var x: Double = 10.5
    var y: Double = 3.0
    var z: Double = x % y
}

// ERROR 19: Break fuera de loop
fun test19() {
    var x: Int = 10
    if (x > 5) {
        break
    }
}

// ERROR 20: Continue fuera de loop
fun test20() {
    var x: Int = 10
    if (x > 5) {
        continue
    }
}

fun main() {
    println("Test de errores semanticos")
}
