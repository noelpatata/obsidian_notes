cv
# Instalacion 

La instalacion es muy simple solo tienes que lanzar el comando  : 
`setup-alpine`

y seguir la guia de instalacion por comandos.  

# Configuración posterior 

> [!tip] 
>  *Esto son configuraciones simples solo tomo un par de anotaciones por si me olvido de las rutas o paquetes en alpine poder consultar rapidamente*

--- 
##  Habilitar repositorios de la comunidad .

Entrar al archivo de repositorios con : 

``` bash 
vi /etc/apk/repositories
```

Y descomentarla linea de repos de la comunidad: 
`#http://dl-cdn.alpinelinux.org/alpine/v3.20/community`

Hacer un apk update para actualizar el indice de paquetes. 

``` bash 
apk update 
```

--- 

## Configurar sudo 

Como root, tienes que instalar un servicio de sudo, yo he escogido el que mas versiones tiene: 

``` bash 
apk add sudo
```

Editar sudoers como *`visudo`* y descomentar el grupo wheel :  

```bash 
visudo /etc/sudoers/
``` 

Busca (o agrega) la línea:
`%wheel ALL=(ALL) ALL`

>[!note] 
>  - `%wheel` → cualquier usuario del grupo `wheel`
>    
> - `ALL=(ALL) ALL` → puede ejecutar cualquier comando como cualquier usuario
> 
> Guarda y cierra (`:wq` en `vi`).

Agrega el *`user`* que necesite *`sudo`* al grupo *`wheel`*

---

## Instalar Netbird 

*Instalar y configurar el netbird es realmente rapido en todas las maquinas.*

Haces curl de su script de instalacion y lanzas el servicio con netbird up. 

``` bash
curl -fsSL https://pkgs.netbird.io/install.sh | sh
netbird up
```

De no estar loggeado te tira un link para que te logges desde el navegador. 

---

## Instalar docker 

1. Instalar Docker en Alpine

```bash 
apk add docker docker-cli docker-compose docker-openrc
```

>[!note] Recuerda 
> Alpine usa **OpenRC**, no systemd.

2. Habilitar el servicio de Docker en OpenRC.

Activa Docker para que arranque con el sistema:

```bash 
rc-update add docker boot
```

3. Iniciar Docker ahora

```bash 
rc-service docker start
```

## Instalar ngrok 


1. Primero hay que instalar algunas herramientas para poder instalarlo luego puedes borrarlas.

``` bash 
apk update
apk add wget unzip bash
```

2. Descarga la última versión estable, descomprime, borra y da permisos de ejecucion.

```bash  
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xvzf ngrok-v3-stable-linux-amd64.tgz 
rm ngrok-stable-linux-amd64.zip
chmod +x ngrok
``` 

3.  Mueve a el directorio de binarios de linux y añade ngrok al path. 

```bash
mv ngrok /usr/local/bin 
export PATH=$PATH:/usr/local/bin/ngrok
```

4. Guarda el token de tu session de ngrok.

```bash 
ngrok config add-authtoken 30EwHVsP5M1A4JD2SjJ2lhcQdWl_6Yv2TryQ5e1Hnnw9KK353
```
