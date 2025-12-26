# core/logging_utils.py
import logging
import os
from datetime import datetime

# Define log file paths
LOG_DIR = 'logs'
API_ERROR_LOG = os.path.join(LOG_DIR, 'api_errors.log')
APP_ERROR_LOG = os.path.join(LOG_DIR, 'app_errors.log')
DB_ERROR_LOG = os.path.join(LOG_DIR, 'db_errors.log')

# Create logs directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)

def log_api_error(error_details):
    """Log API-related errors"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"API_ERROR : {error_details}\n"
    
    with open(API_ERROR_LOG, 'a') as f:
        f.write(f"[{timestamp}] {log_message}")
    
    print(f"API Error logged: {error_details}")

def log_app_error(error_details):
    """Log application-related errors"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"APP_ERROR: {error_details}\n"
    
    with open(APP_ERROR_LOG, 'a') as f:
        f.write(f"[{timestamp}] {log_message}")
    
    print(f"App Error logged: {error_details}")

def log_db_error(error_details):
    """Log database-related errors"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"DB_ERROR: {error_details}\n"
    
    with open(DB_ERROR_LOG, 'a') as f:
        f.write(f"[{timestamp}] {log_message}")
    
    print(f"DB Error logged: {error_details}")