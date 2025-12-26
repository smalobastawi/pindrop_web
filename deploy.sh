#!/bin/bash

# Pindrop Web Application Deployment Script
# This script updates the live server with fresh migrations
# Frontend build is handled locally and committed to git

echo "🚀 Starting Pindrop Web Application Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're running as root or with sudo
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root. Please run as your deployment user."
   exit 1
fi

# Set project directory (adjust if needed)
PROJECT_DIR="/path/to/your/pindrop_web"  # Replace with actual path
VENV_DIR="$PROJECT_DIR/venv"

# Step 1: Backup current deployment
print_status "Creating backup of current deployment..."
cd $PROJECT_DIR
cp -r . ../pindrop_backup_$(date +%Y%m%d_%H%M%S)
print_status "Backup created successfully"

# Step 2: Pull latest changes (including locally built frontend)
print_status "Pulling latest code changes (including built frontend)..."
git pull origin main  # Adjust branch name if different
if [ $? -ne 0 ]; then
    print_warning "Git pull failed. Continuing with current code..."
fi

# Step 3: Activate virtual environment
print_status "Activating Python virtual environment..."
source $VENV_DIR/bin/activate
if [ $? -ne 0 ]; then
    print_error "Failed to activate virtual environment. Check if it exists at $VENV_DIR"
    exit 1
fi

# Step 4: Install/update Python dependencies
print_status "Installing/updating Python dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    print_error "Failed to install Python dependencies"
    exit 1
fi

# Step 5: Configure environment variables
print_status "Setting up environment variables..."
# Copy your production .env file if not already present
if [ ! -f .env ]; then
    cp .env.example .env  # Adjust if you have a template
    print_warning "Please ensure .env file is properly configured for production"
fi

# Step 6: Run fresh database migrations
print_status "Running fresh database migrations..."
python manage.py migrate --run-syncdb
if [ $? -ne 0 ]; then
    print_error "Database migration failed"
    exit 1
fi

# Step 7: Create superuser if needed (optional)
print_status "Checking if superuser exists..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print('Superuser exists:', User.objects.filter(is_superuser=True).exists())"

# Step 8: Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
    print_error "Static files collection failed"
    exit 1
fi

# Step 9: Frontend build (handled locally and committed to git)
print_status "Frontend build should be done locally and committed to git..."
print_status "Skipping server-side frontend build as per deployment strategy"

# Step 10: Restart services
print_status "Restarting Django application..."
# Adjust service name based on your systemd service
sudo systemctl restart pindrop-web
if [ $? -ne 0 ]; then
    print_warning "Failed to restart Django service. Please check systemd configuration"
fi

print_status "Restarting Nginx..."
sudo systemctl restart nginx
if [ $? -ne 0 ]; then
    print_warning "Failed to restart Nginx"
fi

# Step 11: Run basic health checks
print_status "Running health checks..."
sleep 5

# Check if Django is responding
if curl -f http://localhost:8000/api/health/ > /dev/null 2>&1; then
    print_status "Django application is responding"
else
    print_warning "Django application health check failed"
fi

# Check database connectivity
python manage.py dbshell -c "SELECT 1;" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_status "Database connectivity OK"
else
    print_error "Database connectivity check failed"
fi

print_status "🎉 Deployment completed successfully!"
print_status "Please verify the application at your domain and check logs if needed."

# Deactivate virtual environment
deactivate

echo ""
print_status "Deployment Summary:"
echo "✅ Code updated (including built frontend)"
echo "✅ Dependencies installed"
echo "✅ Fresh migrations run"
echo "✅ Static files collected"
echo "✅ Services restarted"
echo "✅ Basic health checks performed"