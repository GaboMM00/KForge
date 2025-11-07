// ============================================
// TEST DE ERRORES LÉXICOS
// ============================================
// Este archivo contiene errores léxicos que el analizador
// léxico de KForge detecta actualmente.

fun main() {
    // ERROR 1: Caracter '@' no reconocido
    var x: Int = 10 @ 5

    // ERROR 2: String sin cerrar
    var mensaje: String = "Hola mundo

    // ERROR 3: Caracter '#' no reconocido
    var dato: Int = 10 # 5

    // ERROR 4: Caracter '$' no reconocido (pero '\$' en string es válido)
    var precio: Double = $19.99

    // ERROR 5: Caracter '&' no reconocido (el lexer espera '&&')
    var comp: Boolean = x & y

    // ERROR 6: Caracter '~' no reconocido
    var invertido: Int = ~x

    // ERROR 7: Caracter '^' no reconocido
    var potencia: Int = 2 ^ 8

    // ERROR 8: Caracter '|' no reconocido (el lexer espera '||')
    var resultado: Boolean = true | false

    // ERROR 9: Comentario de bloque sin cerrar
    /* Este es un comentario
       que nunca se cierra
    var y: Int = 10

    // ERROR 10: Sufijo de tipo inválido en número
    var largo: Int = 100L

    // ERROR 11: Sufijo de tipo inválido en decimal
    var flotante: Double = 3.14f

    // ERROR 12: Secuencia de escape inválida en string
    var texto1: String = "Hola\kMundo"

    // ERROR 13: Secuencia de escape unicode incompleta
    var texto2: String = "Unicode\u12"

    // ERROR 14: Secuencia de escape no reconocida
    var texto3: String = "Test\x"
}
