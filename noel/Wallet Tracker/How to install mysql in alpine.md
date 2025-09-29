# Installation

```bash
apk add mariadb mariadb-client
myql_install_db --user=mysql --datadir=/var/lib/mysql
re-service mariadb start
mysql_install_db
/etc/init.d/mariadb setup
rc-service mariadb start
rc-update add mariadb
```
# User Setup

Inside mysql, create the user:
```bash
CREATE USER 'root'@'192.168.0.21' IDENTIFIED BY 'PNe4Wq0oqvx87oGs6L7Fku9vf';

-- Grant all privileges
GRANT ALL PRIVILEGES ON *.* TO 'root'@'192.168.0.21' WITH GRANT OPTION;

FLUSH PRIVILEGES;
```

# Utils

- To log in mysql just  `mysql -u root -p`
- Restart mysql service `rc-service mariadb restart`
- Execute .sql file in mariadb `mysql -u root -p < /root/my_script.sql`
- List open sockets `netstat -tlnp`