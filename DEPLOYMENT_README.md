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

1. **Build frontend locally to dist folder:**

```bash
cd frontend
npm install
npm run build  # Builds to dist folder (default Vite output)
cd ..
```

2. **Commit built files (force add since dist is ignored):**

```bash
git add frontend/dist/ --force
git commit -m "Build frontend for production deployment"
git push origin main  # Adjust branch if different
```

**Note:** The `frontend/dist/` folder contains the built frontend files that will be served directly by your web server (Nginx). Since `frontend/dist/` is ignored by `.gitignore`, you need to use `--force` to add it to git.

### **Server Deployment:**

1. **SSH into your server**

```bash
ssh your-user@your-server-ip
```

2. **Navigate to project directory**

```bash
cd /var/www/dev/pindrop_web  # Based on your Nginx config
```

3. **Backup current deployment (recommended)**

```bash
cp -r . ../pindrop_backup_$(date +%Y%m%d_%H%M%S)
```

4. **Pull latest code changes (including built frontend)**

```bash
git pull origin main  # Adjust branch if different
```

5. **Verify frontend files are deployed**

```bash
# Check if frontend/dist exists and has files
ls -la frontend/dist/

# If dist folder is missing, force pull the specific folder
git checkout HEAD -- frontend/dist/
```

6. **Activate virtual environment**

```bash
source myenv/bin/activate  # Based on supervisor config
```

7. **Install/update dependencies**

```bash
pip install -r requirements.txt
```

8. **Configure environment (if needed)**
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
ALLOWED_HOSTS=riderapp.testrunner.co.ke
```

9. **Run fresh database migrations**

```bash
python manage.py migrate --run-syncdb
```

10. **Create superuser (if needed)**

```bash
python manage.py createsuperuser
```

11. **Collect static files**

```bash
python manage.py collectstatic --noinput
```

12. **Restart services**

```bash
# Restart Django application via supervisor
sudo supervisorctl restart mydjangoapp

# Restart Nginx
sudo systemctl restart nginx
```

13. **Verify deployment**

```bash
# Check Django logs via supervisor
sudo supervisorctl tail -f mydjangoapp

# Test API endpoint
curl https://riderapp.testrunner.co.ke/api/health/

# Check database
python manage.py dbshell -c "SELECT 1;"

# Clear browser cache and test frontend
# Visit: https://riderapp.testrunner.co.ke
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
sudo supervisorctl restart mydjangoapp
sudo systemctl restart nginx
```

## Troubleshooting: Why Changes Aren't Reflecting

### **Common Issues:**

1. **Frontend files not deployed:**

   - `frontend/dist/` is ignored by git
   - Solution: Use `git add frontend/dist/ --force` locally

2. **Wrong virtual environment:**

   - Your supervisor uses `/var/www/dev/pindrop_web/myenv/`
   - Make sure deployment script uses the same path

3. **Services not restarting:**

   - Use `sudo supervisorctl restart mydjangoapp` (not systemctl)
   - Django runs on port 8001, not 8000

4. **Browser cache:**

   - Hard refresh (Ctrl+F5) or clear browser cache

5. **Nginx caching:**
   - Restart Nginx: `sudo systemctl restart nginx`

### **Debug Steps:**

```bash
# Check if supervisor service is running
sudo supervisorctl status mydjangoapp

# Check Django logs
sudo supervisorctl tail -f mydjangoapp

# Verify frontend files exist
ls -la /var/www/dev/pindrop_web/frontend/dist/

# Test direct API access
curl http://localhost:8001/api/health/

# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log
```
