
Tienes diferentes proyectos con diferentes versiones de nodejs, o como me pasa en ubuntu a mi que la ultima version no esta en los repos de mi distro.

>[!tip] Solucion:
> Instalar NVM un gestor de versiones de nodejs, donde puedes configurar una version por defecto pero también cambiar de version con comandos simples. 

Lo primero borrar el nodejs npm y limpiar dependencias residuales. 

```bash 
sudo apt remove nodejs npm 
sudo apt autoremove -y 
``` 

Ahora ejecutamos el script del repo de nvm: 

```bash 
curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

Puedes recargar la shell haciendo un `source ~/.<shell>rc`  o simplemente abrir otra pestaña de terminal. 

Y procedes a instalar la version deseada de nodejs. 

```bash 
nvm install 22
nvm use 22
nvm alias default 22
``` 



