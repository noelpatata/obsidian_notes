create a jenkins job
inside, configure a webhook
set the token to the webhook

create an HTTP request to trigger the webhook:
```bash
curl -u "${{ env.JENKINS_USERNAME }}:${{ env.JENKINS_API_TOKEN }}" \
	"https://${{ env.JENKINS_HOSTNAME }}/generic-webhook-trigger/invoke" \
	-H "Authorization: Bearer ${{ env.JENKINS_CD_SECRET }}" \
	--data-urlencode "GIT_BRANCH=$GIT_BRANCH&IMAGE_VERSION=latest&REGISTRY_IP=${{ env.REGISTRY_IP }}"
```
``` bash
curl -u "noel:116c832125575ef47efb7ecdc8ff13d24a" \
    "https://jenkins.downops.win/generic-webhook-trigger/invoke" \
    -H "Authorization: Bearer 994dE88BpSSLzdUwC1ZW2AvQz" \
    --data-urlencode "GIT_BRANCH=main&IMAGE_VERSION=latest&REGISTRY_IP=100.96.42.211"
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
                echo "Webhook triggered successfully!"
            }
        }
    }
}
```