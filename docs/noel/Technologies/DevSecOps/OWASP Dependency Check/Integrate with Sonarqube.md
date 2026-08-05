SonarQube's OWASP Dependency Check's Plugin just reports the data generated in the report.json, in this case, in the Jenkins pipeline.
To visualize this data in SonarQube's UI:
# Install plugin
Here are [the releases](https://github.com/dependency-check/dependency-check-sonar-plugin/releases).
After downloading the `.jar`, we move it to the plugins folder of our sonarqube instance.
``` bash
cp sonar-dependency-check-plugin-6.0.0.jar \
    /var/lib/docker/volumes/sonar_extensions/_data/plugins/
```
Now we restart SonarQube, in my case i run:
`docker restart sonarqube`.