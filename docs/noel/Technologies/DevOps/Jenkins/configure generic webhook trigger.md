create the job
check the webhook
set the token to the webhook

create an HTTP request to trigger the webhool:
``` bash
curl -u "noelnoel:111caa56135aa9b5b4b8d2c10357f849c6" "https://jenkins.downops.win/generic-webhook-trigger/invoke" -H 'Authorization: Bearer SIC%4qwH67t!G@z%Nwnr6O6Cr'
```
even though this is a webhook, i still have to login, in this case i used the token.
then i have to add the query param to add the **webhook token**

``` bash
pipeline {
    agent any
    build 'wallettrackercd'
    stages {
        stage('Triggered') {
            steps {
                echo "✅ Webhook triggered successfully!"
            }
        }
    }
}
```