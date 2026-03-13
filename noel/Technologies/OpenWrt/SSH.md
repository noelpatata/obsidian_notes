Como el ssh server solo usa RSA (creo), hay que activar temporalmente el acceso a servidores ssh con rsa (aunque éste sea vulnerable). Es para administrar el OpenWrt de forma temporal, así, no dejamos puertas abiertas a las que podrían acceder desde nuestro portátil:
``` bash
ssh -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedAlgorithms=+ssh-rsa -p [PORT] root@192.168.1.1
```
