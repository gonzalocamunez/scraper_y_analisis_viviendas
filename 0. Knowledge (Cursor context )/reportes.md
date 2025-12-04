# Reportes y mensajería en Consola

## (0) OBJETIVOS E ÍNDICE:

### Objetivo de este documento**: 
 Ofrecer a la IA una guía completa sobre todo lo relativo a los informes (avances, **eventos clave** y estado de ejecución) que el scraper genera para que el usuario pueda entender el avance del proyecto (mensajes en consola, log e informes acumulados de datos extraidos, etc.).
  
### Consideraciones técnicas:
   0) Los **eventos clave** son todos aquellas ocurrencias que explican lo que ocurre durante la ejecución del scraper (códigos de respuesta HTTP, mensajes en consola, errores, cambio de modo de navegación, registro o inyección de una cookie, etc.)
   1) El propósito es que el usuario mantenga visibilidad total del estado de ejecución, el progreso de navegación y los eventos en tiempo real, evitando momentos de confusión o esperas no explicadas. 
   2) Esto permite al usuario verificar que el scraper navega correctamente, respeta los códigos de respuesta HTTP y sigue el flujo de navegación esperado.
   3) La IA considerará hacer un log de los **eventos clave** más relevantes para permitir (al usuario y a la IA) analizar lo que ha ocurrido durante las últimas ejecuciones, entender los motivos de detención (y detección del WAF) y tomar decisiones informadas para hacer los ajustes necesarios.
   4) Utilizaremos la librería `rich` para mostrar los prints en consola con códigos de colores.

### Índice:
   (1) `PRINTS` EN CONSOLA
   (2) `ETIQUETAS` Y `MENSAJES DESTACADOS` POR CATEGORÍA
   (3) `SEÑALES` Y `MANEJO DEL WAF`


## (1) `PRINTS` EN CONSOLA:

Todas imprimen con `console.print(...)` y un `style` específico.

- `log_info(msg)`
  - Formato: `[INFO] {msg}`
  - Estilo: `cyan`
  - Uso: información general.

- `log_warn(msg)`
  - Formato: `[WARN] {msg}`
  - Estilo: `yellow`
  - Uso: advertencias y errores no críticos.

- `log_nav(tag, url, status)`
  - Condición: sólo si `SHOW_NAV` es `True`.
  - Formato: `[NAV] {tag}: {url} status={status}`
  - Estilo dinámico: `green` si `200 <= status < 400`, si no `bright_red`.
  - Uso: hitos de navegación (por ejemplo, al entrar en listados o al pasar de página).

- `log_sys(msg)`
  - Condición: sólo si `SHOW_SYS` es `True`.
  - Formato: `[SYS] {msg}`
  - Estilo: `dim`
  - Uso: logs internos del sistema y progreso del flujo.

- `log_waf(msg)`
  - Formato: `[WAF] {msg}`
  - Estilo: `bright_magenta`
  - Uso: señales/alertas de WAF (respuestas del sitio, desafíos, riesgo elevado).



   ### (2) `ETIQUETAS` Y `MENSAJES DESTACADOS` POR CATEGORÍA:

   A continuación, las etiquetas tal como aparecen en consola y dónde se generan.

   ### Etiquetas base:

   Algunas sugerencias de etiquetas son las siguientes:

   - `[INFO]` — Informativo
   - `[WARN]` — Advertencia
   - `[NAV]` — Navegación
   - `[SYS]` — Sistema
   - `[WAF]` — WAF
   - `[RHYTHM]` — Pausas/ritmo humano en listados o anuncios.
   - `[PROGRESS]` — Progreso acumulado. Imprimirlas al principio y final de cada ejecución.

   La IA debe actualizar este listado conforme vaya modificando (si lo hace) o añadiendo (si lo hace) etiquetas y mensajes.

## (3) `SEÑALES` Y `MANEJO DEL WAF`:

- Clasificación de riesgo en `classify_waf_risk(status)`:
  - `MUY ALTO`: 429, 403, 418, 444
  - `ALTO`: 520–529, 406, 413, 414
  - `MEDIO-ALTO`: 301, 302
  - `MEDIO`: 502, 400, 405
  - `BAJO`: 451, 503
- Cuando se detecta riesgo (`navigate_and_stabilize(...)`):
  - Se emite `[WAF] {nivel} · {tag}: {url} status={status}` en `log_waf(...)`.
- En `stage2_producer(...)` y `stage3_consumer(...)`:
  - Riesgos `MUY ALTO/ALTO` disparan:
    - Reintentos con backoff (cola `retry_queue`).
    - Señal global `NEED_RESTART = True`.
    - Persistencia de `state['last_waf_high'] = True`.


   ### Flujo típico de mensajes

   1) `[NAV]` al abrir home/listados/anuncios.
   2) Si hay riesgo: `[WAF] {nivel}`.
   3) `[SYS] [RHYTHM]` pausas tras navegar o antes/después de visitar anuncios.
   4) `[SYS] [STAGE2]` al iniciar productor y `[PIVOT]/[COUNT]/[START]` al decidir índices.
   5) `[SYS] [STAGE3]` al visitar anuncios en orden; opcionalmente `[PROGRESS]` cada N.
   6) En rotación: `[SYS] [STAGE3] ...; [ROTATE] ...`.

   ### Ejemplos compactos

   - Éxito navegando listado descendente:
      - `[NAV] listado_desc: https://www.idealista.com/... status=200` (verde)
      - `[SYS] [RHYTHM] listado_desc pausa ~1874ms`

   - Riesgo WAF al pasar de página de listado:
      - `[NAV] s2_next: https://www.idealista.com/... status=429` (rojo)
      - `[WAF] [STAGE2] MUY ALTO navegando listado; NEED_RESTART`

   - Visita de anuncio en consumidor con pausa humana:
      - `[SYS] [STAGE3] Visitando 7: 123456789`
      - `[NAV] web_anuncio: https://www.idealista.com/... status=200`
      - `[SYS] [RHYTHM] visita_anuncio pausa ~1542ms`


