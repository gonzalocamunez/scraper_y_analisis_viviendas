# Project Description: scraper_*********

## (0) OBJETIVOS E ÍNDICE:

### Objetivo del scraper: 
Scraping del contenido de todas las páginas de anuncios de ********* (https://www.*********.com/) para la ciudad de Madrid de forma eficiente y evitando la detección por parte del WAF de *********.

### Objetivo de este documento: 
Ofrecer una guía completa y actualizada para que LA IA pueda acceder a toda la información del proyecto, en qué documento está cada parte y qué información contiene. La IA debe actualizar este documento con cualquier adición, modificación o eliminación de archivos o carpetas del proyecto.

### Consideraciones técnicas:
   1) ********* tiene un WAF (Web Application Firewall) que detecta y bloquea peticiones no humanas.
   2) Usaremos Camoufox (docs: `camoufox_doc.md` + `doc_links.md`) + Playwright (docs: `doc_links.md`)
   3) Usaremos proxies de Oxylabs (docs: `proxies.md` + `/knowledge/proxies` folder).
   4) Es importante ir escalando poco a poco y testando cada nuevo desarrollo para asegurar que no dejamos cabos sueltos que puedan delatarnos y al WAF.
   5) El proyecto se ejecutará en un entorno virtual creado dentro de la carpeta de proyecto → `/scraper_*********/venv`.
   

### Índice:
   1) `DECRIPCIÓN DEL PROYECTO`
   2) `DOCUMENTACIÓN DEL PROYECTO`



## (1) `DECRIPCIÓN DEL PROYECTO`:

### EJECUCIÓN: 

El proyecto funciona mediante **dos scripts** que se ejecutan de forma **independiente** pero **coordinada**:
   1) `scraper_links.py` recorre todas las páginas de resultados (`web_listado`) y obtiene los identificadores (`id_anuncio`) de los anuncios de *********.
   2) `scraper_anuncios.py` recorre todas las páginas de anuncio (`web_anuncio`) y obtiene los datos de cada anuncio de *********.

Ambos scrapers vuelcan los datos en `scraper.xlsx`.

### NAVEGACIÓN:
   1) Ambos scrapers siguen las reglas de navegación y selectores de `navegacion_y_selectores.md` y la configuración stealth de `stealth_config.md`.
   2) Para la navegación utilizamos en todo momento proxies de Oxylabs conforme se describe en `proxies.md`.

### REPORTE:
   1) `reportes.md` describe todo lo relativo a los informes (avances, **eventos clave** y estado de ejecución) que el scraper genera para que el usuario pueda entender el avance del proyecto (mensajes en consola, log e informes acumulados de datos extraidos, etc.).

Toda la información relativa al proyecto se encuentra en los documentos que se acaban de mencionar ubicados en la carpeta `/knowledge`. A lo largo del desarrollo del proyecto:
   1) Es posible que sea necesario crear documentos nuevos que se deben añadir y describir en esta sección dónde corresponda en el momento de crearlos.
   2) Es posible que sea necesario actualizar los documentos existentes si se implementan cambios relevantes en el proyecto que requieran una actualización de la documentación.

## (2) `DOCUMENTACIÓN DEL PROYECTO`:

### Documentación de `Camoufox y Playwright`:

Ubicada en la carpeta `/knowledge/teck_stack`.

### Documentación de `Oxylabs`:

Ubicada en la carpeta `/knowledge/proxies` contiene la documentación oficial de Oxylabs.

### Documentación `adicional`:

Ubicada en la carpeta `/knowledge/Otros`:
   1) `checklist_WAF.md` contiene un checklist de posibles medidas para evitar la detección por parte del WAF de *********.
   2) `elementos_stealth.md` contiene un listado de configuraciones e implementaciones en el código que tienen implicaciones en la detección por parte del WAF de *********.


## (3) `ARCHIVOS RELEVANTES` (creados/actualizados)

- `scraper_links.py` (raíz del proyecto): base del scraper de enlaces con etapas `warm_up`, navegación natural y extracción inteligente con `pivote_recientes`.
- `state/links_state.json`: estado persistente (pivote e `known_ids`).
- `.env.example`: plantilla de variables para Oxylabs (usuario, password, endpoint, puerto, país, `sessid`, `sesstime`).
- `camoufox_config.py`: refactor para cargar credenciales desde `.env` y exponer `create_browser(mode, session_id, country)` con presets `eficiente`, `segura` y `warm_up`.
