// Test de la Fase 2: Funciones y Llamadas

// 1. Test de declaración de funciones simples
fun suma(a: Int, b: Int): Int {
    return a + b
}

fun resta(x: Int, y: Int): Int {
    return x - y
}

// 2. Test de función sin parámetros
fun saludar(): Unit {
    var mensaje: String = "Hola"
}

// 3. Test de función con múltiples parámetros
fun multiplicar(a: Int, b: Int, c: Int): Int {
    var resultado: Int = a * b
    resultado = resultado * c
    return resultado
}

// 4. Test de llamadas a funciones
var resultado1: Int = suma(5, 3)
var resultado2: Int = resta(10, 4)
var resultado3: Int = multiplicar(2, 3, 4)

// 5. Test de función que usa otra función
fun calcular(x: Int, y: Int): Int {
    var temp: Int = suma(x, y)
    return temp
}

var resultado4: Int = calcular(7, 8)

// 6. Test de funciones built-in
var arr: IntArray = intArrayOf(1, 2, 3, 4, 5)
println("Resultado de suma: ")
println(resultado1)

// 7. Test de función con variables locales
fun procesar(n: Int): Int {
    var local: Int = n * 2
    var otro: Int = local + 10
    return otro
}

var resultado5: Int = procesar(5)
