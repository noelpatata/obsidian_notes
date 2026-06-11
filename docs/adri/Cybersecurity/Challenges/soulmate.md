
## 1. Reconocimiento 

1. Ejecute el escaneo con `nmap -sSV -Pn -p-` .

```sh
 adri@archlinux  ~  sudo nmap -sS -Pn -p-1000 -v -v  10.10.11.86
Starting Nmap 7.98 ( https://nmap.org ) at 2025-12-25 19:36 +0100
Nmap wishes you a merry Christmas! Specify -sX for Xmas Scan (https://nmap.org/book/man-port-scanning-techniques.html).
Initiating SYN Stealth Scan at 19:36
Scanning soulmate.htb (10.10.11.86) [1000 ports]
Discovered open port 22/tcp on 10.10.11.86
Discovered open port 80/tcp on 10.10.11.86
Completed SYN Stealth Scan at 19:36, 0.73s elapsed (1000 total ports)
Nmap scan report for soulmate.htb (10.10.11.86)
Host is up, received user-set (0.047s latency).
Scanned at 2025-12-25 19:36:55 CET for 1s
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE REASON
22/tcp open  ssh     syn-ack ttl 63
80/tcp open  http    syn-ack ttl 63

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 0.80 seconds
Raw packets sent: 1000 (44.000KB) | Rcvd: 1000 (40.008KB)
```

2. Puse la ip en el navegador, me salio el dominio **`soulmate.htb`**, lo agregue al `/etc/hosts`, y escanee los directorios web con gobuster con varios wordlist de seclist.
- common.txt: 

```sh 
✘ adri@archlinux  ~  gobuster dir -u soulmate.htb -w ~/Documentos/study_files/cyber/worldlist/SecLists/Discovery/Web-Content/common.txt
===============================================================
Gobuster v3.8.2
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
assets               (Status: 301) [Size: 178] [--> http://soulmate.htb/assets/]
index.php            (Status: 200) [Size: 16688]
===============================================================
```