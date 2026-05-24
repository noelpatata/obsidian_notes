# enable kv secrets
``` bash
vault secrets enable -path=secrets -version=2 kv
```
# create a policy
p.hcl:
```
path "secrets/data/wallettracker" {
  capabilities = ["create", "update", "read"]
}
```
create the policy
``` bash
vault policy write wallet-tracker-policy p.hcl
```
# create token for policy
``` bash
vault token create -policy=wallet-tracker-policy
```
# create secrets
``` bash
vault kv put secrets/data/wallettracker \
    MARIADB_ROOT_PASSWORD="adminadmin" \
    MARIADB_DATABASE="wallet_tracker"
    ```
