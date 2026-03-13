(login as root)
``` bash
apk add openssh
rc-update add sshd
rc-service sshd start
```
edit `/etc/ssh/sshd_config`
set `PermitRootLogin yes` (to login as root with password)