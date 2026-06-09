``` bash
vault operator inint
```
then save the token and the unseal keys.
after that run:
``` bash
vault operator unseal [KEY 1] \
vault operator unseal [KEY 2] \
vault operator unseal [KEY 3] \
vault login [TOKEN]
```

enable secrets:
``` bash
vault secrets enable -path=secret kv-v2
```

put secrets in vault:
``` bash
vault kv put secret/wallet-tracker/config MARIADB_ROOT_PASSWORD="your_password"  DATABASE_NAME="wallet_tracker"
```