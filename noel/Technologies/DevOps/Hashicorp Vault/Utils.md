First create a policy for a single path:
``` json
path "secret/data/wallettracker/*" {
  capabilities = ["read"]
}
```

Then create a token

``` bash
vault write sys/auth/token/tune max_lease_ttl=87600h
```

``` bash
vault token revoke hvs.CAESIHR7xtoVuttuzabHJZ7G4N_pNvx-7aIsWJIVoMZI6ScDGh4KHGh2cy51d2U0MVpOUE1EaWNCR1FZT2tDeWkxVjg

```

``` bash
vault token create -policy=wallettracker -ttl=87600h -display-name="wallettracker"
```


