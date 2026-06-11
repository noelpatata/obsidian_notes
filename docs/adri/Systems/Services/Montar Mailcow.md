
## Algunos puntos necesarios a tener en cuenta. 

### En españa bloquean el trafico del puerto 25. 

Los provedores de internet bloquean el puerto 25 en redes residenciales por razones como: 

1. Evitar spammers ya que protocolo 25 se usa mucho para enviar spam. 
2. Seguridad, las redes residenciales no estan protegidas como las redes empresariales, ergo son mas susceptibles a ataques. 
3. Los ISP prefieren que los correos viajen por puertos mas seguros.

**Así que aunque abras puertos en el router ->  no funciona el servicio.**

>[!tip]  Solucion 
> Cambiar el protocolo a uno permitido como el 587 usando **SMPT con STARTLSS** , con el fin de evitar el bloqueo. Y aplicando cifrado seguro para las conexiones de correo.   

---
### El cifrado no puede ser autofirmado.

El cifrado debe ser dado por una entidad certificadora, por que los clientes de correo convencionales no reconcen los autofirmados como una entidad de confianza. 

### DNS y Registros de mail services. 

Para que el servidor de correo funcione correctamente y no te marquen como spam, tienes que configurar mas cosas aparte del mailcow en si. 

**Algunas configuraciones importantes son:**
- Registros MX ( mail exchange ).
*Es  el registro servidores de mail donde le dices al resto de mail servers donde encontrarte.*
- Registros A. ( si te hace falta ).
*Asegurarse de que tu dominio ya esta escrito en el address register de DNS.*
- SPF ( Sender Policy Framework ).
*Es un registro para prevenir que otros servidores se hagan pasar tu servidor, **importantisimo para que nadie envie correos desde tu dominio.***
- DKIM ( DomainKeys Identified Mail ).
*Esto es una clave para garantizar que los correos sean verificados como legitimos y no marcados como spam, unicamente necesitas crear un txt en el DNS provider con la clave publica DKIM.*
- DMARC ( Domain-based Message Authentication, Reporting & Conrmance ). 
*DMARC tambien es para protegerte de la suplantacion de identidad, es una capa adicional que se construye sobre SPF y DKIM , DMARC no solo valida los correos, tambien permite decidir que hacer si un correo en concreto no pasa las verificaciones de autenticidad SPF o DKIM, ya sea revocarlo, marcarlo como spam o rechazarlo.*

