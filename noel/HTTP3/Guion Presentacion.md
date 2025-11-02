# Que es HTTP3
HTTP3 se convirtió en un estandard en 2022 por IETF (Internet Engineering Task Force).
La peculiaridad de este protocolo, es que corre sobre UDP gracias a QUIC (un nuevo protocolo de transporte desarrollado por Google en 2012, y luego adoptado por IETF en 2016).
## Ventajas sobre HTTP1.1 y HTTP2
### Procesamiento de peticiones
HTTP1.1, aunque implemente pipelining, sigue recibiendo las peticiones en orden, y por eso tiene el problema de HOL a nivel de aplicación. Gracias al multiplexing de HTTP2 este problema se solucionó.
![[transport_examples_http.png]]

Aunque HTTP2 implemente multiplexing, sigue dependiendo de TCP, y por eso aunque a nivel de aplicación se libre de HOL, a nivel de transporte sigue sufriendolo.
![[tcp_HOL.png]]

### Seguridad
- Diferencias del handshake
- Vulnerabilidad del 0-RTT

https://datatracker.ietf.org/doc/html/draft-ietf-tls-tls13-21#section-8
https://ieeexplore.ieee.org/document/9024637 
https://www.youtube.com/watch?v=HnDsMehSSY4
# Integracion
# WebTransport