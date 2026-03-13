
# 🖧 Linux Networking & Hardening — HTB Notes

> [!abstract]
> Apuntes completos y offline sobre **configuración de red, NAC, monitoreo, troubleshooting y hardening en Linux**, enfocados a **pentesting (HTB)**.

---

## 📌 Introducción

> [!note]
> Como **pentester**, dominar la **configuración de red en Linux** es una habilidad esencial.

Permite:
- Configurar entornos de laboratorio
- Manipular tráfico de red
- Identificar y explotar vulnerabilidades
- Optimizar procedimientos de prueba

> [!tip]
> Un buen conocimiento de redes = mejor pivoting, sniffing y explotación.

---

## 🌐 Conceptos Clave de Redes

Protocolos fundamentales:
- **TCP/IP** → base de Internet
- **DNS** → resolución de dominios
- **DHCP** → asignación dinámica de IP
- **FTP** → transferencia de archivos

Tipos de interfaces:
- 🧷 Cableadas
- 📡 Inalámbricas
- 🔁 Loopback (`lo`)

---

## 🖥️ Gestión de Interfaces de Red

> [!important]
> Saber listar, activar y configurar interfaces es básico en cualquier auditoría.

### 📋 Ver interfaces

```bash
ifconfig
ip addr
````

### 📊 Ejemplo de salida

```txt
eth0 → 178.62.32.126/18
eth1 → 10.106.0.66/20
lo   → 127.0.0.1
```

---

### ⚙️ Activar interfaz

```bash
sudo ifconfig eth0 up
sudo ip link set eth0 up
```

---

### 🧾 Asignar IP y máscara

```bash
sudo ifconfig eth0 192.168.1.2
sudo ifconfig eth0 netmask 255.255.255.0
```

---

### 🚪 Configurar gateway

```bash
sudo route add default gw 192.168.1.1 eth0
```

---

### 🌍 Configurar DNS

```bash
sudo vim /etc/resolv.conf
```

```txt
nameserver 8.8.8.8
nameserver 8.8.4.4
```

> [!warning]  
> `/etc/resolv.conf` **NO es persistente** (NetworkManager / systemd-resolved).

---

### 💾 Configuración persistente

```bash
sudo vim /etc/network/interfaces
```

```txt
auto eth0
iface eth0 inet static
  address 192.168.1.2
  netmask 255.255.255.0
  gateway 192.168.1.1
  dns-nameservers 8.8.8.8 8.8.4.4
```

```bash
sudo systemctl restart networking
```

---

## 🔐 Network Access Control (NAC)

> [!info]  
> NAC garantiza que **solo dispositivos y usuarios autorizados** accedan a la red.

### 📚 Modelos de NAC

|Modelo|Descripción|
|---|---|
|**DAC**|El propietario decide permisos|
|**MAC**|El SO impone reglas estrictas|
|**RBAC**|Permisos según roles|

---

### 🧠 Analogía rápida

```
Edificio
│
├── DAC → Cada empleado da llaves
├── MAC → Seguridad militar
└── RBAC → Acceso según puesto
```

---

## 🛡️ Implementaciones en Linux

### 🔒 SELinux

- MAC integrado en el kernel
    
- Control granular de procesos y archivos
    
- Muy seguro, complejo
    

### 🪖 AppArmor

- MAC basado en perfiles
    
- Más simple que SELinux
    
- Fácil mantenimiento
    

### 🌐 TCP Wrappers

- Control de acceso por IP
    
- Nivel red
    
- Simple pero limitado
    

---

## 📊 Monitoreo de Red

> [!note]  
> Analizar tráfico permite detectar **credenciales, anomalías y ataques**.

Herramientas:

- `syslog`, `rsyslog`
    
- `ss`, `lsof`
    
- ELK Stack
    
- `tcpdump`, `Wireshark`
    

---

### 📡 Comandos útiles

```bash
ping 8.8.8.8
```

```bash
traceroute www.inlanefreight.com
```

```bash
netstat -a
```

---

## 🛠️ Troubleshooting de Red

### ❌ Problemas comunes

- Sin conectividad
    
- DNS fallando (SIEMPRE es DNS)
    
- Pérdida de paquetes
    
- Red lenta
    

### 🔍 Causas típicas

- Firewalls mal configurados
    
- DNS incorrecto
    
- Hardware defectuoso
    
- Software sin parches
    

---

### 🧰 Herramientas clave

- `ping`
    
- `traceroute`
    
- `netstat`
    
- `tcpdump`
    
- `Wireshark`
    
- `nmap`
    

---

## 🛡️ Hardening en Linux

> [!important]  
> Reducir superficie de ataque es clave tanto en **pentesting** como en **producción**.

### Comparativa rápida

|Herramienta|Nivel|Dificultad|
|---|---|---|
|SELinux|Sistema|Alta|
|AppArmor|Aplicación|Media|
|TCP Wrappers|Red|Baja|

---

## 🧪 Laboratorio Recomendado

> [!tip]  
> Usa **VM personal + snapshots** antes de tocar nada.

### 🔒 SELinux

1. Bloquear acceso a un archivo
    
2. Permitir un servicio solo a un usuario
    
3. Denegar acceso por grupo
    

### 🪖 AppArmor

4. Bloquear archivo
    
5. Permitir servicio a un usuario
    
6. Denegar servicio por grupo
    

### 🌐 TCP Wrappers

7. Permitir servicio desde IP
    
8. Denegar servicio desde IP
    
9. Permitir servicio desde rango IP
    

---

## 🧠 Analogía Global

```
Red Linux
│
├── Interfaces → Cableado
├── NAC        → Seguridad del edificio
├── Monitoreo  → Cámaras
└── Hardening  → Puertas blindadas
```

---

## 📦 Extra: Entorno HTB

- 🐧 Parrot Linux (Pwnbox)
    
- 🌍 Ubicación: UK
    
- ⚡ Latencia ~65ms
    
- 🔄 1 spawn disponible
    

---

## 📚 Referencias

- Hack The Box Academy
    
- Linux Networking
    
- Linux Hardening
    
- `man ifconfig`
    
- `man ip`
    
- `man netstat`
    
- SELinux / AppArmor / TCP Wrappers Docs
    

