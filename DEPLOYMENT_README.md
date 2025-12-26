# Pindrop Web Application - Live Server Update Guide

This guide provides step-by-step instructions for updating your live server with fresh database migrations.

## Prerequisites

- Ubuntu server with root/sudo access
- PostgreSQL database already running and configured
- Domain configured and pointing to your server
- Git repository with latest code
- Python virtual environment set up
- Node.js and npm installed locally (for frontend builds)

## Quick Deployment Steps

### **Local Preparation (Before Server Deployment):**

1. **Build frontend locally:**

```bash
cd frontend
npm install
npm run build
cd ..
```

2. **Commit built files:**

```bash
git add .
git commit -m "Build frontend for production deployment"
git push origin main  # Adjust branch if different
```

### **Server Deployment:**

1. **SSH into your server**

```bash
ssh your-user@your-server-ip
```

2. **Navigate to project directory**

```bash
cd /path/to/your/pindrop_web
```

3. **Backup current deployment (recommended)**

```bash
cp -r . ../pindrop_backup_$(date +%Y%m%d_%H%M%S)
```

4. **Pull latest code changes (including built frontend)**

```bash
git pull origin main  # Adjust branch if different
```

5. **Activate virtual environment**

```bash
source venv/bin/activate  # Adjust path if different
```

6. **Install/update dependencies**

```bash
pip install -r requirements.txt
```

7. **Configure environment (if needed)**
   Ensure your `.env` file has production values:

```bash
# Example .env content
SECRET_KEY=your-production-secret-key
DEBUG=False
DB_NAME=pindrop_web_db
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

8. **Run fresh database migrations**

```bash
python manage.py migrate --run-syncdb
```

9. **Create superuser (if needed)**

```bash
python manage.py createsuperuser
```

10. **Collect static files**

```bash
python manage.py collectstatic --noinput
```

11. **Restart services**

```bash
# Restart Django application (adjust service name)
sudo systemctl restart pindrop-web

# Restart Nginx
sudo systemctl restart nginx
```

12. **Verify deployment**

```bash
# Check Django logs
sudo journalctl -u pindrop-web -f

# Test API endpoint
curl https://your-domain.com/api/health/

# Check database
python manage.py dbshell -c "SELECT 1;"
```

## Automated Deployment

Use the provided `deploy.sh` script for automated deployment:

```bash
# Make script executable
chmod +x deploy.sh

# Edit script to set correct paths
nano deploy.sh

# Run deployment
./deploy.sh
```

## Troubleshooting

### Migration Issues

If migrations fail:

```bash
# Check migration status
python manage.py showmigrations

# Reset migrations (CAUTION: This will drop all data)
python manage.py migrate --fake-initial
python manage.py migrate --run-syncdb
```

### Static Files Issues

```bash
# Clear static files cache
rm -rf staticfiles/
python manage.py collectstatic --clear --noinput
```

### Permission Issues

```bash
# Fix permissions
sudo chown -R www-data:www-data /path/to/project
sudo chmod -R 755 /path/to/project
```

### Database Connection Issues

```bash
# Test database connection
python manage.py dbshell

# Check PostgreSQL service
sudo systemctl status postgresql
```

## Environment Variables

Update your production `.env` file with:

- `DEBUG=False`
- `SECRET_KEY` (generate a new secure key)
- `ALLOWED_HOSTS` (include your domain)
- Database credentials for production
- Any API keys for production

## Monitoring

After deployment:

1. Check application logs
2. Monitor database performance
3. Test all critical features
4. Set up log rotation if not already configured

## Rollback

If deployment fails:

```bash
# Restore from backup
cp -r ../pindrop_backup_DATE/* .

# Restart services
sudo systemctl restart pindrop-web
sudo systemctl restart nginx
```
