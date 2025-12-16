
# Reconnnaissance

La ip del host es:  10.10.11.221
El dominio es: http://2million.htb

# Scan & Enumeration
## Nmap scan 

 adri | 192.168.1.88 | [ Mon Sep 01 19:52:24 ]  
──➤    sudo nmap -sV -Pn -p-1000  10.10.11.221  1>portscan
│ File: portscan
────────────────────────────────────────────────────────────
   1   │ Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-01 19:52 CEST
   2   │ Nmap scan report for 10.10.11.221
   3   │ Host is up (0.042s latency).
   4   │ Not shown: 998 closed tcp ports (reset)
   5   │ PORT   STATE SERVICE VERSION
   6   │ 22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
   7   │ 80/tcp open  http    nginx
   8   │ Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
   9   │
────────────────────────────────────────────────────────────

Viendo que hay un servicio web en el puerto 80 he procedido a intentear conectarme de manera directa con la ip del servidor, me ha redirigido a el dominio 2million.htb. 
Procedo a agregar este domino a hosts. 

## fuzzing de la web en el puerto 80

   │ File: web-fuzz
────────────────────────────────────────────────────────────
   5   │ [+] Url:                     http://2million.htb
   6   │ [+] Method:                  GET
   7   │ [+] Threads:                 10
   8   │ [+] Wordlist:                /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-lowercase-2.3-medium.txt
   9    │ [+] Negative Status codes:   404
  10   │ [+] Exclude Length:          162
  11   │ [+] User Agent:              gobuster/3.8
  12   │ [+] Timeout:                 10s
  13   │ ===============================================================
  14   │ Starting gobuster in directory enumeration mode
  15   │ ===============================================================
  16   │ /home                 (Status: 302) [Size: 0] [--> /]
  17   │ /login                (Status: 200) [Size: 3704]
  18   │ /register             (Status: 200) [Size: 4527]
  19   │ /api                  (Status: 401) [Size: 0]
  20   │ /logout               (Status: 302) [Size: 0] [--> /]
  21   │ /404                  (Status: 200) [Size: 1674]
  22   │ /0404                 (Status: 200) [Size: 1674]
  23   │ /invite               (Status: 200) [Size: 3859]
────────────────────────────────────────────────────────────
### intento de registro 
Intentando registrar no puedo por que me pide un invitecode.  
#### Como conseguir el invitecode. 
En la pagina /invite hay un min.js con los endpoints y el noel ha ido probando y encontro el endpoint /api/v1/invite/generate. 

Esta es la request: 

Este genera un codigo de invitacion valida. 
2A2L3-JI834-GS893-S7TID
y he podido regsitrarme pegando el codigo en /invite. 

**adri@mail. com y 1234 son los user y password.**
a