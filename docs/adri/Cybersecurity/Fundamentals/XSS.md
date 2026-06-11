#xss #web-security #inyeccion #owasp #cybersecurity #burp-suite #dom

# Que es una vuln Cross Site Scripting ( XSS )

Un XSS es un tipo de vulnerabilidad que permite al atacante ejecutar código a través del sitio web a través de las interacciones que tiene el usuario con la app vulnerable.  
Te permite saltarte la protección de SOP que esta diseñada para segregar las diferentes 
webs .

XSS  normalmente permiten a un atacante enmascarar el usuario como usuario victima, realizando cualquiera accion que el usuario puede realizar, y acceder a los datos del usuario. Si el usuario victima tiene acceso privilegiado dentro de la apliacion, el atacante puede ganar acceso a toda la funcionalidad y datos de la aplicacion.

Si un atacante puede controlar un script que esta ejecutado en el navegador de la victima puede comprometer  totalmente ese usuario. 

# Como funciona una XSS? 

XSS funciona manipulando un sitio web vulnerable para que devuelva un codigo JS malicioso a los usuarios. Cuando el codigo se ejecuta dentro del navegador de la victima, el atacante puede comprometer su interacion con la aplicacion.
# XSS PoC

Puedes confirmar la gran mayoría de xss injectando un payload que causa que tu navegador ejecute algun codigo arbitrario de JS. En la portswigger academy recomiendan usar el metodo `print()` por que no esta tan utilizado como `alert()` y puede llegar a colar mas como PoC.

# Cuales son los main types de XSS

- Reflected XSS -> Donde el script viene de la actual HTTP request.
- Stored XSS -> Donde el script reside en la BBDD del sitio web. 
- DOM-based XSS


# Reflected XSS 

La Reflected XSS aparece cuando una aplicacion que recibe datos por HTTP request y de inmediato los incluye de manera insegura. 

Supón que un sitio web tiene una función de búsqueda que recibe el término de búsqueda proporcionado por el usuario en un parámetro de URL:  

`https://insecure-website.com/search?term=gift`  

La aplicación refleja el término de búsqueda proporcionado en la respuesta a esta URL:    

`<p>Buscaste: gift</p>  `

Suponiendo que la aplicación no realiza ningún otro procesamiento de los datos, un atacante puede construir un ataque como este:    
  
  `https://insecure-website.com/search?term=<script>/*+Mal+contenido+aquí...+*/</script> `

Esta URL resulta en la siguiente respuesta:  

`<p>Buscaste: <script>/* Mal contenido aquí... */</script></p>  `

## Impact of **Reflected XSS** attacks. 

Si otro usuario de la aplicación solicita la URL del atacante, entonces el script proporcionado por el atacante se ejecutará en el navegador del usuario víctima, en el contexto de su sesión con la aplicación. Entre otras cosas :  

- Realizar cualquier accion de la apliciacion que el usuario puede realizar.
- Ver informacion que el usuario puede ver.
- Modificar cualquier informacion que el usuiario puede modificar.
- Iniciar interaciones con otros usuarios de la aplicacion incluyendo ataques maliciosos, que aparecen como que los a realizado la victima original.

Hay varias medios por los cuales un atacante puede inducir ha a la victima a realizar una victima que ellos controlan. Esto podria ser por ejemplo dejar links, o enviar un email, tweet o otro mensaje. El ataque puede ser contra un usuario conocido o cualquier ataque indiscriminado contra cualquier usuario de la aplicacion.

La necesidad de un mecanismo externo para el ataque significa que el impacto de la **Reflected XSS** es generalmente menos severo que una  **Stored XSS**. 

## How to find and test for **Reflected XSS**

La gran mayoria de **Reflected XSS** pueden encontrarse rapidamente usando Burp Suite's web vulnerability scanner.

Testear  **Reflected XSS** manualmente involucra las siguientes acciones. 
- Testear cada entry point -> Testear de manera separada cada punto de entrada de datos de las HTTP request. Incluyendo parametros y otros datos dentro de la URL Query el Body de la request,  y url file path. Estoy incluye tambien los HTTP headers, aunque los comportamientos similares a XSS solo pueden activarse mediante ciertos HTTP headers y pueden no ser vulnerables en la practica. 
- Enviar valores alfanumericos -> Por cada punto de entrada de datos entregar un valor unico aleatorio para determinar que valor esta reflejado en la response. 


# Stored XSS



# Other things 

>[!important] Recuerda escapar los JSON correctamente
>  Hay que cerrar los JSON que rompas con } rollo alert()]//  y comentar el resto para poder skipear correctamente.

**Document.write()** escribe **directamente** en el flujo del documento HTML mientras se está cargando (o si se llama antes de que termine el parseo).

El navegador toma tu cadena tal cual, la inserta en el DOM y la **parsea como HTML normal**. Eso significa que:

- Cualquier etiqueta HTML válida se procesa.
- Los `<script>` se ejecutan.
- Los event handlers (onload, onerror, onfocus, etc.) se ejecutan.
- No hay “protección extra” porque no estás asignando a una propiedad del DOM, estás escribiendo en el stream.

Por eso puedes colar payloads mas simples como : 

```js 
'"><svg onload=alert(1)/>);
```


Con element.innerHTML= el comportamiento es diferente. 

Cuando haces div.innerHTML = cadena, el navegador:

1. Toma la cadena.
2. La parsea con un **HTML parser interno**.
3. Crea nodos DOM y los inserta en el elemento.

 **Los `<script>` NO se ejecutan nunca** cuando se insertan vía innerHTML. Es una protección deliberada del navegador desde hace años (Chrome, Firefox, Edge… todos lo hacen). El script se crea como nodo de texto, pero no se ejecuta.

¿cómo se hace XSS con innerHTML? 

Usando vectores que NO dependen de `<script>`  , es decir, etiquetas que disparan eventos automáticamente.

*Por ejemplo: *

```js
<body onresize=print() onload=this.style.width='100px'>
<img src="x" onerror=alert(1)>
<svg onload=alert(1)>
<video><source onerror=alert(1)>
<details open ontoggle=alert(1)>
```


```js
?returnPath=javascript:alert(document.cookie)

Si un atacante puede controlar un script que esta ejecutado en el navegador de la victima puede comprometer  totalmente ese usuario. 
```


### DOM XSS in href attribute sink 

Este tipo de XSS se basa en la injecion en cualquier parametro URL controlado por el atacante.  Gracias a que el navegador permite enviar `javascript:` como protocolo en **href**, si consigues controlar el input, puedes ejecutar codigo.

*PoC:* 

```js
?returnPath=javascript:alert(document.cookie)\
```


###  DOM XSS in jQuery selector sink using a hashchange event

Este tipo de XSS se basa en la injecion de codigo apartir del hash de la url . Esto sucede gracias a que la aplicacion utiliza la funcion de selecion de jquery pasando directamente el contenido del location.hash sin sanitizar. 

*Unos ejemplos de codigo vulnerable:*

```js
$(window).on('hashchange', function() {
    var element = $(location.hash); 
    element[0].scrollIntoView();
});

$(window).on('hashchange', function(){
	var post = $('section.blog-list h2:contains(' +
	decodeURIComponent(window.location.hash.slice(1)) + ')');
	if (post) post.get(0).scrollIntoView();
});
```

En este caso estos dos ejemplos se pueden reventar con el siguente payload: 
```sh
https://sitio-vulnerable.com/#<img src=x onerror=alert(1)>
```

Esto funciona por que como explicabamos antes jQuery no sanitiza perse, y si el desarrollador no sanitiza y pasa directamente el contenido a location.hash puedes crear un elemento que ejecuta un codigo.  

| **Rango de Versiones** | **Estado**                   | **Notas**                                                                    |
| ---------------------- | ---------------------------- | ---------------------------------------------------------------------------- |
| **< 1.9.0**            | **Altamente Vulnerable**     | Cualquier string con `<` dispara el XSS.                                     |
| **1.9.0 a 2.2.4**      | **Vulnerable (con matices)** | Requiere que el payload esté bien formado para saltar el check del selector. |
| **3.0.0+**             | **Mucho más seguro**         | Se corrigieron la mayoría de los vectores de ataque vía selector.            |
*Esta tabla muestra resumido cuales versiones de jQuery son las mas vulnerables.*

### Reflected XSS into attribute with angle brackets HTML-encoded

En este tipo de XSS se basa en que el atacante utiliza la actual request para injectar codigo malicioso, pero se tiene que saltar las protecciones del servidor que  trata encodear
los angle brackets . Esto puede succeder  modificar un input que no sanitiza la entrada en su totalidad.

*como es el caso  del ejemplo:*

```js
<section class="blog-header">  
    <h1>0 search results for 'MardukWasHere" '</h1>  
    <hr>  
</section>  
<section class="search">  
    <form action="/" method="GET">  
        <input type="text" placeholder="Search the blog..." name="search" value="MardukWasHere" "="">  
        <button type="submit" class="button">Search</button>  
    </form>  
</section>
```

Esta puede existir si el elemento se puede modificar para injectar codigo sin necesidad de usar angle brackets. 

*PoC*

```js
aa" onmouseover="alert(1)
```

Es recomendado usar eventos que no fuercen mas de una ejecucion y que sea seguro que se ejecutan en todos los navegadores para asegurarse que funciona en el navegador de la victima. 


### DOM XSS in AngularJS expression  with angle brackets and double quotes 

Este tipo de XSS se basa en la directiva **`ng-app`** de angular, esta directiva permite ejecutar codigo malicioso entre doble quotes. 

*PoC*

```js
<div ng-app>{{7*7}}</div>`
```

Por que funciona esto? 
Por que aunque el servidor http no codifique el div como div si no como texto plano, a angular le da completamente igual por que escanea la pagina despues de que el servidor termino de enviarla. 

>[!note]
Algo a tener en cuenta es que de esta manera no se puede llamar a funciones globales, no funcionan por razones de seguridad angular tiene un parser de la funcion, por lo que debemos forzar al llamarlo desde el constructor para que lo encuentre.
Ademas window esta bloqueado por diseño. 

*Ejemplos:*
`{{$on.constructor('alert(1)')()}}`
`{{$eval.constructor('alert(1)')()}}`

Cuando usas uno de estos ejemplos estás haciendo esto:
- Le pides a la fábrica de funciones (`constructor`) que cree una nueva función con el código `'alert(1)'`.
- Esa nueva función **no pertenece a Angular**, pertenece al navegador.
- Al poner los últimos paréntesis `()`, la ejecutas. Como es una función nativa del navegador, ya no busca `alert` en el `$scope` de Angular, sino en el `window` global.



### CHEATSHEET

```js
\\"+alert(1)}//"
```