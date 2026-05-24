# Enable
``` bash
sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
```
# Make changes persistent
## Save changes
```bash
iptables-save > /etc/iptables.up.rules
```
### Create file
`/etc/network/if-pre-up.d/iptables` with these lines:
``` bash
#!/bin/sh
/sbin/iptables-restore < /etc/iptables.up.rules
```
### Add permissions
 `chmod +x /etc/network/if-pre-up.d/iptables`

# Create
``` bash
iptables -t nat -A PREROUTING -i wt0 -p tcp --dport 5000 -j DNAT --to-destination 192.168.0.24:5000
iptables -t nat -A POSTROUTING -p tcp -d 192.168.0.24 --dport 5000 -j MASQUERADE
```
# List
``` bash
iptables -t nat -L POSTROUTING -n -v
```
# Delete
## List with position
``` bash
iptables -t nat -L POSTROUTING -n --line-numbers
```
## Actually delete iptable
``` bash
$lineNumber=4 && \
iptables -t nat -D POSTROUTING $lineNumber
```