# extract pem from k3s service.key
``` bash
sudo openssl rsa -in /var/lib/rancher/k3s/server/tls/service.key -pubout -out k3s-pub.pem
```
# copy key to vault
``` bash
VAULT_POD=$(kubectl get pod -l app=vault -o jsonpath='{.items[0].metadata.name}') \
kubectl cp k3s-pub.pem $VAULT_POD:/tmp/k3s-pub.pem
```
# authenticate with token
``` bash
kubectl exec -it deployment/vault -- vault write auth/jwt/config \ jwt_validation_pubkeys=@/tmp/k3s-pub.pem \ issuer="https://kubernetes.default.svc.cluster.local"
```
# create role
``` bash
kubectl exec -it deployment/vault -- vault write auth/jwt/role/mariadb \ role_type="jwt" \ bound_audiences="https://kubernetes.default.svc.cluster.local,k3s" \ user_claim="sub" \ bound_subject="system:serviceaccount:default:default" \ policies="wallettracker-policy" \ ttl="1h"
```