# Jenkins plugin
Install OWASP Dependency Check plugin.
# OWSAP Dependency Tool
Add the Dependency-Check installation
![[Pasted image 20260525164946.png]]
# NVD Api Key
In this [link](https://nvd.nist.gov/developers/request-an-api-key) you can request the NVD api key.
Using this key avoids the API's rate limit when fetching vulnerabilities.
# Jenkinsfile
And reference it in the Jenkinsfile:
``` yaml
stage('Dependency Check') {
	steps {
		sh 'mkdir -p dependency-check-report'
		dependencyCheck additionalArguments: "--scan app --project wallet-tracker-api --format ALL --out dependency-check-report --nvdApiKey ${env.NVD_API_KEY}", odcInstallation: 'owasp dependency check 12.2.2'
	}
	post {
		always {
			archiveArtifacts artifacts: 'dependency-check-report/**/*', allowEmptyArchive: true	
		}
	}
}
```