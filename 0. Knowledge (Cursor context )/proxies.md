# Proxies: Guía de uso de proxies Oxylabs.

## (0) OBJETIVOS E ÍNDICE:

### Objetivo del uso de proxies: 
Evitar la detección por parte del WAF de cualquier web, especialmente la web objetivo del proyecto (*********).

### Objetivo de este documento: 
Ofrecer a la IA una guía completa de como utilizar proxies durante el proyecto de scraping de ********* para evitar la detección del WAF.

### Consideraciones técnicas:
   1) SIEMPRE que interaccionemos con una web externa (*********) debemos utilizar proxies.
   2) Sticky session en proxies residenciales con duración de 2 minutos.
   3) Utilizaremos SOLO proxies del protocolo HTTPS.
   4) Para el control de sesión utilizaremos el parámetro `sessid` y `sesstime`.
      4.1) Es clave que `sesstime` sea MÁS LARGO que el tiempo de rotación que queremos aplicar en el script.
      4.2) Cambiando `sessid` el gateway asigna una IP NUEVA inmediatamente y logramos rotar la IP.
         EJEMPLO: Si queremos rotar la IP cada 2 minutos, debemos poner `sesstime-20` (cualquiera mayor que 2 minutos) y a los 2 minutos cambiar de `sessid` para obligar al gateway a asignar una IP NUEVA.
      4.3) Con la rotación de IP tiene que venir una rotación COHERENTE del resto del fingerprint
      4.4) Esta rotación se definirá en detalle en `rotacion_y_detencion.md`.

### Índice:
   1) `ACCESO A LOS PROXIES`
   2) `ROTACIÓN DE IP` y `CONTROL DE SESIÓN`
   3) `CONSUMO` DE DATOS Y `COSTE`:


## (1) `ACCESO A LOS PROXIES`:

**Credenciales**:
   - Número de proxies: 5 proxies (5 endpoints SIMULTÁNEOS)
   - Tipo de proxies: Residential Proxies 
   - Protocolo: HTTPS
   - Country entry (Country = Spain, City = Any)
   - Sticky session (10 minutes)
   - user = gcbmasd_residencial_xD9F5
   - password = HMn6dUTg_WmC6tL

**Endpoints del proxy 1 al 5**:
```
Endpoint 1 = https://customer-gcbmasd_residencial_xD9F5-cc-es-sessid-0674154480-sesstime-20:HMn6dUTg_WmC6tL@pr.oxylabs.io:7777
Endpoint 2 = https://customer-gcbmasd_residencial_xD9F5-cc-es-sessid-0674154481-sesstime-20:HMn6dUTg_WmC6tL@pr.oxylabs.io:7777
Endpoint 3 = https://customer-gcbmasd_residencial_xD9F5-cc-es-sessid-0674154482-sesstime-20:HMn6dUTg_WmC6tL@pr.oxylabs.io:7777
Endpoint 4 = https://customer-gcbmasd_residencial_xD9F5-cc-es-sessid-0674154483-sesstime-20:HMn6dUTg_WmC6tL@pr.oxylabs.io:7777
Endpoint 5 = https://customer-gcbmasd_residencial_xD9F5-cc-es-sessid-0674154484-sesstime-20:HMn6dUTg_WmC6tL@pr.oxylabs.io:7777
```

## (3) `ROTACIÓN DE IP` y `CONTROL DE SESIÓN`:

  ### Política de `ROTACIÓN DE IP` de Oxylabs:
   - Esta es la política de rotación de IP de Oxylabs por defeto, no obstante nosotros no seguiremos esta política ya que rotaremos manualmente modificando `sessid` como veremos a continuación en `CONTROL DE SESIÓN`.

    #### Sticky session: 
      - El gateway mantiene la misma dirección IP desde 1 hasta 30 minutos:
         - Si no tocamos `sessid`, el gateway mantiene la IP durante los minutos configurados (10 por defecto) salvo que el proxy se caiga por algún motivo.
         - Si modificamos `sessid`, el gateway asigna una IP NUEVA inmediatamente.

      Cuando la sesión expira (se agota el tiempo configurado en `sesstime`) o el proxy se cae, el sistema asigna automáticamente una **nueva dirección IP AL MISMO sessid**. Esto es importante porque si no rotamos en ese momento el resto del fingerprint nos delatamos al WAF.

      Por este motivo, **ES CLAVE DEFINIR UN `sesstime` más largo que el tiempo de rotación que definamos en nuestro scraper** de manera que controlemos el momento de la rotación y la hagamos de forma coordinada (IP + resto del fingerprint)

    #### Rotating session: 
      - El gateway cambia a una nueva IP con cada petición.

  ### `CONTROL DE SESIÓN`en nuestro scraper:

   El parámetro `sessid` (ID de sesión) te permite mantener la misma dirección IP para ejecutar múltiples solicitudes. Para reutilizar la misma IP varias veces, hay que configurar los proxies como sticky session y mantener el mismo sessid.

   En el endpoint, sessid se encuentra a continuación del literal `sessid-` y se corresponde con una cadena alfanumérica de 10 dígitos creada aleatoriamente, por ejemplo, sessid-abcde12345.

   En el endpoint, el parámetro `sesstime` (Tiempo de sesión) te permite definir la duración de la sesión en minutos. En el endpoint, sesstime se encuentra a continuación del literal `sesstime-` y se corresponde con una cadena numérica de 2 dígitos que define la duración de la sesión en minutos.

   #### Ejemplo (`Endpoint 5`):

   **endpoint value (incl. sessid y sesstime)**:
   ```
   Endpoint 5 = https://customer-gcbmasd_residencial_xD9F5-cc-es-sessid-0792340091-sesstime-30:HMn6dUTg_WmC6tL@pr.oxylabs.io:7777
   ```
   **sessid & sesstime values**:
   ```
   sessid = 0792340091
   sesstime = 30
   ```

## (3) `CONSUMO` DE DATOS Y `COSTE`:

10 euros por cada 1 GB descargado usando los proxies y con derecho a acceder a 5 endpoints SIMULTÁNEOS.


