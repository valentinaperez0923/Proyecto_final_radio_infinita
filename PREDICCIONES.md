# Predicciones

Antes de correr una función clave anotamos qué esperamos que devuelva. Después la corremos y comparamos. Si no coincide, explicamos por qué: si nos equivocamos nosotras o si encontramos un error en el código.

**Importante:** la predicción se escribe *antes* de correr el código.


Para correr cada ejemplo: abrir una terminal en la carpeta del proyecto, escribir `python`, y pegar el código.

## 1. `afinidad` con escuchas completas y cortadas

```python
from modelo import Cancion, Oyente
from criterios import afinidad
a = Cancion(1, "A", "Los Pesos", bpm=125, duracion=180)
b = Cancion(2, "B", "Nadia K", bpm=155, duracion=200)
o = Oyente("Prueba")
o.registrar_escucha(a, completa=True)
o.registrar_escucha(b, completa=True)
o.registrar_escucha(a, completa=False)
o.registrar_escucha(a, completa=True)
print(afinidad(a, o.escuchas))
```

- **Predicción:** (Claude(IA)), 16/11. Solo cuentan las escuchas completas: son 3 (A, B, A) y 2 son de Los Pesos, así que `afinidad` da 2/3: se imprime `0.6666666666666666`. La escucha cortada de A no cuenta.
- **Resultado:** `0.6666666666666666`
- **¿Coincidió? ¿Por qué?:** Sí. Confirma la decisión 7: la escucha cortada queda en el historial (cuenta para los filtros), pero no suma afinidad.

## 2. `Cancion.energia` en los bordes

```python
from modelo import Cancion
for bpm in (65, 69, 70, 165, 250):
    print(bpm, Cancion(1, "X", "Y", bpm=bpm, duracion=100).energia)
Cancion(1, "X", "Y", bpm=30, duracion=100)
```

- **Predicción:** (Claude(IA)), 16/11. Con la fórmula `min(10, max(1, (bpm - 60) // 10))`: 65 → 1, 69 → 1, 70 → 1, 165 → 10, 250 → 10. La última línea da `ValueError`, porque los bpm tienen que estar entre 40 y 250.
- **Resultado:** `65 1`, `69 1`, `70 1`, `165 10`, `250 10` y después `ValueError: Los bpm tienen que estar entre 40 y 250`.
- **¿Coincidió? ¿Por qué?:** Sí. Se ve el efecto de los topes: cualquier canción de menos de 80 bpm queda con energía 1, y cualquiera de 160 o más queda con 10. Una canción de 30 bpm no se puede crear, porque `Cancion` valida sus datos al crearse.

## 3. `la_que_hace_mas_que_no_suena`

```python
from modelo import Oyente
from catalogo_datos import CATALOGO
from radio import la_que_hace_mas_que_no_suena
tres = CATALOGO.canciones[:3]          # ids 1, 2 y 3
o = Oyente("Prueba")
for i in (2, 1, 3, 1):
    o.registrar_escucha(CATALOGO.canciones[i - 1], completa=True)
print(la_que_hace_mas_que_no_suena(tres, o.escuchas).titulo)
```

- **Predicción:** (Claude(IA)), 16/11. Las escuchas quedan en las posiciones 2 → 0, 1 → 1 y 3, 3 → 2. Gana la de posición más chica, la id 2, así que se imprime `Sprint`.
- **Resultado:** `Sprint`
- **¿Coincidió? ¿Por qué?:** Sí. La id 1 sonó dos veces, pero lo que cuenta es la última vez que sonó, no cuántas veces.

## 4. `con_pausas` con un flujo que sí termina

```python
from radio import con_pausas
print(list(con_pausas(range(7), 3, "P")))
```

- **Predicción:** (Claude(IA)), 16/11. `[0, 1, 2, 'P', 3, 4, 5, 'P', 6]`. Después del 6 no hay pausa, porque `range(7)` termina antes de juntar otros 3 elementos.
- **Resultado:** `[0, 1, 2, 'P', 3, 4, 5, 'P', 6]`
- **¿Coincidió? ¿Por qué?:** Sí. `con_pausas` funciona con cualquier flujo, también con uno que termina, y pone la pausa solo cuando se juntaron `n` elementos.

## 5. `elegir` con otra energía objetivo

```python
from modelo import Oyente
from catalogo_datos import CATALOGO
from criterios import afinidad, energia_objetivo, ponderado
from radio import Radio
radio = Radio(CATALOGO, [ponderado(0.5, afinidad), energia_objetivo(4)], [], n_pausa=4)
print(radio.elegir_siguiente(Oyente("Prueba")).titulo)
```

- **Predicción:** (Claude(IA)), 16/11. Sin historial la afinidad vale 0 para todas, así que gana la canción con energía más cerca de 4. La única de energía 4 es Bajada (100 bpm → 4), así que se imprime `Bajada`.
- **Resultado:** `Bajada`
- **¿Coincidió? ¿Por qué?:** Sí. Sin historial la afinidad no influye y decide la energía objetivo, como dice la decisión 11.

## 6. la radio sin registrar escuchas

```python
from itertools import islice
from modelo import Oyente
from catalogo_datos import CATALOGO
from criterios import afinidad, energia_objetivo, variedad no_repetir_cancion, ponderado
from radio import Radio
radio = Radio(CATALOGO, [ponderado(0.5, afinidad), energia_objetivo(8)],
              [variedad(2), no_repetir_cancion(10)], n_pausa=4)
print([c.titulo for c in islice(radio.canciones(Oyente("Prueba")), 4)])
```

**Predicción:** (Delfina), 16/11. Sin llamar a `registrar_escucha`, `oyente.escuchas` es una tupla vacía en cada vuelta, así que los filtros devuelven `True` para las 18 canciones y la afinidad vale 0.0 para todas (queda 0.0 después de `ponderado`). Con objetivo 8, las canciones de energía 8 (Subida, Pulso y Doble Tiempo) empatan con 10 puntos, y el desempate por `-c.id` elige la de id 3. Como `elegir` es pura y recibe los mismos datos en las 4 vueltas, esperamos que imprima `['Subida', 'Subida', 'Subida', 'Subida']`.
**Resultado:** ['Subida', 'Subida', 'Subida', 'Subida']
**¿Coincidió?:** Sí. `Radio.canciones` llama a `elegir_siguiente` en cada vuelta y como nadie registra escuchas, `elegir` recibe siempre los mismos datos y devuelve siempre la misma canción. Es el riesgo de la decisión 5: la radio solo aprende si quien consume el flujo registra cada escucha antes de pedir la siguiente.

## 7. `con_pausas` con n = 1

```python
from radio import con_pausas
print(list(con_pausas("abc", 1, "P")))
```

**Predicción:** (Delfina), 16/11. Con n = 1, el contador llega a 1 en cada elemento, así que después de cada letra sale una pausa y el contador vuelve a 0. Esperamos que imprima `['a', 'P', 'b', 'P', 'c', 'P']`. La última pausa queda después de la `c`.
**Resultado:** ['a', 'P', 'b', 'P', 'c', 'P']
**¿Coincide?:** Sí. `yield (elemento)` sale antes del `if`, y con n = 1 el `if` se cumple en todas las vueltas, así que cada letra va seguida de una pausa. A diferencia de la predicción 4, donde el último grupo quedó incompleto y no tuvo pausa, acá cada grupo tiene un solo elemento y siempre se completa.

## 8. el filtro `variedad` con distintas ventanas

```python
from modelo import Oyente
from catalogo_datos import CATALOGO
from criterios import variedad
c = CATALOGO.canciones
o = Oyente("Prueba")
o.registrar_escucha(c[0], completa=False)   # Arranque, Los Pesos
o.registrar_escucha(c[1], completa=True)    # Sprint, Nadia K
o.registrar_escucha(c[3], completa=True)    # Calma, Río Lento
print(variedad(3)(c[2], o.escuchas), variedad(2)(c[2], o.escuchas), variedad(3)(c[8], o.escuchas))
```

**Predicción** (Olivia), 17/11.

## 9. el límite de memoria del oyente

```python
from modelo import Oyente
from catalogo_datos import CATALOGO
o = Oyente("Prueba", memoria=3)
for c in CATALOGO.canciones[:5]:
    o.registrar_escucha(c, completa=True)
print([e.cancion.id for e in o.escuchas])
```

**Predicción:** (Olivia), 17/11