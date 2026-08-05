JenkinsFile
``` yaml
stage('Push Docker Image') {

steps {

withCredentials([usernamePassword(credentialsId: params.DOCKER_REGISTRY_CREDENTIALS, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {

sh '''

echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin ${REGISTRY}

docker tag wallet-tracker ${REGISTRY}/wallet-tracker:${IMAGE_VERSION}

docker push ${REGISTRY}/wallet-tracker:${IMAGE_VERSION}

docker logout ${REGISTRY}

'''
}
}
}
```