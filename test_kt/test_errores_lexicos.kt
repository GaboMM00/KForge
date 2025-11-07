// ============================================
// TEST DE ERRORES LÉXICOS
// ============================================
// Este archivo contiene errores léxicos que el analizador
// léxico de KForge detecta actualmente.
//
// Nota: Ver docs/errores_lexicos_pendientes.md para una lista completa
// de errores léxicos pendientes de implementación.

fun main() {
    // ERROR 1: Caracter '@' no reconocido
    var x: Int = 10 @ 5

    // ERROR 2: String sin cerrar
    var mensaje: String = "Hola mundo

    // ERROR 3: Caracter '#' no reconocido
    var dato: Int = 10 # 5

    // ERROR 4: Caracter '$' no reconocido
    var precio: Double = $19.99

    // ERROR 5: Caracter '&' no reconocido (el lexer espera '&&')
    var comp: Boolean = x & y

    // ERROR 6: Caracter '~' no reconocido
    var invertido: Int = ~x

    // ERROR 7: Caracter '^' no reconocido
    var potencia: Int = 2 ^ 8

    // ERROR 8: Caracter '|' no reconocido (el lexer espera '||')
    var resultado: Boolean = true | false
}
