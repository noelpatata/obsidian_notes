
# Objetivo. 

Web app donde puedes ejecutar o comandos, o scripts de tu carpeta para diferentes plataformas desde el rpi-pico como BadUSB. 
## Frontend simple con HTML + JS + CSS 

1. Muestra los scripts almacenados en la carpeta scripts.
2. Ejecuta los scripts haciendo los  comandos, muestra la salida si es posible recuperarla.
3. Ejecuta los scripts literalmente descargandolos copiandolos. 
4. 3 Hecho herramienta all in one, descarga/escribe el script, otorga los permisos de ejecucion, ejecuta, borra todo rastro....  
5. Chat con LLM te orienta sobre la app, pidele que haga por ti lo que no sepas. 
6. Consola de comandos indivuduales
## Backend flack python. 

5. Sirve los archivos de comandos en lote.
6. Sirve los scripts que tienes almacenados al front.
7. LLM transforma scripts en archivos de comandos en lote y los sirve. 
8. LLM pides x y trata de hacer comandos en lote para conseguir el fin y los sirve. 
## Pico HTTP backend server && BadUSB. 

1.  Controlador que ejecuta comandos dados por el HTTP server. 

# Limitaciones.

1. Potencia y memoria del pico son limitadores clave a la hora de la transmisión y escritura del texto. 
2. Limitacion de transmision de datos para no saturar los recursos del pico, max 4096 buffer. 
3. LLM suele ser pesado o inutil cuanto mas pesado menos inutil. 
4. El  LLM puede fallar en algunos casos, puede requerir optimizacion. 

5. Sacar las respuestas de los comandos deja rastro, y enviarlas a el front de alguna manera mas aun. 

# Soluciones. 

1. GET donde se pasa el texto a escribir por parametro msg, siempre y cuando sea posible y lo mas optimo. 
2.  POST donde se pasan textos largos en formato raw. 
	1. Decode mas liviano que JSON. 
	2. Splitear estas peticiones con content-length a menos de 4096 bytes . 
	3. Esto deja descansar la CPU, acosta de algo mas de ram, mas liviano que 400 get con url encode. 
3. Implementaciones keep alive para ahorrar tramas TCP. 
4. Implementar LLM en el backend no importa gasto de recursos, dentro de unos limites. 
		1. Aprender sobre como optimizar LLM para las tareas que llevaran acabo, y realizar todas las optimizaciones necesarias. 
