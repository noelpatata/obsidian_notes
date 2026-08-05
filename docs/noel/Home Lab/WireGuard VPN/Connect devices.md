# Generate keys
For each device that connects to our VPN, we need a pair of keys.
I generate keys like this:
```bash
umask go=
wg genkey | tee wgserver.key | wg pubkey > wgserver.pub
wg genkey | tee wgclient.key | wg pubkey > wgclient.pub
wg genpsk > wgclient.psk
```
# Add peer
``` bash
VPN_IF="vpn" uci set network.wgmorde="wireguard_${VPN_IF}" uci set network.wgmorde.public_key="$(cat wgmorde.pub)" uci set network.wgmorde.preshared_key="$(cat wgmorde.psk)" uci add_list network.wgmorde.allowed_ips="192.168.9.3/32" uci commit network service network restart
```
# Android
For connecting my phone I can use `qrencode` package to generate a QR code of my keys, and scan it in the WireGuard phone application:
``` bash
cat << EOF | qrencode -t ansiutf8 [Interface] PrivateKey = $(cat wgclient.key) Address = 192.168.9.2/32 DNS = 192.168.1.1 [Peer] PublicKey = $(cat wgserver.pub) PresharedKey = $(cat wgclient.psk) Endpoint = YOUR_PUBLIC_IP:51820 AllowedIPs = 192.168.0.0/16 PersistentKeepalive = 25 EOF
```
# Arch linux
## Install Wireguard
```bash
sudo pacman -S wireguard-tools
```
## Setup
Create the file `/etc/wireguard/wg0.conf`
```bash
[Interface]
PrivateKey = PASTE_WGMORDE_KEY
Address = 192.168.9.3/32
DNS = 192.168.1.1

[Peer]
PublicKey = PASTE_WGSERVER_PUB
PresharedKey = PASTE_WGMORDE_PSK
Endpoint = YOUR_PUBLIC_IP:51820
AllowedIPs = 192.168.0.0/16
PersistentKeepalive = 25
```
## Connect to VPN
``` bash
sudo wg-quick up wg0
```
## Disconnect to VPN
``` bash
sudo wg-quick down wg0
```
## Troubleshooting
You might need to run `sudo systemctl restart systemd-resolved` before connecting to the vpn.