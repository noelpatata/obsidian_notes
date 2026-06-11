#sop #cors #web-security #fundamentos #cybersecurity #glosario

# Glosario de Ciberseguridad

## Conceptos de Red y Acceso

- **Same Origin Policy (SOP)** -> Es una medida de seguridad que restringe la forma en que los documentos o scripts de un origen pueden interactuar con recursos de otro origen, previniendo así posibles ataques. Ver también [[XSS]] para vulnerabilidades que explotan esta política.
- **Cross-Origin Resource Sharing (CORS)** -> Es un mecanismo que permite a los servidores especificar quién puede acceder a los recursos, relajando así las restricciones impuestas por el SOP cuando sea necesario.
- **CSRF (Cross-Site Request Forgery)** -> Vulnerabilidad que induce al navegador de una víctima autenticada a enviar peticiones HTTP no deseadas a una aplicación vulnerable. El atacante aprovecha la sesión activa del usuario para realizar acciones en su nombre sin su consentimiento.
- **Privilege Escalation** -> Técnica mediante la cual un atacante obtiene permisos superiores a los que le corresponden, ya sea de forma vertical (más privilegios) o horizontal (acceso a otro usuario con los mismos privilegios). Ver [[Networking config]] para hardening que previene esto.

## Técnicas de Ataque

- **XSS (Cross-Site Scripting)** -> Vulnerabilidad que permite inyectar scripts maliciosos en páginas web vistas por otros usuarios. Ver [[XSS]] para más detalles y tipos (Reflected, Stored, DOM-based).
- **SQL Injection (SQLi)** -> Inyección de código SQL malicioso en consultas de bases de datos, permitiendo al atacante manipular datos, autenticarse sin credenciales o ejecutar comandos administrativos.
- **Path Traversal (Directory Traversal)** -> Técnica que explota una validación insuficiente de rutas para acceder a archivos y directorios fuera del directorio previsto, como `/etc/passwd` o archivos de configuración.
- **Phishing** -> Técnica de ingeniería social que suplanta entidades legítimas (emails, sitios web, mensajes) para engañar a las víctimas y robar credenciales, datos financieros o instalar malware.
- **Social Engineering** -> Manipulación psicológica para engañar a personas y que revelen información confidencial o realicen acciones que comprometan la seguridad. El phishing es un subconjunto de esta técnica.
- **Brute Force** -> Método de ataque que prueba sistemáticamente todas las combinaciones posibles de credenciales, contraseñas o claves hasta encontrar la correcta. Es efectivo pero lento y ruidoso.
- **Dictionary Attack** -> Variación del brute force que utiliza una lista predefinida de palabras comunes y variaciones en lugar de probar todas las combinaciones posibles. Más rápido que el brute force puro.

## Análisis y Herramientas

- **OWASP (Open Web Application Security Project)** -> Organización sin fines de lucro dedicada a mejorar la seguridad del software. Publica el famoso "OWASP Top 10" con las vulnerabilidades web más críticas.
- **CTF (Capture The Flag)** -> Competencia de ciberseguridad donde los participantes resuelven retos de seguridad para encontrar "flags" ocultas. Sirven como práctica para pentesting y análisis forense.
- **Burp Suite** -> Plataforma de prueba de seguridad web utilizada para realizar análisis de aplicaciones web, incluyendo proxy, scanner de vulnerabilidades y herramientas de manipulación de tráfico HTTP/S.
- **Netcat (nc)** -> Herramienta de red versátil conocida como el "swiss army knife" de la red. Permite crear conexiones TCP/UDP, transferir archivos, escuchar puertos y establecer shells reversas.
- **Reverse Shell** -> Tipo de shell donde la víctima se conecta activamente al atacante, permitiendo evadir firewalls que bloquean conexiones entrantes. Ver [[Networking config]] para configuración de red.
- **Bind Shell** -> Tipo de shell donde el servidor escucha en un puerto y el atacante se conecta a él. Más expuesto a firewalls que el reverse shell.

## Otros Términos

- **Payload** -> Código o datos enviados a un sistema vulnerable para ejecutar una acción específica, ya sea exploratoria, de acceso o de denegación de servicio.
- **Exploit** -> Código o técnica que aprovecha una vulnerabilidad para obtener acceso no autorizado o ejecutar código arbitrario en un sistema.
- **0-day (Zero-day)** -> Vulnerabilidad desconocida por el vendor o para la cual no existe parche. El término también se refiere al propio exploit que la explota.
