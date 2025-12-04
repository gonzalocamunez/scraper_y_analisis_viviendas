# Nuevos Desarrollos y Modificaciones Sustanciales

Fecha: 2025-09-10

## 1) Nuevos desarrollos (Están en el código actualmente pero no están documentados en la documentación inicial: `project_description.md`, `navegacion_y_selectores.md`, `stealth_config.md`, `proxies.md`)

- Escritor a Excel en `scraper_links.py`:
  - Función `write_links_to_excel(ids)` que crea/actualiza `scraper.xlsx` (hoja `links`) con columnas: `id_anuncio`, `url_anuncio`, `ts_insert`.
  - Se invoca al finalizar cada pasada de extracción para volcar solo los nuevos IDs.

- Estado stealth ampliado en `state/links_state.json`:
  - Campos añadidos: `session_id`, `last_rotate_ts`, `consecutive_200`, `last_waf_high`, `estado`, `modo`.
  - Lógica de recuperación automática tras `C200_RECOVERY_THRESHOLD` códigos 200.

- Rotación programática de identidad (IP + fingerprint):
  - `ensure_session_id()` y `rotate_session_id()` generan `sessid` de 10 dígitos y lo persisten en estado.
  - `seed=session_id` al crear el navegador para alinear fingerprint con la IP.

- Backoff adaptativo por modo (normal/segura/warm_up):
  - `navigate_and_stabilize()` aplica tiempos de espera y jitter distintos según el modo.

- Gate de cookies en detección:
  - Si `last_waf_high=True`, no se inyectan cookies previamente guardadas hasta recuperar normalidad.

- "Feed" de proxies (preparado en `.env`):
  - Variables `OXYLABS_SESSID_1..5` con los 5 `sessid` reales para habilitar un pool de 5 instancias (implementación próxima).

- Pool multi-worker (5 instancias) en `scraper_links.py`:
  - Implementado con `multiprocessing.Pool`, un worker por `OXYLABS_SESSID_i`.
  - Reparto de páginas por bloques contiguos: cada worker recibe un `start_page` distinto y procesa `PAGES_PER_WORKER` páginas.
  - Deduplicación y escritura a Excel consolidada desde el proceso padre.
  - Si `PAGES_PER_WORKER <= 0` → reparto `round-robin` ilimitado: `step_size = workers`, `start_page = i+1`.
  - Watchdog anti-bloqueo configurable: `STALL_TIMEOUT_SEC` (por defecto 180s) para detener un worker si no hay progreso.

- Reportes (consola y resumen de ejecución):
  - Consola opcional con `rich` mediante variables en `.env`:
    - `PROGRESS=1` para progreso por worker (`[PROGRESS] [W#] ...`).
    - `SHOW_NAV=1` para navegación (`[NAV] tag url status=...`).
    - `SHOW_SYS=1` para mensajes del sistema/ritmo (`[SYS] ...`).
    - `SHOW_WAF=1` para eventos de detección WAF (`[WAF] ...`).
  - Resumen de ejecución en `state/report_links.json` con: número de workers, `pages_per_worker`, páginas iniciales de cada worker, nuevos por worker, total de nuevos y total acumulado en `known`.

## 2) Modificaciones sustanciales (implementaciones que existían en la documentación inicial que han sufrido modificaciones relevantes que no están documentadas en la documentación inicial: `project_description.md`, `navegacion_y_selectores.md`, `stealth_config.md`, `proxies.md`)

- `camoufox_config.py`:
  - `get_proxy(session_id, country)` ahora:
    - Usa `HTTPS` (`server=https://pr.oxylabs.io:7777`).
    - Normaliza `country` a minúsculas (`cc-es`).
    - Por defecto `OXYLABS_SESSION_TIME=30` si no se define.
    - Genera `session_id` de 10 dígitos si no se pasa (ni está en `.env`).
  - `build_camoufox_config()` y `create_browser()` aceptan `session_id` y `country`; los presets por modo (`eficiente`, `segura`, `warm_up`) están centralizados.

- `.env.example`:
  - `OXYLABS_SESSION_TIME=30` (antes 60) y añadidos placeholders `OXYLABS_SESSID_1..5` para el pool de proxies.

- `scraper_links.py`:
  - Añadidas llamadas a `seed=session_id` en `create_browser()`.
  - Añadido `write_links_to_excel()` y su invocación.
  - Rotación periódica en modo normal (120s) y rotación forzada en detección.
  - Clasificación de riesgo por códigos HTTP y backoff por modo.
  - Pool multi-worker con reparto por bloques, progreso opcional y resumen de ejecución.
  - Modo ilimitado `round-robin` cuando `PAGES_PER_WORKER<=0` y watchdog de estancamiento.

- `knowledge/project_description.md`:
  - Añadida sección de “Archivos Relevantes”.

- `.env.example`:
  - Añadidas variables de reporting: `PROGRESS`, `SHOW_NAV`, `SHOW_SYS`, `SHOW_WAF` y `PAGES_PER_WORKER`.

## 3) Sistema de Recuperación Post-Detección WAF

### Descripción
Sistema avanzado de recuperación tras detección WAF que ejecuta medidas adicionales después de la rotación forzada para "normalizar" la nueva identidad ante el WAF sin cambiar la navegación básica.

### Funcionalidades Implementadas

#### Re-warm-up Automático
- **Activación**: Tras `force_full_rotation()` se marca `needs_rewarmup = True`
- **Secuencia**: HOME → MAPA → LISTADO (igual que warm-up inicial)
- **Cookies frescas**: Genera y guarda nuevas cookies con la nueva identidad
- **Logging**: `[RE-WARMUP]` tags para seguimiento

#### Actividad Humana Simulada
- **Páginas inocuas**: /ayuda/, /contacto/, HOME
- **Navegación**: 1-2 páginas aleatorias con scroll ligero
- **Dwell time**: 1-2 segundos por página simulando lectura
- **Objetivo**: Simular "usuario confundido que explora" tras error

#### Parámetros URL Post-Detección
- **Activación**: `build_web_anuncio_url(post_detection=True)`
- **Parámetros especiales**: `?utm_source=web&ref=direct`, `?source=bookmark`
- **Objetivo**: Romper patrones de navegación detectados por WAF

#### Flujo de Recuperación
1. **Detección WAF** → `force_full_rotation()` + `needs_rewarmup = True`
2. **Verificación** → Si `needs_rewarmup`, ejecutar recuperación
3. **Re-warm-up** → Secuencia HOME→MAPA→LISTADO con nueva identidad
4. **Actividad humana** → Navegación inocua con scroll y pausas
5. **Reinyección** → Cookies frescas alineadas con nueva sesión
6. **Reintento** → Continuar con el anuncio que falló
7. **Limpieza** → `needs_rewarmup = False` si exitoso

### Aplicabilidad
- **Scraper de anuncios**: ✅ Implementado completamente
- **Scraper de links**: ⚠️ Adaptable (requiere integración)
- **Stealth config**: ✅ Compatible con modos existentes

Notas:
- Pool de 5 instancias implementado (con reparto por bloques contiguos).
- Pendiente aplicar jitter ±25% en la rotación periódica durante `modo_detección` (rotation_normal*).
