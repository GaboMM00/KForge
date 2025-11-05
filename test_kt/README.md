# Test Kotlin Files (`test_kt/`)

Esta carpeta contiene **archivos de código Kotlin** (`.kt`) que sirven como casos de prueba para el compilador KForge.

## 📁 Propósito

Los archivos en esta carpeta son **código fuente Kotlin** que prueba características específicas del lenguaje implementadas en cada fase del desarrollo.

## 📝 Archivos Actuales

### `test_fase1.kt`
Prueba todas las características implementadas en la **Fase 1**:
- Palabra clave `until` en loops
- Operadores lógicos `&&` y `||`
- Declaraciones de variables sin inicialización
- Palabras clave `break` y `continue`
- Combinaciones de las características anteriores

## 🔄 Cómo Usar Estos Tests

Estos archivos **NO se ejecutan directamente**. Son usados por los scripts Python en la carpeta `tests/`:

```bash
# Desde la raíz del proyecto
python tests/test_compilador.py test_kt/test_fase1.kt
```

O puedes cargarlos en la UI gráfica de KForge.

## ➕ Agregar Nuevos Tests

Cuando implementes una nueva fase, crea un nuevo archivo:

```bash
# Para Fase 2
test_kt/test_fase2.kt

# Para Fase 3
test_kt/test_fase3.kt
```

### Plantilla para Nuevos Tests

```kotlin
// Test de la Fase N: [Descripción]

// 1. Test de [característica 1]
// Código de prueba aquí

// 2. Test de [característica 2]
// Código de prueba aquí

// 3. Test combinado
// Código que combina varias características
```

## ✅ Convenciones

1. **Nombres**: `test_faseN.kt` donde N es el número de fase
2. **Comentarios**: Cada sección de prueba debe estar comentada
3. **Organización**: Agrupar tests por característica
4. **Cobertura**: Cubrir casos normales y casos edge

## 📚 Referencias

- Ver `ROADMAP.md` para el plan completo de fases
- Ver `tests/README.md` para los scripts de test Python
