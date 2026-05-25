# Vault token
All secrets inside the vault must rotate automatically.
The following assets depend on a VAULT_TOKEN that expires, meaning that at the moment someone manually updates that token, the following assets are affected:
- Github Secrets
- Jenkins Credentials
# SonarQube token
Jenkins Credentials