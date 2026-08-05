# Dependencies
`apk add certbot certbot-dns-cloudflare nginx`
# Nginx
At least a http virtualhost is required so the certbot can do the challenge to issue the certificate:
`/etc/nginx/http.d/wallettracker.conf`
``` bash
server {
    listen 80;
    server_name api.wallettracker.downops.win;
location /.well-kown/acme-challenge/ {
        root /var/www/certbot;
    }
    location / {
        return 301 https://$host$request_uri;
    }
}
```

# Certificate
Create the file and folder
`mkdir -p /root/.secrets/certbot`
`vi /root/.secrets/certbot/cloudflare.ini`
```bash
dns_cloudflare_api_token = API_TOKEN
```

Run
```bash
certbot certonly --dns-cloudflare --dns-cloudflare-credentials /root/.secrets/certbot/cloudflare.ini -d api.wallettracker.downops.win --non-interactive --agree-tos -m nnag@downops.win
```

# Nginx
Back to Nginx.
After successfully creating the certificate, we can configure the virtualhost to use it, and also remove the certbot challenge from the http block:
``` bash
server {                                             
    listen 443 ssl;                                  
    server_name api.wallettracker.downops.win;
                                                     
    ssl_certificate /etc/letsencrypt/live/api.wallett
    ssl_certificate_key /etc/letsencrypt/live/api.wal
                                                     
    ssl_protocols TLSv1.2 TLSv1.3;                   
    ssl_ciphers HIGH:!aNULL:!MD5;                    
                                      
    location / {                                     
        include uwsgi_params;                        
        uwsgi_pass unix:/tmp/app.sock;               
    }                                                
}                                                    
                                              
server {                                      
    listen 80;                                       
    return 301 https://$host$request_uri;            
}   
```

`nginx s -reload`

# Cloudflared

Configure the tunnel:
`root/cloudflared/config.yml`
``` bash
tunnel: TUNNEL_ID         
credentials-file: /root/.cloudflared/TUNNEL_ID.json
                                                     
ingress:                                   
  - hostname: api.wallettracker.downops.win
    service: https://127.0.0.1:443
    originRequest:          
      originServerName: api.wallettracker.downops.win
  - service: http_status:404
```

Run the tunnel as a background service:
``` bash
rc-update add cloudflared default
rc-service cloudflared start
```