First login:
``` bash
sudo cloudflared login
```
then create the tunnel:
``` bash
sudo cloudflared tunnel create my-tunnel
```
configure the file to indicate the service you are exposing. `/root/.cloudflared/config.yml`:
``` yml
tunnel: TUNNEL_NAME
credentials-file: /root/.cloudflared/<tunnel-id>.json

ingress:
  - hostname: jenkins.example.com
    service: http://localhost:8080
  - service: http_status:404
    ```
then i have to configure the tunnel so it redirects to my service with the following http put request:
``` bash
sudo cloudflared tunnel route dns my-tunnel test.downops.win
```
**notice**
maybe you have to delete old dns records for your domain before the step above.
then you just run the tunnel:
```bash
sudo cloudflared tunnel run my-tunnel
```