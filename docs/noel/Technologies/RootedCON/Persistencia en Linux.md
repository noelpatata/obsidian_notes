# Definicion
Mantener acceso a la victima sin ser detectado.
## Fuentes
MITTRE TA0003.
Internal all the things.
https://pberba.github.io Hunting for Persistence in Linux
elastic.co/security-labs Linux Persistence Detection Engineering
blog.thc.org/infecting-ssh-public-keys-backdoor
## Deteccion a traves de eventos
Modificar archivos de configuracion
Trap
Paquetes de instalacion
Udev rules
Fail to ban -> Se dispara un bloqueo en cuanto se hace un ataque de fuerza bruta
### Explotar claves asimetricas
La mitigacion es usar una gestion de identidades centralizada e ignorar las authorized_keys locales.
### Claves de un solo usuario
Identidades que sol permiten ejecutar comandos especificos por clave
## Directivas
Las directivas definidas en la configuracion del demonio ssh tienen prioridad sobre las que he configurado en el archivo de configuracion tanto a nivel global como de usuario.
AuthorizedKeysCommand -> es el comando que se usa para verificar las claves, es un vector de ataque atractivo para los atacantes
.ssh/rc -> script que se ejecuta al conectar por ssh, a nivel de usuario y a nivel global
PermitLocalCommand y LocalCommand -> Directiva para ejecutar comandos a nivel de cliente
RemoteCommand -> Al iniciar sesion en un servidor, ejecutar comando en la maquina remota, es decir, al servidor que me estoy conectando.
## Port knocking
en la configuracion de ssh hay un valor llamado sequence. despues de una secuencia de puertos se puede abrir el puerto 22.
ejemplo:
intento en 7000, intento en 8000, e intento en 9000
secuence = 7000,8000,9000
despues de eso, el puerto 22 se abre. 

