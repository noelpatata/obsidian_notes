We'll need a docker compose with a postgresql and another one for the pgadmin4:
``` bash
sudo docker pull dpage/pgadmin4
sudo docker run -d --name pgadmin -p 5050:80 -e 'PGADMIN_DEFAULT_EMAIL=noel@nnovo.dev' -e 'PGADMIN_DEFAULT_PASSWORD=adminadmin' dpage/pgadmin4
```