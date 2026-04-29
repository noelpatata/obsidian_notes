listar dispositivos 

```bash
morde@laptop ~/Desktop lsusb  
Bus 005 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
...
```

Seleccionar USB a utilizar

``` bash
sudo pamusb-conf --add-device DEVICE_ID
```

Añadir usuario al dispositivo

```bash
sudo pamusb-conf --add-user USERNAME
```

Issues
Doesnt fucking authenticate background services and asks for your password, for example KDE-Wallet