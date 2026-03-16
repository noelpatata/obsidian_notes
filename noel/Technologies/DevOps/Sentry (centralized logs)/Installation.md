# Sentry Self-Hosted Installation Guide - Alpine Linux

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [System Preparation](#system-preparation)
3. [Docker Installation](#docker-installation)
4. [Sentry Installation](#sentry-installation)
5. [Configuration](#configuration)
6. [SSL/TLS Setup (Optional)](#ssltls-setup-optional)
7. [Maintenance](#maintenance)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Hardware Requirements (Proxmox VM/CT)

- **CPU:** 2 cores minimum, 4 cores recommended
- **RAM:** 4GB minimum, 8GB recommended (Sentry is memory-intensive)
- **Disk:** 50GB minimum, 100GB recommended
- **Network:** Static IP recommended

### Software Requirements

- Alpine Linux 3.18 or newer
- Internet connection for downloading packages

---

## System Preparation
### 1. Update System

```bash
# Update package index
apk update

# Upgrade existing packages
apk upgrade

# Install essential tools
apk add curl wget git bash nano sudo
```

### 2. Configure Repositories

```bash
# Edit repositories file
nano /etc/apk/repositories

# Ensure these lines are uncommented:
http://dl-cdn.alpinelinux.org/alpine/v3.18/main
http://dl-cdn.alpinelinux.org/alpine/v3.18/community

# Update again
apk update
```

---

## Docker Installation

### 1. Install Docker

```bash
# Install Docker
apk add docker docker-compose

# Enable Docker service
rc-update add docker boot

# Start Docker service
service docker start

# Verify installation
docker --version
docker-compose --version
```

### 2. Configure Docker

```bash
# Add current user to docker group (if not root)
addgroup yourusername docker

# Configure Docker daemon
cat > /etc/docker/daemon.json <<EOF
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
EOF

# Restart Docker
service docker restart
```

---

## Sentry Installation

### 1. Download Sentry Self-Hosted

```bash
# Create directory for Sentry
mkdir -p /opt/sentry
cd /opt/sentry

# Clone Sentry self-hosted repository
git clone https://github.com/getsentry/self-hosted.git .

# Check latest stable version
git tag -l | tail -5

# Checkout latest stable (optional, or use main branch)
# git checkout 23.12.0
```

### 2. Configure System Resources

```bash
# Increase vm.max_map_count for Elasticsearch
echo "vm.max_map_count=262144" >> /etc/sysctl.conf
sysctl -p

# Make it permanent across reboots
echo "vm.max_map_count=262144" > /etc/sysctl.d/99-sentry.conf
```

### 3. Pre-Installation Configuration

```bash
# Edit environment variables (optional)
nano .env

# Key settings to review:
# SENTRY_IMAGE=getsentry/sentry:latest
# SENTRY_EVENT_RETENTION_DAYS=90
# SENTRY_MAIL_HOST=your-smtp-server
```

### 4. Run Installation Script

```bash
# Make install script executable
chmod +x install.sh

# Run installation (this will take 10-20 minutes)
./install.sh

# During installation you'll be prompted to:
# 1. Create admin account
# 2. Set admin password
# 3. Confirm configuration

# Example:
# Email: admin@yourdomain.com
# Password: YourSecurePassword123!
```

**Installation Output:**

```
-----------------------------------------------------------------
You're all done! Run the following command to get Sentry running:

  docker-compose up -d

-----------------------------------------------------------------
```

### 5. Start Sentry

```bash
# Start all Sentry services
docker-compose up -d

# Check status
docker-compose ps

# You should see services like:
# - sentry-web
# - sentry-worker
# - sentry-cron
# - postgres
# - redis
# - etc.
```

### 6. Verify Installation

```bash
# Check logs
docker-compose logs -f web

# Wait for this message:
# "Listening at: http://0.0.0.0:9000"

# Check if Sentry is accessible
curl http://localhost:9000
```

**Access Sentry Web Interface:**

- Open browser: `http://your-alpine-ip:9000`
- Login with admin credentials created during installation

---

## Configuration

### 1. Initial Sentry Setup (Web Interface)

**First Login:**

1. Navigate to `http://your-ip:9000`
2. Login with admin credentials
3. Complete setup wizard:
    - Organization name: "Your Company"
    - Root URL: `http://your-ip:9000` (or domain)
    - Admin email settings

### 2. Create Project for Android App

```
1. Click "Projects" → "Create Project"
2. Select platform: "Android"
3. Project name: "Wallet Tracker"
4. Team: Default
5. Alert settings: Default
6. Click "Create Project"
7. Copy the DSN (Data Source Name) - you'll need this for Android
   Example: http://abc123def456@your-ip:9000/1
```

### 3. Configure Email Notifications (Optional)

```bash
# Stop services
cd /opt/sentry
docker-compose down

# Edit sentry.conf.py
nano sentry/sentry.conf.py

# Add email configuration:
# SENTRY_OPTIONS["mail.backend"] = "smtp"
# SENTRY_OPTIONS["mail.host"] = "smtp.gmail.com"
# SENTRY_OPTIONS["mail.port"] = 587
# SENTRY_OPTIONS["mail.username"] = "your-email@gmail.com"
# SENTRY_OPTIONS["mail.password"] = "your-app-password"
# SENTRY_OPTIONS["mail.use-tls"] = True
# SENTRY_OPTIONS["mail.from"] = "sentry@yourdomain.com"

# Restart services
docker-compose up -d
```

### 4. Configure Data Retention

```bash
# Edit .env file
nano .env

# Set retention period (days)
SENTRY_EVENT_RETENTION_DAYS=90

# Restart to apply changes
docker-compose restart
```

### 5. Configure Performance Monitoring

**In Sentry Web UI:**

```
1. Go to Settings → Projects → Wallet Tracker
2. Click "Performance"
3. Enable "Performance Monitoring"
4. Set sample rate: 1.0 (100% for development, 0.1-0.2 for production)
5. Save changes
```

---

## SSL/TLS Setup (Optional)

### Option 1: Nginx Reverse Proxy with Let's Encrypt

```bash
# Install Nginx
apk add nginx certbot certbot-nginx

# Create Nginx configuration
cat > /etc/nginx/http.d/sentry.conf <<EOF
server {
    listen 80;
    server_name sentry.yourdomain.com;

    location / {
        proxy_pass http://localhost:9000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Start Nginx
rc-update add nginx
service nginx start

# Get SSL certificate
certbot --nginx -d sentry.yourdomain.com

# Nginx will be automatically configured with SSL
```
---

## Maintenance

### 1. Backup Sentry Data

```bash
#!/bin/bash
# /opt/sentry/backup.sh

BACKUP_DIR="/opt/sentry-backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup Postgres database
docker-compose exec -T postgres pg_dump -U postgres postgres > \
    $BACKUP_DIR/sentry_postgres_$DATE.sql

# Backup volumes
docker run --rm \
    -v sentry-postgres:/source \
    -v $BACKUP_DIR:/backup \
    alpine tar czf /backup/sentry_postgres_volume_$DATE.tar.gz -C /source .

# Keep only last 7 days of backups
find $BACKUP_DIR -type f -mtime +7 -delete

echo "Backup completed: $DATE"
```

```bash
# Make backup script executable
chmod +x /opt/sentry/backup.sh

# Add to crontab for daily backups
crontab -e

# Add this line (backup at 2 AM daily):
0 2 * * * /opt/sentry/backup.sh >> /var/log/sentry-backup.log 2>&1
```

### 2. Update Sentry

```bash
cd /opt/sentry

# Pull latest changes
git pull

# Stop services
docker-compose down

# Pull new images
docker-compose pull

# Run install script again
./install.sh

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f web
```

### 3. Clean Up Old Data

```bash
# Sentry automatically cleans up based on SENTRY_EVENT_RETENTION_DAYS
# But you can manually trigger cleanup:

docker-compose exec web sentry cleanup --days 30

# Clean up Docker images
docker system prune -a
```

### 4. Monitor Resource Usage

```bash
# Check disk usage
df -h

# Check Docker container stats
docker stats

# Check Sentry-specific logs
docker-compose logs -f --tail=100 web
docker-compose logs -f --tail=100 worker

# Monitor Postgres size
docker-compose exec postgres psql -U postgres -c \
    "SELECT pg_size_pretty(pg_database_size('postgres'));"
```

---

## Troubleshooting

### Issue 1: Services Won't Start

```bash
# Check Docker service
service docker status

# Check container logs
docker-compose logs web
docker-compose logs worker

# Restart all services
docker-compose restart

# If complete reset needed:
docker-compose down
docker-compose up -d
```

### Issue 2: Out of Memory

```bash
# Check memory usage
free -h

# Increase swap (temporary fix)
dd if=/dev/zero of=/swapfile bs=1G count=4
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

# Make swap permanent
echo "/swapfile none swap sw 0 0" >> /etc/fstab
```

### Issue 3: Disk Space Full

```bash
# Check disk usage
df -h
du -sh /var/lib/docker/*

# Clean Docker
docker system prune -a --volumes

# Reduce retention period
nano .env
# Set: SENTRY_EVENT_RETENTION_DAYS=30
docker-compose restart
```

### Issue 4: Can't Access Web Interface

```bash
# Check if port 9000 is open
netstat -tulpn | grep 9000

# Check firewall (if using)
iptables -L

# Check if web service is running
docker-compose ps web

# Check web logs
docker-compose logs web
```

### Issue 5: Database Connection Issues

```bash
# Check Postgres status
docker-compose ps postgres

# Access Postgres shell
docker-compose exec postgres psql -U postgres

# Check database size
\l+

# Exit Postgres
\q

# Restart Postgres
docker-compose restart postgres
```

### Issue 6: Worker Not Processing Events

```bash
# Check worker logs
docker-compose logs worker

# Restart workers
docker-compose restart worker

# Scale workers if needed
docker-compose up -d --scale worker=3
```

---

## Advanced Configuration

### 1. Configure Firewall

```bash
# Install ufw
apk add ufw

# Default policies
ufw default deny incoming
ufw default allow outgoing

# Allow SSH
ufw allow 22/tcp

# Allow Sentry web interface
ufw allow 9000/tcp

# If using SSL:
ufw allow 80/tcp
ufw allow 443/tcp

# Enable firewall
ufw enable

# Check status
ufw status
```

### 2. Set Up Monitoring (Optional)

```bash
# Install monitoring tools
apk add htop iotop

# Create monitoring script
cat > /opt/sentry/monitor.sh <<'EOF'
#!/bin/bash
echo "=== Docker Containers ==="
docker-compose ps

echo -e "\n=== Resource Usage ==="
docker stats --no-stream

echo -e "\n=== Disk Usage ==="
df -h

echo -e "\n=== Sentry Queue Status ==="
docker-compose exec -T web sentry queues list
EOF

chmod +x /opt/sentry/monitor.sh

# Run monitoring
/opt/sentry/monitor.sh
```

### 3. Configure Log Rotation

```bash
# Create logrotate configuration
cat > /etc/logrotate.d/sentry <<EOF
/var/log/sentry/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 root root
    sharedscripts
}
EOF
```

---

## Performance Tuning

### 1. Optimize Docker Compose

```bash
cd /opt/sentry

# Edit docker-compose.override.yml (create if doesn't exist)
cat > docker-compose.override.yml <<EOF
version: '3.4'

services:
  web:
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G

  worker:
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
EOF

# Restart to apply
docker-compose up -d
```

### 2. Optimize Postgres

```bash
# Edit Postgres configuration
docker-compose exec postgres bash

# Inside container:
cat >> /var/lib/postgresql/data/postgresql.conf <<EOF
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 128MB
EOF

exit

# Restart Postgres
docker-compose restart postgres
```

---

## Quick Reference Commands

```bash
# Start Sentry
cd /opt/sentry && docker-compose up -d

# Stop Sentry
cd /opt/sentry && docker-compose down

# Restart Sentry
cd /opt/sentry && docker-compose restart

# View logs
cd /opt/sentry && docker-compose logs -f

# Check status
cd /opt/sentry && docker-compose ps

# Access Sentry shell
cd /opt/sentry && docker-compose exec web sentry shell

# Create superuser
cd /opt/sentry && docker-compose exec web sentry createuser

# Run cleanup
cd /opt/sentry && docker-compose exec web sentry cleanup --days 30

# Backup database
cd /opt/sentry && docker-compose exec postgres pg_dump -U postgres postgres > backup.sql

# Update Sentry
cd /opt/sentry && git pull && docker-compose pull && docker-compose up -d
```

---

## Post-Installation Checklist

- [ ] Sentry web interface accessible at `http://your-ip:9000`
- [ ] Admin account created and can login
- [ ] Android project created in Sentry
- [ ] DSN copied for Android integration
- [ ] Email notifications configured (optional)
- [ ] SSL/TLS configured (optional but recommended)
- [ ] Firewall rules configured
- [ ] Backup script created and scheduled
- [ ] Resource monitoring set up
- [ ] Documentation of admin credentials stored securely

---

## Security Best Practices

1. **Change default ports** if exposed to internet
2. **Use strong passwords** for admin account
3. **Enable SSL/TLS** for production
4. **Configure firewall** to restrict access
5. **Regular backups** of database and configurations
6. **Keep Sentry updated** to latest stable version
7. **Monitor resource usage** to prevent DoS
8. **Restrict network access** to trusted IPs only
9. **Use secrets management** for sensitive configs
10. **Enable 2FA** for admin accounts (in Sentry UI)

---

## Support and Resources

- **Sentry Documentation:** https://docs.sentry.io/
- **Self-Hosted Repository:** https://github.com/getsentry/self-hosted
- **Community Forum:** https://forum.sentry.io/
- **Discord:** https://discord.gg/sentry

---

**Installation Complete! 🎉**

Your Sentry instance is now ready to receive error reports from your Android application.

Next step: Configure your Android app using the companion guide "Sentry Android Integration Guide".