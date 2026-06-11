#opencode #ia #coding-assistant #open-source #cheatsheet #agents

Open Code es una plataforma de coding con IA, como es Claude Code, con una gran diferencia, es de codigo abierto. Tiene dos maneras de cobrarte por el uso, un plan llamado Go de 10 dolares, donde te dan 60 dolares para gastar en ciertos modelos que entran en la suscripcion que van cambiando, pero son por regla general modelos abiertos, baratos.  Y  el modelos Zen que  cobra a destajo por uso de cada modelo, donde siempre hay unos pocos modelos gratuitos de manera temporal que van cambiando.  

## Cheatsheet

- Puedes usar @ para referenciar archivos. 
- No hace falta hacer `ctrl + c ` para copiar prompts o texto que te da con doble click. 
- Con  `!` puedes entrar a el modo shell,  no hace falta pedir comandos minimos o cambiar a otra terminal. 
- Relacionado con la anterior, puedes referenciar los comandos que hiciste en el pasado o su salida para preguntar sobre el output o el comando en si. 
- Cuando pegas textos largos, o imagenes sale como `[Pasted tal]` como referencia. 
- Con `/timeline` puedes ver todos los prompts, buscar, y moverte entre ellos, ademas con entrando en un prompt puedes copiar forkear o volver al mensaje. 
- Para cambiar el tema con `/themes` y buscar entre los temas. 
- Otro comando muy util es `/undo` ahora mismo no se si esta roto por que hay issues de github que pintaban que estaba roto, pero la idea este comando es deshacer los cambios, por si olvidaste hacer commit, o simplemente no los quieres, pero tiene la posibilidad de reverter ese undo, volviendo al ejemplo de antes por si querias comitear cambios antes del mensaje que hiciste. 
 
##  Agents

Open code tiene dos agentes nativos: 

**Build** => Tiene acceso a disco, capacidad de escritura y ejecucion de comandos, por lo tanto es el agente al que pedirle que haga las acciones deseadas. 

**Plan** => No tiene permisos de escritura, se utiliza para ver como se desarrolla el agente planificando la accion deseada, es interesante para ver como se desarrolla, y poder corregir, añadir, quitar, validar, o hacer que nos pregunte, sobre lo que el agente a planificado. 

 > [!tip] Ahorra tokens
>Esto esta bien por que puedes usar un agente para planificar bien lo que necesitas,  y luego poder construirlo con otro modelo gratuito, mas barato, o simplemente el mismo con menos nivel de razonamiento. 

