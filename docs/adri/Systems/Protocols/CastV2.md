## **Protocolo CastV2**

**CastV2** es el **protocolo de comunicación utilizado por dispositivos con Chromecast integrado**, como televisores TCL, Google Chromecast, Google Home, y apps compatibles.

Su propósito principal es **permitir que un dispositivo emisor (móvil, PC, servidor) controle y envíe contenido a un receptor (TV o altavoz)** de manera segura y estandarizada.

## **Características principales**

#### 1. **Arquitectura cliente-servidor**

- El **emisor** (app móvil, navegador o servidor) inicia la conexión.	
- El **receptor** (TV o Chromecast) escucha en el **puerto 8009** (por lo general) y responde a comandos.
#### 2. **Protocolo basado en WebSockets**    

- La comunicación es **binaria**, no texto plano.
- Se transmite mediante **mensajes codificados en protobuf** (Google Protocol Buffers), que definen tipos de comandos y estados.

#### 3. **Seguridad**    

- Usa **TLS** para cifrar la conexión.
- La sesión se identifica mediante un **UUID**, y los mensajes incluyen autenticación y control de sesiones.

#### 4. **Canales (namespaces)**

- **Receiver**: control de la TV, estado, volumen.
- **Media**: reproducción de audio/video.
- **YouTube**: comandos específicos de YouTube.
- **Custom**: apps personalizadas pueden definir su propio namespace para enviar/recibir datos.        
#### 5.  **Comandos Permitidos por Google Cast (CASTv2)**

##### **Conectar y obtener estado** :
- **CONNECT** → establece la sesión Cast
- **GET_STATUS** → pide el estado actual del receptor (volumen, app activa, etc.)
- **PING / PONG** → mantener viva la conexión

##### **Control del Receptor (la TV)** :

*Son comandos al _receiver_, es decir, al sistema Cast de la TV.*

>[!note] Ejemplos de **appId**:
> - YouTube → `YouTube`
>     
> - Netflix → `Netflix`
>     
> - Spotify → `CC32E753`
>     
> - Default Media Receiver → `CC1AD845`

**Lanzar una app Cast** : 
- `LAUNCH <appId>`

**Detener una app** : 
- `STOP <sessionId>`

**Cambiar volumen del televisor** : 
- `SET_VOLUME level=<0.0-1.0>   SET_VOLUME muted=true|false`

#####  **Control de reproducción (solo dentro de apps Cast)**

*Estos comandos se envían al _media channel_ después de lanzar una app.*

Obtener información del contenido: 
 - GET_STATUS
Reproducir contenido:
- LOAD < mediaObject >

> [!tip] 
> (mediaObject incluye URL, tipo MIME, título, etc.)

 Comandos de control multimedia <tiempo_en_segundos>
- PLAY 
- PAUSE
- STOP 
- SEEK 

##### **Mensajes personalizados (Custom Channels)**

Solo si la app de Cast lo soporta:
- SEND_MESSAGE namespace="<tu_namespace>" data="< JSON >" 
