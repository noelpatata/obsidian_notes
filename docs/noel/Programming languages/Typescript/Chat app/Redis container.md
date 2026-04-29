
### Start container with password 
``` bash
sudo docker run --name redis_chat -p 6379:6379 -d redis redis-server --requirepass s
```

### Interact with redis cli
``` bash
docker exec -it my-redis redis-cli
```