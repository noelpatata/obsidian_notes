#escaneo #enumeracion #pentesting #metodologia #cybersecurity

# Escaneo y Enumeración

##### El escaneo es la fase que precede a la [[Reconnaissance|reconocimiento]], y consiste en recolectar información sobre posibles objetivos con el fin de cumplir la tarea, sea análisis forense o pentest. Ejemplos de esta fase incluyen la detección de sistemas en la red, la identificación puertos, servicios y sus posibles vulnerabilidades.
##### La enumeración, por su parte, se centra en profundizar sobre los datos obtenidos durante el escaneo, extrayendo información mas especifica (como usuarios, recursos compartidos, aplicaciones, versiones de servicios), lo que facilita una comprensión de posibles rastros a seguir o vías de ataque.
 *Es importante guardar y formatear la información de los resultados de estas para tal de facilitar el uso de esta mas adelante.*

> [!tip] Herramientas útiles
> Para escaneo de puertos y servicios, consulta el [[Nmap cheatsheet]].

---

## Herramientas de escaneo

### [[Nmap cheatsheet|Nmap]]

La herramienta estándar para escaneo de redes y puertos. Permite descubrir hosts, identificar puertos abiertos, detectar servicios y versiones, y ejecutar scripts NSE para vulnerabilidades.

```bash
# Descubrir hosts en la red
nmap -sn 192.168.1.0/24

# Escaneo SYN rápido de todos los puertos
sudo nmap -sS -p- -T4 target

# Detección de servicios y versiones
nmap -sV -p22,80,443 target

# Escaneo agresivo (OS + scripts + traceroute)
sudo nmap -A target
```

### Masscan

Escáner de puertos masivo y ultra-rápido. Escanea millones de segundos en segundos, pero sacrifica precisión por velocidad. Ideal para mapear grandes rangos de IP.

```bash
# Escanear 10000 puertos en un rango de IPs
masscan 10.0.0.0/8 -p0-65535 --rate=10000 -oL resultados.txt

# Escanear puertos específicos
masscan 192.168.1.0/24 -p22,80,443 --rate=5000
```

> [!warning] Consideraciones con Masscan
> - Es extremadamente ruidoso y puede ser detectado fácilmente por IDS/IPS.
> - No detecta versiones de servicios, solo puertos abiertos.
> - Combinar con Nmap para obtener información detallada después del barrido inicial.

### Nikto

Escáner de vulnerabilidades web que detecta archivos peligrosos, configuraciones obsoletas y problemas comunes en servidores web.

```bash
nikto -h https://target.com
nikto -h target -p 8080
```

### Gobuster / Dirb / Feroxbuster

Herramientas de fuzzing de directorios y archivos ocultos en servidores web (directory brute-forcing).

```bash
# Gobuster - Enumerar directorios
gobuster dir -u https://target.com -w /usr/share/wordlists/dirb/common.txt

# Feroxbuster - Escaneo recursivo
feroxburst -u https://target.com -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

---

## Técnicas de enumeración

### Enumeración de usuarios

- **SMTP VRFY**: Verificar si un usuario existe en el servidor de correo.
- **LDAP Enumeration**: Consultar el directorio LDAP para obtener información de usuarios y grupos.
- **SNMP Enumeration**: Obtener información del dispositivo vía SNMP (community strings por defecto).
- **Brute Force de login**: Probar credenciales comunes contra servicios expuestos.

### Enumeración de servicios

```bash
# Enumerar SMB (Windows)
enum4linux -a target
smbclient -L //target -N

# Enumerar SNMP
snmpwalk -v2c -c public target

# Enumerar DNS
dnsrecon -d target.com -t std
```

### Enumeración web

```bash
# HTTP headers y tecnología
curl -I https://target.com

# Tecnologías con WhatWeb
whatweb https://target.com

# Subdominios
subfinder -d target.com
amass enum -d target.com
```

---

## Flujo de trabajo recomendado

1. **Descubrimiento de hosts**: Usar `nmap -sn` o `masscan` para identificar IPs activas.
2. **Escaneo de puertos**: Identificar puertos abiertos con `nmap -sS -p-`.
3. **Detección de servicios**: Obtener versiones con `nmap -sV`.
4. **Enumeración profunda**: Usar herramientas específicas por servicio (enum4linux, nikto, gobuster).
5. **Documentación**: Guardar todos los resultados en formatos parseables (`-oN`, `-oX`, `-oG`).

---

## Mejores prácticas

> [!important] Reglas de oro
> - **Guardar siempre los resultados** en archivos para referencia futura y para generar reportes.
> - **Empezar con escaneos suaves** (`-T2` o `-T3`) antes de pasar a modos agresivos.
> - **Respetar el alcance del pentest**: no escanear IPs o puertos fuera del scope acordado.
> - **Evitar `-A` en entornos productivos** por ser demasiado ruidoso y potencialmente disruptivo.
> - **Usar credenciales válidas** cuando sea posible para obtener mejor enumeración.
> - **Combinar herramientas**: Nmap para descubrimiento, herramientas especializadas para enumeración profunda.
> - **Verificar falsos positivos**: Los resultados automáticos pueden contener errores, siempre validar manualmente.

> [!note] Notas relacionadas
> - [[Reconnaissance]] para la fase previa de reconocimiento
> - [[Nmap cheatsheet]] para comandos detallados de Nmap
> - [[Vocabulary]] para definiciones de términos técnicos
