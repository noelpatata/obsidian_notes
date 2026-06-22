# change timezone
``` bash
apk add tzdata && \
cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime && \
echo "Europe/Madrid" > /etc/timezone
```