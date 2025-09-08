
Generate certificate

``` bash
openssl req -newkey rsa:2048 -nodes -keyout private.key -x509 -days 365 -out certificate.crt -subj "/CN=localhost"
```

Encapsulate certs and create .pfx

``` bash
  345  openssl pkcs12 -export   -out certificate.pfx   -inkey private.key   -in certificate.crt   -password pass:8SI1eMbT97arxo
```