
``` bash
iptables -t nat -A PREROUTING -i wt0 -p tcp --dport 5000 -j DNAT --to-destination 192.168.0.24:5000
sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
iptables -t nat -A POSTROUTING -p tcp -d 192.168.0.24 --dport 5000 -j MASQUERADE
```
Now the machine that executes this will redirect to port 5000 on ip 192.168.0.24