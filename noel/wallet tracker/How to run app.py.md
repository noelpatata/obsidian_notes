Check the requirements.txt:
``` txt
flask==3.1.0
flask_sqlalchemy==3.1.1
PyJWT==2.10.1
mysqlclient==2.2.6
uwsgi==2.0.28 # <-- for windows
cryptography==44.0.0
#waitress==3.0.2 # <-- for linux
```

# Linux
```
uwsgi --http 127.0.0.1:5051 --master -p 4 -w app:app
```

# Windows
``` bash
waitress-serve --host 127.0.0.1 app:app
```