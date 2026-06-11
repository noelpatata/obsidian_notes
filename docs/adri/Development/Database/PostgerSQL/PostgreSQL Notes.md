
######  Postgres es un sistema de administración de bases de datos relacionales FOO que se basa en SQL como interfaz para leer y editar datos, ofrece mas características que MySQL, aporta mas flexibilidad en cuanto a tipos de datos,  integridad de los datos, escalabilidad simultaneidad e. Postgres es apliamble y versatil, y de codigo abierto.


# Características de Postgres.

Postgres viene repleta de abundantes características y extensiones para crear bases de datos altamente escalables y fáciles de administrar, al tiempo que proporciona replicación y concurrencia sin fisuras a través de múltiples entornos. 

*Otras caracteristicas :*

### Cumplimiento ACID.

Postgres siguie los principios ACID(atomicidad, cosisntencia, aislamiento, durabilidad), lo que garantiza la integridad y confiabilidad de los datos, incluso en caso de fallas del sistema.

### Tipos de datos. 

Funciona con datos realcionales FOO, por lo tanto ofrece un amplio numero de tipos de datos integrados, incluyendo enteros numericos, cadenas ,fechas, JSON, XML, geometricos, direciones de red, GUID's ... Ademas los usuarios pueden definir mas tipos de datos personalizados. 

### Indexación Avanzada. 

El sistema de postgres admite diversos tipso de indices como arbol B, hash, GIST ( Arbol de busqueda generalizado), SP-GIST ( arbol de busqueda generalizado con particiones espaciales), GIN ( indice invertido generalizado), BRIN ( indice de rango de bloques). Esto permite una recuperacion de datos eficiente incluso para grandes conjuntos de datos. 

### Control de concurrencia. 

Si varios usuarios acceden a los datos al mismo tiempo,  los sistemas de administración de bases de datos suelen bloquear el acceso a los registros para evitar conflictos de lectura/escritura. Postgres gestiona esto de manera eficiente mediante el control de concurrencia por versiones multiples, esto consigue que las lecturas no bloquean las escrituras y viceversa, esto permite el trabajo simultaneo ademas de garantizar la consistencia de los datos. 
### Replicación y alta disponibilidad. 

Tiene diferentes opciones de replicación incluidas asincronas y sincronas, así como funciones integradas como replicación de steraming y la replicación lógica, lo que grantiza la redundancia de datos y la alta disponibilidad. 
### Búsqueda de texto completo. 

Tiene solidadas capacidades de busqueda de texto completo gracais a sus funcionalidades integradas como los tipos tsvector y tsquery, asi como la extension pg_trgm para la conincidencia de triagramas. 

### Permite lenguaje profundo. 

Postgres es una de los sistemas mas flexibles para los developers, debido a su compatiblidad y soporte de multiples lenguajes, como python, javascript, c/c++, ruby... Hay una larga lista de lenguajes con soporte maduro para postgres, per,itiendo a los developers realizar tareas de automatizacion en cualquier lenguaje sin generar conflictos.

### Recuperación de un punto en el tiempo. 

Postgres permite a los developers utilizar PITR (Recuperación de un punto en el tiempo) para restaurara bases de datos, cuando se ejecutan inciativas de recuperacion de datos. Dado que posgres mantiene un registro de escritura anticipada ( WAL) en todo momento, registra todos los cambios de la base de datos, lo cual  facilita la restauración de los sistemas de archivos a un punto de partida estable. 

### Procedimientos almacenados. 

Postgres soporta múltiples lenguajes de procedimiento, ofreciendo a los developers la posibilidad de crear sub-rutinas personalizadas denominadas, procedimientos almacenados. Estos procedimientos pueden crear e invocar en una base de datos determinada. Con el uso de extensiones, los lenguajes procedimentales también pueden utilizarse para el desarrollo en muchos otros lenguajes de programación, incluidos Perl, Python, JavaScript y Ruby.

### Características de seguridad. 

Proporciona caracteristicas de seguirdad robustas que incluyen encriptacion SSL control de acceso basado en roles, seguirdad a nivel de fila y auditoria de BBDD. Todo esto para poder progteger datos confidenciales del acceso no autorizado. 

### Envoltorios de datos externos. 

Permite acceder a datos alamacenados en fuentes externas como otras BBDD relacionales, BBDD no SQL o incluso servicios web atraves de envoltorios de datos exeternos lo que permite una integración perfecta con fuentes de datos heterogéneas. 

### Soporte geoespacial. 

Esto significa que incluye soporte para tipos de datos y funciones geoespaciales, lo que lo hace adecuado para aplicaciones que necesitan de estos datos, requieren de análisis de datos espaciales o sistemas de información geográfica. 
### Escalabilidad y particionado. 

Esta diseñado para poder escalar tanto vertical como horizontalmente, lo que permite manejar cargas de trabajos y volúmenes de datos crecientes agregando mas recursos o distribuyendo datos entre múltiples servidores, ademas de soportar también el particionado de tablas que permite dividir tablas grandes en fragmentos mas pequeños y manejables esto puede mejorar el rendimiento de las consultas y simplificar la gestión de los datos. 


# Diferencias entre Postgres y MySQL. 

Los dos sistemas son muy parecidos pero tienen características que los diferencian, y comprender las características distintivas es fundamental para elegir el sistema adecuado para las necesidades especificas.  

*Estos son los elementos principales que los diferencian:*
### Tipos de datos. 

MySQL es un sistema únicamente relacional, mientras que Posgres permite almacenar datos como objetos con propiedades, lo que facilita conceptos como objetos con propiedades, facilitando las interacciones entre objetos padre-hijo y herencias, en definitiva ofrece muchos mas tipos de datos, como como JSON,XML, direciones I.P, UUID...

### Gestión de columnas autoincrementales. 

MySQL genera automatícamente valores enteros unicos para las columnas cuando se marca como `AUTO_INCREMENT`. En cambio postgres ofrece una funcionalidad similar a través del sequence tipo de dato. 

### Tipos de indicies admitidos. 

MySql ofrece indices de arbol B, arbol R, de expresion y hash, mientras postgre ofrece una amplia gama de indices.
*mas informacion en las caracteristicas de idexacion avanzada.*

### Capacidades de búsqueda de texto completo. 

Postgres ofrece una amplia gama de funciones robustas y avanzadas para la búsqueda de texto completo mientras, MySQL aunque tambien cuenta con este tipo de funciones, no son tan completas como la implementación en postgres. 

### DDL transaccional . 

Postgres admite operaciones DDL ( lenguaje de definicion de datos) transacionales, lo que significa que las operaciones que alteran el esquema pueden incluirse en un bloque de trasaccioón y revertirse si es necesario. En MySQL las sentencias DDL no suelen ser transacionales, por lo tanto si se produce un error durante una operacion que altera el esquema no se puede revertir. 

### Cumplimiento ACID. 

Aunque ambos sitemas son compatibles con ACID, MySQL es compatible solo con el motores innoDB y NDB cluster, mientras que postgres es compatible en la totaliad de sus configuraciones. 

### Soporte de vistas materializadas. 

Ambos sistemas soportan las vistas tablas especiales que rellenan automaticamente mediante una consulta que selecciona datos de una o mas tablas. Sin embargo postgres admite vistas materializadas, estas vistas son persistentes almacenan los valores de la consulta de generación en el sistema archivos, lo que permite un mejor rendimiento en operaciones complejas. 

### Idiomas disponibles para escribir procedimientos almacenados. 

Ambos sistemas de gestión de bases de datos (SGBD) los admiten, pero PostgreSQL supera a MySQL al permitir la escritura de procedimientos almacenados en PL/pgSQL, PL/Tcl, PL/Perl y PL/Python, además de SQL.

### Tipos de activadores disponibles. 

Los disparadores SQL son operaciones que se ejecutan automaticamente cuando ocurren eventos especificos en la BBDD. Mysql solo admite disparadores AFTER y BEFORE para las sentencias insert update y delete. En cambio postgres tambien porporciona el disparador INSTEAD OF para realizar acciones en las vistas. 

## Cual elegir ? 

**Ambos tienen pros y contras y se deben contrastar en base a las necesidades de cada proyecto, MySQL es mas rápido peerse, pero postgres puede optimizarse para ser tan o mas rápido, aportando mayor flexibilidad, y consistencia de los datos, a costa de un mayor gasto de recursos.
A si que siempre se tiene que estudiar cual es la opción que mas encaja en el proyecto.** 


# Guia cliente PSQL

PSQL es el cliente de terminal de postgres. 