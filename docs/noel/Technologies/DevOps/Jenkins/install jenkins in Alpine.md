install jdk and jre
``` bash
apk add openjdk21 openjdk21-jre
```
add repos
```bash
wget -O /etc/apk/keys/jenkins-ci.org.key https://pkg.jenkins.io/redhat-stable/jenkins-ci.org.key \
echo "https://pkg.jenkins.io/redhat-stable" >> /etc/apk/repositories
```
install and run jenkins
``` bash
apk add jenkins
rc-update add jenkins
rc-service jenkins start
```
