# Bitácora de uso de IA

Registramos cada uso de IA: qué pedimos, qué devolvió, qué corregimos o rechazamos y por qué.

## 1. 27/10 – Elección de proyecto

**Quién:** Olivia · **Herramienta:** Claude
**Qué se pidió:** una explicación de los tres proyectos (Ruta viva, Mercado de cartas, Radio infinita).
**Qué devolvió:** recomendó Radio infinita: el catálogo es inventado y el flujo infinito encaja con generadores. Dijo que Mercado de cartas era el más difícil por las operaciones que tienen que salir "todo o nada".
**Qué decidimos nosotras:** elegimos Radio infinita, tomamos las descripciones de Claude y su recomendación como orientación, la decisión fue del grupo.

## 2. 27/10 – Elección de la variante

**Quién:** Delfina· **Herramienta:** Claude
**Qué se pidió:** opciones de variantes y qué significaba "variante".
**Qué devolvió:** una tabla con 6 combinaciones de variantes.
**Qué decidimos nosotras:** rechazamos la recomendación que nos dió Claude y elegimos la opción de una radio para entrenar, que aprende de escuchas completas para recomendar nuevas canciones y hace una pausa cada N temas, porque era la más simple de implementar y probar, y nos deja margen para el cambio de requisito que se nos exige.

## 3. 27/10 – Primeras decisiones de diseño

**Quién:** Delfina· **Herramienta:** Claude
**Qué se pidió:** ayuda para entender las decisiones abiertas de la variante.
**Qué devolvió:** preguntas sobre qué es una pausa, qué es una escucha completa y dónde vive el contador de pausas, con dos opciones explicadas (contador en el flujo o en el oyente).
**Qué decidimos nosotras:** la pausa va cada N canciones, la escucha completa es un evento binario (escuchó la canción completa o no), el contador vive en el flujo, porque así es automático y el programa no le consulta constantemente al oyente, interrumpiendo su escucha.

## 4. 27/10 – Borrador de UML

**Quién:** Valentina· **Herramienta:** Claude
**Qué se pidió:** un primer diagrama de clases.
**Qué devolvió:** un UML en Mermaid.
**Qué se corrigió o rechazó y por qué:** lo rechazamos porque todavía no habíamos tomado las decisiones de diseño, y preferimos hacer el UML después. Además tenía dos errores:
- La interfaz decía un método `duracion_seg()`, pero las clases tenían un atributo `duracion`.
- Dibujaba `Criterio` como una clase, cuando la misma IA había sugerido que fuera una función.

## 5. 27/10 – Documento de diseño completo

**Quién:** Olivia· **Herramienta:** Claude
**Qué se pidió:** que armara todos los pasos del Hito 1 para la variante 6, para ver cómo quedaría.
**Qué devolvió:** un documento de diseño completo y archivos de bitácora y predicciones ya armados.
**Qué se corrigió o rechazó y por qué:** lo rechazamos porque queríamos ver un ejemplo para entender, no un documento terminado para entregar. Le pedimos un esbozo corto y armamos el diseño nosotras.

## 6. 27/10 al 10/11 – Git y GitHub

**Quién:** Olivia y Delfi· **Herramienta:** Claude
**Qué se pidió:** cómo clonar el repositorio, subir cambios desde la terminal y desde VS Code, y por qué no funcionaba el pull.
**Qué devolvió:** los comandos paso a paso, y cómo revisar en GitHub si los cambios se habían subido.
**Qué aprendimos / decidimos:** el pull no traía nada porque los cambios de Delfi nunca se habían subido: su compu no tenía permiso para hacer push. VS Code ofreció crear un *fork*, y **no lo aceptamos**, porque los cambios se habrían ido a una copia aparte y no al repo del grupo.

## 7. Decisiones de diseño 2 a 6

**Quién:** (completar) · **Herramienta:** (completar)
**Qué se pidió:** (completar: ayuda para decidir si los criterios son funciones o clases, cómo combinarlos, el desempate, quién registra las escuchas y si el oyente es mutable).
**Qué devolvió:** (completar)
**Qué decidimos nosotras:** (completar: qué opción eligieron en cada una y por qué).

## 8. 05/11 – Revisión del diseño y del UML

**Quién:** Olivia · **Herramienta:** Claude
**Qué se pidió:** revisar lo que teníamos (DISENO, README, UML) y qué seguía.
**Qué devolvió:** encontró cuatro problemas: el README contradecía al DISENO (decía oyente inmutable y criterios puros); el UML no coincidía con las decisiones (faltaba la Pausa, una interfaz y la relación de la Radio con el Catálogo); el catálogo se podía modificar; y un hueco en la variedad.
**Error real de la IA:** el hueco de la variedad venía de un diseño en el que nos ayudó la IA. El oyente solo guardaba las escuchas completas, así que si alguien cortaba una canción, la radio no se enteraba de que había sonado y podía volver a ponerla enseguida. No lo marcó cuando armamos esa parte.
**Qué decidimos nosotras:** el catálogo es fijo y el mismo para todos los oyentes. El oyente pasa a guardar todas las escuchas, marcando si fue completa o no.

## 9. 05/11 – Primer código

**Quién:** Olivia · **Herramienta:** Claude
**Qué se pidió:** arreglar el diseño y adelantar un código muy sencillo.
**Qué devolvió:** `modelo.py`, `criterios.py`, `radio.py` y `test_radio.py`.
**Qué se corrigió y por qué:** le pedimos que nos pasara el texto para copiar y cambiar nosotras, en vez de archivos ya hechos. Le pedimos que no tocara el diseño hasta tener el código. (completar: qué cambiaron ustedes al revisarlo)

## 10. 05/11 – Catálogo, programa principal y más tests

**Quién:** Olivia · **Herramienta:** Claude
**Qué se pidió:** el catálogo de canciones y lo que faltara del código.
**Qué devolvió:** `catalogo_datos.py` (18 canciones inventadas), `main.py` y `test_mas.py`.
**Error real de la IA:** al correr `main.py`, la radio repetía siempre las mismas 3 canciones. El filtro de variedad no dejaba repetir el artista, pero sí la misma canción, y la afinidad premiaba cada vez más lo ya escuchado. Es un ejemplo real de burbuja de filtro.
**Qué se corrigió:** se agregó el filtro `no_repetir_cancion`.

## 11. 05/11 – La energía depende de los bpm

**Quién:** Olivia · **Herramienta:** Claude
**Qué se pidió:** **corregimos a la IA**: en su código la energía era un dato escrito a mano, pero nosotras habíamos decidido que se calcula a partir de los bpm.
**Qué devolvió:** cambió `Cancion` para que guarde los bpm y calcule la energía.
**Qué decidimos nosotras:** (completar: si se quedan con la fórmula que propuso la IA, "cada 10 bpm por encima de 60 suma 1 de energía", o usan otra).

## 12. 05/11 – Revisión con otra conversación

**Quién:** Delfi y Olivia · **Herramienta:** Claude (dos conversaciones distintas)
**Qué se pidió:** Delfi pidió una revisión del código y la tabla de funciones puras; Olivia le pasó esa revisión a la otra conversación.
**Qué devolvió:** la revisión de Delfi decía que faltaban tests que ya existían (no había visto `test_mas.py`), y su tabla decía que los criterios eran puros, contradiciendo nuestro DISENO. La otra conversación lo marcó.
**Qué decidimos nosotras:** que los criterios reciban las escuchas en vez del oyente, para que sean puros de verdad; que el oyente recuerde solo sus últimas 100 escuchas, para que el historial no crezca para siempre; y sumar los tests que sí faltaban (empate, pausas inválidas).
**Error real de la IA:** al escribir uno de los tests nuevos, la IA pidió todas las canciones juntas antes de anotar las escuchas. Así la radio nunca aprendía y el test fallaba. Se corrigió recorriendo el flujo de a una canción.

## 13. 10/11 – Archivos que faltaban

**Quién:** Olivia · **Herramienta:** Claude
**Qué se pidió:** qué nos faltaba en el repo.
**Qué devolvió:** revisó nuestros archivos y encontró que faltaban `main.py` y `test_mas.py`, que varios archivos estaban en una versión vieja y que a `catalogo_datos.py` le faltaba la línea `from modelo import Cancion, Catalogo`.
**Qué hicimos:** actualizamos todo y corrimos los tests: (completar: cuántos pasaron).

---

## Resumen de errores reales de la IA

1. **UML con inconsistencias** (entrada 4): método `duracion_seg()` contra atributo `duracion`, y el criterio dibujado como clase.
2. **Hueco en la variedad** (entrada 8): las canciones cortadas no contaban como "sonadas".
3. **Burbuja de filtro** (entrada 10): la radio repetía siempre 3 canciones.
4. **Energía mal modelada** (entrada 11): la IA la puso como un dato aparte, y la corregimos nosotras.
5. **Test que no dejaba aprender a la radio** (entrada 12).