``` bash
kubectl create secret docker-registry harbor-secret \
  --docker-server=registry.downops.win \
  --docker-username='USER' \
  --docker-password='TOKEN' \
  -n default
  ```