### Decisión 1: variante de radio infinita

Variante elegida: Radio para entrenar. La señal de aprendizaje son las escuchas completas del oyente y la regla de programación propia son las pausas cada N temas. Elegimos esta combinación porque permite separar con claridad el estado (el historial del oyente, que es lo único que cambia) de los criterios de elección (que solo leen ese estado), y porque la regla de pausas se puede implementar como una transformación del flujo sin modificar el criterio que elige las canciones.

Pausa: se inserta una pausa cada N canciones (N es un parámetro de la emisora).

Escucha completa: es el evento "terminó la canción entera". Es un dato binario por escucha: o la escuchó completa o no (la cortó/saltó).

Decisión: el contador de pausas vive en el flujo.

La pausa cada N canciones es una regla de programación de la emisora, no una preferencia del oyente. Por eso se implementa como una transformación del flujo de canciones que inserta una Pausa cada N elementos, y el Oyente no conoce esa regla. Así el Oyente solo guarda sus gustos (el historial de escuchas) y dos oyentes comparten la misma regla sin duplicar estado.

**Alternativa descartada: contador en el Oyente.** Habría mezclado gustos con una regla de programación, y obligaba a actualizar el oyente en cada canción solo para saber cuándo tocaba la pausa. Tendría sentido si cada oyente pudiera tener su propio ritmo de pausas, pero no es un requisito de esta variante.

### Decisión 2: los criterios de elección son funciones

Un criterio recibe una canción y un oyente y devuelve un puntaje, y no necesita recordar nada entre una llamada y otra: el único estado relevante vive en el `Oyente`, que es mutable (ver Decisión 6). Un criterio solo lee al oyente, nunca lo modifica ni produce otros efectos. Por eso modelamos los tres criterios (afinidad según el historial de escuchas completas, energía para entrenar y variedad) como funciones: los que puntúan tienen la forma (Cancion, Oyente) -> float y los que filtran, (Cancion, Oyente) -> bool. Los que necesitan un valor de configuración, como el nivel de energía objetivo o la cantidad de canciones hacia atrás que mira la variedad, lo reciben fijado de antemano, de modo que todos se tratan igual. Esto permite agregar un criterio nuevo escribiendo una función nueva, sin modificar las existentes, y combinarlos con funciones de orden superior.

Como el oyente es mutable, estas funciones no son puras en sentido estricto: con los mismos argumentos pueden dar otro resultado si el oyente cambió entre una llamada y otra. Sin embargo, no tienen efectos secundarios y se prueban armando un oyente a mano. Esto lo registramos en la tabla de funciones del núcleo.

**Alternativa descartada: una clase por criterio con una interfaz común.** Habría dado polimorfismo explícito y los parámetros como atributos, pero cada clase habría tenido un solo método y ningún estado que proteger, así que agregaba estructura sin aportar nada al diseño.

### Decisión 3: los criterios se combinan con filtros y puntajes

Los criterios se dividen en dos tipos. Los **filtros** (variedad) responden si una canción puede sonar ahora y funcionan como veto: una canción que no los pasa queda descartada. Los **puntajes** (afinidad según el historial de escuchas completas y energía para entrenar) ordenan las canciones que sobreviven. La radio primero aplica los filtros al catálogo y después suma los puntajes de las candidatas restantes. De este modo la regla de variedad no se puede compensar con una afinidad alta: es una condición, no un peso. Cada criterio sigue siendo una función independiente y ninguno se modifica para combinarlos.

**Alternativa descartada: suma ponderada de todos los criterios.** Era más simple y se afinaba cambiando pesos, pero permitía que una afinidad alta compensara la repetición de un artista, que es justamente lo que la regla de variedad quiere evitar.

**Caso borde: el filtro descarta todo el catálogo.** Si ninguna canción pasa los filtros (por ejemplo, con un catálogo chico en el que todos los artistas sonaron hace poco), la radio emite la canción que hace más tiempo que no suena. De esta forma el flujo nunca se corta, y la elección sigue siendo coherente con el objetivo de la variedad, porque se prioriza lo que menos se repitió.

**Alternativas descartadas para este caso:** relajar el filtro y elegir entre todo el catálogo, porque un criterio de puntaje podría volver a elegir una canción repetida; y emitir una pausa, porque habría pausas que no responden a la regla de cada N temas y se mezclarían dos reglas distintas.

### Decisión 4: el desempate se resuelve por el id de la canción

Cuando dos o más canciones empatan, ya sea en puntaje o en cuánto hace que no suenan, gana la de id más chico. Con esto el flujo depende solo de los datos y nunca del orden en que vienen las canciones en el catálogo ni del azar, de modo que con el mismo catálogo y el mismo oyente la radio produce siempre la misma secuencia. Además es fácil de verificar con un test.

**Alternativa descartada: desempatar al azar.** Habría dado más variedad, pero rompe la restricción de que, con los mismos datos, la radio produzca siempre el mismo flujo, y obligaría a inyectar una fuente de azar para poder probarla.

**Alternativa descartada: dejar que decida el orden del catálogo.** Es lo más simple, pero haría que el resultado cambiara con solo reordenar la lista, algo que el enunciado señala como problema.

### Decisión 5: quién registra las escuchas

`registrar_escucha_completa` lo llama quien consume el flujo (el programa principal o los tests), no la Radio. La Radio decide qué suena y el consumidor informa cómo terminó la escucha.

**Alternativa descartada: que la Radio registre.** Habría mezclado la regla de programación con el estado del oyente, y la Radio necesitaría igual recibir de afuera si la escucha fue completa.

### Decisión 6: el oyente es mutable

El `Oyente` guarda una lista `escuchas_completas` y `registrar_escucha_completa(cancion)` la modifica agregando la canción. Elegimos esto porque el flujo es infinito y se consume de a poco: la radio lee la misma lista del oyente cada vez que elige la siguiente canción, y así aprende de cada escucha sin que haya que entregarle un oyente nuevo en cada vuelta. La mutación queda en un único lugar, el método de registro; los criterios solo leen.

El costo es que los criterios dejan de ser funciones puras en sentido estricto (ver Decisión 2), y que dos oyentes simultáneos necesitan cada uno su propio objeto `Oyente`, mientras comparten la Radio y el Catálogo.

**Alternativa descartada: oyente inmutable.** `registrar_escucha_completa` habría devuelto un oyente nuevo con la lista más larga, dejando intacto el anterior. Mantenía los criterios como funciones puras y facilitaba los tests, pero obligaba al consumidor a pasarle a la radio un oyente nuevo después de cada escucha, y con un flujo infinito eso complica el uso sin aportar una ventaja que necesitemos en esta variante.