First we build our Dockerfile:
``` bash
docker build -t wallet_tracker_mysql .
```

Then we create the container

``` bash
docker run -d  --name wallet_tracker_mysql -e MYSQL_ROOT_PASSWORD=adminadmin -e MYSQL_DATABASE=wallet_tracker -e MYSQL_USER=root -e MYSQL_PASSWORD=adminadmin -p 3306:3306  wallet_tracker_mysql
```

Start it
``` bash
docker start wallet_tracker_mysql
```