# Nuevos desarrollos stealth y robustez

Este documento resume los desarrollos recientes aplicados a los scrapers, indicando explícitamente en qué archivo/s se ha implementado cada uno.

## 1) Estados, Modos y Recuperación
- [scraper_anuncios.py]
  - Se mapea `estado_normal → modo_normal (config_eficiente)` y `estado_deteccion → modo_detección (config_segura)` al crear el navegador con Camoufox.
  - Recuperación a normalidad: tras `C200_RECOVERY_THRESHOLD` respuestas 200 consecutivas, se pasa a `estado_normal`/`modo_normal`.
- [scraper_links_async.py]
  - Ya existía. Se mantiene como referencia de buenas prácticas.

## 2) Rotación FORZADA + No filtraciones de identidad
- [scraper_anuncios.py]
  - `force_full_rotation(state)`: rota `sessid`, cambia a `estado_deteccion`/`modo_detección`, persiste y loguea.
  - `scrape_anuncio_with_state()`: tras códigos de riesgo (403/429, etc.), invoca rotación forzada, cierra `page`, abre otra y vuelve a inyectar la cookie de validación.
  - Cookie injection SIEMPRE que se abre/reabre una `page`.
- [scraper_links_async.py]
  - Ya implementado con lógica equivalente.

## 3) Rotación PERIÓDICA con jitter por modo
- [scraper_anuncios.py]
  - `maybe_rotate_periodic(state)`: 
    - `modo_normal`: umbral base `ROTATE_PERIOD_SEC` (120 s). 
    - `modo_detección`: `rotation_normal*` = base ± 25%.
  - Se invoca antes de cada navegación al `web_anuncio` durante los reintentos.
- [scraper_links_async.py]
  - Ya implementado. Se replica el comportamiento.

## 4) Reintentos con backoff dependiente del modo
- [scraper_anuncios.py]
  - 3 reintentos por `web_anuncio` con backoff + jitter:
    - `modo_detección`: 2–5 s ± 50%.
    - `modo_normal`: 0.8–2.0 s ± 10%.
- [scraper_links_async.py]
  - Ya existía con filosofía equivalente (async + jitter).

## 5) Warm-up y Validación de Cookie
- [scraper_anuncios.py]
  - `etapa_warm_up()`: HOME → MAPA → LISTADO, guardado de cookies.
  - `scrape_anuncio_with_state()`: inyección de cookie siempre al abrir `page`.
- [scraper_links_async.py]
  - Equivalente: validación/inyección de cookie y navegación pre-listado.

## 6) Logs y Métricas de Progreso
- [scraper_anuncios.py]
  - `log_nav`, `log_waf`, `log_progress`, `write_progress` habilitados por variables de entorno (`SHOW_NAV`, `SHOW_WAF`, `PROGRESS`).
  - Reporte final `report_anuncios.json`.
- [scraper_links_async.py]
  - Ya existía con mayor granularidad (async).

## 7) Persistencia Inmediata por Ítem
- [scraper_anuncios.py]
  - `write_anuncios_to_excel()` thread-safe por worker. Escribe cada anuncio inmediatamente.
- [scraper_links_async.py]
  - Persistencia equivalente para links.

## 8) Skip list por ejecución + failed_reasons persistentes
- [scraper_anuncios.py]
  - En `worker_process_anuncios()` se añade una skip list por ejecución (`skipped_this_run`) para evitar reintentar el mismo ID dentro de la misma ejecución del worker.
  - Persistencia en estado de `failed_reasons` con causas: `no_200_tras_reintentos`, `excel_write_failed`, `invalid_proxy`, `asyncio_in_loop`, `exception`.
  - `failed_ids` se guarda para reintentos en próximas ejecuciones (conforme a la guía).
- [scraper_links_async.py]
  - Ya tenía una lógica de clasificación de riesgos y reintentos; esta clasificación de razones se replica en anuncios (adaptada a sync).

## 9) Compatibilidad multi-worker
- [scraper_anuncios.py]
  - Estado por worker `anuncios_state_worker_{id}.json`.
  - Reparto FIFO secuencial de IDs pendiente.
- [scraper_links_async.py]
  - Arquitectura async; mantiene round-robin y persistencia inmediata.

## 10) Consideraciones futuras
- [Ambos]
  - Unificación de logs/formatos entre scrapers.
  - Filtro “A/B” con query param inocuo en `web_anuncio` si persisten ciertos 403.
  - Limpieza de lints (long lines/whitespace) cuando estabilice la funcionalidad.
