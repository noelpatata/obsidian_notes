# Que es el reconocimiento en ciberseguridad? 

##### La fase de reconocimiento es esencial para identificar vulnerabilidades y asegurar la robustez de tus sistemas, consiste en recopilar la mayor cantidad de información sobre nuestros objetivos, con el tal de facilitar mas adelante cumplir con nuestras metas de manera mas efectiva.  

###### *Se divide en dos tipos:* 
### Pasivo
Donde la recopilación de información se realiza sin interacción con los sistemas, webs ni persona, por ejemplo con herramientas de OSINT para recopilar los datos de las redes sociales, leaks públicos, información compartida por parte del objetivo por un descuido... La información obtenida podría no ser valida. 
### Activo
Este interactua de manera directa con los sistemas que se encuentran a nuestro alcance, por ejemplo hacer un, escaneo de la red, de sus puertos, nslookup, pero siempre de manera global, para poder profundizar en la fase de escaneo y enumeración, llamar un responsable para sacarle información con ingeniería social ... Esto aumenta el riesgo de ser descubierto. 


# Practicas y consideraciones 

##### Aquí una lista de las practicas y consideraciones para realizar un reconocimiento efectivo, y agilizar el trabajo en un pentesting, análisis forense, o doxeo. 

1. **Documentación de las acciones realizadas :**  Mantener una documentación de las acciones que hacemos, para poder replicarlas. Lo que significa registrar cada paso importante , búsquedas herramientas utilizadas y el resultado de todas estas acciones.
2. **Recolección de evidencias:** Cada dato recopilado debe estar respaldado por pruebas solidas, puede ser tomando capturas de pantalla, guardando registros de actividad, o cualquier otro tipo de dato que respalde la evidencia. 
3. **Mantenimiento de la confidencialidad:** Evitar la exposición de datos sensibles. 
4. **Verificación de la información recolectada:** No es bueno confiar directamente en los datos obtenidos, una de las tareas es verificarlos con las evidencias, y diferentes fuentes o métodos.
5. **Automatización:** Para aumentar la productividad y eficiencia, descargar o desarrollar scripts que nos ayuden con la automatización de la fase, sin olvidar supervisar y validar los datos obtenidos.

# Retos y dificultades

##### Existen dificultades que hay que superar para realizar las tareas de manera efectiva, como protecciones, banneos automáticos si detectan algún escaneo, información obtenida y verificada como falso positivo por estar anticuada... Aquí un listado de las mas destacadas : 

1. **Adaptación ante defensas avanzadas:** Superar las implementaciones de seguridad de los firewalls, honeypots, sistemas de prevención de intrusiones, son un desafió para realizar reconocimiento en redes y servidores, de no sortearlos con efectividad, habría exito en la tarea. 
2. **Identificación de recursos ocultos:** Es otro reto que afrontar, identificar recursos, subdominios, paginas no indexadas, puertos, servicios, y direcciones internas que no se exponen al exterior. 
3. **Gestión de la sobrecarga de datos recopilados:** Cuando se tiene demasiada información, puede dar a una sobrecarga de datos, es importante identificar la información realmente útil y veraz.
4. **Eliminar duplicados y verificar la información:** Toda la información recopilada debe ser verificada atraves de diferentes fuentes y herramientas, ademas, se deben purgar los duplicados, y quedarnos con la información relevante. 