create the job
check the webhook
set the token to the webhook

create an HTTP request to trigger the webhool:
``` bash
curl -u "noelnoel:111caa56135aa9b5b4b8d2c10357f849c6" "http://jenkins.downops.win/generic-webhook-trigger/invoke"
```
even though this is a webhook, i still have to login, in this case i used the token.
then i have to add the query param to add the **webhook token**