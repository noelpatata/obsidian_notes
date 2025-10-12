create the job
check the webhook
set the token to the webhook

create an HTTP request to trigger the webhool:
``` bash
curl -u "$username:$apitoken" "$url" -H 'Authorization: Bearer $token'
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