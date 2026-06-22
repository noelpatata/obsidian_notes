When I restart the container the postgres database is down for some reason.
I solved this issue by running these two commands:
``` bash
docker compose up -d postgres && \
docker compose restart apiserver
```