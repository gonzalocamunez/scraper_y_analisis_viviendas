# Elementos de fingerprint, stealth y dead‑giveaways (Scraper)

Basado en `knowledge/checklist_WAF.md`, el código `camoufox_scraper.py` y el ejemplo `knowledge/scripts/camoufox_config.py`.

Formato por elemento:
Nombre amigable (entre paréntesis: objeto y tipo; incluir identificador y ruta para grep)
:: Descripción breve
  * (A) fingerprint → trade‑offs
  * (B) stealth → por qué añade stealth
  * (C) dead_giveaways → por qué delata

---

## (A) Configuraciones_fingerprint (ordenadas por mayor impacto)

### (A.1) Fingerprint configurable (Camoufox):

(1.1) WebGL vendor/renderer (Camoufox, argumento 'webgl_config'; identificador: `webgl_config=`; ruta: `camoufox_scraper.py` → `Camoufox(... webgl_config=get_webgl_config(SESSID))`)
:: Fija `(vendor, renderer)` de WebGL, afectando hash WebGL/canvas y capacidades.
   * Trade‑offs:
     - Pros: coherencia con `os="macos"` y UA; estable por sesión; rotación por `SESSID` tras restart.
     - Contras: desalineación OS/UA es sospechosa; rotación excesiva aparenta “device churn”.
   * Relaciones: `os`, `headers.User-Agent`, `navigator.platform`, `screen`/`window.devicePixelRatio`, `fonts`; el par debe existir para el `os` objetivo.
   * Estado en nuestro código: Presente — `webgl_config=get_webgl_config(SESSID)` en F1/F2/challenge.

(1.2) Fuentes visibles (Camoufox, argumento 'fonts'; helper: `get_mac_fonts` ; identificador: `fonts=`; ruta: `Camoufox(... fonts=get_mac_fonts(SESSID, 12))`)
:: Define set de fuentes detectables por CSS/canvas que influye en métricas y canvas.
   *  Trade‑offs:
     - Pros: lista verosímil macOS; rotación por sesión con `SESSID` renueva identidad.
     - Contras: combinaciones raras delatan; cambios intra‑sesión generan inestabilidad; debe alinear con OS/UA.
   *  Relaciones: `os`, `navigator.userAgent` (OS), `fonts:spacing_seed` (métricas), `locale` (conjuntos de glifos regionales).
   *  Estado en nuestro código: Presente — `fonts=get_mac_fonts(SESSID, 12)`; helper `get_mac_fonts()`.

(1.3) Sistema operativo reportado (Camoufox, argumento 'os'; identificador: `os="macos"`; ruta: `Camoufox(... os="macos")`)
:: Afecta `navigator.platform`, parte del UA y APIs relacionadas.
   *  Trade‑offs:
     - Pros: coherente con WebGL Apple y fonts.
     - Contras: si timezone/idioma/proxy no acompañan, crea disonancias.
   *  Relaciones: `navigator.platform`, `navigator.hardwareConcurrency`, `headers.User-Agent`, `webgl_config`, `fonts`, `locale`, `timezone`.
   *  Estado en nuestro código: Presente — `os="macos"` en F1/F2/challenge.

(1.4) GeoIP habilitado (Camoufox, argumento 'geoip'; identificador: `geoip=True`; ruta: `Camoufox(... geoip=True)`)
:: Alinea geolocalización con IP del proxy.
   *  Trade‑offs:
     - Pros: reduce incoherencias IP↔geoloc.
     - Contras: cambios bruscos de región pueden levantar señales.
   *  Relaciones: `locale`, `headers.Accept-Language`, `navigator.language(s)`, `timezone`, `webrtc:ipv4/ipv6`.
   *  Estado en nuestro código: Presente — `geoip=True` en F1/F2/challenge.

(1.5) Bloqueo de WebRTC (Camoufox, argumento 'block_webrtc'; identificador: `block_webrtc=True`)
:: Parchea APIs WebRTC para evitar fugas.
   *  Trade‑offs:
     - Pros: elimina fugas de IP/RTC; reduce superficie de fingerprint.
     - Contras: webs que dependen de RTC pueden fallar; bloqueo total también es patrón detectable en ciertos contextos.
   *  Por qué añade stealth: evita filtrado IP/RTC y superficies adicionales de detección.
   *  Estado en nuestro código: Presente — `block_webrtc=True`.

### (A.2) Spoofed by GeoIP=True (Camoufox): IP's `longitude`, `latitude`, `timezone`, `country`, `locale`, and `WebRTC IP`.

(2.1) WebRTC IP (Config avanzado; identificadores: `webrtc:ipv4`, `webrtc:ipv6`; toggle: `block_webrtc=True`)
:: IPs de WebRTC deben coincidir con la IP de proxy/geoip o deshabilitarse completamente.
   *  Relaciones: `geoip`, `proxy`, `navigator.onLine`.
   *  Estado en nuestro código: Presente — `block_webrtc=True` (WebRTC bloqueado).
   *  Al estar definido por Camoufox de manera inteligente (GeoIP=True), no es necesario explicitarlo.

(2.2) Locale & Intl (Camoufox, argumento 'locale'; identificador: `locale=`)
:: Define `Intl` y prioriza `navigator.language(s)`; acepta lista o país para autogenerar distribución lingüística.
   *  Relaciones: `headers.Accept-Language`, `navigator.language(s)`, `geoip`→`timezone` y país.
   *  Estado en nuestro código: No presente — no fijamos `locale` explícito.

### (A.3) Fingerprint injection (Camoufox): Esto valores los inyecta Camoufox en base al contexto.

(3.1) Propiedades de Navigator (Navigator, implícito; identificadores: `navigator.userAgent`, `navigator.platform`, `navigator.languages`, `navigator.hardwareConcurrency`, `navigator.maxTouchPoints`)
:: Conjunto de señales JS que definen el “dispositivo” Firefox camuflado.
   *  Relaciones: `os`, `locale`, `headers.User-Agent`/`headers.Accept-Language`, `screen`/`window.devicePixelRatio`, `webgl_config`.
   *  Estado en nuestro código: Presente (implícito) — Camoufox inyecta `navigator.*`.

(3.2) Headers HTTP (Red, override; identificadores: `headers.User-Agent`, `headers.Accept-Language`, `headers.Accept-Encoding`)
:: Encabezados de red coherentes con `navigator.*`. Si `headers.User-Agent` no se fija, cae a `navigator.userAgent` (doc oficial).
   *  Relaciones: `navigator.userAgent`, `locale`→`Accept-Language`, `proxy`/`geoip`.
   *  Estado en nuestro código: No presente — no usamos `headers=` ni `set_extra_http_headers`.

(3.3) Screen constraints (BrowserForge, argumento 'screen'; identificador: `screen=`)
:: Restringe dimensiones de `screen.*` en el fingerprint.
   *  Relaciones: `window.innerWidth/Height`, `window.devicePixelRatio`, cálculos de `canvas`/`webgl`.
   *  Estado en nuestro código: No presente — no fijamos `screen`.

Config avanzado (Camoufox gestiona estos parámetros por defecto)
(3.4) Viewport de ventana (Camoufox, argumento 'window'; identificador: `window=(w,h)`)
:: Fija `window.innerWidth/Height` y afecta `outer*` y offsets.
   *  Relaciones: `screen.*`, `window.devicePixelRatio`; evitar combinaciones imposibles (p. ej., DPR que no existe en el SO/GPU objetivo).
   *  Estado en nuestro código: No presente — no fijamos `window`.

(3.5) Media & Audio (Config avanzado; identificadores: `mediaDevices:*`, `AudioContext:*`)
:: Cantidad de micrófonos/cámaras/altavoces y parámetros de AudioContext.
   *  Relaciones: `os` y expectativas de hardware; valores extremos/anómalos pueden delatar.
   *  Estado en nuestro código: No presente — no hay overrides de `mediaDevices`/`AudioContext`.

(3.6) Canvas (Config avanzado; identificadores: `canvas:aaOffset`, `canvas:aaCapOffset`)
:: Anti‑fingerprinting de canvas a nivel de motor; evita “ruido” detectable.
   *  Relaciones: `screen`/`window.devicePixelRatio`, `webgl`.
   *  Estado en nuestro código: No presente — no configuramos `canvas:*`.

(3.7) Cohesión y rotación por sesión (Estrategia; identificadores: `SESSID`→seed para `fonts` y `webgl_config`)
:: Mantener huella estable dentro de la sesión y rotarla tras WAF/restart para cortar escaladas.
   *  Relaciones: `fonts`, `webgl_config`, `proxy` (sticky/rotating), `headers.User-Agent`.
   *  Estado en nuestro código: Presente — `SESSID`, `user_data_dir` por sesión y bucle `while True` con `NEED_RESTART`.

---

## (B) Configuraciones_stealth (no cambian huella, reducen detectabilidad)

### (B.0) Clasificación rápida:
  (B.1) **De Camoufox:** 1) Evaluación fuera del main world; 2) Contexto persistente por sesión; 3) No bloquear WebGL; 4) Humanize; 5) Addons.
  (B.2) **Funciones Custom:** 6) Desplazamiento humano suave; 7) Esperas seguras con jitter; 8) Resolver desafíos en headful; 9) Auto‑restart/backoff; 10) Logs y clasificación de riesgo.
  (B.3) **Proxies:** 11) Política de proxy y rotación coordinada.
  (B.4) **Otros:** —

### (B.1) **De Camoufox:

(1.1) Evaluación fuera del main world (Camoufox, argumento 'main_world_eval'; identificador: `main_world_eval=False`)
:: Minimiza huellas de instrumentación en el mundo principal JS.
   *  Trade‑offs:
     - Pros: menor exposición de intrumentación; evita colisiones con scripts de la página.
     - Contras: algunas páginas requieren hooks en main world; posibles incompatibilidades; debugging más complejo.
   *  Por qué añade stealth: reduce side‑effects detectables por anti‑bot.
   *  Estado en nuestro código: Presente — `main_world_eval=False` en F1/F2/challenge.

(1.2) Contexto persistente por sesión (Camoufox, argumentos 'persistent_context' y 'user_data_dir'; identificadores: `persistent_context=True`, `user_data_dir=`)
:: Conserva cookies/localStorage por sesión.
   *  Trade‑offs:
     - Pros: continuidad realista; menos fricción en consent/retos; mejora conversiones de navegación.
     - Contras: acumula estado “sucio”; si la sesión queda marcada, persiste la marca; necesita resets prudentes.
   *  Por qué añade stealth: continuidad realista y menor fricción en retos.
   *  Estado en nuestro código: Presente — `persistent_context=True`, `user_data_dir=SESSION_USER_DATA_DIR`.

(1.3) No bloquear WebGL (Camoufox, argumento 'block_webgl'; identificador: `block_webgl=False`)
:: Mantiene APIs gráficas disponibles.
   *  Trade‑offs:
     - Pros: se ajusta a comportamiento esperado de navegadores reales; mayor compatibilidad.
     - Contras: expone hash/capacidades WebGL y potencial fingerprint; si el perfil GPU es raro, puede delatar.
   *  Por qué añade stealth: bloquear WebGL es patrón común de bots.
   *  Estado en nuestro código: Presente — `block_webgl=False`.

(1.4) Humanize (Camoufox, argumento 'humanize'; identificador: `humanize=True`)
:: Simula micro‑movimientos y timings parecidos a un usuario humano.
   *  Trade‑offs:
    - Pros: reduce patrones deterministas de interacción; mejora realismo.
    - Contras: añade latencia adicional; si se combina con bloqueos de imágenes, algunos gestos pueden no tener efecto visual (aceptable).
   *  Por qué añade stealth: introduce jitter y señales de actividad de usuario a nivel del motor del navegador.
   *  Estado en nuestro código: Presente — activado como `humanize=True` en los tres contextos `Camoufox(...)`:
    - `handle_challenge_if_any()` (headful, imágenes ON)
    - Fase 1 (Sticky, recolección; imágenes OFF)
    - Fase 2 (Rotating, visita; imágenes OFF)

(1.5) Bloqueo de imágenes en scraping (Camoufox, argumento 'block_images'; identificador: `block_images=True`; ruta: Fase 1 y Fase 2)
:: Descarga HTML/CSS/JS sin solicitar imágenes.
   *  Trade‑offs:
    - Pros: reduce ancho de banda y ruido de red; acelera listados simples.
    - Contras: patrón de recursos anómalo; algunos retos/consents necesitan imágenes y fallan.
   *  Por qué delata: ratio de recursos atípico; algunos challenges requieren imágenes.
   - Estado en nuestro código: Presente — `block_images=True` en F1/F2; `False` en challenge.

(1.6) Addons (Camoufox, argumento 'addons'; identificador: `addons=[...]`)
:: Carga extensiones de Firefox (p. ej., uBlock Origin) para modificar comportamiento de red/UI.
   *  Trade‑offs:
    - Pros: puede reducir ruido de anuncios/trackers; normaliza patrón de recursos en algunos sitios.
    - Contras: extensiones cambian fingerprint (WebExtensions IDs, APIs); rutas locales y versiones deben ser coherentes; riesgo de delatarse si la combinación no es común.
   *  Evidencia: doc oficial de Camoufox indica soporte de `addons` y su impacto en entorno de navegador.
  - Estado en nuestro código: Pendiente — no activado aún. Decisión: posponer hasta validar el impacto de `humanize=True` y WAF; si se activa, preferir uBlock Origin estable y documentar ruta/versión.


### (B.2) **Funciones Custom:**

(2.1) Desplazamiento humano suave (función helper; identificador: `gentle_scroll(`; ruta: `camoufox_scraper.py` → `gentle_scroll(page)`)
:: Scroll corto con pausas para carga perezosa y gesto humano.
   *  Trade‑offs:
     - Pros: favorece carga perezosa; patrón de interacción más natural; reduce picos de red.
     - Contras: añade latencia; si el patrón es siempre idéntico podría perfilarse (mitigar con jitter).
   * Por qué añade stealth: simula lectura y actividad de usuario.
   * Estado en nuestro código: Presente — `gentle_scroll(page)` en listados.

(2.2) Esperas seguras con jitter (función helper; identificador: `safe_wait_page(`; ruta: `camoufox_scraper.py` → `safe_wait_page(page, ...)`)
:: Pausas aleatorias en ms/centésimas y checks de página.
   *  Trade‑offs:
     - Pros: evita timings deterministas; reduce condiciones de carrera y errores visibles.
     - Contras: reduce throughput; jitter demasiado corto/no natural puede ser inefectivo.
   * Por qué añade stealth: evita timings deterministas y errores visibles.
   * Estado en nuestro código: Presente — `safe_wait_page(...)` ampliamente usado.

(2.3) Resolver desafíos en headful (función; identificador: `handle_challenge_if_any(`; ruta: `camoufox_scraper.py`)
:: Abre ventana visible con imágenes habilitadas para resolver CAPTCHAs/turnstile si aparecen.
   * Trade‑offs:
     - Pros: posibilita resolver retos que requieren interacción real o rendering completo.
     - Contras: mayor consumo (UI e imágenes); depende de intervención; cambia el patrón de recursos.
   * Por qué añade stealth: coincide con comportamiento humano ante desafíos.
   * Estado en nuestro código: Presente — `handle_challenge_if_any()` crea contexto headful con imágenes.

(2.4) Auto‑restart con backoff y nueva identidad (bandera/estado/helpers; identificadores: `NEED_RESTART`, `_ensure_session_user_data_dir`, `_gen_sessid`, `waf_consec_muy_alto_f2`)
:: Ante 403/429/418/444 hace backoff y reinicia con nuevo `user_data_dir`, `SESSID`, `fonts` y `webgl_config`.
   * Trade‑offs:
     - Pros: corta escaladas WAF; recupera la ejecución; identidad fresca.
     - Contras: costo temporal y de progreso; reinicios frecuentes también son patrón; complejidad de estado.
   * Por qué añade stealth: corta escalada WAF y evita insistir con identidad marcada.
   * Estado en nuestro código: Presente — contador `waf_consec_muy_alto_f2`, flag `NEED_RESTART`, bucle `while True`.

(2.5) Logs y clasificación de riesgo (funciones; identificadores: `classify_waf_risk(`, `log_waf(`)
:: Etiquetado de estados HTTP/challenges y decisiones adaptativas.
   * Trade‑offs:
     - Pros: observabilidad; permite respuestas adaptativas y tuning fino.
     - Contras: mala clasificación conduce a sobrerreacción; logging excesivo afecta rendimiento.
   * Por qué añade stealth: permite respuestas proactivas ante señales WAF.
   * Estado en nuestro código: Presente — funciones `classify_waf_risk`, `log_waf`, `log_sys`.

### (B.3) **Proxies:**

(3.1) Política de proxy y rotación coordinada (constantes/credenciales; identificadores: `STICKY_PROXY_SERVER`, `ROTATING_PROXY_SERVER`, `PROXY_USERNAME-sessid-{SESSID}`)
:: Sticky para F1 y rotating para F2; `SESSID` incrustado en sticky para identidad estable.
   * Trade‑offs:
     - Pros: sticky da consistencia de identidad; rotating reduce bloqueos y distribuye riesgo.
     - Contras: rotación excesiva parece “device churn”; sticky prolongado puede ser marcado; coste de proxy.
   * Por qué añade stealth: equilibrio entre coherencia (F1) y rotación segura (F2).
   * Estado en nuestro código: Presente — F1 usa sticky con `-sessid-{SESSID}`, F2 usa rotating.

---

## (C) Dead giveaways (potenciales delatores)

### (C.0) Clasificación rápida
  (C.1) De Camoufox: 1) Bloqueo de imágenes en scraping; 2) Caché deshabilitada; 3) Headless; 4) WebGL bloqueado; 5) COOP deshabilitado.
  (C.2) Funciones Custom: —
  (C.3) Proxies: —
  (C.4) Otros: 6) Desalineación OS/UA/WebGL/Fonts; 7) Accept‑Language vs locale/navigator; 8) Viewport/DPR imposibles; 9) Valores de Navigator incoherentes; 11) Set de fuentes anómalo.

### (C.1) **De Camoufox:**

(1.1) Bloqueo de imágenes en scraping (Camoufox, argumento 'block_images'; identificador: `block_images=True`; ruta: Fase 1 y Fase 2)
:: Descarga HTML/CSS/JS sin solicitar imágenes.
  * Trade‑offs:
    - Pros: reduce ancho de banda y ruido de red; acelera listados simples.
    - Contras: patrón de recursos anómalo; algunos retos/consents necesitan imágenes y fallan.
  * Por qué delata: ratio de recursos atípico; algunos challenges requieren imágenes.
  * Estado en nuestro código: Presente — `block_images=True` en F1/F2; `False` en challenge.

(1.2) Caché deshabilitada (Camoufox, argumento 'enable_cache'; identificador: `enable_cache=False`)
:: Repetición de estáticos sin hits de caché/validaciones.
  * Trade‑offs:
    - Pros: depuración más determinista; evita efectos de caché sucia entre sesiones.
    - Contras: mayor tráfico y latencia; menos realista frente a navegadores de usuarios.
  * Por qué delata: navegadores reales usan caché; patrón puede marcarse.
  * Estado en nuestro código: Presente — `enable_cache=False`.

(1.3) Headless (Camoufox, argumento 'headless'; identificadores: `headless=True` en scraping; `headless=False` en challenges)
:: Modo sin UI en scraping; visible solo para desafíos.
  * Trade‑offs:
     - Pros: mejor rendimiento y menor consumo de recursos.
     - Contras: si fallan ofuscaciones (p. ej., `navigator.webdriver`), delata; algunas UIs no renderizan correctamente.
  * Por qué delata: si ofuscación falla (p. ej., `navigator.webdriver`), headless es señal directa.
  * Estado en nuestro código: Presente — F1/F2 headless; challenge headful.

(1.4) WebGL bloqueado (Camoufox, argumento 'block_webgl'; identificador: `block_webgl=True`)
:: Desactiva WebGL.
  * Trade‑offs:
     - Pros: reduce superficie de fingerprint de WebGL.
     - Contras: rompe compatibilidad en sitios que esperan WebGL; patrón típico de bots.
  * Por qué delata: muchos sitios esperan WebGL; el propio doc recomienda evitarlo salvo casos especiales.
  * Estado en nuestro código: No presente — usamos `block_webgl=False`.

(1.5) COOP deshabilitado (Camoufox, argumento 'disable_coop'; identificador: `disable_coop=True`)
:: Deshabilita Cross‑Origin‑Opener‑Policy globalmente.
  * Trade‑offs:
     - Pros: puede resolver flujos con iframes/challenges (p. ej., algunos turnstile) muy restrictivos.
     - Contras: comportamiento atípico de aislamiento; riesgo de romper integridad/seguridad percibida.
  * Por qué delata: comportamiento atípico; usar solo cuando sea imprescindible (p. ej., turnstile en iframes).
  * Estado en nuestro código: No presente — no fijamos `disable_coop`.

### (C.2) **Otros:**

(2.1) Desalineación OS/UA/WebGL/Fonts
:: Mezclar SO/UA con `webgl_config` o set de fuentes de otra plataforma.
  * Trade‑offs:
     - Pros: ninguno — se debe evitar.
     - Contras: combinaciones imposibles o raras son fácilmente detectables por datasets.
  * Por qué delata: combinaciones no soportadas para ese SO son detectables por datasets (evidencia en doc de `webgl_config`).
  * Estado en nuestro código: No presente por diseño — `os="macos"` + `webgl_config`/`fonts` alineados; vigilar elección aleatoria de `get_webgl_config()`.

(2.2) Accept‑Language vs locale/navigator
:: `headers.Accept-Language` no coincide con `locale`/`navigator.languages`.
  * Trade‑offs:
     - Pros: ninguno.
     - Contras: incoherencia regional visible; contradice señales de GeoIP/Intl.
  * Por qué delata: inconsistencia regional; contradice GeoIP (doc GeoIP genera locale/language).
  * Estado en nuestro código: No presente — no forzamos headers; confiamos en `geoip=True`.

(2.3) Viewport/DPR imposibles
:: `window.innerWidth/Height` y `devicePixelRatio` no cuadran con `screen.*`.
  * Trade‑offs:
     - Pros: ninguno.
     - Contras: métricas físicas irreales; alto poder de delación por checks de layout/canvas.
  * Por qué delata: combinaciones físicamente improbables; sospecha de manipulación (hipótesis basada en prácticas anti‑bot).
  * Estado en nuestro código: No presente — no fijamos `window`/`screen`.

(2.4) Valores de Navigator incoherentes
:: `navigator.hardwareConcurrency`/`platform`/`maxTouchPoints` incompatibles con el SO elegido.
  * Trade‑offs:
     - Pros: ninguno.
     - Contras: perfil de hardware improbable; contradicciones cruzadas con UA/OS/WebGL.
  * Por qué delata: perfil de hardware improbable (hipótesis basada en prácticas anti‑bot).
  * Estado en nuestro código: No presente — Camoufox genera valores coherentes con `os`.

(2.5) Set de fuentes anómalo
:: Falta de tipografías base del SO o exceso de fuentes exóticas.
  * Trade‑offs:
     - Pros: ninguno.
     - Contras: fingerprint de fuentes fuera de distribución esperada; métricas/canvas anómalos.
  * Por qué delata: métricas de fuentes anómalas y combos improbables (hipótesis).
  * Estado en nuestro código: Potencial — `get_mac_fonts()` usa `random.sample` de lista amplia; a vigilar.

---

## Notas y recomendaciones
- Alinear `os`, `webgl_config` y `fonts` con UA/región del proxy.
- Rotar por sesión (no intra‑sesión) para evitar “device churn”.
- Activar imágenes cuando suban señales WAF o en páginas sensibles.
- Considerar habilitar caché en sesiones largas para normalizar patrón de red.
