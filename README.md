# Proyecto final: Radio infinita

Una radio que emite un flujo infinito de canciones, elige la siguiente según lo que el oyente va escuchando y hace una pausa cada cierta cantidad de canciones.

## Variante del grupo

**Radio para entrenar.**
- **Señal de aprendizaje:** las escuchas completas del oyente.
- **Regla de programación propia:** una pausa cada N canciones.

## Justificación de la variante

Elegimos esta combinación porque permite separar con claridad el estado (el historial del oyente, que es lo único que cambia) de los criterios de elección (funciones puras que solo leen ese historial). La regla de pausas se puede implementar como una transformación del flujo, sin modificar el criterio que elige las canciones. También era la más simple de implementar y probar, y nos deja margen para el cambio de requisito.

## Definiciones

- **Pausa:** se inserta una pausa cada N canciones. N y la duración de la pausa son parámetros de la emisora, no del oyente.
- **Escucha completa:** es el evento "terminó la canción entera". Es un dato binario por escucha: o la escuchó completa o no (la cortó o la saltó).
- **Energía:** número de 1 a 10 que se calcula a partir de los bpm de la canción. La radio para entrenar apunta a una energía objetivo.

## Cómo funciona

1. La `Radio` aplica los **filtros** (variedad de artistas, no repetir canciones) al catálogo.
2. Con las canciones que quedan, suma los **puntajes** (afinidad con las canciones que el oyente escuchó completas y cercanía a la energía objetivo).
3. Elige la de mayor puntaje. Si hay empate, gana la canción con el id más chico, así que con los mismos datos el flujo es siempre el mismo.
4. Cada N canciones inserta una `Pausa`.
5. Quien consume el flujo (`main.py`) registra cómo terminó cada escucha en el `Oyente`, y la radio aprende de eso.

Las decisiones de diseño y las alternativas que descartamos están en `DISENO.md`.

## Estructura del proyecto

| Archivo | Qué contiene |
|---|---|
| `modelo.py` | Datos: `Cancion`, `Pausa`, `Escucha`, `Catalogo`, `Oyente` |
| `criterios.py` | Criterios de elección (funciones puras): puntajes y filtros |
| `radio.py` | La `Radio` y su flujo infinito |
| `catalogo_datos.py` | El catálogo de 18 canciones inventadas |
| `main.py` | Programa principal: arma la radio y simula a un oyente, es donde se da "correr" al programa |
| `test_radio.py`, `test_mas.py` | Tests de prueba |
| `DISENO.md` | Decisiones de diseño |
| `ETICA.md` | Riesgos éticos y marco legal |
| `BITACORA_IA.md` | Registro del uso de IA |

## Cómo correrlo

Hace falta Python 3 y `pytest` para los tests.

### Instalar pytest

```
python -m pip install pytest
```

### Correr el programa

```
python main.py
```

Imprime los primeros 12 elementos del flujo (canciones y pausas) para un oyente simulado. El oyente simulado escucha completas las canciones de energía 7 o más, así que el resultado es siempre el mismo.

### Correr los tests

```
python -m pytest
```

Corre `test_radio.py` y `test_mas.py` juntos. Si todo anda bien, al final aparece `28 passed`. Con `-v` se ve cada test por nombre.

Los tests no se corren con el botón de "Run Python File" de VS Code: ese botón solo carga el archivo y no ejecuta ningún test.
