tags: ["redis","database","cli","cheatsheet","crud"]


Redis-cli 
---


> [!tip]
>*El CLI de redis se usa para interactuar con el redis servier. Este te permite interactuar con la bbdd para manejar los datos monitoraer el rendimiento, debugar.* 



---

Estas son algunas maneras de conectarse
---

Te conectas con redis-cli  donde -h es el host y -p es el puerto: 

```bash 
	redis-cli -h host -p 6379 
``` 

Con auth por parametro  : 

```bash 
redis-cli -h example.com -p 6379 -a 'mi_password'
```

**Si por param** de no ponerla y requerirla se completa la conexion pero  da un error  de no autenticado, no puedes ejecutar la mayoria de comandos  : 

```bash 
(error) NOAUTH Authentication required.
``` 

De todas maneras luego puedes autenticarte con: 
```bash 
AUTH password  
``` 

Tambien puedes conectarte  usando URL : 

```bash 
redis-cli -u redis://:mi_password@example.com:6379
```


---


🗃️   Selección y gestión de datos :  
---

> [!recuerda]
> Redis **no usa bases de datos ni tablas como SQL**.  
> Piensa en **“bases de datos” = namespaces numerados (0–15 por defecto)**  
> y en **“tablas” = conjuntos de claves** agrupadas por prefijo (ej. `user:1:name`).

##### Mostrar info general del servidor

```bash
INFO
```

#####  Ver la base de datos actual

```bash 
SELECT 
```

##### Cambiar de base de datos (0–15 por defecto)

```bash 
SELECT 1
```

#####  Listar cuántas claves hay

```bash 
DBSIZE
```

##### Borrar toda la base actual

```bash 
FLUSHDB
```

#####  Borrar todas las bases

```bash 
FLUSHALL
```



---


🔑 Claves (Keys)
---

##### Ver todas las claves (⚠️ cuidado en producción)

```bash 
KEYS *
```

##### Buscar por patrón

```bash 
KEYS user:*
```

##### Eliminar una clave


```bash 
DEL user:1
```

##### Comprobar si existe

```bash 
EXISTS user:1 
``` 


---

🧱 “Tabla” tipo STRING (pares clave-valor)
---- 

> [!info]  
> Equivalente a una tabla simple con una columna `value`.
##### Crear o actualizar

```bash 
SET user:1:name "Carlos"
```

##### Leer valor

```bash
GET user:1:name
```

##### Incrementar numérico

```bash
INCR visitas:pagina
```
##### Expiración (TTL)

```bash
EXPIRE user:1:name 60 TTL user:1:name
```

##### Eliminar

```bash
DEL user:1:name
```



---


🧩 “Tabla” tipo HASH (estructura tipo objeto / fila)
---


> [!info]  
> Para guardar una entidad con varios campos (como una fila SQL).

##### Crear una “fila”

```bash
HSET user:1 name "Carlos" email "carlos@ejemplo.com" age 30
```

##### Leer campo específico

```bash
HGET user:1 name
```

##### Leer todos los campos

```bash
HGETALL user:1
```

##### Actualizar un campo

```bash
HSET user:1 email "nuevo@correo.com"
```

##### Eliminar campo

```bash
HDEL user:1 age
```
##### Listar claves del hash

```bash
HKEYS user:1
```



---


📜 “Tabla” tipo LIST (lista ordenada tipo cola o pila)
--- 

##### Crear (insertar al final)

```bash
RPUSH cola tareas tarea1 tarea2 tarea3
```
##### Leer rango (0 = primero, -1 = último)

```bash
LRANGE cola tareas 0 -1
```

##### Insertar al principio

```bash
LPUSH cola tareas tarea0
```

##### Extraer primer elemento (como ```bash
pop)

```bash
LPOP cola tareas
```

##### Extraer último elemento

```bash
RPOP cola tareas
```



---


🧮 “Tabla” tipo SET (conjunto sin duplicados)
----

##### Agregar elementos

```bash
SADD roles admin editor viewer
```

##### Ver todos los elementos

```bash
SMEMBERS roles
```

##### Ver si contiene un valor

```bash
SISMEMBER roles admin
```

##### Eliminar un valor

```bash
SREM roles editor
```



---


🏅 “Tabla” tipo ZSET (conjunto ordenado con puntuación)
---

##### Agregar elementos con puntuación

```bash
ZADD ranking 100 "Alice" 200 "Bob"
```
##### Ver todo (ordenado por puntuación ascendente)

```bash
ZRANGE ranking 0 -1 WITHSCORES
```

##### Obtener ranking inverso (descendente)

```bash
ZREVRANGE ranking 0 -1 WITHSCORES
```

##### Actualizar puntuación

```bash
ZINCRBY ranking 50 "Alice"
```

##### Eliminar elemento

```bash
ZREM ranking "Bob"
```



---


🔍 Búsquedas y patrones
---

##### Buscar todas las claves con prefijo

```bash
SCAN 0 MATCH user:* COUNT 100
```


> [!note]  
> SCAN es preferible a 
> `KEYS para producción (no bloquea el servidor).`



---


⚙️ Otras utilidades
---
##### Ver tipo de una clave

```bash
TYPE user:1
```

##### Ver tiempo de vida restante

```bash
TTL user:1

##### Persistir (quitar TTL)

```bash
PERSIST user:1

##### Copiar una clave

```bash
COPY origen destino
```



---


💾 Guardar / cargar
---


##### Forzar guardado en disco (snapshot)

```bash
SAVE
```

##### Guardado en background

```bash
BGSAVE
```

##### Exportar / importar (dump y restore)

```bash
DUMP user:1 RESTORE user:2 0 <datos_serializados>
```



---


🔐 Autenticación y conexión
---

##### Autenticarte manualmente

```bash
AUTH mi_password
```

##### Cambiar a DB 1

```bash
SELECT 1
```

##### Salir del CLI	

```bash 
QUIT
```



---


# 🧭 Ejemplo de flujo tipo “CRUD” completo



> [!done]  
> Usa prefijos (`user:1`, `order:12`, `session:xyz`) para simular “tablas” en Redis.  
> Esto te permite mantener una estructura tipo SQL sin perder velocidad.

##### Crear usuario

```bash 
HSET user:1 name "Ana" email "ana@ejemplo.com"
```

##### Leer usuario

```bash 
HGETALL user:1
```

##### Actualizar correo

```bash 
HSET user:1 email "nuevo@correo.com"
```

#####  Eliminar usuario

```bash 
DEL user:1
``` 



---

