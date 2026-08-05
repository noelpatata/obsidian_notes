# Installation
``` bash
apk update \
apk add docker-registry \
mkdir -p /var/lib/docker-registry \
chown docker-registry:docker-registry /var/lib/docker-registry \
rc-update add docker-registry default \
service docker-registry start
```
# Authentication
``` bash
apk add apache2-utils \
mkdir -p /etc/docker-registry/auth \
htpasswd -Bc /etc/docker-registry/auth/registry.password noel
```
then edit `/etc/docker-registry/config.yml` and add:
``` yaml
auth:                                                                         
  htpasswd:       
    realm: basic-realm      
    path: /etc/docker-registry/auth/registry.password
```

# Run over https
## Create certificate
``` bash
apk add nginx openssl \
mkdir -p /etc/nginx/ssl \
cat > openssl.cnf <<EOF [req] distinguished_name = req_distinguished_name x509_extensions = v3_req prompt = no [req_distinguished_name] CN = 100.96.42.211 [v3_req] subjectAltName = IP:100.96.42.211 EOF \
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-keyout /etc/nginx/ssl/registry.key \
-out /etc/nginx/ssl/registry.crt \
-config openssl.cnf -extensions v3_req
```
## Configure nginx
add this config to `/etc/nginx/http.d/registry.conf`:
``` conf
server {
    listen 443 ssl;
    server_name 100.96.42.211;

    ssl_certificate /etc/nginx/ssl/registry.crt;
    ssl_certificate_key /etc/nginx/ssl/registry.key;

    # Ajuste para permitir subida de imágenes grandes
    client_max_body_size 0;

    # Chunked transfer encoding para Docker
    chunked_transfer_encoding on;

    location /v2/ {
        # No permitir versiones viejas de Docker
        if ($http_user_agent ~* (Docker/1.3|Docker/1.4|Docker/1.5|Docker/1.6)) {
            return 404;
        }

        proxy_pass                          http://localhost:5000;
        proxy_set_header  Host              $http_host;
        proxy_set_header  X-Real-IP         $remote_addr;
        proxy_set_header  X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header  X-Forwarded-Proto $scheme;
        proxy_read_timeout                  900;
    }
}
```
## Import certificate in client
``` bash
mkdir -p /etc/docker/certs.d/100.96.42.211/ \
cp yourcert /etc/docker/certs.d/100.96.42.211/ca.crt
systemctl restart docker
```
start services
``` bash
rc-update add nginx \
service nginx start
```
