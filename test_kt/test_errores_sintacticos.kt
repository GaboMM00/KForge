// ============================================
// TEST DE ERRORES SINTÁCTICOS
// ============================================
// Este archivo contiene errores sintácticos que el analizador
// sintáctico (parser) de KForge debe detectar.

// ERROR 1: Falta tipo de variable
fun test1() {
    var x = 10
}

// ERROR 2: Falta símbolo '=' en asignación (en la misma línea)
fun test2() {
    var arr: IntArray intArrayOf(1, 2, 3)
}

// ERROR 3: Falta paréntesis de cierre en expresión
fun test3() {
    var resultado: Int = (10 + 5
}

// ERROR 4: Falta llave de cierre en función
fun test4() {
    var x: Int = 10
    println(x)
// Falta '}'

// ERROR 5: Falta 'in' en for loop
fun test5() {
    for (i 0..10) {
        println(i)
    }
}

// ERROR 6: Falta dos puntos ':' antes del tipo
fun test6() {
    var numero Int = 20
}

// ERROR 7: Falta tipo de retorno con return explícito
fun test7() {
    return 42
}

// ERROR 8: Falta coma en lista de parámetros
fun test8(a: Int b: Int): Int {
    return a + b
}

// ERROR 9: Falta paréntesis en llamada a función
fun test9() {
    println "Hola mundo"
}

// ERROR 10: Falta condición en if
fun test10() {
    if {
        println("Error")
    }
}

// ERROR 11: Falta corchete de cierre en array
fun test11() {
    var arr: IntArray = intArrayOf(1, 2, 3
}

// ERROR 12: Expresión incompleta
fun test12() {
    var x: Int = 10 +
}

// ERROR 13: Falta cuerpo de función
fun test13()

// ERROR 14: Operador inválido en posición incorrecta
fun test14() {
    var x: Int = + 10
}

// ERROR 15: Falta paréntesis de cierre en while
fun test15() {
    while (x < 10 {
        x = x + 1
    }
}
