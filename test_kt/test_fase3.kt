// Test de la Fase 3: Arrays y Propiedades

// 1. Test de arrays básicos
var numeros: IntArray = intArrayOf(1, 2, 3, 4, 5)
var decimales: DoubleArray = doubleArrayOf(1.5, 2.5, 3.5)

// 2. Test de acceso a propiedad .size en arrays
var tamano: Int = numeros.size
var tam2: Int = decimales.size

// 3. Test de acceso a elementos de array
var primero: Int = numeros[0]
var segundo: Int = numeros[1]
var ultimo: Int = numeros[4]

// 4. Test de modificación de elementos de array
numeros[0] = 10
numeros[2] = 30

// 5. Test de propiedad .length en String
var mensaje: String = "Hola Mundo"
var longitud: Int = mensaje.length

// 6. Test de acceso encadenado: array[i].property (conceptual)
var valor: Int = numeros[0]
println("Primer elemento:")
println(valor)

// 7. Test de uso de .size en expresiones
var mitad: Int = numeros.size / 2
var total: Int = numeros.size + decimales.size

// 8. Test de .size en for loop
for (i in 0 until numeros.size) {
    var elem: Int = numeros[i]
}

// 9. Test de función que usa .size
fun obtenerTamano(arr: IntArray): Int {
    return arr.size
}

var tamanoDinamico: Int = obtenerTamano(numeros)

// 10. Test de comparaciones con .size y .length
if (numeros.size > 3) {
    println("Array grande")
}

if (mensaje.length > 5) {
    println("Mensaje largo")
}

// 11. Test de operaciones con .size
var capacidad: Int = numeros.size * 2
var promedio: Int = total / numeros.size
