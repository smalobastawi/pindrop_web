# Customer API Postman Collection

This repository contains a complete Postman collection for testing the Customer Portal API, including authentication, customer management, order creation, tracking, and delivery management endpoints.

## Files Included

- **`customer_api_postman_collection.json`** - Complete Postman collection with all API endpoints
- **`customer_api_environment.json`** - Sample environment with pre-configured variables
- **`POSTMAN_SETUP_GUIDE.md`** - Detailed setup and usage instructions

## Quick Start

### 1. Import Collection

1. Open Postman
2. Click "Import" → Select `customer_api_postman_collection.json`
3. Click "Import" → Select `customer_api_environment.json` (optional but recommended)

### 2. Configure Environment

1. Select the "Customer API Environment" from environment dropdown
2. Update the `base_url` variable if your API runs on a different port/domain
3. Set `username` and `password` for authentication

### 3. Test API

1. Run "Login - Obtain JWT Token" to get authenticated
2. Explore customer endpoints like "Register Customer" or "Get Customer Portal"
3. Create orders and track them using the tracking functionality

## API Endpoints Covered

### Authentication

- `POST /api/token/` - Login (JWT token obtain)
- `POST /api/token/refresh/` - Refresh JWT token

### Customer Management

- `POST /api/customer/register/` - Register new customer
- `GET /api/customer/portal/` - Get customer portal (authenticated)
- `POST /api/customer/portal/` - Create new order (authenticated)
- `GET /api/customer/track/?tracking_number={number}` - Track order (public)

### Customer CRUD Operations

- `GET /api/customers/` - List customers
- `POST /api/customers/` - Create customer
- `GET /api/customers/{id}/` - Get customer details
- `PATCH /api/customers/{id}/` - Update customer
- `DELETE /api/customers/{id}/` - Delete customer

### Delivery Management

- `GET /api/deliveries/` - List deliveries (role-based filtering)
- `GET /api/deliveries/{id}/` - Get delivery details
- `POST /api/deliveries/{id}/update_status/` - Update delivery status
- `GET /api/dashboard/` - Get dashboard statistics

### Additional Resources

- `GET /api/packages/` - List packages
- `GET /api/drivers/` - List drivers
- `GET /api/payments/` - List payments
- `GET /api/status-updates/` - List status updates

## Key Features

✅ **JWT Authentication** - Automatic token management  
✅ **Role-based Access** - Different endpoints for customers, drivers, and admins  
✅ **Order Tracking** - Public endpoint for tracking orders by tracking number  
✅ **Complete CRUD** - Full customer and delivery management  
✅ **Auto-variables** - Tracking numbers and IDs automatically stored  
✅ **Error Handling** - Comprehensive error response handling  
✅ **Sample Data** - Pre-configured environment with sample values

## Sample Order Creation

```json
{
  "package": {
    "description": "Laptop Computer",
    "weight": 2.5,
    "dimensions": "35x25x5",
    "package_type": "parcel",
    "value": 50000,
    "special_instructions": "Handle with care - Fragile"
  },
  "delivery": {
    "pickup_address": "Westlands, Nairobi",
    "delivery_address": "Karen, Nairobi",
    "estimated_pickup": "2025-12-13T10:00:00Z",
    "estimated_delivery": "2025-12-13T16:00:00Z",
    "priority": 2
  },
  "payment": {
    "amount": 250.0,
    "payment_method": "cash"
  }
}
```

## Authentication Flow

1. **Register/Login**: Use customer registration or login with existing credentials
2. **Token Storage**: JWT tokens automatically stored in environment variables
3. **API Access**: All protected endpoints automatically use the stored token
4. **Token Refresh**: Automatic refresh token handling for expired sessions

## Testing Workflows

### Customer Journey

1. Register customer account
2. Login to get JWT tokens
3. View customer portal (profile + order history)
4. Create new delivery order
5. Track order using generated tracking number

### Admin/Driver Journey

1. Login with admin/driver credentials
2. List all deliveries and customers
3. Update delivery statuses with location tracking
4. View dashboard statistics and reports

## Requirements

- **Postman** (latest version recommended)
- **Django Backend** running with the Customer Portal API
- **Database** properly configured and migrated
- **Valid user accounts** for testing authentication

## Support

For detailed setup instructions, troubleshooting, and advanced usage, see `POSTMAN_SETUP_GUIDE.md`.

## API Base URL

Default: `http://localhost:8000/api`

Update the `base_url` environment variable for different environments (staging, production, etc.).
