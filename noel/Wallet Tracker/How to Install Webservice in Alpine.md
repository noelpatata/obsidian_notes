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
module = app:app          ; Flask app entry point
master = true             ; Enable master process
processes = 4             ; Number of worker processes
socket = /tmp/app.sock     ; Unix socket for Nginx
chmod-socket = 660        ; Socket permissions
chown-socket = nginx:nginx; Socket owner
vacuum = true             ; Clean up socket on exit
die-on-term = true
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
  -keyout /etc/nginx/ssl/flask.key \
  -out /etc/nginx/ssl/flask.crt
```

Setup virtualhost in `/etc/nginx/http.d/wallettracker.conf`:
``` bash
server {
    listen 443 ssl;
    server_name 192.168.0.21;

    ssl_certificate /etc/nginx/ssl/wallettracker.crt;
    ssl_certificate_key /etc/nginx/ssl/wallettracker.key;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/tmp/app.sock;
    }
}

server {
    listen 80;
    server_name 192.168.0.21;
    return 301 https://$host$request_uri;
}
```

After configuring the virtual host, we run `nginx` to start the web server.

# Create OpenRC service

First we create the file `/etc/init.d/wallettracker`:
``` bash
#!/sbin/openrc-run
description="WalletTracker uWSGI"
directory="/srv/WalletTrackerAPI"
pidfile="/run/wallettracker.pid"
user="nginx"
group="nginx"
VENV_PATH="/srv/WalletTrackerAPI/.venv"

export WALLET_TRACKER_DB_USER=root
export WALLET_TRACKER_DB_PASSWORD=PNe4Wq0oqvx87oGs6L7Fku9vf
export WALLET_TRACKER_DB_HOST=192.168.0.24
export WALLET_TRACKER_DB_NAME=wallet_tracker
export WALLET_TRACKER_SECRET=s0m3r4nd0mt3xt

command="${VENV_PATH}/bin/uwsgi"
command_args="--ini ${directory}/app.ini"
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



