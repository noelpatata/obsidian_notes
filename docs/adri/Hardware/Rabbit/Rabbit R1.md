
> [!note] 
> **Estado:** Documentado y funcional a marzo 2026  
> **Chip:** Mediatek MT6765 (Helio P35)  
> **OS base:** Android 13 AOSP (modo kiosko)  
> **Objetivo:** Backup → Token API → Bootloader → Ubuntu Touch

## 📋 Índice

- [[#Arquitectura real del R1]]
- [[#Lo que necesitas antes de empezar]]
- [[#Paso 1 — Backup completo con MTKClient]]
- [[#Paso 2 — Extraer tu Account Key (Carroot)]]
- [[#Paso 3 — Desbloquear el bootloader (r1_escape)]]
- [[#Paso 4 — Instalar Ubuntu Touch]]
- [[#Paso 5 — Usar la API con tu token]]
- [[#Recursos y comunidades]]
- [[#Preguntas frecuentes]]

---

## Arquitectura real del R1

### ¿Qué es rabbitOS por dentro?

RabbitOS es una **kiosk app** corriendo sobre Android 13 AOSP. Esto significa:

| Característica      | Detalle                                                       |
| ------------------- | ------------------------------------------------------------- |
| OS base             | Android 13 AOSP                                               |
| App principal       | `tech.rabbit.r1launcher.r1`                                   |
| Usuario del sistema | `u0_a66` (usuario normal, sin root)                           |
| Modo de ejecución   | Kiosk mode (sin barra de navegación, sin salida a otras apps) |
| IA local            | **Ninguna** — todo va a servidores de Rabbit en la nube       |
| Comunicación        | WebSocket + JSON sobre HTTPS                                  |

> [!note] **Conclusión:** 
>  RabbitOS no tiene acceso root. Es un bonito frontend que llama a una API remota. Python corre como usuario Android estándar.

### Hardware

| Componente      | Especificación                  |
| --------------- | ------------------------------- |
| Chip            | Mediatek MT6765 (Helio P35)     |
| RAM             | 4GB                             |
| Almacenamiento  | 128GB                           |
| Botones físicos | Solo PTT (Push-to-Talk) lateral |
| Conectividad    | USB-C, WiFi, 4G                 |

### ¿Por qué el MT6765 es importante?

El MT6765 tiene una **vulnerabilidad en el bootrom** descubierta en 2019. El bootrom es memoria de solo lectura grabada en silicio en fábrica. Ningún OTA puede parchearla. Esto significa que:

- Aunque Rabbit actualice el firmware, el exploit sigue funcionando
- No necesitas permiso de Rabbit para usar este método
- Funciona en **cualquier versión de firmware**, incluyendo la última

---

## Lo que necesitas antes de empezar

### Software en tu PC

- [ ] Python 3.11.6 (versión específica recomendada)
- [ ] Git
- [ ] Chrome o Chromium (para Carroot)
- [ ] Drivers MediaTek Preloader USB VCOM
- [ ] Drivers ADB/Fastboot de Google

### Repos que necesitarás

```
https://github.com/bkerler/mtkclient
https://github.com/RabbitHoleEscapeR1/r1_escape
https://devices.ubuntu-touch.io/device/r1/
https://gist.github.com/DavidBuchanan314/aafce6ba7fc49b19206bd2ad357e47fa
```

### Herramientas online

```
https://retr0.id/stuff/r1_jailbreak/   ← Carroot (jailbreak sin modificar)
https://rabbitmods.net                  ← Wiki de flashing
```


> [!tip] ⚠️ **Importante:**
>  Haz siempre el backup ANTES de cualquier modificación. Sin backup no hay vuelta atrás.

---

## Paso 1 — Backup completo con MTKClient

> **Objetivo:** Guardar todo el firmware original antes de tocar nada.  
> **Modifica el dispositivo:** ❌ No  
> **Necesita dev mode:** ❌ No  
> **Funciona con firmware actualizado:** ✅ Sí

### Por qué funciona sin modo desarrollador

MTKClient no usa ADB. Se comunica directamente con el **bootrom del chip** antes de que Android arranque. El dispositivo no necesita estar encendido.

### Proceso

```bash
# 1. Clonar el repo
git clone https://github.com/bkerler/mtkclient
cd mtkclient

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Apagar el R1 completamente

# 4. Conectar USB al PC
# En este punto MTKClient detectará el chip en modo Preloader

# 5. Hacer el backup completo
python mtk rf backup_all.bin
```

### Qué hace el script internamente

Como el R1 no tiene botones de volumen, no puedes entrar en modo BROM manualmente. MTKClient usa `mtkbootcmd.py` para **enviar el comando FASTBOOT directamente via el puerto serie del preloader**, forzando el modo BROM por software. No necesitas ningún botón.

### Resultado esperado

Un archivo `backup_all.bin` con todo el firmware original. Guárdalo en un lugar seguro. Con este archivo puedes volver al estado inicial en cualquier momento.

---

## Paso 2 — Extraer tu Account Key (Carroot)

> **Objetivo:** Obtener tu `accountKey` para usar la API de Rabbit.  
> **Modifica el dispositivo:** ❌ No (jailbreak tethered, no persistente)  
> **Necesita dev mode:** ❌ No  
> **Necesita bootloader desbloqueado:** ❌ No

### ¿Qué es el accountKey?

Es tu token de autenticación personal con el backend de Rabbit. Está almacenado en **texto plano** en los logs internos del dispositivo. Es tuyo, en tu dispositivo, y no cambia a menos que resetees el R1 a fábrica.

Formato en la API:

```
"token": "rabbit-account-key+" + ACCOUNT_KEY
```

### Proceso con Carroot

1. Abre **Chrome o Chromium** en tu PC
2. Ve a `retr0.id/stuff/r1_jailbreak/`
3. Conecta el R1 por USB
4. Sigue las instrucciones en pantalla
5. Carroot te abrirá una shell con acceso root temporal
6. Busca tu accountKey:

```bash
# Opción 1 — buscar en logs
grep -r "accountKey" /data/data/tech.rabbit.r1launcher.r1/

# Opción 2 — buscar en archivos de la app
find /data/data/tech.rabbit.r1launcher.r1/ -name "*.json" -exec grep -l "accountKey" {} \;

# Opción 3 — buscar en todos los logs
grep -r "rabbit-account-key" /data/data/tech.rabbit.r1launcher.r1/files/logs/
```

7. **Anota el valor** en un lugar seguro

### ¿Por qué funciona Carroot sin modificar nada?

Carroot es un jailbreak **tethered**, lo que significa que solo funciona mientras el dispositivo está conectado por USB y no hace cambios permanentes. Cuando desconectas el R1, vuelve al estado normal.

---

## Paso 3 — Desbloquear el bootloader (r1_escape)

> **Objetivo:** Desbloquear el bootloader para poder flashear ROMs alternativas.  
> **Modifica el dispositivo:** ✅ Sí (permanente)  
> **Necesita dev mode de Rabbit:** ❌ No  
> **Funciona con firmware actualizado:** ✅ Sí

### Proceso

```powershell
# 1. Descargar el repo
git clone https://github.com/RabbitHoleEscapeR1/r1_escape
cd r1_escape

# 2. Descargar system.img.xz desde las releases del repo
# y extraerlo en la misma carpeta

# 3. Ejecutar el script como administrador en PowerShell
.\r1.ps1

# 4. Conectar el R1 cuando el script lo indique
# El script automáticamente:
#   - Detecta el dispositivo en modo Preloader
#   - Lo lleva a modo BROM
#   - Desbloquea el bootloader
#   - Flashea la imagen del sistema
```

### ¿Qué pasa con mis datos?

El proceso de desbloqueo normalmente **borra el dispositivo** (factory reset). Por eso el paso 2 (extraer accountKey) va antes que este paso.

### Vía oficial alternativa (si prefieres)

Si no quieres usar MTKClient puedes pedir a Rabbit el modo desarrollador oficial:

1. Contacta a soporte de Rabbit
2. Solicita activación de modo desarrollador
3. En 1-2 días aparece en tu Rabbit Hole: _"Developer allow R1 bootloader to be unlocked"_

> El CEO de Rabbit anunció oficialmente soporte para desbloqueo de bootloader con herramienta oficial de flashing.

---

## Paso 4 — Instalar Ubuntu Touch

> **Objetivo:** Instalar Ubuntu Touch como OS principal.  
> **Necesita bootloader desbloqueado:** ✅ Sí  
> **Soporte oficial UBports:** ✅ Sí (desde OTA-10, septiembre 2025)

### Estado del port

Ubuntu Touch OTA-10 añadió soporte **oficial** para el Rabbit R1. No es un port experimental. Está en el canal estable de UBports.

### Proceso con UBports Installer

1. Descarga **UBports Installer** desde `devices.ubuntu-touch.io`
2. Abre el installer
 
3. Conecta el R1 con el bootloader ya desbloqueado
4. El installer flashea todo automáticamente

### Recursos específicos del port

```
https://devices.ubuntu-touch.io/device/r1/
https://github.com/MinatiScape/ubtouch-on-r1
```

### ¿Puedo volver a rabbitOS?

Sí. Con el backup del Paso 1 puedes volver al estado original en cualquier momento usando MTKClient para restaurar el backup.

---

## Paso 5 — Usar la API con tu token

> **Objetivo:** Conectarse al backend de Rabbit desde cualquier dispositivo usando tu accountKey.

### La API documentada por David Buchanan

La comunicación es **WebSocket + JSON**. El token va así:

```python
import websocket
import json

ACCOUNT_KEY = "tu-account-key-aqui"

ws = websocket.WebSocket()
ws.connect("wss://api.rabbit.tech/ws")  # endpoint aproximado

auth_message = {
    "token": "rabbit-account-key+" + ACCOUNT_KEY
}

ws.send(json.dumps(auth_message))
```

### El problema del fingerprint JA3

El servidor de Rabbit verifica el **fingerprint JA3** del cliente TLS. Esto significa que si te conectas desde un script Python normal, el servidor puede rechazarte porque el fingerprint no coincide con el del R1 real.

La comunidad de **Rabbitude** en Discord tiene implementaciones Python que ya resuelven este problema replicando el fingerprint correcto.

### Recursos para la API

```
Gist de Buchanan:
https://gist.github.com/DavidBuchanan314/aafce6ba7fc49b19206bd2ad357e47fa

Reimplementación open source del backend:
https://github.com/nicholasgasior/rabbitude-backend
```

---

## Recursos y comunidades

### Repositorios clave

|Repo|Descripción|
|---|---|
|`bkerler/mtkclient`|Herramienta principal para chips MTK|
|`RabbitHoleEscapeR1/r1_escape`|Scripts de desbloqueo de bootloader|
|`MinatiScape/ubtouch-on-r1`|Port de Ubuntu Touch|
|`TurboTheTurtle/rabbit-r1-firmware`|Guías para CipherOS y restore stock|

### Webs útiles

|URL|Descripción|
|---|---|
|`retr0.id/stuff/r1_jailbreak/`|Carroot — jailbreak tethered sin modificar|
|`devices.ubuntu-touch.io/device/r1/`|Página oficial R1 en UBports|
|`rabbitmods.net`|Wiki completa de flashing|
|`da.vidbuchanan.co.uk/blog/r1-jailbreak.html`|Blog técnico de Buchanan|

### Comunidades

- **Discord de Rabbitude** — la comunidad más activa, tienen implementaciones Python de la API
- **XDA Forums** — busca "Rabbit R1 bootloader unlock tutorial"
- **Foro UBports** — soporte para Ubuntu Touch en el R1

---

## Preguntas frecuentes

### ¿Funciona con la última versión del firmware?

✅ Sí. El exploit MTK está en el bootrom (silicio), ningún OTA puede parcharlo.

### ¿Necesito permiso de Rabbit para desbloquear el bootloader?

❌ No, si usas MTKClient/r1_escape. ✅ Solo si quieres usar la vía oficial de Rabbit.

### ¿El R1 tiene acceso root en stock?

❌ No. La app corre como `u0_a66`, usuario Android estándar sin privilegios.

### ¿Python en el R1 puede ejecutar cosas a nivel root?

❌ No en stock. Con Magisk instalado: ✅ sí.

### ¿Puedo volver a rabbitOS después de instalar Ubuntu Touch?

✅ Sí, con el backup del Paso 1.

### ¿El R1 tiene botones de volumen para entrar en BROM?

❌ No. Solo tiene el botón PTT. MTKClient resuelve esto por software con `mtkbootcmd.py`.

---

_Guía generada en marzo 2026 — verifica siempre los repos originales para cambios recientes_