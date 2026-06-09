create the certificate with the local address as the subject:
``` bash
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/registry.key \
  -out /etc/nginx/ssl/registry.crt \
  -subj "/CN=100.96.42.211" \
  -addext "subjectAltName=IP:100.96.42.211,IP:192.168.0.24"
```
and add the crt to trusted certificates in jenkins:
`/etc/docker/certs.d/192.168.0.24/ca.crt`
