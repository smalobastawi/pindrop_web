# PinDrop Delivery System - Architecture Guide

## Overview

This document outlines the updated architecture for the PinDrop delivery system, which now supports both customers and riders through a unified platform with mobile app compatibility.

## Architecture Components

### 1. Frontend (Customer & Rider Portal)

- **Location**: `frontend/src/`
- **Framework**: Vue.js with Vue Router
- **Features**:
  - Unified registration for customers and riders
  - User type selection during registration
  - Rider-specific fields (license, vehicle information)
  - Customer portal for order management
  - Order tracking functionality
  - Mobile-responsive design

### 2. Backend API (Django REST Framework)

- **Location**: `api/`
- **Features**:
  - Customer and Rider registration endpoints
  - Unified authentication system
  - Mobile API compatibility
  - Real-time order tracking
  - Admin panel integration

### 3. Mobile App API Endpoints

- **Location**: `api/views.py` - Mobile-specific views
- **Features**:
  - API versioning support
  - Device token registration for push notifications
  - Mobile-optimized user profile management
  - Cross-platform compatibility

### 4. Admin Panel

- **Location**: `admin_panel/`
- **Features**:
  - Rider approval workflow
  - Customer and Rider management
  - User status management (active/inactive/suspended)
  - Dashboard with comprehensive statistics
  - Audit logging

### 5. Database Models

#### Customer Model

```python
class Customer(models.Model):
    user_type = models.CharField(choices=[('customer', 'Customer'), ('rider', 'Rider'), ('both', 'Both')])
    status = models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('suspended', 'Suspended'), ('pending_approval', 'Pending Approval')])
    device_token = models.CharField(max_length=500, blank=True, null=True)
    push_enabled = models.BooleanField(default=True)
```

#### Driver (Rider) Model

```python
class Driver(models.Model):
    status = models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('suspended', 'Suspended'), ('pending_approval', 'Pending Approval')])
    license_number = models.CharField(max_length=50, unique=True)
    vehicle_type = models.CharField(choices=[('bicycle', 'Bicycle'), ('motorcycle', 'Motorcycle'), ('car', 'Car'), ('van', 'Van'), ('truck', 'Truck')])
    device_token = models.CharField(max_length=500, blank=True, null=True)
```

## Key Features

### 1. Unified Registration System

- Single registration form supporting both customer and rider types
- Dynamic fields based on user type selection
- Separate validation for rider-specific information

### 2. Mobile App Compatibility

- RESTful API endpoints optimized for mobile devices
- Push notification support via device tokens
- Cross-platform authentication
- API versioning for future enhancements

### 3. Admin Management

- **Rider Approval Process**: New riders require admin approval before activation
- **User Status Management**: Active, inactive, suspended, pending approval states
- **Comprehensive Dashboard**: Statistics for customers, riders, and deliveries
- **Audit Trail**: Track all admin actions and user activities

### 4. Authentication & Authorization

- JWT-based authentication
- Role-based access control (admin, customer, rider)
- Token refresh mechanism
- Secure API endpoints

## API Endpoints

### Registration Endpoints

```
POST /api/register/              # Unified registration
POST /api/register/customer/     # Customer registration
POST /api/register/rider/        # Rider registration
```

### Customer Endpoints

```
POST /api/customer/portal/       # Create order
GET  /api/customer/portal/       # Get customer portal data
GET  /api/customer/track/        # Track order
```

### Mobile App Endpoints

```
GET  /api/mobile/version/        # API version info
GET  /api/mobile/profile/        # Get user profile
PUT  /api/mobile/profile/        # Update user profile
POST /api/mobile/device-token/   # Register device token
```

### Admin Endpoints

```
GET  /api/admin/dashboard/stats/                    # Dashboard statistics
GET  /api/admin/riders/pending_approvals/          # Get pending riders
POST /api/admin/riders/{id}/approve_rider/         # Approve rider
POST /api/admin/riders/{id}/reject_rider/          # Reject rider
GET  /api/admin/user-management/users_summary/     # Users summary
```

## Database Migrations

After updating the models, run the following commands:

```bash
python manage.py makemigrations delivery
python manage.py makemigrations admin_panel
python manage.py migrate
```

## Frontend Build

To build the updated frontend:

```bash
cd frontend
npm install
npm run build
```

## Security Considerations

1. **Input Validation**: All user inputs are validated on both frontend and backend
2. **Authentication**: JWT tokens with proper expiration and refresh mechanism
3. **Authorization**: Role-based access control for different user types
4. **Data Protection**: Sensitive rider information (license numbers) properly handled
5. **Audit Logging**: All admin actions are logged for security monitoring

## Future Enhancements

1. **Real-time Notifications**: WebSocket integration for live updates
2. **Location Services**: GPS tracking for riders and delivery status
3. **Payment Integration**: Online payment processing for orders
4. **Analytics Dashboard**: Advanced reporting and analytics
5. **Multi-language Support**: Internationalization for global deployment

## Deployment Notes

1. **Environment Variables**: Configure proper API URLs and security settings
2. **Database**: Ensure PostgreSQL or MySQL for production use
3. **File Storage**: Configure proper media file storage for profile images
4. **CORS Settings**: Configure CORS for mobile app communication
5. **SSL/TLS**: Enable HTTPS for secure communication

This architecture provides a scalable foundation for a modern delivery system supporting both customers and riders through web and mobile platforms.
