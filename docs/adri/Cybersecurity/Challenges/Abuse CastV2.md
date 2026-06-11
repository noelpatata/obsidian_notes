# Que es cast 

CastV2 es el protocolo seguro y en tiempo real que permite “castear” contenido desde un dispositivo a un receptor compatible, controlando reproducción, apps y volumen mediante mensajes binarios sobre WebSockets cifrados.

>[!note] Cabe recordar que NO puedes hacer 
>
> - Comandos del sistema Android
>     
> - Cambiar input HDMI
>     
> - Encender/apagar (salvo en modelos con soporte CEC)
>     
> - Ajustes de TV (brillo, canales, etc.)
>     
> - ADB o shell
>     
> - Cargar apps que no sean Cast
> 


Vale pero no puedes ejecutar los comandos de manera directa necesitas una herramienta para poder usarlos comandos de cast. 

Asi que he desarrollado un script en python para poder conectarnos al websocket y ejecutar comandos . 

He elegido python mas que nada por la libreria de pychromecast, aunque vi una utlidad similar para js que podrias ejecutar con nodejs. 

> [!note]  Dependencias . 
> 
> - Pychromecast 
>  Utilizo la libreria de pychromecast por que ya funciona, esta hecho y me facilita todo el script a algo muy simple, que solo tengo que pasar ip y accion desdeada 

###### El script en cuestion : 

```python 

import sys
import pychromecast
from pychromecast.controllers.youtube import YouTubeController

if len(sys.argv) < 3:
	print("Uso:")
	print(" python cast.py <IP_TV> <accion> [parametro]")
	print("\nAcciones disponibles:")
	print(" play_url <url>")
	print(" pause")
	print(" play")
	print(" stop")
	print(" volume <0.0-1.0>")
	print(" mute")
	print(" unmute")
	print(" youtube <video_id>")

sys.exit(1)

ip = sys.argv[1]
accion = sys.argv[2]
param = sys.argv[3] if len(sys.argv) > 3 else None

print("Buscando dispositivos Cast...")
devices, browser = pychromecast.discovery.discover_chromecasts()
cast_info = next((d for d in devices if d.host == ip), None)

if not cast_info:
	print("No se encontró ningún dispositivo Cast en:", ip)
	pychromecast.discovery.stop_discovery(browser)
	sys.exit(1)

  

print("Dispositivo encontrado:", cast_info.friendly_name)
cast_data = (
	cast_info.host,
	cast_info.port,
	cast_info.uuid,
	cast_info.model_name,
	cast_info.friendly_name
	)

cast = pychromecast.get_chromecast_from_host(cast_data)
pychromecast.discovery.stop_discovery(browser)
cast.wait()
mc = cast.media_controller

if accion == "play_url":

	if not param:
		print("Falta URL")
		sys.exit(1)

	mc.play_media(param, "video/mp4")
	mc.block_until_active()
	mc.play()
	print("Reproduciendo:", param)

elif accion == "pause":

	mc.pause()
	print("Pausado")
	
elif accion == "play":	
	
	mc.play()
	print("Play")

elif accion == "stop":
	
	mc.stop()
	print("Stop")
	
elif accion == "volume":

	if not param:
		print("Falta nivel de volumen (0.0-1.0)")
		sys.exit(1)
			
	cast.set_volume(float(param))
	print("Volumen:", param)
	
elif accion == "mute":

	cast.set_volume_muted(True)
	print("Mute activado")
  
elif accion == "unmute":

	cast.set_volume_muted(False)
	print("Mute desactivado")

elif accion == "youtube":

	if not param:
	print("Falta video_id de YouTube")
	sys.exit(1)

	yt = YouTubeController()
	cast.register_handler(yt)
	yt.play_video(param)
	print("YouTube →", param)

else:

	print("Acción desconocida:", accion)

```

--- 
 
##### Explicacion 

Aqui dejo una pequeña explicacion bloque por bloque de que hace cada cosa : 

