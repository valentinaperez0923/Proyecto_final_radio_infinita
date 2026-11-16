# Decisiones de diseño

### Decisión 1: variante de radio infinita

Variante elegida: **radio para entrenar**. La señal de aprendizaje son las escuchas completas del oyente y la regla de programación propia son las pausas cada N temas. Elegimos esta combinación porque permite separar con claridad el estado (el historial del oyente, que es lo único que cambia) de los criterios de elección (que solo leen ese estado), y porque la regla de pausas se puede implementar como una transformación del flujo sin modificar el criterio que elige las canciones. También era la más simple de implementar y probar.

**Pausa:** se inserta una pausa cada N canciones. N y la duración de la pausa son parámetros de la emisora.

**Escucha completa:** es el evento "terminó la canción entera". Es un dato binario por escucha: o la escuchó completa o no (la cortó o la saltó).

**Decisión:** el contador de pausas vive en el flujo.

La pausa cada N canciones es una regla de programación de la emisora, no una preferencia del oyente. Por eso se implementa como una transformación del flujo de canciones que inserta una `Pausa` cada N elementos, y el `Oyente` no conoce esa regla. Así el `Oyente` solo guarda sus gustos (el historial de escuchas) y dos oyentes comparten la misma regla sin duplicar estado.

En el código esto son dos piezas separadas:
- `Radio.canciones(oyente)` es el generador que solo elige canciones (no sabe nada de pausas).
- `con_pausas(elementos, n, pausa)` es una función que recibe *cualquier* flujo y le intercala `pausa` cada `n` elementos. No sabe nada de canciones, catálogos ni oyentes.

`Radio.flujo` es la composición de las dos: `con_pausas(self.canciones(oyente), self.n_pausa, self.pausa)`. Por eso la regla de pausas se prueba sola, con letras en vez de canciones (`con_pausas(iter("abcdef"), 2, "P")` da `a, b, P, c, d, P, ...`), y una regla de flujo nueva se agrega envolviendo el flujo, sin tocar la elección de canciones.

**Alternativa descartada (era nuestra primera versión): el contador de pausas dentro del mismo ciclo que elige las canciones.** Funcionaba igual, pero mezclaba dos responsabilidades en un mismo bucle: para probar las pausas había que armar un catálogo y un oyente, y para agregar otra regla de flujo había que modificar el ciclo que elige canciones.

**Alternativa descartada: contador en el `Oyente`.** Habría mezclado gustos con una regla de programación, y obligaba a actualizar el oyente en cada canción solo para saber cuándo tocaba la pausa. Tendría sentido si cada oyente pudiera tener su propio ritmo de pausas, pero no es un requisito de esta variante.

### Decisión 2: los criterios son funciones puras sobre las escuchas

Un criterio recibe una canción y la tupla de escuchas del oyente, y devuelve un resultado. El oyente entrega su historial como tupla porque un criterio solo lee y no puede modificarlo. No recuerda nada entre una llamada y otra, no modifica nada y no tiene efectos secundarios.

Los criterios son de dos tipos:
- **Puntajes:** `(Cancion, escuchas) -> float`. Más alto es mejor. Son `afinidad` y `energia_objetivo`.
- **Filtros:** `(Cancion, escuchas) -> bool`. Si devuelve `False`, la canción no puede sonar ahora. Son `variedad` y `no_repetir_cancion`.

Los criterios que necesitan un valor de configuración (el objetivo de energía, o cuántas escuchas hacia atrás mira un filtro) se crean con una función que recibe ese valor y devuelve el criterio ya configurado (por ejemplo `energia_objetivo(8)` o `variedad(2)`). Así todos tienen la misma forma y se tratan igual. Agregar un criterio nuevo es escribir una función nueva, sin tocar las existentes.

Para darle peso a un puntaje, `ponderado(peso, puntaje)` devuelve un puntaje nuevo que multiplica el resultado del original por `peso` (ver decisión 11). El puntaje original no se modifica.

Para que los criterios sean puros, no reciben al `Oyente` sino solo su historial. 

**Alternativa descartada: pasarle el `Oyente` completo al criterio.** Era más corto, pero el oyente es mutable y el resultado podía cambiar entre dos llamadas con los mismos argumentos, y para probar un criterio había que armar un oyente entero.

### Decisión 3: los criterios se combinan con filtros y puntajes

La radio primero aplica los **filtros** al catálogo y después suma los **puntajes** de las candidatas que sobreviven. Los filtros funcionan como veto: una afinidad alta no puede compensar la repetición de un artista o de una canción, porque es una condición, no un peso. Cada criterio sigue siendo una función independiente y ninguno se modifica para combinarlos.

**Alternativa descartada: suma ponderada de todos los criterios (filtros incluidos).** Era más simple y se afinaba cambiando pesos, pero permitía que una afinidad alta compensara la repetición de un artista, que es justamente lo que la regla de variedad quiere evitar. Los pesos sí se usan, pero solo *entre los puntajes* (ver decisión 11): los filtros siguen siendo un veto.

**Caso borde: el filtro descarta todo el catálogo.** Si ninguna canción pasa los filtros, la radio emite la canción que hace más tiempo que no suena (una que nunca sonó, o que ya salió del historial). Así el flujo nunca se corta, y la elección es coherente con el objetivo de la variedad, porque se prioriza lo que menos se repitió.

### Decisión 4: el desempate se resuelve por el id de la canción

Cuando dos o más canciones empatan, ya sea en puntaje o en cuánto hace que no suenan, gana la de id más chico. Con esto el flujo depende solo de los datos y nunca del orden del catálogo ni del azar: con el mismo catálogo y el mismo oyente la radio produce siempre la misma secuencia.

**Alternativa descartada: desempatar al azar.** Habría dado más variedad, pero rompe la restricción de que, con los mismos datos, la radio produzca siempre el mismo flujo, y obligaría a inyectar una fuente de azar para poder probarla.

### Decisión 5: quién registra las escuchas

`registrar_escucha(cancion, completa)` lo llama quien consume el flujo (el programa principal o los tests), no la `Radio`. La `Radio` decide qué suena y el consumidor informa cómo terminó la escucha.

**Alternativa descartada: que la `Radio` registre.** Habría mezclado la regla de programación con el estado del oyente.

**Riesgo conocido: que el consumidor se olvide de registrar.** La radio solo aprende si quien consume el flujo registra cada escucha *antes* de pedir el siguiente elemento. Si se olvida, el historial no cambia, `elegir` recibe siempre los mismos datos y, como es pura, devuelve siempre lo mismo: sin registrar, el flujo da "Subida" cuatro veces seguidas.

Lo dejamos así a propósito para separar lo puro de los efectos: `elegir` y los criterios solo calculan, y el único lugar donde cambia el estado es `registrar_escucha`, que llama el consumidor (en `main.py`, donde también viven los otros efectos: imprimir y decidir cómo terminó cada escucha). La radio no puede saber por sí misma si una canción se escuchó completa: ese dato viene de afuera.

Para que no se pueda olvidar, habría que hacer que el flujo *no pueda avanzar* sin esa información. Por ejemplo: que `flujo` reciba una función `como_termino(cancion) -> bool` y registre él mismo cada escucha antes de elegir la siguiente; o usar un generador que reciba el resultado con `send(completa)` y dé error si se le pide la siguiente canción sin haberlo recibido. En los dos casos el flujo pasaría a tener efectos (modifica al oyente), que es lo que quisimos evitar.

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

### Decisión 11: los puntajes tienen peso, y la energía objetivo gana

**Problema.** La radio sumaba los puntajes con el mismo peso, pero no estaban en la misma escala: `energia_objetivo` da hasta 10 puntos y `afinidad` contaba escuchas completas sin tope. Cuanto más escuchaba el oyente a un artista, más pesaba la afinidad, hasta tapar a la energía. Con objetivo 8 y un oyente que escuchó completas 6 canciones de Río Lento, la radio elegía "Respira" (energía 3), que no sirve para entrenar.

**Cambios.**
1. `afinidad` devuelve una **fracción entre 0 y 1**: la parte de las escuchas completas que fueron de ese artista. Así no crece sin tope con el uso.
2. `ponderado(peso, puntaje)` crea un puntaje nuevo que multiplica el resultado de otro por `peso`. No modifica ningún criterio: los envuelve, igual que `con_pausas` envuelve el flujo.

**Qué gana cuando chocan: la energía objetivo.** Es una radio para entrenar: si la música no tiene la energía que pide el entrenamiento, no cumple su función, por más que sea de un artista que le gusta al oyente. Por eso usamos `ponderado(0.5, afinidad)` junto con `energia_objetivo(objetivo)` sin modificar.

Con ese peso la afinidad suma como máximo 0.5, y el puntaje de energía de dos canciones que están a distinta distancia del objetivo difiere en al menos 1 punto. Entonces una canción más cerca del objetivo siempre le gana a una más lejos, y la afinidad decide **entre canciones igual de cerca** del objetivo (por ejemplo, entre dos de energía 8, suena la del artista que el oyente escucha completo más seguido). La señal de aprendizaje sigue funcionando, pero dentro de lo que sirve para entrenar.

**Por qué 0.5 y no 1.** Con peso 1 la afinidad puede valer lo mismo que un punto de energía: una canción de energía 7 de un artista que el oyente escucha siempre empataría con una de energía 8 de un artista nuevo, y el empate lo resolvería el id, que es arbitrario. Con un peso menor que 1 ese empate no puede pasar.

**Alternativa descartada: que gane la afinidad (peso alto, por ejemplo 5 o más).** Tendría sentido en una radio para escuchar música tranquila o descubrir artistas parecidos, pero en esta variante haría que el oyente que escucha mucho a un artista lento reciba música lenta para entrenar.

El test `test_mucha_afinidad_no_gana_a_la_energia_objetivo` usa el ejemplo de arriba (3 y 6 escuchas completas de Río Lento, objetivo 8) y comprueba que en los dos casos suene una canción de energía 8.

### Decisión 12: los criterios son funciones, no clases

Cada criterio hace una sola cosa: recibe una canción y las escuchas, y devuelve un número (puntaje) o un booleano (filtro). Por eso lo escribimos como una función y no como una clase con un único método.

En Python una función también es un objeto: se puede guardar en una lista, pasar como argumento y devolver desde otra función. La `Radio` recibe `puntajes` y `filtros` como listas de funciones y las llama a todas de la misma manera, sin saber cuál es cuál. Es polimorfismo sin herencia: alcanza con que todas tengan la misma forma (`Puntaje` o `Filtro`, definidos en `criterios.py`).

Los criterios que necesitan configuración usan **funciones de orden superior**, es decir, funciones que reciben o devuelven otras funciones:
- `energia_objetivo(8)`, `variedad(2)` y `no_repetir_cancion(10)` reciben un valor y devuelven el criterio ya configurado. El valor queda guardado dentro de la función devuelta (una *clausura*), que cumple el papel que en una clase cumpliría un atributo.
- `_sin_repetir(que_comparar, ultimas)` recibe una función (qué dato de la canción comparar) y con eso arma los dos filtros sin repetir código.
- `ponderado(peso, puntaje)` recibe un puntaje y devuelve otro.
- `elegir` usa `max` y `min` con `key=`, que también reciben una función.

**Qué cambiaría si fueran clases.** Una clase `Criterio` con un método `puntuar` y subclases (`Afinidad`, `EnergiaObjetivo`, ...) guardaría la configuración en atributos y permitiría heredar comportamiento. A cambio, cada criterio nuevo sería una clase con `__init__` y un método, la `Radio` dependería de esa jerarquía, y un criterio podría guardar estado entre llamadas y dejar de ser puro sin que se note. Con funciones, combinar criterios (como hace `ponderado`) es envolver una función en otra.

**Alternativa descartada: clase abstracta `Criterio` con subclases.** Tendría sentido si un criterio necesitara más de un método (por ejemplo, `puntuar` y `explicar` por qué eligió una canción) o guardar estado propio. No es nuestro caso.

### Decisión 13: composición en lugar de herencia, y una interfaz para lo que sale al aire

En el proyecto no hay herencia entre nuestras clases. Las piezas se arman **por composición**:
- La `Radio` *tiene* un `Catalogo`, una tupla de puntajes, una tupla de filtros y una `Pausa`. Cambiar cómo elige es pasarle otros criterios, no escribir una subclase.
- El `Oyente` *tiene* su historial de `Escucha`, y cada `Escucha` *tiene* una `Cancion`.
- `Radio.flujo` compone el generador de canciones con `con_pausas` (decisión 1).

Por la radio pueden salir canciones y pausas, así que el flujo es de tipo `Iterator[Emitible]`. `Emitible` es un `Protocol` (en `modelo.py`): una interfaz que pide tener `duracion`. `Cancion` y `Pausa` la cumplen sin heredar de ella, solo por tener ese atributo (tipado estructural). El único lugar donde distinguimos el tipo es `main.py`, que muestra distinto una canción y una pausa.

**Alternativa descartada: que `Pausa` herede de `Cancion`.** Una pausa sería una "canción sin artista": tendría que tener id, bpm y artista inventados, rompería las validaciones de `Cancion`, y los filtros y puntajes la tratarían como una canción más.

**Alternativa descartada: una subclase `RadioConPausas(Radio)`.** Cada regla de flujo nueva (pausas, bloques temáticos, intensidad creciente) sería otra subclase, y combinar dos reglas obligaría a herencia múltiple. Con `con_pausas` cada regla es una función que envuelve el flujo, y se pueden encadenar.

**Alternativa descartada: una clase base abstracta (`ABC`) en lugar de `Protocol`.** También funcionaría, pero obliga a que `Cancion` y `Pausa` hereden de ella. Con `Protocol` alcanza con cumplir la interfaz.

### Decisión 14: el flujo infinito es perezoso

La radio no tiene una lista de reproducción. `Radio.canciones` es un generador con `while True` que elige una canción recién cuando se le pide la siguiente (con `next()` o en un `for`). `con_pausas` también es un generador, así que el flujo completo se calcula de a un elemento por vez. Quien lo consume decide cuánto pedir: `main.py` usa `itertools.islice` para cortarlo en 12 elementos.

Así se representa algo que nunca termina sin quedarse sin memoria: el flujo no se guarda en ningún lado, y lo único que crece con el uso es el historial del oyente, que tiene tope (decisión 10).

Además, la evaluación perezosa es necesaria para que la radio aprenda: la canción siguiente depende de cómo terminó la anterior, y eso se sabe recién cuando el consumidor la registra (decisión 5).

Lo comprueban `test_el_flujo_no_se_corta` (se pueden pedir 500 elementos) y `test_el_flujo_es_perezoso`.

**Alternativa descartada: calcular de antemano una lista de N canciones.** Un flujo infinito no se puede calcular entero, y una lista armada por adelantado no podría tener en cuenta escuchas que todavía no ocurrieron.

## Cambio de requisito y refactor

El docente pidió dos cambios (están en el archivo `Cambio`).

**1. Las pausas como transformación del flujo.**
- **Antes:** `Radio.flujo` era un solo ciclo que elegía la canción, llevaba el contador y metía la pausa.
- **Después:** `con_pausas(elementos, n, pausa)` es una función aparte que no sabe de canciones, y `Radio.flujo` es `con_pausas(self.canciones(oyente), self.n_pausa, self.pausa)` (decisión 1).
- **Cómo comprobamos que no se rompió nada:** los 28 tests que había siguen pasando, y con solo este cambio `main.py` imprime exactamente lo mismo que antes.
- **Test nuevo:** `test_con_pausas_intercala_una_pausa_cada_n`, que prueba la regla sin catálogo ni oyente.

**2. Pesos en los puntajes.**
- **Antes:** `afinidad` contaba escuchas completas sin tope y se sumaba con el mismo peso que `energia_objetivo`. Con 6 escuchas completas de Río Lento y objetivo 8 ganaba "Respira" (energía 3).
- **Después:** `afinidad` es una fracción entre 0 y 1, `ponderado(peso, puntaje)` permite darle peso a cualquier puntaje, y la radio usa `ponderado(0.5, afinidad)`: gana la energía objetivo (decisión 11).
- **Tests nuevos:** `test_mucha_afinidad_no_gana_a_la_energia_objetivo` (el ejemplo de Río Lento, con 3 y 6 escuchas) y `test_ponderado_multiplica_el_puntaje`.
- **Efecto en `main.py`:** cambia el orden de las canciones 8 a 12. Es esperable, porque cambió cuánto pesa la afinidad.

**Qué hizo fácil el cambio.** Ninguno de los dos obligó a modificar los criterios existentes ni la función `elegir`: las pausas se agregaron envolviendo el flujo, y los pesos envolviendo un puntaje. Es la ventaja de tener los criterios como funciones independientes (decisiones 2 y 12) y el flujo como composición de generadores (decisiones 1 y 14).

**Además:** se agregó un `.gitignore` y se sacaron del repositorio los archivos `__pycache__` y `.pyc`. El riesgo de que el consumidor se olvide de registrar las escuchas está explicado en la decisión 5.

## Dónde usamos objetos y dónde funciones puras

- **Objetos** para lo que existe en el mundo de la radio y tiene reglas que cuidar. `Cancion`, `Pausa`, `Escucha` y `Catalogo` son inmutables (`frozen=True`) y validan sus datos al crearse (invariantes: bpm entre 40 y 250, duración mayor que 0, catálogo no vacío y sin ids repetidos). El `Oyente` es el único objeto que cambia y encapsula su historial: solo se modifica con `registrar_escucha` y se lee como tupla. La `Radio` guarda la configuración de la emisora.
- **Funciones puras** para todo lo que calcula: los criterios, `elegir`, `la_que_hace_mas_que_no_suena`, `con_pausas` y los textos de `main.py`.
- **Efectos** (mostrar en pantalla, decidir cómo terminó cada escucha, modificar el historial) solo en `main.py` y en `Oyente.registrar_escucha`.

La tabla con cada función del núcleo, si es pura y, si no lo es, por qué está ahí, está en `FUNCIONES_PURAS.md`. El UML final y lo que cambió respecto del inicial están en `UML.md`.

