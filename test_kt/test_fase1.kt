// Test de la Fase 1: Operadores y Control de Flujo Básico

// 1. Test de 'until'
var suma: Int = 0
for (i in 0 until 5) {
    suma = suma + i
}

// 2. Test de operadores lógicos && y ||
var x: Int = 10
var y: Int = 5
var resultado: Boolean

if (x > 5 && y < 10) {
    resultado = true
}

if (x < 0 || y > 0) {
    resultado = false
}

// 3. Test de declaración sin inicialización
var contador: Int
contador = 0

// 4. Test de break
var n: Int = 0
while (n < 10) {
    if (n == 5) {
        break
    }
    n = n + 1
}

// 5. Test de continue
var j: Int = 0
while (j < 10) {
    j = j + 1
    if (j == 5) {
        continue
    }
}

// 6. Test combinado
var activo: Boolean = true
for (k in 0 until 3) {
    if (activo && k > 0) {
        break
    }
}
