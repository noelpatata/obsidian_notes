# Openwrt
- I just followed [this guide](https://openwrt.org/docs/guide-user/services/ddns/cloudflare) to setup the cloudflare ddns client.
- The ddns config file is `/etc/config/ddns`
After editting that file, you can restart with `/etc/init.d/ddns restart`
# Auth method
The problem with the guide above is that the auth method (Bearer token) is not supported because the cloudflare ddns client is very old, so I need to use a Global token:
You can generate that token in cloudflare -> profile -> api tokens -> global token (scroll down)
``` bash
uci set ddns.cloudflare.username='your.email@example.com' uci set ddns.cloudflare.password='your_global_api_key' uci commit ddns /usr/lib/ddns/dynamic_dns_updater.sh -v 1 -S cloudflare start
```
Also change this property since the client version is old:
``` bash
uci set ddns.cloudflare.lookup_host='home.downops.win' uci commit ddns /etc/init.d/ddns restart
```
# Run service
``` bash
/etc/init.d/ddns enable
/etc/init.d/ddns restart
```
# Cloudflare
Just create a type A DNS Record with no proxy.