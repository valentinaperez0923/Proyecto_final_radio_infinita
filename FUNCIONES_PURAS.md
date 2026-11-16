# Funciones del núcleo: ¿son puras?

Una función es **pura** si con los mismos argumentos devuelve siempre lo mismo y no cambia nada fuera de ella: no modifica objetos, no imprime y no depende del reloj ni del azar.

| Función | Archivo | ¿Pura? | Por qué / si no es pura, por qué está ahí |
|---|---|---|---|
| `Cancion.energia` | `modelo.py` | Sí | Se calcula solo con los bpm de la canción, que no cambian (la canción es inmutable). |
| Validaciones (`__post_init__` de `Cancion`, `Pausa` y `Catalogo`) | `modelo.py` | Sí | Solo revisan los datos y dan error si no son válidos. No modifican nada. |
| `Oyente.registrar_escucha` | `modelo.py` | **No** | Modifica el historial del oyente. Está ahí porque la radio tiene que aprender: alguien tiene que recordar lo que pasó. Concentramos ese cambio en un único método del único objeto mutable (decisión 6). |
| `Oyente.escuchas` | `modelo.py` | **No** | No modifica nada, pero devuelve distinto según lo que se haya registrado antes: depende del estado del oyente, no de sus argumentos. Está ahí para que los criterios reciban una copia que no se puede modificar (una tupla) y no al oyente entero (decisión 2). |
| `afinidad` | `criterios.py` | Sí | Solo lee la canción y la tupla de escuchas. |
| `energia_objetivo(objetivo)` | `criterios.py` | Sí | Devuelve un puntaje; el puntaje que devuelve también es puro. |
| `ponderado(peso, puntaje)` | `criterios.py` | Sí | Devuelve un puntaje nuevo. Es puro siempre que el puntaje que recibe sea puro. |
| `_sin_repetir`, `variedad`, `no_repetir_cancion` | `criterios.py` | Sí | Devuelven filtros puros. Dan error si `ultimas` es menor que 1. |
| `la_que_hace_mas_que_no_suena` | `radio.py` | Sí | Con las mismas canciones y escuchas devuelve siempre la misma canción. |
| `elegir` | `radio.py` | Sí | Es el centro de la radio: con las mismas canciones, escuchas y criterios devuelve siempre la misma canción, incluso si hay empates (decisión 4). |
| `con_pausas` | `radio.py` | Sí | Es un generador: no modifica nada y con la misma entrada produce la misma secuencia. Lo único que hace es ir recorriendo el iterador que recibe, que es lo normal en un generador. |
| `Radio.elegir_siguiente` | `radio.py` | **No** | Lee el historial actual del oyente: con el mismo oyente puede devolver otra canción después de un registro. Es el puente entre el oyente (que cambia) y `elegir` (pura). |
| `Radio.canciones` | `radio.py` | **No** | Generador infinito que llama a `elegir_siguiente`. Cada canción depende del historial en el momento en que se pide. |
| `Radio.flujo` | `radio.py` | **No** | Compone `canciones` con `con_pausas` y por eso también depende del estado del oyente. Tiene que ser así para que la radio aprenda mientras se consume el flujo (decisión 14). |
| `escucho_completa` | `main.py` | Sí | Simula al oyente con una regla fija (energía 7 o más). En una radio real no sería una función pura: la respuesta vendría de la persona. |
| `texto_cancion`, `texto_pausa` | `main.py` | Sí | Arman el texto sin imprimirlo. |
| `main` | `main.py` | **No** | Imprime en pantalla y registra las escuchas. Es a propósito el lugar donde se juntan los efectos, para que el resto del programa solo calcule. |

**Resumen.** El único cambio de estado está en `Oyente.registrar_escucha`, y lo único que se muestra en pantalla está en `main`. Las funciones no puras de `Radio` no modifican nada: solo leen el estado del oyente en el momento en que se las llama.
