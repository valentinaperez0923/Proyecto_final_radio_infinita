# Decisiones de diseño

### Decisión 1: variante de radio infinita

Variante elegida: **radio para entrenar**. La señal de aprendizaje son las escuchas completas del oyente y la regla de programación propia son las pausas cada N temas. Elegimos esta combinación porque permite separar con claridad el estado (el historial del oyente, que es lo único que cambia) de los criterios de elección (que solo leen ese estado), y porque la regla de pausas se puede implementar como una transformación del flujo sin modificar el criterio que elige las canciones. También era la más simple de implementar y probar.

**Pausa:** se inserta una pausa cada N canciones (N es un parámetro de la emisora, así no se interrumpe la escucha del oyente, junto con la duración de la pausa).

**Escucha completa:** es el evento "terminó la canción entera". Es un dato binario por escucha: o la escuchó completa o no (la cortó o la saltó).

**Decisión:** el contador de pausas vive en el flujo.

La pausa cada N canciones es una regla de programación de la emisora, no una preferencia del oyente. Por eso se implementa como una transformación del flujo de canciones que inserta una `Pausa` cada N elementos, y el `Oyente` no conoce esa regla. Así el `Oyente` solo guarda sus gustos (el historial de escuchas) y dos oyentes comparten la misma regla sin duplicar estado.

**Alternativa descartada: contador en el `Oyente`.** Habría mezclado gustos con una regla de programación, y obligaba a actualizar el oyente en cada canción solo para saber cuándo tocaba la pausa. Tendría sentido si cada oyente pudiera tener su propio ritmo de pausas, pero no es un requisito de esta variante.

### Decisión 2: los criterios son funciones puras sobre las escuchas

Un criterio recibe una canción y la tupla de escuchas (decidimos que las canciones del oyente se guardaran en tuplas en vez de listas, porque estos datos son inmutables) del oyente, y devuelve un resultado. No recuerda nada entre una llamada y otra, no modifica nada y no tiene efectos secundarios.

Los criterios son de dos tipos:
- **Puntajes:** `(Cancion, escuchas) -> float`. Más alto es mejor. Son `afinidad` y `energia_objetivo`.
- **Filtros:** `(Cancion, escuchas) -> bool`. Si devuelve `False`, la canción no puede sonar ahora. Son `variedad` y `no_repetir_cancion`.

Los criterios que necesitan un valor de configuración (el objetivo de energía, o cuántas escuchas hacia atrás mira un filtro) se crean con una función que recibe ese valor y devuelve el criterio ya configurado (por ejemplo `energia_objetivo(8)` o `variedad(2)`). Así todos tienen la misma forma y se tratan igual. Agregar un criterio nuevo es escribir una función nueva, sin tocar las existentes.

Para que los criterios sean puros, no reciben al `Oyente` sino solo su historial. 
**Alternativa descartada: pasarle el `Oyente` completo al criterio.** Era más corto, pero el oyente es mutable y el resultado podía cambiar entre dos llamadas con los mismos argumentos, y para probar un criterio había que armar un oyente entero.

### Decisión 3: los criterios se combinan con filtros y puntajes

La radio primero aplica los **filtros** al catálogo y después suma los **puntajes** de las candidatas que sobreviven. Los filtros funcionan como veto: una afinidad alta no puede compensar la repetición de un artista o de una canción, porque es una condición, no un peso. Cada criterio sigue siendo una función independiente y ninguno se modifica para combinarlos.

**Alternativa descartada: suma ponderada de todos los criterios.** Era más simple y se afinaba cambiando pesos, pero permitía que una afinidad alta compensara la repetición de un artista, que es justamente lo que la regla de variedad quiere evitar.

**Caso borde: el filtro descarta todo el catálogo.** Si ninguna canción pasa los filtros, la radio emite la canción que hace más tiempo que no suena (una que nunca sonó, o que ya salió del historial). Así el flujo nunca se corta, y la elección es coherente con el objetivo de la variedad, porque se prioriza lo que menos se repitió.

### Decisión 4: el desempate se resuelve por el id de la canción

Cuando dos o más canciones empatan, ya sea en puntaje o en cuánto hace que no suenan, gana la de id más chico. Con esto el flujo depende solo de los datos y nunca del orden del catálogo ni del azar: con el mismo catálogo y el mismo oyente la radio produce siempre la misma secuencia.

**Alternativa descartada: desempatar al azar.** Habría dado más variedad, pero rompe la restricción de que, con los mismos datos, la radio produzca siempre el mismo flujo, y obligaría a inyectar una fuente de azar para poder probarla.

### Decisión 5: quién registra las escuchas

`registrar_escucha(cancion, completa)` lo llama quien consume el flujo (el programa principal o los tests), no la `Radio`. La `Radio` decide qué suena y el consumidor informa cómo terminó la escucha.

**Alternativa descartada: que la `Radio` registre.** Habría mezclado la regla de programación con el estado del oyente.

### Decisión 6: el oyente es mutable, pero los criterios no

El `Oyente` guarda su historial y `registrar_escucha` lo modifica agregando una `Escucha`. Elegimos esto porque el flujo es infinito y se consume de a poco: la radio lee el historial del mismo oyente cada vez que elige la siguiente canción, y así aprende de cada escucha sin que haya que entregarle un oyente nuevo en cada vuelta.

La mutación solo se da en el método de registro. La propiedad `escuchas` devuelve una tupla, así que los criterios solo pueden leer y nadie puede modificar el historial desde afuera. Dos oyentes simultáneos necesitan cada uno su propio objeto `Oyente`, y comparten la `Radio` y el `Catalogo`.

**Alternativa descartada: oyente inmutable.** `registrar_escucha` habría devuelto un oyente nuevo con el historial más largo. Mantenía todo puro, pero obligaba al consumidor a pasarle a la radio un oyente nuevo después de cada escucha, y con un flujo infinito eso complica el uso sin aportar una ventaja que necesitemos.

### Decisión 7: el oyente guarda todas las escuchas, completas o no

El historial guarda una `Escucha` (canción + si fue completa) por cada canción que sonó, no solo las completas.

Antes el oyente guardaba solo las escuchas completas. Eso dejaba un hueco: si alguien cortaba una canción, la radio no se enteraba de que había sonado y podía volver a ponerla enseguida. Ahora una canción cortada también cuenta para los filtros de variedad y de no repetir. Para el puntaje `afinidad` solo cuentan las completas, que sigue siendo la señal de aprendizaje de la variante.

### Decisión 8: el catálogo es fijo y el mismo para todos

El `Catalogo` es inmutable (una tupla de canciones) y se arma una sola vez. Se valida al crearlo: no puede estar vacío ni tener ids repetidos. Todos los oyentes comparten el mismo catálogo, y la `Radio` nunca lo modifica.

**Alternativa descartada: catálogo mutable con `agregar_cancion`.** Permitía agregar canciones, y un catálogo que cambia mientras el flujo está corriendo rompe la garantía de que los mismos datos dan el mismo flujo.

### Decisión 9: la energía se calcula a partir de los bpm

La `Cancion` guarda los `bpm` y la energía (de 1 a 10) se calcula, no se escribe a mano: cada 10 bpm por encima de 60 suma 1 punto, con mínimo 1 y máximo 10. Así un mismo dato no se guarda en dos lugares que puedan contradecirse. El puntaje `energia_objetivo(objetivo)` da `10 - |energia - objetivo|`: más puntos cuanto más cerca esté la energía del objetivo.

**Alternativa descartada: guardar la energía como dato de cada canción.** Era más simple, pero corríamos el riesgo de que los bpm y la energía no coincidieran.

### Decisión 10: el historial tiene un límite

El oyente recuerda solo sus últimas 100 escuchas (`memoria=100`), en una estructura que descarta las más viejas al agregar nuevas. Así el historial no crece para siempre en un flujo infinito, y además es una forma de minimización de datos.

El costo es que el oyente se "olvida" de lo que escuchó hace mucho: una canción que salió del historial se trata como si nunca hubiera sonado.

**Alternativa descartada: historial sin límite.** Era más simple, pero en una radio infinita la memoria crece sin fin y se guardan datos del oyente más tiempo del necesario.