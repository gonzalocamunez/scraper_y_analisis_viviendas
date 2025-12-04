# Configuración stealth

## (0) OBJETIVOS E ÍNDICE:

### Objetivo de este documento**:

Ofrecer a la IA una guía completa y en detalle sobre como definir la `configuración stealth` de todos los elementos (argumentos, parámetros y medidas antidetección) que potencialmente afectan a la detección por parte del WAF para ambos scrapers (`scraper_links.py` y `scraper_anuncios.py`). EL objetivo de este documento es definir el protocolos que permitan al script ajustar la configuración y el comportamiento de navegación en función de lo que ocurra durante la ejecución.

### Consideraciones técnicas:
   1) La `configuración stealth`:
      1) Incluye elementos en el código o fuera de él (Ejemplo: proxies).
      2) Se aplica en ambos scrapers (`scraper_links.py` y `scraper_anuncios.py`). Las especificidades que pudiera haber se definen en este documento.
   2) El script detecta los `ESTADOS DE EJECUCIÓN` a los que responde con `MODOS DE NAVEGACIÓN`.
   3) El script detecta los `EVENTOS DE DETECCIÓN` y responde cambiando de estado (`estado_deteccion`) y modo (`modo_detección`) y aplicando una `rotación forzada`.
   4) Es probable que tengamos que crear uno o varios archivos .json para persistir datos más allá de `scraper.xlsx`.
   5) Para detectar y persistir la cookie de validación que generaremos durante la etapa warmup, tendremos que buscar la forma de hacerlo.

### Índice:
   1) `ESTADOS` DE EJECUCIÓN                   → `MODOS` DE NAVEGACIÓN
   2) `MODOS` DE NAVEGACIÓN                    = Configuración de navegador (`config`) + Patrón de navegación (`nav`) + Rotación de identidad (`rotation`)
   3) `CONFIGURACIÓN` DE NAVEGADOR (CAMOUFOX)
   4) `PATRÓN` DE NAVEGACIÓN
   5) ROTACIÓN DE `IDENTIDAD` (`PERIÓDICA` Y `FORZADA`)


## (1) `ESTADOS` DE EJECUCIÓN:

### Definición de los `ESTADOS` DE EJECUCIÓN:

Los `ESTADOS` DE EJECUCIÓN se activan cuando se cumplen ciertas condiciones, ya sean del propio script o de su interacción con idealista.

Algunos ejemplos de cambios de estado de ejecución:
   1) El script avanza de la etapa warm-up a la etapa normal (Ejemplo: Termina la etapa de navegación warm-up y pasa de `estado_warm_up` a `estado_normal`)
   2) El script recibe `evidencias de detección` por parte del WAF de idealista (Ejemplo: Recibe una respuesta HTTP 403 y pasa de estado `estado_normal` a `estado_deteccion`).
   3) El script recibe `evidencias de normalidad` por parte del WAF de idealista (Ejemplo: Recibe una respuesta HTTP 200 y pasa de estado `estado_deteccion` a `estado_normal`).

### `ACTIVACIÓN` (y `desactivación`) de los `ESTADOS` DE EJECUCIÓN:

   1) `estado_warm_up`: 
      * Se activa al inicio del script y se mantiene hasta que el script avanza a la etapa de navegación normal.
      * Se desactiva al finalizar la etapa de navegación warm-up e iniciarse la siguiente etapa de navegación.
   2) `estado_normal`: 
      * Se activa cuando el script avanza de la etapa de navegación `warm-up` a las siguientes etapa de navegacións de navegación.
   * Se activa cuando se da una `VUELTA A LA NORMALIDAD` = el script recibe `evidencias de normalidad` de la inteacción con idealista.
   * Se mantiene activado salvo que recibamos `evidencias de detección` por parte del WAF de idealista. En ese caso se pasa al `estado_deteccion`.
   3) `estado_deteccion`: 
      * Se activa cuando se da un `EVENTO DE DETECCIÓN` = el script recibe `evidencias de detección` de la inteacción con idealista.
      * Se desactiva cuando se da una `VUELTA A LA NORMALIDAD` = el script recibe `evidencias de normalidad` de la inteacción con idealista. En ese caso se pasa al `estado_normal`.

### `ESTADOS` y sus `MODOS` DE NAVEGACIÓN:

`ESTADOS` DE EJECUCIÓN      → `MODOS` DE NAVEGACIÓN
   1) `estado_warm_up`   → `modo_warm_up`
   2) `estado_normal`    → `modo_normal` 
   3) `estado_deteccion` → `modo_detección`

### Códigos HTTP y su riesgo de detección por el WAF:

   1) `códigos de riesgo`:
      * MUY ALTO  			→ 429, 403, 418, 444
      * ALTO     			   → 520-529, 406, 413, 414  
      * MEDIO-ALTO			→ 301, 302 (CAPTCHA, TURNSTILE)
      * MEDIO	     			→ 502, 400, 405
      * BAJO      			→ 451, 503
   2) `códigos de normalidad`:
      * SIN RIESGO			→ 200
   
### Evidencias = (1) `evidencias de detección` y (2) `evidencias de normalidad`:

   1) `evidencias de detección`:
      * Presencia de `códigos de riesgo`.
      * Cualquier otro elemento que indique que hemos sido detectados.

   2) `evidencias de normalidad`:
      * Ausencia de `códigos de riesgo`.
      * Presencia de varios códigos HTTP=200 seguidos.


## (2) `MODOS` DE NAVEGACIÓN:

### Qué son los `MODOS` DE NAVEGACIÓN:

Los `MODOS` DE NAVEGACIÓN son la respuesta de nuestro script al cambio de `ESTADO` y siguen una serie de reglas:

   1) Durante el `estado warm-up` se activa el `modo warm-up`:
      1) Asume que estamos en el primer contacto con el WAF de idealista, al principio de la ejecución del script. 
      2) El objetivo de este modo es que el WAF nos envíe una cookie de validación que guardaremos para inyectarla en la navegación posterior.
      3) Utiliza la configuración y navegación más seguras posibles (`config_warm_up` y `nav_warm_up`) y sin rotación de identidad (`rotation_none`).
      4) Continua en `estado warm-up` (y modo) hasta que termina la etapa de navegación `warm-up`.
   2) Durante el `estado normal` se activa el `modo normal`:
      1) Asume que navegamos normalmente, con la cookie de validación inyectada y sin levantar sospechas.
      2) El objetivo de este modo es navegar lo más rápido y con el menor consumo de datos posible sin levantar sospechas por parte del WAF.
      3) Utiliza la configuración y navegación más eficientes posibles (`config_eficiente` y `nav_eficiente`) y con rotación de identidad (`rotation_normal`).
      4) Continua en estado (y modo) `normal` hasta que recibe evidencias de detección por parte del WAF de idealista.
   3) Durante el `estado detección` se activa el `modo detección`:
      1) Asume que hemos sido detectados por el WAF de idealista (`EVENTO DE DETECCIÓN`)
      2) El objetivo de este modo es continuar navegando sin ser detectados y, tras un tiempo sin detección, volver a un estado WAF bajo (estado `normal`).
      3) Lo primero que hace es una `rotación forzada` que involucra un cambio de IP de todos los proxies coordinado con el resto de elementos del fingerprint.
      4) Después cambia a configuración y navegación seguras (`config_segura` y `nav_segura`) y a una rotación de identidad (`rotation_normal*`).
      5) Continua en `estado detección` (y modo) hasta que recibe `evidencias de normalidad` por parte del WAF de idealista.

### Configuración de los `MODOS` DE NAVEGACIÓN:

`MODOS` DE NAVEGACIÓN     = Configuración de navegador (`config`) + Patrón de navegación (`nav`) + Rotación de identidad (`rotation`)
   1) `modo_warm_up`     = `config_warm_up`                      + `nav_warm_up`                + `rotation_none`
   2) `modo_normal`      = `config_eficiente`                    + `nav_eficiente`              + `rotation_normal`
   3) `modo_detección`   = `config_segura`                       + `nav_segura`                 + `rotation_normal*`


## (3) `CONFIGURACIÓN` DE NAVEGADOR (`CAMOUFOX`)

### `configuraciones de navegador` (`Camoufox()`):

Las `configuraciones de navegador` definen el comportamiento del navegador y están definidas por los argumentos de la función `Camoufox()` los cuales tienen implicaciones sobre la detectabilidad, la velocidad de la ejecución del scraper o el consumo de datos entre otros.

Existen 3 `configuraciones de navegador`, una para cada `MODO` DE NAVEGACIÓN:
   1) `modo_warm_up`     = `config_warm_up`
   2) `modo_normal`      = `config_eficiente`
   3) `modo_detección`   = `config_segura`

### Argumentos de la función `Camoufox()`:

EL el proyecto tiene una configuración por defecto (`config_eficiente`) que es la base para la configuración de Camoufox en todo el proyecto. La `config_eficiente` por tanto se aplica por defecto en ambos scrapers (`scraper_links.py` y `scraper_anuncios.py`) salvo que se indique lo contrario. Alternativamente, tenemos dos configuraciones alternativas: `config_segura` y `config_warm_up`

A continuación se muestra `config_eficiente` (en código) y alternativas (`config_segura` y `config_warm_up`) en comentarios:

```python
with Camoufox(
    headless=True,                # True en `config_eficiente` y `config_segura`. False en `config_warm_up`.
    i_know_what_im_doing=True,    # True siempre.
    humanize=True,                # True siempre.
    main_world_eval=False,        # False siempre.
    persistent_context=False,    # False siempre. No queremos persistir datos entre sesiones del navegador.
    #user_data_dir="./user_data", # Omitimos porque usamos persistent_context=False. Es el dir para persistir datos (Cookies, localStorage, historial, configuración, etc).
    enable_cache=False,           # False siempre. Navegamos headfull en warm-up, guardamos cookie de validación y la inyectamos después.
    #block_webrtc=False,          # Lo omitimos (False por defecto). Camoufox lo cubre con su spoofing (GeoIP).
    #block_webgl=False,           # Lo omitimos (False por defecto). Camoufox lo cubre con su spoofing.
    #disable_coop=True,           # Lo omitimos (False por defecto). En `config_warm_up` lo activamos (True) para Turnstile/CAPTCHA.
    block_images=True,            # True en `config_eficiente`. False en `config_segura` y `config_warm_up`.
    os=["windows", "macos"],      # Rota aleatoriamente entre `windows` y `macos` haciendo spoofing  de sus font, webgl y + elementos.
    fonts=get_extra_fonts("session_123", 12),  # Añade, a las fonts del `os`, fonts extra de un pool de forma aleatoria.
    geoip=True,                   # True siempre.
    proxy={                       # Asignar un nuevo `sessid` cambia la IP (No esperamos a que expire `sesstime`)
        'server': 'http://pr.oxylabs.io:7777',                                                        # Datos de ejemplo (no válidos).
        'username': f'customer-{USERNAME}-cc-{COUNTRY}-sessid-{session_id}-sesstime-{session_time}',  # Datos de ejemplo (no válidos).
        'password': PASSWORD                                                                          # Datos de ejemplo (no válidos).
    }
) as browser:
    page = browser.new_page()
    page.goto("https://www.idealista.com/")

```

Por tanto, y a modo de resumen a continuación se muestran las 3 configuraciones con sus respectivos parámetros en un diccionario:

```python
`config_eficiente` = { 'headless': True, 'i_know_what_im_doing': True, 'humanize': True, 'main_world_eval': False, 'persistent_context': False, 'enable_cache': False, 'block_images': True, 'os': ['windows', 'macos'], 'fonts': get_extra_fonts("session_123", 12), 'geoip': True, 'proxy': { 'server': 'EJEMPLO', 'username': 'EJEMPLO', 'password': 'EJEMPLO' } }

`config_segura` = { 'headless': True, 'i_know_what_im_doing': True, 'humanize': True, 'main_world_eval': False, 'persistent_context': False, 'enable_cache': False, 'block_images': False, 'os': ['windows', 'macos'], 'fonts': get_extra_fonts("session_123", 12), 'geoip': True, 'proxy': { 'server': 'EJEMPLO', 'username': 'EJEMPLO', 'password': 'EJEMPLO' } }

`config_warm_up` = { 'headless': False, 'i_know_what_im_doing': True, 'humanize': True, 'main_world_eval': False, 'persistent_context': False, 'enable_cache': False, 'block_images': False, 'os': ['windows', 'macos'], 'fonts': get_extra_fonts("session_123", 12), 'geoip': True, 'proxy': { 'server': 'EJEMPLO', 'username': 'EJEMPLO', 'password': 'EJEMPLO' } }
```

### Instancias de la función `Camoufox()`:

Dado que vamos a navegar con 5 proxies, vamos a tener que navegar con 5 instancias de la función `Camoufox()` activas en todo momento, cada una de ellas con un proxy asignado y  configurada con unos parámetros diferentes:
   1) Cada instancia de `Camoufox()` se generará con unos parámentros definidos en base al `MODO` y su `configuración de navegador` (revisar sección anterior).
   2) Con el cambio de `sessid` en el enpoint, Oxylabs nos asignará un nuevo proxy (nueva IP) y con ello, esa instancia de `Camoufox()` generará:
      1) longitude, latitude, timezone, country, locale, & spoof the WebRTC IP address acordes a la IP asignada gracias a GeoIP=True.
   3) Además, cada instancia de `Camoufox()` se generará:
      1) con unos valores aleatorios para los parámetros `os` lo cual determinará el listado base de `fonts`.
      2) Adicionalmente a las `fonts` base, se añadirán `fonts` extra de un pool para completar el listado de forma realista.
   4) El resto de aspectos de la navegación de cada instancia de `Camoufox()` se definen automáticamente por Camoufox en base a la automatización de su `FINGERPRINT` injection.

#### `FINGERPRINT` Spoofing/injection:

El `FINGERPRINT` son todos los elementos visibles por parte del WAF que, conjuntamente con nuestro **`IP`** conforman la `IDENTIDAD`.

Camoufox crea (spoof) todos los elementos del `FINGERPRINT` de forma coordinada:
   1) Navigator properties spoofing (device, browser, locale, etc.)
   2) Support for emulating screen size, resolution, etc.
   3) Spoof WebGL parameters, supported extensions, context attributes, and shader precision formats.
   4) Spoof the CPU Canvas fingerprint by manipulating the anti-aliasing logic (closed source)
   5) Spoof inner and outer window viewport sizes
   6) Spoof AudioContext sample rate, output latency, and max channel count
   7) Spoof device voices & playback rates
   8) Spoof the amount of microphones, webcams, and speakers avaliable.
   9) Network headers (Accept-Languages and User-Agent) are spoofed to match the navigator properties
   10) WebRTC IP spoofing at the protocol level
   11) Geolocation, timezone, and locale spoofing
   12) Battery API spoofing
   13) Anti font fingerprinting:
      1) Automatically uses the correct system fonts for your User Agent
      2) Bundled with Windows, Mac, and Linux system fonts
      3) Prevents font metrics fingerprinting by randomly offsetting letter spacing
   14) Automatically generates & injects unique device characteristics into Camoufox based on their real-world distribution
   15) WebGL fingerprint injection & periodic rotation (consistent within sessions, rotated between sessions)
   16) Uses the correct system fonts and subpixel antialiasing & hinting based on your target OS
   17) Avoid proxy detection by calculating your target geolocation, timezone, & locale from your proxy's target region
   18) Calculate and spoof the browser's language based on the distribution of language speakers in the proxy's target region
   19) Remote server hosting to use Camoufox with other languages that support Playwright
   20) Built-in virtual display buffer to run Camoufox headfully on a headless server
   21) Toggle image loading, WebRTC, and WebGL


## (4) `PATRÓN` DE NAVEGACIÓN:

### `Patrón de navegación` en `modo warm-up` (=`nav_warm_up`)
   
   1) **OBJETIVO**:  EL objetivo de `nav_warm_up` es enviar al WAF señales de navegación idénticas a las humanas para que nos envíe una cookie de validación que guardaremos para inyectarla en la navegación posterior. 

   2) **Parámetros:**
      * "Camoufox(headless=False)"
      * "Camoufox(block_images=False)" 
      * Tiempos humanos: Think Time y Scroll time realistas (máximo 10s) y aleatorizados + (en cada uno de ellos) jitter aleatorizado dentro de unos márgenes en segundos (máximo 700ms)

   3) **Comportamiento de navegación:**
      * Realizamos la navegación descrita en la etapa `warm-up` (ver `navegacion_y_selectores.md`) con elementos de humanización realistas, aceptamos cookies, resolvemos CAPTCHA o Turnstile (manual o de forma automática) si se nos presenta. Cumplimos con los `parámetros de navegación` del `modo warm-up`. 


### `Patrón de navegación` en `modo normal` (=`nav_eficiente`)
   
   1) **OBJETIVO**: El objetivo de 'nav_eficiente' es cumplir con los criterios de seguridad sin comprometer la eficiencia del scraper.

   2) **Parámetros:**
      * "Camoufox(headless=True)"
      * "Camoufox(block_images=True)"
      * Tiempos humanos: Think Time y Scroll time solo si son necesarios y de ser así, cortos (máximo 2s) y aleatorizados + (en cada uno de ellos) jitter aleatorizado dentro de unos márgenes en milisegundos (máximo 100ms)

   3) **Comportamiento de navegación:**
      * Asumimos que estamos fuera del radar del WAF y por tanto nos limitamos a realizar de forma eficiente la navegación descrita en la etapa `normal` (ver `navegacion_y_selectores.md`) cumpliendo con los los `parámetros de navegación` del `modo normal`. 

   4) **`Lógica de reintentos`**:
      - Reintentar un máximo de 3 veces (3 `id_anuncio`) para `scraper_links.py` y 3 veces (3 `web_anuncio`) para `scraper_anuncios.py` y `scraper_ubicacion.py`.
      - Aplicar un Backoff incremental añadiendo jitter con un valor aleatorio entre -10% y +10%.
      - Tras agotar los reintentos máximos, se marcará como `failed` y se continua con el siguiente elemento, dejando guardado el elemento para su reintentado en la próxima ejecución.


### `Patrón de navegación` en `modo detección` (=`nav_segura`)
   
   1) **OBJETIVO**: El objetivo de 'nav_segura' es minimizar la detección del WAF.

   2) **Parámetros:**
      * "Camoufox(headless=True)"
      * "Camoufox(block_images=False)"   
   3) **Tiempos humanos:**
      * Think Time y Scroll time solo si son necesarios y de ser así, cortos (máximo 5s) y aleatorizados + (en cada uno de ellos) jitter aleatorizado dentro de unos márgenes en milisegundos (máximo 500ms)
   4) **Comportamiento de navegación:**
      * Asumimos que estamos bajo la detección del WAF y por tanto realizamos la navegación descrita en la etapa `normal` (ver `navegacion_y_selectores.md`) cumpliendo con los los `parámetros de navegación` del `modo detección`. 
   5) **`Lógica de reintentos`**:
      - Reintentar un máximo de 3 veces (3 `id_anuncio`) para `scraper_links.py` y 3 veces (3 `web_anuncio`) para `scraper_anuncios.py`.
      - Aplicar un Backoff incremental añadiendo jitter con un valor aleatorio entre -50% y +50%.
      - Tras agotar los reintentos máximos, se marcará como `failed` y se continua con el siguiente elemento, dejando guardado el elemento para su reintentado en la próxima ejecución.




## (5) ROTACIÓN DE `IDENTIDAD` (`PERIÓDICA` Y `FORZADA`)

### Definición de `IDENTIDAD` (frente al WAF):

La `IDENTIDAD` es todo lo que el WAF puede detectar de nuestro scraper.

El elemento primero y principal de `IDENTIDAD` es el **`IP`** del proxy y por tanto un cambio en la `IP` implica que es necesario rotar todo el resto de elementos que conforman la `IDENTIDAD` de nuestro scraper PARA CADA UNO DE LOS PROXIES.

Por lo tanto, una ROTACIÓN DE `IDENTIDAD` es la acción de cambiar TODOS LOS ELEMENTOS SUSCEPTIBLES DE SER DETECTADOS POR EL WAF EN EL MOMENTO EXACTO EN EL QUE CAMBIAMOS EL PROXY PARA CADA UNO DE ELLOS. En nuestro caso, vamos a navegar utlizando 5 proxies por lo tanto, una rotación de identidad implica rotar los 5 proxies/IP y asignarles a cada uno su `FINGERPRINT` (revisar `FINGERPRINT` en este documento).

Por tanto, `IDENTIDAD` = `IP` (del proxy) + `FINGERPRINT`.

Cuándo hablamos de `ROTACIÓN DE IDENTIDAD` nos referimos a crear 5 identidades diferentes para los 5 proxies que vamos a utilizar para navegar de forma que podamos hacer una navegación eficiente utilizando cada uno de los proxies de forma individual para nuestra navegación. Es decir, una `ROTACIÓN DE IDENTIDAD` completa implica rotar los 5 proxies/IP y asignarles a cada uno su `FINGERPRINT`.


### `Rotación PERIÓDICA` (de `IDENTIDAD`):

Una `Rotación PERIÓDICA` se produce cada X minutos según la definamos en el código y tiene por objetivo renovar nuestra navegación cada cierto tiempo para evitar darle el tiempo suficiente al WAF para que detecte patrones de navegación asociados a nuestra IP.

La rotación periódica funciona de la siguiente manera:
   1) Para el `modo warm-up` NO se aplica rotación periódica (`rotation_none`)
   2) Para el `modo normal` se aplica rotación periódica con un valor definido en minutos en el código (`rotation_normal`). Comenzar con 2 minutos.
   3) Para el `modo detección` se aplica rotación periódica (`rotation_normal*`). Proceso de rotación periódica
      - `rotation_normal*` = `rotation_normal` modificada (valor de `rotation_normal` + o - un valor aleatorio entre 0 y 25%).
      - RECORDATORIO: 
         - Al activarse el `estado_deteccion` (tras un `EVENTO DE DETECCIÓN`), se aplica una `rotación forzada` y se pasa a `modo detección` (modo `nav_segura` y `rotation_normal*`)
         - Después de esto se pasa a la rotación periódica del `modo detección` (=`rotation_normal*`).
      

### `Rotación FORZADA` (de `IDENTIDAD` y `MODO`):

Una `Rotación FORZADA` se produce de forma inmediata tras producirse un `EVENTO DE DETECCIÓN` (revisar `EVENTO DE DETECCIÓN` en este documento) y tiene por objetivo salir de la detección del WAF cambiando nuestra `IDENTIDAD` y nuestro `MODO` (`modo_detección`)

Inmediatamente tras activar el `EVENTO DE DETECCIÓN`, el scraper debe:
   1) Hacer una `Rotación FORZADA`:
      1.1 Rotar todos los proxies (`IP`) cambiando sessid (revisar documento `proxies.md` para ver el detalle).
      1.2 Rotar para cada uno de ellos su `fingerprint`.
   2) Inyectar la cookie de validación que guardamos en la etapa `warm-up`.
   3) Cambiar su estado de ejecución a `estado_deteccion` y su modo de navegación a `modo_detección`.
        - RECORDATORIO: 
         - Al activarse el `estado_deteccion` (tras un `EVENTO DE DETECCIÓN`), se aplica una `rotación forzada` y se pasa a `modo detección` (modo `nav_segura` y `rotation_normal*`)
         - Después de esto se pasa a la rotación periódica del `modo detección` (=`rotation_normal*`).
         - `rotation_normal*` = `rotation_normal` modificada (valor de `rotation_normal` + o - un valor aleatorio entre 0 y 25%).







 
 
 












































