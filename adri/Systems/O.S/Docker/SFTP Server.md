
>[!tip] 
>Esto realmente es solo para no perder el archivo y la imagen que me gusto para hacer el sftp 

### Esta es la imagen de docker. 

	atmoz/sftp:latest

### Este es el `docker-compose.yml` en cuestion

Esto realmente solo es para no perder el earchivo 

```yml 
services:
sftp:
image: atmoz/sftp:latest
container_name: sftp_container
environment:
  - SFTP_USERS=adrian:1234:1001  # usuario:contraseña:UID
volumes:
  - /srv/data:/home/adrian/data
  - ~/.ssh/id_ed25519.pub:/home/adrian/.ssh/authorized_keys:ro
ports:
  - "2222:22"  # puerto SSH/SFTP
restart: unless-stopped
```
