
# scanning & enumeration 
--- 
###  Router - 192.168.1.1 

Nmap scan report for 192.168.1.1
Host is up, received arp-response (0.011s latency).
Scanned at 2025-11-08 18:30:38 CET for 2s
Not shown: 96 closed tcp ports (reset)
PORT   STATE    SERVICE REASON
21/tcp filtered ftp     no-response
22/tcp open     ssh     syn-ack ttl 64
23/tcp filtered telnet  no-response
80/tcp open     http    syn-ack ttl 64
MAC Address: CC:D4:A1:1F:5E:50 (MitraStar Technology)





### Ubiquiti - 192.168.1.43
Nmap scan report for 192.168.1.43
Host is up, received arp-response (0.0066s latency).
Scanned at 2025-11-08 18:30:38 CET for 1s
Not shown: 99 closed tcp ports (reset)
PORT   STATE SERVICE REASON
22/tcp open  ssh     syn-ack ttl 64
MAC Address: 78:8A:20:83:B1:D7 (Ubiquiti)

###  Impresora hp  - 192.168.1.135
Nmap scan report for 192.168.1.135
PORT     STATE SERVICE    REASON
80/tcp   open  http       syn-ack ttl 64
443/tcp  open  https      syn-ack ttl 64
631/tcp  open  ipp        syn-ack ttl 64
8080/tcp open  http-proxy syn-ack ttl 64
9100/tcp open  jetdirect  syn-ack ttl 64
9220/tcp open  unknown    syn-ack ttl 64
MAC Address: C8:D3:FF:CA:B8:C3 (Hewlett Packard)

## TVs 35, 176 
###  TCL TV  - 192.168.1.35
Nmap scan report for 192.168.1.35
PORT     STATE SERVICE         VERSION
8008/tcp open  http?
|_http-csrf: Couldn't find any CSRF vulnerabilities.
|_http-dombased-xss: Couldn't find any DOM based XSS.
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
8009/tcp open  ssl/castv2w      Ninja Sphere Chromecast driver
8443/tcp open  ssl/https-alt?
|_http-aspnet-debug: ERROR: Script execution failed (use -d to debug)
|_http-vuln-cve2014-3704: ERROR: Script execution failed (use -d to debug)
9000/tcp open  ssl/cslistener?
MAC Address: C4:8B:66:E2:61:5A (Hui Zhou Gaoshengda Technology)

Ataques que te podrian hacer ? 
- Atraves del puerto 8009 puedes ejecutar comandos de cast como bajar volumen, subir, poner videos de una url, y apagar la tele no estoy seguro de si se puede encender. 
- 

###  firestick - 192.168.1.176
Nmap scan report for 192.168.1.176
PORT     STATE SERVICE REASON
8009/tcp open  ajp13   syn-ack ttl 64
MAC Address: C0:8D:51:E6:6D:88 (Amazon Technologies)

## mini pcs 38, 145 

### minipc or raspi -  192.168.1.38
map scan report for 192.168.1.38
PORT     STATE SERVICE     REASON
1978/tcp open  unisql      syn-ack ttl 128
1979/tcp open  unisql-java syn-ack ttl 128
5040/tcp open  unknown     syn-ack ttl 128
5357/tcp open  wsdapi      syn-ack ttl 128
7680/tcp open  pando-pub   syn-ack ttl 128
MAC Address: 84:47:09:17:CE:2C (Shenzhen IP3 Century Intelligent Technology)

###  minipc server  - 192.168.1.145 
Nmap scan report for 192.168.1.145
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
5901/tcp open  vnc-1
8443/tcp open  https-alt
9091/tcp open  xmltec-xmlmail
MAC Address: 84:47:09:13:1A:29 (Shenzhen IP3 Century Intelligent Technology)


## cams 51, 112, 113, 114, 116

### camera 1 - 192.168.1.112 
Nmap scan report for 192.168.1.112
PORT     STATE SERVICE
80/tcp   open  http
554/tcp  open  rtsp
1935/tcp open  rtmp
8080/tcp open  http-proxy
MAC Address: 44:01:BB:9B:BC:6A (Shenzhen Bilian Electronic，LTD)
###  camera 2 - 192.168.1.113 
Nmap scan report for 192.168.1.113
PORT     STATE SERVICE    REASON
80/tcp   open  http       syn-ack ttl 64
554/tcp  open  rtsp       syn-ack ttl 64
1935/tcp open  rtmp       syn-ack ttl 64
8080/tcp open  http-proxy syn-ack ttl 64
MAC Address: E0:09:BF:84:56:FB (Shenzhen Tong BO WEI Technology)
### camera 3 -192.168.1.114
Nmap scan report for 192.168.1.114
PORT     STATE SERVICE REASON
80/tcp   open  http    syn-ack ttl 64
554/tcp  open  rtsp    syn-ack ttl 64
1935/tcp open  rtmp    syn-ack ttl 64
#### listar el method 
554/tcp open   rtsp
|_rtsp-methods: OPTIONS, DESCRIBE, ANNOUNCE, SETUP, PLAY, RECORD, PAUSE, TEARDOWN, SET_PARAMETER, GET_PARAMETER

MAC Address: FC:5F:49:7D:83:88 (Zhejiang Dahua Technology)


### camera 4 - 192.168.1.116
Nmap scan report for 192.168.1.116
MAC Address: FC:5F:49:7A:76:6E (Zhejiang Dahua Technology)
### camera 5  - 192.168.1.51
Nmap scan report for 192.168.1.51
PORT     STATE SERVICE    REASON
80/tcp   open  http       syn-ack ttl 64
554/tcp  open  rtsp       syn-ack ttl 64
1935/tcp open  rtmp       syn-ack ttl 64
8080/tcp open  http-proxy syn-ack ttl 64
MAC Address: 44:01:BB:9B:CA:D9 (Shenzhen Bilian Electronic，LTD)






## camara alarma antigua ?? - 192.168.34  
Nmap scan report for 192.168.1.34
PORT   STATE SERVICE REASON
80/tcp open  http    syn-ack ttl 64
MAC Address: 00:1D:94:18:09:1C (Climax Technology)


##   espresif esp32  - no ports. 

	can be movi cam ?? 
	can be door controllers ?? 

All 100 scanned ports on 192.168.1.107 .
MAC Address: C8:C9:A3:25:F5:20 (Espressif

Nmap scan report for 192.168.1.178
MAC Address: 30:83:98:82:44:8C (Espressif)


# bypassing firewall
--- 

>[!note] info 
> Parece que habian dos firewalls, uno del ubiquiti y otro del router creo quizas algun minipc nose.
>  


Para saltarme los firewalls simplemente con nmap indique la opcion -Pn (no ping ) durante aen escaneo, y utilice la opcion -g para redirigir el  trafico del puerto origen a otro para pasar el ubiquiti.

Para entenderlo mejor revisa esto  => 

Esto devolvia el escaneo del  ubiquiti:  

```bash 
PORT   STATE SERVICE REASON
22/tcp open  ssh     syn-ack ttl 64
MAC Address: 78:8A:20:83:B1:D7 (Ubiquiti)
``` 


>[!note]
>obviamente con -Pn para no obtener hosts down


Y si trataba de **escanear una ip de el router** *(red origen privada)*, que no estaba en la red wifi de  **Ubiquti**  *(punto de acceso)* , **no devolvia nada del host esperado**. 

	nmap daba  la respuesta que hemos visto arriba. 

Basicamente nmap no conseguia que **el trafico no pasara a el ubiquiti** *(tiene un firewall)*.  

Pero por lo que sea **permite el trafico por el puerto 22**.

	eso es una mala implementacion, que se puede aprovechar.

>[!tip]  
> Ahi entra menos "-g " le dices al nmap que haga el **escaneo con el puerto 22 como origen** pasando el trafico por este puerto abierto, y **consiguiendo escanear el objetivo final** que esta fuera de la red principal. 


# gain acces to cams -5, 112, 113 
---


