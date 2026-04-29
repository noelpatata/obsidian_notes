# Flask app
``` Dockerfile
FROM python:3.12-alpine
RUN apk update && \
apk add --no-cache mariadb-dev gcc musl-dev build-base linux-headers
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apk del gcc musl-dev build-base linux-headers
COPY . .
EXPOSE 5000
CMD ["uwsgi", "--ini", "uwsgi.ini"]
```

- `WORKDIR` the working directory
- `EXPOSE` port exposed to the host
- `RUN` This commands are executed during the build process
- `CMD` This commands run when the container is already executed


# Mysql
``` Dockerfile
FROM mysql:8.0-debian
RUN apt update && apt install -y gettext-base && rm -rf /var/lib/apt/lists/*
COPY sql_schema/init.sql.template /docker-entrypoint-initdb.d/init.sql.template
```

- `FROM` name of the image
- `RUN` run basic commands 
- `COPY`just copy files from the current context inside the container