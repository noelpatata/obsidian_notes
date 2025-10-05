First login:
``` bash
sudo cloudflared login
```
then create the tunnel:
``` bash
sudo cloudflared tunnel create my-tunnel
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