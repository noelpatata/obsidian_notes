This helm is like a package manager but for sort of "modules" I use in my infra, for example, i want to implement Hashicorp vault because my secrets are stored in a vault, i install the "hashicorp" plugin with helm
# install helm
``` bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```
# install hashicorp vault
``` bash
helm repo add hashicorp https://helm.releases.hashicorp.com \
helm repo update \
helm install vault hashicorp/vault \
  --set "injector.externalVaultAddr=https://vault.downops.win"
```

# authentication
`/route/to/kubernetes.crt` is in your kubernetes cluster, in k3s's case is in `/var/lib/rancher/k3s/server/tls/server-ca.crt`

``` bash
vault auth enable kubernetes \
vault write auth/kubernetes/config \ kubernetes_host="https://100.96.193.254:6443" \ kubernetes_ca_cert=/route/to/kubernetes.crt \ issuer="https://kubernetes.default.svc.cluster.local" \
```
## create policy
``` bash
cat <<EOF > wallet-policy.hcl path "secret/data/wallettracker/*" { capabilities = ["read"] } EOF \
vault policy write wallet-policy wallet-policy.hcl
```

## create role
``` bash
vault write auth/kubernetes/role/wallet-role \
    bound_service_account_names=wallet-sa \
    bound_service_account_namespaces=default \
    policies=wallet-policy \
    ttl=24h
```