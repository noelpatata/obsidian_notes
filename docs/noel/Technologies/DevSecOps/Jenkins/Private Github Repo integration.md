In Jenkins you can configure the Script file `Jenkinsfile` to get retrieved from the repository.
But if the Github repo is private, you won't be able to reach it.
- That's why you should generate a paired-keys:
`ssh-keygen -t ed25519 -C "jenkins-lanoiapintada" -f jenkins_lanoiapintada -N ""`
- Then add the public key to the Github repo [here](https://github.com/noelpatata/lanoiapintada/settings/keys)
- Add the private key as a "SSH Username with Private key" credential in Jenkins
- And also of course add the private key to `ssh_known_hosts`:
`ssh-keyscan -t ed25519 github.com | tee -a /etc/ssh/ssh_known_hosts`
This command works because the key I generated matches the ssh-keyscan filter and because my Alpine runs over root.
