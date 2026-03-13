# Setup python virtual environment

``` bash
python -m venv .venv \
source .venv/bin/activate
```

# Install dependencies

```bash
apk add mariadb-dev gcc musl-dev python3-dev build-base linux-headers py3-pip
pip install -r requirements.txt
```

# Setup uwsgi

Create app.ini file:
``` bash
[uwsgi]
module = main:app
master = true
processes = 4
socket = /tmp/app.sock
chmod-socket = 660
chown-socket = nginx:nginx
vacuum = true
die-on-term = true
log.to = /var/log/wallettracker.log (REVISAR NO SE SI SE LLAMA ASI EXACTAMENTE)
```

Then test it with:
```bash
uwsgi --ini app.ini
```

# Setup nginx

``` bash
apk add nginx
```

Create certificates:
``` bash
mkdir -p /etc/nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/wallettracker.key \
  -out /etc/nginx/ssl/wallettracker.crt
```

Setup virtualhost in `/etc/nginx/http.d/wallettracker.conf`:
``` bash
server {
    listen 443 ssl;
    server_name [Server IP];

    ssl_certificate /etc/nginx/ssl/wallettracker.crt;
    ssl_certificate_key /etc/nginx/ssl/wallettracker.key;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/tmp/app.sock;
    }
}

server {
    listen 80;
    server_name [Server IP];
    return 301 https://$host$request_uri;
}
```

After configuring the virtual host, we run `nginx` to start the web server.

# Create OpenRC service
First we create the log files:
```bash
mkdir -p /var/logs
touch /var/logs/wallettracker.log
chown nginx:nginx /var/logs/wallettracker.log
chmod 644 /var/logs/wallettracker.log
```
Then we create the service `/etc/init.d/wallettracker`:
``` bash
#!/sbin/openrc-run
description="WalletTracker uWSGI"
directory="/srv/WalletTrackerAPI/app"
pidfile="/run/wallettracker.pid"
user="nginx"
group="nginx"
VENV_PATH="/srv/WalletTrackerAPI/app/.venv"

export WALLET_TRACKER_DB_USER=root
export MYSQL_ROOT_PASSWORD=PNe4Wq0oqvx87oGs6L7Fku9vf
export WALLET_TRACKER_DB_HOST=192.168.0.24
export MYSQL_DATABASE=wallet_tracker
export WALLET_TRACKER_SECRET=s0m3r4nd0mt3xt

command="${VENV_PATH}/bin/uwsgi"
command_args="--ini ${directory}/uwsgi.ini"
command_background="yes"

start_pre() {
    checkpath --directory --owner $user:$group ${pidfile%/*}
}
```

``` bash
chmod +x /etc/init.d/wallettracker
```

Load the service:
``` bash
rc-update add wallettracker default
rc-service wallettracker start
rc-service wallettracker status
```



