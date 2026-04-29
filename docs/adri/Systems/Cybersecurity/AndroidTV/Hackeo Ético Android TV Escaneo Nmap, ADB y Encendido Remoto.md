
**Herramientas:** `nmap`, `adb`, `wakeonlan`, `curl`, `pychromecast`  
**Objetivo:** Entender puertos abiertos, riesgos y cómo encender el TV remotamente.

---

## 1. Resultado del Escaneo Nmap (`nmap -sV --script=vuln`)

```text
PORT     STATE SERVICE         VERSION
8008/tcp open  http?
|_http-csrf: Couldn't find any CSRF vulnerabilities.
|_http-dombased-xss: Couldn't find any DOM based XSS.
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
8009/tcp open  ssl/castv2      Ninja Sphere Chromecast driver
8443/tcp open  ssl/https-alt?
|_http-aspnet-debug: ERROR: Script execution failed
|_http-vuln-cve2014-3704: ERROR: Script execution failed
9000/tcp open  ssl/cslistener?
```

### Interpretación:
| Puerto | Servicio          | ¿Vulnerable? | Notas                                 |
| ------ | ----------------- | ------------ | ------------------------------------- |
| 8008   | HTTP              | No           | Panel web (quizás admin). No XSS/CSRF |
| 8009   | Cast (Chromecast) | No           | Protocolo de transmisión. Normal      |
| 8443   | HTTPS             | No           | Panel alternativo. No .NET            |
| 9000   | ADB SSL?          | Depende      | Puede ser ADB cifrado                 |

> **Nmap NO encontró CVEs conocidos** → Pero **NO significa que sea seguro**.

---

## 2. Confirmación: Puerto **5037** = ADB Clásico (SIN SSL)

```bash
nmap -p 5037 --script=adb-server-version <IP>
```
Salida esperada:
```text
5037/tcp open  adb  Android Debug Bridge version 1.0.41
```

**¡ADB está EXPUESTO y SIN CIFRADO!**  
Cualquiera en la red puede:
- Tomar control total
- Instalar apps
- Ver pantalla
- Encender/apagar

---

## 3. Cómo Encender el Android TV por ADB (Puerto 5037)

### Comando directo (1 línea):
```bash
adb connect <IP>:5037 && adb shell input keyevent 26
```

### Explicación de `keyevent`:
| Código | Acción                           |
| ------ | -------------------------------- |
| `26`   | Botón **POWER** (enciende/apaga) |
| `224`  | **Wake up** (enciende pantalla)  |

---

## 4. Script Automático: `encender_tv.sh`

```bash
#!/bin/bash

IP="192.168.1.100"  # ← CAMBIA AQUÍ

echo "[*] Conectando a ADB en $IP:5037..."
adb connect $IP:5037 > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "[+] Conectado! Encendiendo TV..."
    adb shell input keyevent 26
    echo "[✓] TV encendido!"
else
    echo "[!] Falló. ¿ADB activado? ¿IP correcta?"
    exit 1
fi
```

### Uso:
```bash
chmod +x encender_tv.sh
./encender_tv.sh
```

---

## 5. Comandos Útiles por ADB (5037)

| Comando                                     | Descripción       |
| ------------------------------------------- | ----------------- |
| `adb shell whoami`                          | Usuario actual    |
| `adb shell screencap -p /sdcard/screen.png` | Captura pantalla  |
| `adb pull /sdcard/screen.png`               | Descargar captura |
| `adb install app.apk`                       | Instalar app      |
| `adb shell pm list packages`                | Listar apps       |
| `adb shell dumpsys power`                   | Estado de energía |
| `adb reboot`                                | Reiniciar TV      |

---

## 6. Otros Métodos para Encender (Alternativas)

### A. Wake-on-LAN (WoL) + ADB

```bash
# 1. Obtén MAC
adb shell ip neigh | grep <IP>

# 2. Envía magic packet
wakeonlan aa:bb:cc:dd:ee:ff

# 3. Enciende
adb connect <IP>:5037 && adb shell input keyevent 26
```

### B. Google Cast (Puerto 8008/8009)
```bash
pip install pychromecast
```

```python
import pychromecast
cast = pychromecast.get_chromecast(friendly_name="Tu TV")
cast.quit_app()  # Fuerza encendido
```

---

## 7. Riesgos de Seguridad (¡ALTO!)

| Riesgo                | Impacto                         |
| --------------------- | ------------------------------- |
| ADB 5037 abierto      | **Control total** por red local |
| Panel web (8008/8443) | Posible login débil             |
| Firmware viejo        | Exploits conocidos              |

---

## 8. Cómo Proteger el Android TV (¡HAZ ESTO YA!)

1. **Desactiva ADB en red**  
   → Ajustes → Sistema → Opciones de desarrollador → **Desactiva "Depuración ADB"**

2. **Bloquea puertos en el router**  
   → 5037, 8008, 8443, 9000

3. **Actualiza el sistema**  
   → Ajustes → Sistema → Actualizaciones

4. **No uses UPnP ni port forwarding**

---

## 9. Resumen Rápido

| Acción         | Comando                                                |
| -------------- | ------------------------------------------------------ |
| Conectar ADB   | `adb connect <IP>:5037`                                |
| Encender TV    | `adb shell input keyevent 26`                          |
| Todo en uno    | `adb connect <IP>:5037 && adb shell input keyevent 26` |
| Script auto    | Usa `encender_tv.sh`                                   |
| Desactivar ADB | Ajustes → Opciones de desarrollador                    |


---