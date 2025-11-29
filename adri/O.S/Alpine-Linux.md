
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