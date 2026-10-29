### Decisión 1: variante de radio infinita

Variante elegida: Radio para entrenar. La señal de aprendizaje son las escuchas completas del oyente y la regla de programación propia son las pausas cada N temas. Elegimos esta combinación porque permite separar con claridad el estado (el historial del oyente, inmutable) del cálculo puro (los criterios de elección), y porque la regla de pausas se puede implementar como una transformación del flujo sin modificar el criterio que elige las canciones.
Pausa: se inserta una pausa cada N canciones (N es un parámetro de la emisora).
Escucha completa: es el evento “terminó la canción entera”. Es un dato binario por escucha: o la escuchó completa o no (la cortó/saltó).
Decisión: el contador de pausas vive en el flujo.
La pausa cada N canciones es una regla de programación de la emisora, no una preferencia del oyente. Por eso se implementa como una transformación del flujo de canciones que inserta una Pausa cada N elementos, y el Oyente no conoce esa regla. Así el Oyente solo guarda sus gustos (el historial de escuchas) y dos oyentes comparten la misma regla sin duplicar estado.
Alternativa descartada: contador en el Oyente.
Habría mezclado gustos con una regla de programación, y obligaba a actualizar el oyente en cada canción solo para saber cuándo tocaba la pausa. Tendría sentido si cada oyente pudiera tener su propio ritmo de pausas, pero no es un requisito de esta variante.

### Decisión 2: los criterios de elección son funciones

Un criterio recibe una canción y un oyente y devuelve un puntaje, y no necesita recordar nada entre una llamada y otra: el único estado relevante vive en el `Oyente`, que es inmutable. Por eso modelamos los tres criterios (afinidad por escuchas completas, energía para entrenar y variedad) como funciones puras con la misma forma, `(Cancion, Oyente) -> float`. Los que necesitan un valor de configuración, como el nivel de energía objetivo o la cantidad de canciones hacia atrás que mira la variedad, lo reciben fijado de antemano, de modo que todos se tratan igual. Esto permite agregar un criterio nuevo escribiendo una función nueva, sin modificar las existentes, y combinarlos con funciones de orden superior.

**Alternativa descartada: una clase por criterio con una interfaz común.** Habría dado polimorfismo explícito y los parámetros como atributos, pero cada clase habría tenido un solo método y ningún estado que proteger, así que agregaba estructura sin aportar nada al diseño.