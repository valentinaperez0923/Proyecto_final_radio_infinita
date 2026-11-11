# ETICA.md

## 1. Datos que maneja la aplicación

- **Nombre del oyente** (`Oyente.nombre`) e **historial de escuchas**: una lista de pares (canción, ¿se escuchó completa?), de hasta 100 elementos (`memoria=100`). No se guarda la hora, ni la ubicación, ni ningún otro identificador.
- **Catálogo**: 18 canciones con metadatos inventados por nosotras. No son datos personales y no se usa audio.
- **Dónde viven**: solo en memoria mientras corre el programa. El código actual no escribe archivos ni envía nada por red; `main.py` solo imprime en pantalla.
- Hoy el oyente es simulado, si la radio pasara a tener oyentes reales, el historial sería un dato personal: la Ley 18.331 define dato personal como "información de cualquier tipo referida a personas físicas o jurídicas determinadas o determinables" (art. 4 lit. D). Qué se escucha, y qué se corta, puede además dejar entrever creencias o preferencias.

## 2. Riesgo ético concreto y cambio de diseño

**Riesgo: la burbuja de filtro.** La radio aprende de las escuchas completas, y el puntaje `afinidad` premia a los artistas que ya se escucharon enteros. Al correr `main.py` por primera vez la radio repetía siempre las mismas 3 canciones: cada escucha completa aumentaba la afinidad de lo mismo, y el oyente nunca descubría nada nuevo.

**Cambio de diseño que lo mitiga.** La variedad es un *filtro* y no un puntaje: una afinidad alta no puede compensar la repetición de un artista. Además se agregó el filtro `no_repetir_cancion` y se hizo que el oyente guarde también las escuchas cortadas, porque una canción cortada también sonó. 

**Límite que queda.** La radio es "para entrenar" y apunta a energía 8, y `energia` se calcula a partir de los bpm. Los artistas de ritmo lento puntúan menos por una decisión de diseño. Además, el oyente simulado solo escucha completas las canciones de energía 7 o más, así que esas canciones nunca ganan afinidad. Es una consecuencia del tipo de emisora, pero deja en desventaja a ciertos artistas.

## 3. Marco legal

**Ley 18.331 (protección de datos personales).** Si la radio tuviera oyentes reales, serían relevantes los siguientes artículos:
- **Arts. 7 y 8**: los datos deben ser "no excesivos" en relación con la finalidad y deben eliminarse cuando dejan de ser necesarios. El límite de 100 escuchas es una forma de minimización. Lo introdujimos para que el historial no crezca sin fin, y además sirve a este principio.
- **Art. 9**: el tratamiento requiere consentimiento libre, previo, expreso e informado, y el **art. 13** exige informar antes la finalidad y los derechos del titular.
- **Arts. 14 y 15**: derecho de acceso y de rectificación o supresión. Hoy no hay un método para borrar el historial de un oyente; sería el primer cambio si se pasara a datos reales.
- **Art. 18**: prohíbe formar bases de datos que revelen "directa o indirectamente" datos sensibles. Un historial de escucha podría hacerlo.

**Ley 9.739 (derechos de autor), modificada por Leyes 17.616 y 19.857.**
- **Art. 2**: el derecho de comunicar al público incluye la transmisión por radiodifusión u otro medio, "sea o no mediante suscripción o pago", y la puesta a disposición del público.
- **Art. 39 lit. B y D**: los productores de fonogramas tienen derecho exclusivo de autorizar la puesta a disposición de sus fonogramas, y junto con los intérpretes tienen derecho a una remuneración equitativa por su uso en radiodifusión.
- **Art. 44 lit. B, num. 6**: es reproducción ilícita transmitir sonidos por estaciones radiodifusoras sin autorización del autor.
- **Art. 58**: las entidades de gestión colectiva necesitan autorización del Poder Ejecutivo y contratan con las empresas de radiodifusión.
- **Aplicación al proyecto**: nuestro catálogo es inventado y no usa audio, así que no se reproduce ni comunica ninguna obra de terceros. Una radio real con música real necesitaría licencias.

## 4. Uso de IA

Usamos Claude para elegir el proyecto, entender la variante, discutir decisiones de diseño, revisar el UML, escribir el código base y revisar el repositorio. Cada uso está en `BITACORA_IA.md`. Las decisiones de diseño las tomamos nosotras, y rechazamos o corregimos varias propuestas de la IA.

Los errores de la IA tienen relación directa con la ética de la aplicación: el hueco de variedad (una canción cortada no contaba como sonada) y la burbuja de filtro salieron de un diseño en el que nos ayudó la IA, y los detectamos nosotras al correr el programa, no la IA. Claude también ayudó a ubicar y extraer el texto de las leyes citadas arriba. 