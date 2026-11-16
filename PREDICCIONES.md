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

- **Predicción (quién, fecha):**
- **Resultado:**
- **¿Coincidió? ¿Por qué?:**

## 2. `Cancion.energia` en los bordes

```python
from modelo import Cancion
for bpm in (65, 69, 70, 165, 250):
    print(bpm, Cancion(1, "X", "Y", bpm=bpm, duracion=100).energia)
Cancion(1, "X", "Y", bpm=30, duracion=100)
```

- **Predicción (quién, fecha):**
- **Resultado:**
- **¿Coincidió? ¿Por qué?:**

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

- **Predicción (quién, fecha):**
- **Resultado:**
- **¿Coincidió? ¿Por qué?:**

## 4. `con_pausas` con un flujo que sí termina

```python
from radio import con_pausas
print(list(con_pausas(range(7), 3, "P")))
```

- **Predicción (quién, fecha):**
- **Resultado:**
- **¿Coincidió? ¿Por qué?:**

## 5. `elegir` con otra energía objetivo

```python
from modelo import Oyente
from catalogo_datos import CATALOGO
from criterios import afinidad, energia_objetivo, ponderado
from radio import Radio
radio = Radio(CATALOGO, [ponderado(0.5, afinidad), energia_objetivo(4)], [], n_pausa=4)
print(radio.elegir_siguiente(Oyente("Prueba")).titulo)
```

- **Predicción (quién, fecha):**
- **Resultado:**
- **¿Coincidió? ¿Por qué?:**
