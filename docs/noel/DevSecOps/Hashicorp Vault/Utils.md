# enable kv secrets
``` bash
vault secrets enable -path=secrets -version=2 kv
```
# define a policy
p.hcl:
```
path "secrets/data/wallettracker" {
  capabilities = ["create", "update", "read"]
}
```
# create the policy
``` bash
vault policy write wallet-tracker-policy p.hcl
```
# create token for policy
``` bash
vault token create -policy=wallet-tracker-policy -ttl=87600h -display-name="wallettracker"
```
# create secrets
``` bash
vault kv put secrets/data/wallettracker \
    MARIADB_ROOT_PASSWORD="adminadmin" \
    MARIADB_DATABASE="wallet_tracker"
```

```
