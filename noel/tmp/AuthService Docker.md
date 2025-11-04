# Docker mariadb

database template
``` bash
CREATE DATABASE IF NOT EXISTS auth;  
USE auth;  
CREATE TABLE User (  
  id BIGINT NOT NULL AUTO_INCREMENT,  
  username VARCHAR(45) NOT NULL,  
  password LONGTEXT NULL,  
  salt LONGTEXT NULL,  
  PRIMARY KEY (id),  
  UNIQUE INDEX username_UNIQUE (username ASC) VISIBLE  
);
```
dockerfile
``` bash
FROM mariadb:latest  
RUN apt-get update && \  
    apt-get install -y gettext-base  
  
COPY init.sql.template /docker-entrypoint-initdb.d/init.sql.template
```
build image
``` bash
docker build -t cmariadb 
```
run container
``` bash
docker run -d --name mariadb -e MARIADB_DATABASE=auth -e MARIADB_ROOT_PASSWORD=adminadmin cmariadb
```