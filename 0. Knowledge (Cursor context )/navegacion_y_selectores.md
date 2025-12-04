# Navegación y selectores

## (0) OBJETIVOS E ÍNDICE:

### Objetivo de este documento: 
  Ofrecer a la IA una guía completa de la **navegación por la web objetivo** y los **selectores CSS** de la página de ********* para que pueda acceder a las distintas urls y extraer la información que necesitamos.

### Índice:
   1) `URLS`
   2) `SELECTORES`
   3) `NAVEGACIÓN`



## (1) `URLS`:

Para entender el proceso de scraping es clave entender las urls, su estructura y su navegación.

### Navegación natural de un usuario en un browser:
   Home → Mapa → Listado → Anuncio

### URLs:

**Home**: Estas URL son únicas y no varían. Son las siguientes:
   * `home` = https://www.*********.com/
   * `mapa` = https://www.*********.com/venta-viviendas/madrid-madrid/mapa
   * `web_listado` = https://www.*********.com/venta-viviendas/madrid-madrid/  

**Listado ordenado por fecha**: Varían en base a un patrón fijo que se observa en los ejemplos de esta sección. Son las siguientes:
   - Listados recientes:
      * `web_listado_recientes_pag_1` = https://www.*********.com/venta-viviendas/madrid-madrid/?ordenado-por=fecha-publicacion-desc
      * `web_listado_recientes_pag_2` = https://www.*********.com/venta-viviendas/madrid-madrid/pagina-2.htm?ordenado-por=fecha-publicacion-desc
      * `web_listado_recientes_pag_3` = https://www.*********.com/venta-viviendas/madrid-madrid/pagina-3.htm?ordenado-por=fecha-publicacion-desc
      * El patrón continúa con `web_listado_recientes_pag_4`, `web_listado_recientes_pag_5`, etc.
   - Listados antiguas:
      * `web_listado_antiguas` = https://www.*********.com/venta-viviendas/madrid-madrid/?ordenado-por=fecha-publicacion-asc
      * `web_listado_antiguas_pag_2` = https://www.*********.com/venta-viviendas/madrid-madrid/pagina-2.htm?ordenado-por=fecha-publicacion-asc
      * `web_listado_antiguas_pag_3` = https://www.*********.com/venta-viviendas/madrid-madrid/pagina-3.htm?ordenado-por=fecha-publicacion-asc
      * El patrón continúa con `web_listado_antiguas_pag_4`, `web_listado_antiguas_pag_5`, etc. 
**Como construir URLs de anuncio (`web_anuncio`)**: Varían en base a un patrón fijo que se observa en los ejemplos de esta sección. Son las siguientes:
   * `web_base_inmueble` = https://www.*********.com/inmueble/
   * `web_anuncio` = https://www.*********.com/inmueble/xxxxxxxxx/  # `web_anuncio` = urljoin de `web_base_inmueble` + `id_anuncio`.
   * `id_anuncio` = xxxxxxxxx                                       # xxxxxxxxx = ID único de cada anuncio de 10 dígitos.


## (2) `SELECTORES`:

### Selectores de navegación:

Los índices de los selectores CSS ("nth-child(i)") en la `web_listado` a veces no siguen el orden que se muestra a continuación. Parece que a veces el orden se salta un índice y continua de +2 en +2 (pasa de pares a impares o viceversa).

**Items de anuncios** - Estos selectores contienen el `id_anuncio` de los anuncios de una `web_listado`. 
  * `primer_anuncio` = #main-content > section.items-container.items-list > article:nth-child(2) > div.item-info-container > a
  * `segundo_anuncio` = #main-content > section.items-container.items-list > article:nth-child(4) > div.item-info-container > a
  * `tercer_anuncio` = #main-content > section.items-container.items-list > article:nth-child(6) > div.item-info-container > a
  * ... y Así sucesivamente.                   # El índice de los selectores `nth-child(x)` se incrementa de +2 en +2.

**Botón de siguiente página** 
Este selector se corresponde con el botón de siguiente página y es el que el script debe encontrar cuándo haya acabado de recorrer todos los anuncios de la `web_listado` para pasar a la siguiente.
  * `next_page` = #main-content > section.items-container.items-list > div.pagination > ul > li.next > a


### Selectores de datos:

Criterio de utilización:
Los índices de los selectores CSS ("nth-child(i)") parecen encajar con la estructura de la `web_anuncio`.

Selectores de **Datos únicos**: Estos incluyen un número fijo de hijos (Quiero extraer el texto de todos):
   * `precio` = #main > div > main > section.detail-info.ide-box-detail-first-picture.ide-box-detail--reset.overlay-box > section > div.info-data > span > span
   * `m2` = #main > div > main > section.detail-info.ide-box-detail-first-picture.ide-box-detail--reset.overlay-box > section > div.info-features > span:nth-child(1)
   * `habitaciones` = #main > div > main > section.detail-info.ide-box-detail-first-picture.ide-box-detail--reset.overlay-box > section > div.info-features > span:nth-child(2)
   * `piso_exterior_ascensor`	= #main > div > main > section.detail-info.ide-box-detail-first-picture.ide-box-detail--reset.overlay-box > section > div.info-features > span:nth-child(3)
   * `detalles` = #main > div > main > section.detail-info.ide-box-detail-first-picture.ide-box-detail--reset.overlay-box > section > div.info-features (el elemento contiene varios hijos. Quiero extraer el texto de todos)
  * `comentario_anunciante` = #main > div > main > section.detail-info.ide-box-detail-first-picture.ide-box-detail--reset.overlay-box > section > div.commentsContainer > div.comment > div > p

Selectores de **Datos listados**: Estos pueden incluir varios hijos de forma variable (Quiero extraer el texto de todos):
   * `caracteristicas_basicas` = #details > div.details-property > div.details-property-feature-one > div > ul 
   * `edificio` = #details > div.details-property > div.details-property-feature-one > div:nth-child(4) > ul 
   * `equipamiento` = #details > div.details-property > div.details-property-feature-two > div:nth-child(2) > ul 
   * `certificado_energetico` = #details > div.details-property > div.details-property-feature-two > div:nth-child(4) > ul
   * `ubicación` = #headerMap > ul

   

La `fecha de actualización`no viene de un único selector si no que hay que extraerla en base a dos selectores:
   * `Anuncio_actualizado_el_XX_de_XXXX` = #stats > p
    - Este selector contiene un texto con la fecha de actualización del anuncio (sin el año). Se muestra tal así = `Anuncio_actualizado_el_XX_de_XXXX`.
   * `Anuncio actualizado hace XX días` = #main > div > main > section.detail-info.ide-box-detail-first-picture.ide-box-detail--reset.overlay-box > section > section.details-box.date-update-block > p
    - Este selector contiene un texto con el número de días que ha pasado desde la última actualización del anuncio. Se muestra tal así = `Anuncio actualizado hace XX días`

   → **Con el contenido de ambos campos** podemos obtener la fecha de actualización del anuncio completa con día, mes y año.
    


## (3) `NAVEGACIÓN`:

### NAVEGACIÓN EN `scraper_links.py`:

#### OBJETIVO: `scraper_links.py` es el script que se encarga de obtener todos los enlaces de los anuncios de ********* (`web_anuncio`). Tiene como objetivo lo siguiente:
   1) Recorrer las `web_listado`.
   2) Extraer los `id_anuncio` y construir un listado.
   3) Con todos los `id_anuncio` construir las url de todas las `web_anuncio`.

#### ETAPAS:
   * ETAPA 1: `WARM-UP` Y `VALIDACIÓN` DEL WAF
      1) Conexión y warm-up del proxy.
      2) Navegación humana controlada a la `home` de *********: headful, sin paralelización, aceptando cookies, resolviendo CAPTCHA si apareciese, etc.
      3) ********* inyecta una cookie de validación y nosotros la guardamos.
      4) Tomar esa cookie de validación para inyectarla en la navegación posterior.
   * ETAPA 2: `NAVEGACIÓN NATURAL` HASTA COMIENZO DE SCRAPER
      1) Desde la `home`, navegamos hasta el `mapa` de la ciudad de Madrid.
      2) Desde el `mapa`, navegamos hasta la primera `web_listado` de la ciudad de Madrid. 
   * ETAPA 3: `NAVEGACIÓN INTELIGENTE` (CON USO DE PIVOTES):
    0) CONTEXTO:
      -  Desde la primera `web_listado` (en función de la ordenación recientes/antiguos), aquí es dónde scraper_links.py trata de obtener el máximo número (idealmente el 100%) de id_anuncio recorriendo una a una las `web_listado`. 
      - Debido a que el listado de anuncios depende de los usuarios que los gestionan y de la compra/venta de los pisos, el listado de anuncios se actualiza en tiempo real y se añaden y eliminan `web_anuncio` del listado constantemente.
    1) PROCESO: 
      1) Alicar el '####Proceso de `NAVEGACIÓN INTELIGENTE`' descrito en el siguiente epígrafe.
      2) En caso de que sea necesario, aplicar la `lógica de reintentos` descrita en `stealth_config.md` según el `modo de navegación` en el que estemos en ese momento.

##### Proceso de `NAVEGACIÓN INTELIGENTE`:

CONTEXTO:
* El proceso comienza en la primera ejecución asumiendo que el scraper nunca se ha ejecutado y por tanto no se ha extraido ninguna información previa. 
* El proceso tiene por objetivo ser eficiente en la navegación y para ello utiliza un listado ordenado siempre con un criterio fijo cuya única variación es la adición o eliminación de elementos pero nunca una modificación del orden de los mismos.
* La ordenación por fecha de publicación reciente, nos permite:
  - Mantener el orden de los anuncios fijo (= por fecha de publicación).
  - Obtener los anuncios recientes primero y después en base a un pivote previamente registrado, saltar todos los anuncios ya registrados en la ejecución anterior.
  - Conforme van avanzando las ejecuciones, el scraper va recogiendo información previa y la va utilizando para continuar desde el punto en que se dejó en la anterior ejecución.


PROCESO:
**`PRIMERA`EJECUCIÓN**:
  1) **Obtención de nuevos:** Comienza en `web_listado_recientes_pag_1` (por primera vez) y registra todos los `id_anuncio` de la primera página (comenzando por el primer `id_anuncio` disponible), después de la segunda y así sucesivamente. 
  2) **Detención y registro de pivote:** Si la ejecución se detiene, el scraper identifica en qué `id_anuncio` se ha quedado (y en qué página de `web_listado_recientes` si hiciera falta) y lo registra en un documento JSON como `pivote_recientes` = último elemento registrado por el scraper. **Contiene dos datos**:
    - La posición absoluta 1‑based del `id_anuncio` contando desde el comienzo de la ejecución, el primer `id_anuncio` registrado. `pivote_recientes` es por tanto el último elemento que hemos registrado contando desde el primero.
    - El `id_anuncio` que hemos registrado en el último elemento.


**`SEGUNDA` EJECUCIÓN**:
  1) **Obtención de nuevos:** Comienza en `web_listado_recientes_pag_1` (ya que es posible que se hayan añadido anuncios nuevos desde la anterior ejecución) y el scraper registra todos los `id_anuncio` que sean nuevos de la primera página, después de la segunda y así sucesivamente. 
  2) **Llegada a elemento conocido:** En el momento que se encuentra un `id_anuncio` que ya tenemos registrado, el scraper asume que nos encontramos en el primer `id_anuncio` de la ejecución anterior (PRIMERA EJECUCIÓN). 
  3) **Salto a pivote:** Desde ese elemento, el scraper cuenta n veces, siendo n el `pivote_recientes` de la ejecución anterior.
  4) **Ajuste o no de pivote:** Una vez en ese elemento (debido a que el listado está vivo), hay que comprobar si ese elemento se corresponde con el id_anuncio de `pivote_recientes`.
    (a) Si es así, el siguiente elemento debería contener un `id_anuncio` que no hemos registrado todavía y el scraper debería continuar la ejecución desde ahí y encontrar únicamente elementos con `id_anuncio` nuevos.
    (b) Si no es así, es debido a que se han eliminado uno o varios elementos del listado y por tanto el punto de comienzo se encuentra en elementos anteriores.
  5) **Detención y registro de nuevo pivote:** Si la ejecución se detiene, el scraper identifica en qué `id_anuncio` se ha quedado (y en qué página de `web_listado_recientes` si hiciera falta) y lo registra en un documento JSON como el nuevo `pivote_recientes`.

**`TERCERA` EJECUCIÓN** y siguientes: Se continua el proceso de forma idéntica a la SEGUNDA EJECUCIÓN.


### NAVEGACIÓN EN  `scraper_anuncios.py`

#### OBJETIVO: `scraper_anuncios.py` es el script que se encarga de obtener todos los datos de los anuncios de ********* (`web_anuncio`). Tiene por objetivo lo siguiente:
  1) Recorrer las `web_anuncio`.
  2) Extraer los datos de la `web_anuncio` y volcarlos en un archivo Excel.

#### ETAPAS:
* ETAPA 1: `WARM-UP` Y `VALIDACIÓN` DEL WAF
  1) Conexión y warm-up del proxy.
  2) Navegación humana controlada a la `home` de *********: headful, sin paralelización, aceptando cookies, resolviendo CAPTCHA si apareciese, etc.
  3) ********* inyecta una cookie de validación y nosotros la guardamos.
  4) Tomar esa cookie de validación para inyectarla en la navegación posterior.
* ETAPA 2: `NAVEGACIÓN NATURAL` HASTA COMIENZO DE SCRAPER
  1) Desde la `home`, navegamos hasta el `mapa` de la ciudad de Madrid.
  2) Desde el `mapa`, navegamos hasta la primera `web_listado` de la ciudad de Madrid.
* ETAPA 3: `NAVEGACIÓN SECUENCIAL`:
  1) Consumir el listado de `web_anuncio` (`id_anuncio` + `web_base_inmueble`) y visitar una a una las url en el mismo orden en que se obtuvieron (criterio FIFO).
  2) En cada visita, extraer únicamente los datos de la `web_anuncio` y volcarlos en un archivo Excel.
  3) En caso de que sea necesario, aplicar la `lógica de reintentos` descrita en `stealth_config.md` según el `modo de navegación` en el que estemos en ese momento.








