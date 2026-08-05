# Openwrt
Create NAT rule to redirect traffic from port 853 to the home server hosting the adguard.
# Create cert with certbot
``` bash
`sudo certbot certonly -d home.downops.win --dns-cloudflare --dns-cloudflare-credentials /root/.secrets/certbot/cloudflare.ini --dns-cloudflare-propagation-seconds 60`
```
# UI Setup
Settings -> Encryption Settings
And change the domain and the cert paths.
Something like `/etc/letsencrypt/live/home.downops.win/fullchain.pem`
# IDK
I just had to change the domain of my certificate created with certbot.
And I had to run this command:
``` bash
sudo certbot certonly --expand -d adguard.downops.win -d home.downops.win --dns-cloudflare --dns-cloudflare-credentials /root/.secrets/certbot/cloudflare.ini
```
Honestly, I don't even know how I created the certificate, so I just added the home.downops.win domain with certbot.
Token was expired and it couldn't accomplish the challenge, so I had to update the cloudflare token in `/root/.secrets/certbot/cloudflare.ini` with a Edit DNS template Token.