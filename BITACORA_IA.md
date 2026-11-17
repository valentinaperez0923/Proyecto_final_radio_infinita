# Bitácora de uso de IA

Registramos cada uso de IA: qué pedimos, qué devolvió, qué corregimos o rechazamos y por qué.

## 1. 27/10 – Elección de proyecto

**Quién:** Olivia. **Herramienta:** Claude
**Qué se pidió:** una explicación de los tres proyectos (Ruta viva, Mercado de cartas, Radio infinita).
**Qué devolvió:** recomendó Radio infinita: el catálogo es inventado y el flujo infinito encaja con generadores. Dijo que Mercado de cartas era el más difícil por las operaciones que tienen que salir "todo o nada".
**Qué decidimos nosotras:** elegimos Radio infinita, tomamos las descripciones de Claude y su recomendación como orientación, la decisión fue del grupo.

## 2. 27/10 – Elección de la variante

**Quién:** Delfina. **Herramienta:** Claude
**Qué se pidió:** opciones de variantes y qué significaba "variante".
**Qué devolvió:** una tabla con 6 combinaciones de variantes.
**Qué decidimos nosotras:** rechazamos la recomendación que nos dio Claude y elegimos la opción de una radio para entrenar, que aprende de escuchas completas para recomendar nuevas canciones y hace una pausa cada N temas, porque era la más simple de implementar y probar, y nos deja margen para el cambio de requisito que se nos exige.

## 3. 27/10 – Primeras decisiones de diseño

**Quién:** Delfina. **Herramienta:** Claude
**Qué se pidió:** ayuda para entender las decisiones abiertas de la variante.
**Qué devolvió:** preguntas sobre qué es una pausa, qué es una escucha completa y dónde vive el contador de pausas, con dos opciones explicadas (contador en el flujo o en el oyente).
**Qué decidimos nosotras:** la pausa va cada N canciones, la escucha completa es un evento binario (escuchó la canción completa o no), el contador vive en el flujo, porque así es automático y el programa no le consulta constantemente al oyente, interrumpiendo su escucha.

## 4. 27/10 – Borrador de UML

**Quién:** Valentina. **Herramienta:** Claude
**Qué se pidió:** un primer diagrama de clases.
**Qué devolvió:** un UML en Mermaid.
**Qué se corrigió o rechazó y por qué:** lo rechazamos porque todavía no habíamos tomado las decisiones de diseño, y preferimos hacer el UML después. Además tenía dos errores:
- La interfaz decía un método `duracion_seg()`, pero las clases tenían un atributo `duracion`.
- Dibujaba `Criterio` como una clase, cuando la misma IA había sugerido que fuera una función.

## 5. 5/11 – Revisión del diseño y del UML

**Quién:** Olivia. **Herramienta:** Claude
**Qué se pidió:** revisar lo que teníamos (DISENO, README, UML) y qué seguía.
**Qué devolvió:** encontró tres problemas: el README contradecía al DISENO (decía oyente inmutable y criterios puros); el UML no coincidía con las decisiones (faltaba la Pausa, una interfaz y la relación de la Radio con el Catálogo); el catálogo se podía modificar.
**Error real de la IA:** había un hueco de variedad, que venía de un diseño en el que nos ayudó la IA, de este error nos percatamos nosotras. El oyente solo guardaba las escuchas completas, así que si alguien cortaba una canción, la radio no se enteraba de que había sonado y podía volver a ponerla enseguida. No lo marcó cuando armamos esa parte.
**Qué decidimos nosotras:** el catálogo es fijo y el mismo para todos los oyentes. El oyente pasa a guardar todas las escuchas, marcando si fue completa o no.

## 6. 5/11 – Primer código

**Quién:** Malena. **Herramienta:** Claude
**Qué se pidió:** arreglar el diseño y adelantar un código muy sencillo.
**Qué devolvió:** `modelo.py`, `criterios.py`, `radio.py` y `test_radio.py`.
**Qué se corrigió y por qué:** le pedimos que nos pasara el texto para copiar y cambiar nosotras, en vez de archivos ya hechos. Le pedimos que no tocara el diseño hasta tener el código. 

## 7. 5/11 – Catálogo, programa principal y más tests

**Quién:** Olivia. **Herramienta:** Claude
**Qué se pidió:** el catálogo de canciones y qué faltaba del código.
**Qué devolvió:** `catalogo_datos.py` (18 canciones inventadas), `main.py` y `test_mas.py`.
**Error real de la IA:** al correr `main.py`, la radio repetía siempre las mismas 3 canciones. El filtro de variedad no dejaba repetir el artista, pero sí la misma canción, y la afinidad premiaba cada vez más lo ya escuchado. Acá se nota un ejemplo real de burbuja de filtro, de la cual nos percatamos y corregimos.
**Qué se corrigió:** se agregó el filtro `no_repetir_cancion`.

## 8. 5/11 – La energía depende de los bpm

**Quién:** Olivia. **Herramienta:** Claude
**Qué se pidió:** corregimos a la IA: en su código la energía era un dato escrito a mano, pero nosotras habíamos decidido que se calcula a partir de los bpm.
**Qué devolvió:** cambió `Cancion` para que guarde los bpm y calcule la energía.
**Qué decidimos nosotras:** el puntaje se calcula de la siguiente manera: mientras más cerca esté el número de bpms del número objetivo, más puntos tiene la canción.

## 9. 05/11 – Revisión con otra conversación

**Quién:** Delfina. **Herramienta:** Claude 
**Qué se pidió:** Delfina pidió una revisión del código y la tabla de funciones puras.
**Qué devolvió:** la revisión de Delfina decía que faltaban tests que ya existían (no había visto `test_mas.py`), y su tabla decía que los criterios eran puros, contradiciendo nuestro DISENO. 
**Qué decidimos nosotras:** que los criterios reciban las escuchas en vez del oyente, para que sean puros de verdad; que el oyente recuerde solo sus últimas 100 escuchas, para que el historial no crezca para siempre; y sumar los tests que sí faltaban (empate, pausas inválidas).
**Error real de la IA:** al escribir uno de los tests nuevos, la IA pidió todas las canciones juntas antes de anotar las escuchas. Así la radio nunca aprendía y el test fallaba. Se corrigió recorriendo el flujo de a una canción.

## 10. 10/11 – Archivos que faltaban

**Quién:** Olivia. **Herramienta:** Claude
**Qué se pidió:** qué nos faltaba en el repositorio.
**Qué devolvió:** revisó nuestros archivos y encontró que faltaban `main.py` y `test_mas.py`, que varios archivos estaban en una versión vieja y que a `catalogo_datos.py` le faltaba la línea `from modelo import Cancion, Catalogo`.
**Qué hicimos:** actualizamos todo y corrimos los tests.

## 11. 11/11 - Simplificaciones

**Quién:** Malena. **Herramienta:** Claude
**Qué se pidió:** que unificara variedad y no_repetir_cancion con una función base, que renombrara la función pura a elegir, y la escribiera en pasos con comentarios y agregara los tipos que faltan.
**Qué devolvió:** revisó nuestros archivos y modificó lo que le pedimos. También simplificó todo para que el código quedase sencillo.

## 12. 12/11 - Correcciones

**Quién:** Delfina. **Herramienta:** Claude
**Qué se pidió:** que mejorara nuestro código.
**Qué devolvió:** revisó los archivos y nos avisó que `radio.py` y `criterios.py` tenían los mismos contenidos que `DISENO.md`.
**Qué hicimos:** arreglamos los errores y actualizamos `DISENO.md`

## 13. 16/11 – Cambios pedidos por la docente (archivo `Cambio`)

**Quién:** Malena. **Herramienta:** Claude
**Qué se pidió:** que aplicara los cambios del archivo `Cambio`: pausas como transformación del flujo y pesos para los puntajes.
**Qué devolvió:** revisó lo que ya teníamos hecho (`con_pausas`, `ponderado`, `afinidad` como fracción, `.gitignore`) y comprobó que con solo el cambio de pausas `main.py` imprime exactamente lo mismo que antes.
**Error encontrado:** el test de `con_pausas` comparaba todo el flujo de `"abcdef"` contra 6 elementos, pero el flujo sigue con `e, f, P`, así que fallaba. Se corrigió tomando los primeros 6 con `islice`.
**Qué decidimos:** que gane la energía objetivo, con `ponderado(0.5, afinidad)` (justificado en `DISENO.md`, decisión 11). Con la afinidad como fracción, `main.py` cambia el orden de las canciones 8 a 12; es esperable, porque cambió cuánto pesa la afinidad.

## 14. 16/11 – Revisión contra la letra del proyecto

**Quién:** Malena. **Herramienta:** Claude
**Qué se pidió:** comparar el repositorio con la letra del proyecto y escribir lo que faltaba de documentación.
**Qué devolvió:** encontró que faltaban el UML final, la tabla de funciones puras, el sesgo hacia lo más popular en `ETICA.md`, varias preguntas de diseño sin responder en `DISENO.md` (clase o función, composición o herencia, evaluación perezosa) y que `PREDICCIONES.md` estaba vacío. 
**Qué revisamos o corregimos:** hicimos el UML final, agregamos la tabla de funciones puras y no puras (con la explicación de cada una), anotamos el sesgo hacia lo más popular en `ETICA.md`, respondimos las preguntas sobre diseño que faltaban.

## 15. 16/11 – Predicciones

**Quién:** Malena. **Herramienta:** Claude
**Qué se pidió:** que escribiera las predicciones de `PREDICCIONES.md`.
**Qué devolvió:** predijo los 5 casos leyendo el código, sin correrlo, y después los corrió y comparó. Las 5 predicciones coincidieron con el resultado. Las predicciones están firmadas como Claude (IA) en el archivo.

## 16. 16/11 - Energía

**Quién:** Delfina. **Herramienta:** Claude
**Qué se pidió:** que se calcule la energía de cada canción de `catalogo_datos.py`.
**Qué devolvió:** una lista con la energía de cada canción.
**¿En qué la usamos?:** agregamos comentarios al lado de las canciones para facilitar las predicciones.