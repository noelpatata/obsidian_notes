# Open Code

#opencode #ia #coding-assistant #open-source #cheatsheet #agents

Open Code es una plataforma de coding con IA, como es Claude Code, con una gran diferencia, es de código abierto. Tiene dos maneras de cobrarte por el uso, un plan llamado Go de 10 dólares, donde te dan 60 dólares para gastar en ciertos modelos que entran en la suscripción que van cambiando, pero son por regla general modelos abiertos, baratos. Y el modelo Zen que cobra a destajo por uso de cada modelo, donde siempre hay unos pocos modelos gratuitos de manera temporal que van cambiando.  

## Cheatsheet

- Puedes usar @ para referenciar archivos. 
- No hace falta hacer `ctrl + c ` para copiar prompts o texto que te da con doble click. 
- Con  `!` puedes entrar al modo shell, no hace falta pedir comandos mínimos o cambiar a otra terminal. 
- Relacionado con la anterior, puedes referenciar los comandos que hiciste en el pasado o su salida para preguntar sobre el output o el comando en si. 
- Cuando pegas textos largos, o imágenes sale como `[Pasted tal]` como referencia. 
- Con `/timeline` puedes ver todos los prompts, buscar, y moverte entre ellos, además con entrando en un prompt puedes copiar forkear o volver al mensaje.
- Para cambiar el tema con `/themes` y buscar entre los temas. 
- Otro comando muy útil es `/undo`

>[!note] /undo 
>ahora mismo está roto, hay issues de github que pintaban que estaba roto, pero la idea este comando es deshacer los cambios, por si olvidaste hacer commit, o simplemente no los quieres, pero tiene la posibilidad de reverter ese undo, volviendo al ejemplo de antes por si querías comitear cambios antes del mensaje que hiciste.

- `/compact` ayuda básicamente a compactar el contexto para reducir el uso de tokens como contexto, ayuda no gastar tanto saldo, y a reducir la distracción al modelo. 
 
##  Agents

Open code tiene dos agentes nativos: 

**Build** => Tiene acceso a disco, capacidad de escritura y ejecución de comandos, por lo tanto es el agente al que pedirle que haga las acciones deseadas.

**Plan** => No tiene permisos de escritura, se utiliza para ver como se desarrolla el agente planificando la acción deseada, es interesante para ver como se desarrolla, y poder corregir, añadir, quitar, validar, o hacer que nos pregunte, sobre lo que el agente ha planificado.

 > [!tip] Ahorra tokens
>Está bien por que puedes usar un agente para planificar bien lo que necesitas, y luego poder construirlo con otro modelo gratuito, más barato, o simplemente el mismo con menos nivel de razonamiento.


# Agent Md 

Es un archivo que indica al agente como debe actuar en el work dir, es un must para poder explicarle al agente como queremos que trabaje en cada proyecto. Básicamente tú les defines las reglas.


>[!tip]
>Algo útil respecto a tener diferentes agentes, es que puedes orquestar entre estos las tareas a cada uno en un solo prompt para dividir el trabajo entre todos para obtener el mejor resultado.
>
>**El contexto es limitado usar diferentes agentes para enfocar el trabajo a cada uno ayuda con la distracción de los modelos.**

En realidad puedes crear tantos como puedas, van en la carpeta `/.opencode/agents/`

**Los más estandarizados son:**
### Design.md
Es básicamente lo mismo que el agent.md pero, orientado al diseño de tu proyecto.
### Reviewer.md 
Para revisar el código, confirmar que está correcto, y sigue las prácticas correspondientes al proyecto.
### Security.md
Parecido al de arriba orientado a la seguridad, le puedes dar más permiso a la hora de ejecutar comandos, a diferencia del reviewer, obviamente orientado a auditar el proyecto. 
### DocsWriter.md 
Un agente para escribir la documentación del proyecto.


# Agent skills 

Las Agents skills son una tecnología, es un estándar que hace crecer las capacidades y la experiencia de la inteligencia artificial. 

Puedes instalar diferentes skills o pedirle al modelo que desarrolle una skill en base algo que ya ha hecho correctamente, por pedir puedes pedirla antes, pero si lo haces cuando ya 
sabes que realizo el trabajo correctamente, es mejor. 

>[!note] 
>Las skills son un must, no un más, hay herramientas externas que requieren que instales su skill para poder ser utilizadas, desde crear video, o hacer diseño. Podrías hacer tus propias skills para que la IA use mejor tus MCPs.  
### Auto Skills 

Midudev creó un [repositorio](https://github.com/midudev/autoskills) que detecta las dependencias de tu proyecto y te recomienda que instales las skills que mejor pueden venir a tu proyecto, importante destacar que además estas son auditadas.

# Commands

De la misma manera que con los agentes puedes crear tus propios comandos dentro de la carpeta `./.opencode/commands`  creas un `markdown.md` con el nombre que le quieras dar al comando por ejemplo. 

>[!note] En que se diferencia de una skill 
> Realizar un comando a simple vista puede parecer no tener diferencia, hacer comandos de una skill, pero para que el modelo haga acciones en cadena de la misma manera que una skill sin hacer un prompt, es mucho más rápido y útil y actúan de la misma manera.
>  Por ej: 
> - como hacer los commits directamente 
> - la verdad se me ocurren pocas ideas más en este momento, realmente le veo más potencial a una skill donde le puedes ser más específico en cada caso concreto, pero para el caso concreto anterior si tiene potencial, igual hay más casos de usos que es útil. 
