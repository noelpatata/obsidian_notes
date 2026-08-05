# Installation and Setup
## Installation
``` docker
name: Dependency-Track
services:
  apiserver:
    image: ghcr.io/dependencytrack/apiserver:5.0.2
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      DT_DATASOURCE_URL: "jdbc:postgresql://postgres:5432/dtrack"
      DT_DATASOURCE_USERNAME: "dtrack"
      DT_DATASOURCE_PASSWORD: "dtrack"
    ports:
    - "0.0.0.0:8080:8080"
    volumes:
    - "apiserver-data:/data"
    restart: unless-stopped

  frontend:
    image: ghcr.io/dependencytrack/frontend:5.0.2
    environment:
      API_BASE_URL: "http://192.168.0.67:8080"
    ports:
    - "0.0.0.0:8081:8080"
    restart: unless-stopped

  postgres:
    image: postgres:18-alpine
    environment:
      POSTGRES_DB: "dtrack"
      POSTGRES_USER: "dtrack"
      POSTGRES_PASSWORD: "dtrack"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 5s
      timeout: 3s
      retries: 3
    volumes:
    - "postgres-data:/var/lib/postgresql"

volumes:
  apiserver-data: {}
  postgres-data: {}
```
## Create a project
Projects > Create Project.
## Create the API key
Administration > Access Management > Teams.
And create a token for the Team you want.
## Enable different vulnerability sources
NVD is enabled by default, but we also have Github and Osv.
Go to Administration > Vulnerability Sources, enable them and then click over "Mirror now" to update the vulnerability sources.

# Sonarqube Integration
 In this [link](https://github.com/noelpatata/dependency_tracker_plugin) you can find the plugin used to fetch Dependency Track results into Sonarqube's UI.