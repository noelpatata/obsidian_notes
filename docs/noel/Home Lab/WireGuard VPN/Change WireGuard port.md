``` bash
NEW_PORT="2222"
uci set network.vpn.listen_port="${NEW_PORT}"
uci set firewall.wg.dest_port="${NEW_PORT}"
uci commit network
uci commit firewall
service network restart
service firewall restart
```