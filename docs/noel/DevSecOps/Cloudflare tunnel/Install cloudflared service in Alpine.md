# Download binary

```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O /usr/bin/cloudflared && chmod +x /usr/bin/cloudflared
```

# Create service
``` bash
#!/sbin/openrc-run
name="cloudflared"
description="Cloudflare Tunnel"
command="/usr/bin/cloudflared"
command_args="tunnel run --token TUNNEL_TOKEN"
command_background=true
pidfile="/run/cloudflared.pid"
output_log="/var/logs/cloudflared.log"
error_log="/var/logs/cloudflared.log"

depend() {
  need net
}
```

# Start service
``` bash
chmod +x /etc/init.d/cloudflared
rc-update add cloudflared default
rc-service cloudflared start
```