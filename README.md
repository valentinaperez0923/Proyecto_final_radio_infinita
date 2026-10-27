# Proyecto_final_radio_infinita
## Variante del grupo
## Justificación de la variante

Elegimos una radio para entrenar, con escuchas completas como señal de aprendizaje y una pausa cada N temas como regla de programación propia. Esta combinación permite separar con claridad el estado (el historial del oyente, inmutable) del cálculo puro (los criterios de elección), y la regla de pausas se puede implementar como una transformación del flujo sin modificar el criterio que elige las canciones.

## Definiciones

- **Pausa:** se inserta una pausa cada N canciones. N es un parámetro de la emisora.
- **Escucha completa:** es el evento "terminó la canción entera". Es un dato binario por escucha: o la escuchó completa o no (la cortó o la saltó).

## Decisiones de diseño

### Decisión 1: el contador de pausas vive en el flujo

La pausa cada N canciones es una regla de programación de la emisora, no una preferencia del oyente. Por eso se implementa como una transformación del flujo de canciones que inserta una `Pausa` cada N elementos, y el `Oyente` no conoce esa regla. Así el `Oyente` solo guarda sus gustos (el historial de escuchas) y dos oyentes comparten la misma regla sin duplicar estado.

**Alternativa descartada: contador en el `Oyente`.** Habría mezclado gustos con una regla de programación, y obligaba a actualizar el oyente en cada canción solo para saber cuándo tocaba la pausa. Tendría sentido si cada oyente pudiera tener su propio ritmo de pausas, pero no es un requisito de esta variante.