# `checklist_WAF.md` WAF

---
## OBJETIVO del DSD:

  **Objetivo final**: Guiar a un asistente de IA, tras `solicitud` del usuario, en la creación de un DSD que contenga un Estatus de Detección, Estatus de Anti-detección, un Ranking de Hipótesis de detección y una serie de propuestas de mejora en base a todo el análisis realizado.

  **Consideraciones técnicas**:
    (1) El `checklist_WAF.md` aspira a ser un listado _completo_ que cubra el 100% de los aspectos a tener en cuenta con independencia de la técnica que usemos (requests , otros clientes HTTP o headless browser).
    (2) Algunos puntos del `checklist_WAF.md` pueden estar fuera del alcance del código en si mismo (Ej: calidad de los proxies) pero pueden ser igualmente cruciales.

---

## `checklist_WAF.md` WAF

(A evaluar por orden de importancia si utilizamos headless browser):

  **A. Monitorización de navegacion y detección Inicial**
    -01- Ejecutar el código en modo headful primero para detectar desafíos JS, CAPTCHAs o mensajes de detección y generar y almacenar cookies.
    -02- Configurar alertas automáticas en el código para detectar blocks, CAPTCHAs o rate limits o similar.
    -03- Monitorizar latencia al conectarnos con web target para asegurar que no supera umbrales de detección (típicamente >500ms es sospechoso).
    -04- Implementar logging de respuestas HTTP para detectar códigos de estado sospechosos (429, 403, 503) y tiempos de respuesta.
    -05- Implementar manejo de errores de proxy con fallback automático a proxies alternativos usando try-except blocks.

  **B. Proxies** - Este bloque lo cumplimos con Oxylabs (confirmado).
    -06- Usar exclusivamente proxies residenciales o mobile que sean anonymous/elite y verificar que no estén en blacklists.
    -07- Implementar rotación automática de IPs con pools de al menos 10-20 proxies para evitar patrones detectables.
    -08- Verificar que los proxies no filtren información en headers HTTP_VIA, HTTP_X_FORWARDED_FOR o REMOTE_ADDR.
    -09- Validar que los proxies soporten HTTP/2 y TLS 1.3 para evitar downgrade attacks.

  **C. Headless Browser Stealth (Solo para navegadores sin cabeza o headless)**
    -10- Aplicar stealth mode completo ocultando navigator.webdriver y otras propiedades de automatización.
    -11- Patchear más de 200 browser leaks usando bibliotecas como puppeteer-stealth o playwright-stealth.
    -12- Configurar viewport y resolución realistas que coincidan con dispositivos comunes.
    -13- Simular eventos de hardware (batería, memoria, CPU cores) con valores consistentes.

  **E. Gestión de Sesiones y Cookies**
    -14- Utilizar objetos de sesión persistentes que almacenen y envíen cookies de forma automática y realista.
    -15- Implementar cookie persistence entre sesiones para mantener autenticación y preferencias.
    -16- Generar y mantener cookies de sesión coherentes que simulen comportamiento de usuario real.

  **F. Rate Limiting y Control de Tráfico**
    -17- Evitar superar rate limits en múltiples intervalos: por segundo (max 1-2 req/s), minuto (max 60 req/min), hora y día.
    -18- Implementar backoff exponencial cuando se detecten signos de throttling (aumentar delays progresivamente).
    -19- Distribuir requests usando task queues (como Celery) para control granular de rate limiting.

  **G. Navegación y Comportamiento Humano**
    -20- Utilizar patrones de navegación “humanos”: navegación desde la home hasta la web target por una vía existente en GUI browser.
    -21- Implementar tiempos “humanos” con variación estocástica: think time (2-7s), scroll time (1-3s) y jitter variables en milisegundos.
    -22- Simular movimientos de mouse realistas y patrones de click con variación natural en coordenadas.
    -23- Implementar patrones de scroll orgánicos con aceleración/desaceleración natural y paradas aleatorias.

  **H. Fingerprinting y Headers**
    -24- Enviar fingerprint completamente realista mediante spoofing de headers críticos: User-Agent, Accept-Language, Accept-Encoding, Referer.
    -25- Implementar TLS fingerprinting evasion usando bibliotecas como curl-impersonate o TLS-Proxy para emular navegadores reales.
    -26- Aplicar HTTP/2 fingerprinting bypass configurando correctamente SETTINGS frames, WINDOW_UPDATE y stream priorities.
    -27- Evitar canvas y WebGL fingerprinting mediante spoofing de APIs gráficas con valores consistentes por sesión.
    -28- Rotar User-Agents de manera inteligente manteniendo consistencia con otros headers (OS, browser version).

  **I. Evasión de Trampas y Detección Avanzada**
    -29- Implementar detección y evitar honeypot traps analizando elementos ocultos (display:none, position:absolute left:-9999px).
    -30- Evitar interactuar con elementos fuera del viewport o con dimensiones zero.
    -31- Implementar detección de datos falsos comparando precios/datos servidos vs. valores esperados.

  **J. JavaScript Challenges y CAPTCHA**
    -32- Preparar solución para JavaScript challenges (Cloudflare, etc.) usando headless browsers con capacidades JS completas.
    -33- Integrar servicios de solución de CAPTCHA (CapSolver, 2captcha) para automatizar resolución.
    -34- Implementar detección automática de challenges JS y CAPTCHAs para triggear soluciones apropiadas.

  **K. Detección de Patrones de Comportamiento**
    -35- Evitar patrones de timing perfectos introduciendo variabilidad natural en todas las acciones.
    -36- Implementar simulación de errores humanos (clicks fallidos ocasionales, retrocesos).
    -37- Variar rutas de navegación para evitar patrones repetitivos detectables.

  **L. Monitorización y Alertas**
    -38- Configurar alertas automáticas para detectación de blocks, CAPTCHAs o rate limits.
    -39- Implementar métricas de éxito (success rate, response times, error patterns) para monitorización continua.
    -40- Mantener logs detallados de todas las interacciones para análisis post-mortem en caso de detección.

  **M. Técnicas Avanzadas de Evasión**
    -41- Considerar bypass de CDN enviando requests directamente a servidores origen cuando sea posible.
    -42- Implementar request chaining navegando a través de múltiples páginas antes de alcanzar el target.
    -43- Usar browser contexts separados para diferentes tareas y evitar contaminación de sesión.
    -44- Desarrollar scripts automáticos para validar el cumplimiento técnico de los puntos más críticos del `checklist_WAF.md`, comprobando headers, cookies y fingerprints en tiempo real.
    -45- Realizar pruebas regulares contra diferentes tipos de WAF (AWS, Cloudflare, Akamai, etc.) y variantes modernas para evitar sesgos en la evasión.
    -46- Implementar un sistema formal para reportar falsos positivos/negativos, facilitando un loop de feedback continuo y mejora persistente.
    -47- Definir métricas cuantitativas mínimas aceptables de efectividad (ej: success rate, ratio de error por tipo de WAF).
    -48- Documentar incidentes y escenarios de fallo habituales y soluciones basadas en experiencia previa.

  **N. Auto‑restart de sesión y concurrencia segura — Añadido 2025‑08‑27**
    -49- Auto‑restart loop: ante riesgo WAF alto (p.ej., 429/403 repetidos, CAPTCHA persistente), setear flag `NEED_RESTART` y reiniciar el ciclo.
    -50- Regeneración de sesión: crear nuevo `user_data_dir` por sesión y una nueva `sessid` de Oxylabs antes de reintentar.
    -51- Estado de almacenamiento: guardar/restaurar storage state (cookies, localStorage) dentro del directorio de sesión para continuidad controlada.
    -52- Backoff: aplicar backoff exponencial y jitter (p.ej., 5s, 15s, 45s…) antes de reintentar tras detección.
    -53- Límites de concurrencia: mantener bajo el número de páginas simultáneas; empezar con 1–2 y aumentar gradualmente según métricas sin disparar detección.
    -54- Paralelismo por fases: permitir asincronía en recolección de IDs; en scraping de `web_anuncio`, preferir pipeline en serie o lotes pequeños espaciados.
    -55- Rotación coordinada: al reiniciar, rotar también UA fingerprint y proxy; evitar reusar combinación previa inmediatamente.
    -56- Observabilidad: loggear motivo del restart, IDs afectados y nueva identidad (hash anonimizado) para análisis posterior.

## Consideraciones generales:
  **1. Machine Learning Detection**: Los sistemas anti-bot modernos usan ML, por lo que la variabilidad es crucial en todos los aspectos.
  **2. Behavioral Analysis**: Los patrones de comportamiento son tan importantes como los aspectos técnicos.
  **3. Evolución Constante**: Este `checklist_WAF.md` debe actualizarse cada 3-6 meses según evolucionen las técnicas de detección.
  **4. Testing Continuo**: Implementar tests regulares contra diferentes tipos de WAF para validar efectividad.


Este `checklist_WAF.md` [revisado con validaciones automatizadas, métricas formales y ciclo de feedback documentado] proporciona cobertura completa y sistemática de las técnicas anti-detección más actuales, [incluyendo mejores prácticas de testing y reporting moderno en el sector (2024-2025)]

## Audiencia Objetivo:
Asumir que el lector principal del FSD es un **analista de datos junior**: El resultado del FSD debe ser claro, accionable y entendible.
