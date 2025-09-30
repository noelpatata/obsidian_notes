## 1️⃣ Modern Workflow Overview

**Goal:** Automate build → test → deploy, so you never SSH in manually.

Modern workflow:

1. **Dockerize everything** (Flask app + MySQL, optionally Redis, etc.).
    
2. **Build Docker images** in GitHub Actions when you push/merge.
    
3. **Push images to Docker Hub** or any registry.
    
4. **Deploy automatically** using Docker Compose and Watchtower on your Proxmox server.
    

---

## 2️⃣ Dockerizing Your Flask App

**Dockerfile (Flask app):**

```dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY ./app ./app

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app/main.py"]
```

---

## 3️⃣ Docker Compose for Flask + MySQL

You already have a custom MySQL Dockerfile. Let’s combine everything:

**docker-compose.yml:**

```yaml
version: "3.9"

services:
  db:
    build:
      context: ./mysql
      dockerfile: Dockerfile
    container_name: myapp-db
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: mydb
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql

  web:
    build: .
    container_name: myapp-web
    environment:
      DATABASE_URL: mysql+pymysql://root:rootpassword@db:3306/mydb
    ports:
      - "5000:5000"
    depends_on:
      - db
    restart: always

volumes:
  db_data:
```

> Note: With this setup, `web` will connect to MySQL via the Docker network `db:3306`.

---

## 4️⃣ GitHub Actions CI/CD Pipeline

Here’s a simple workflow that builds, tests, and pushes your Docker image on **push to main**.

**.github/workflows/deploy.yml:**

```yaml
name: Build & Deploy

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Log in to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build Docker image
      run: docker build -t mydockerhubuser/my-flask-app:latest .

    - name: Push Docker image
      run: docker push mydockerhubuser/my-flask-app:latest
```

**Secrets** to add in GitHub:

- `DOCKER_USERNAME` → your Docker Hub username
    
- `DOCKER_PASSWORD` → your Docker Hub password
    

> After this, your server can use **Watchtower** to automatically pull the latest image and restart the container.

---

## 5️⃣ Watchtower on Production

Watchtower monitors containers and updates them when a new image is pushed:

```bash
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  --cleanup \
  --interval 30
```

- `--interval 30` → check every 30 seconds.
    
- `--cleanup` → remove old images automatically.
    

Your `docker-compose.yml` can then just start the app with the `latest` tag. Watchtower will auto-update when GitHub Actions pushes a new image.

---

## ✅ 6️⃣ Advantages of This Setup

- **No manual SSH deployments**: GitHub Actions + Watchtower handles it.
    
- **Versioned deployments**: Every push to `main` triggers a new container build.
    
- **Reproducible environments**: Docker ensures Flask and MySQL versions are consistent.
    
- **Clean rollback**: Previous images are retained; you can manually revert if needed.
    

---

If you want, I can **write the full folder structure + Dockerfiles + Compose + Watchtower setup** specifically tailored to your Flask + MySQL setup, ready to push to GitHub and deploy automatically.

Do you want me to do that next?