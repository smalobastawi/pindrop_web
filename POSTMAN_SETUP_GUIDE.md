# Postman Collection Setup Guide

## Overview

This Postman collection provides a complete testing suite for the Customer Portal API. It includes authentication, customer management, order creation, tracking, and delivery management endpoints.

## Prerequisites

1. **Postman** installed on your system
2. **Django backend server** running on `http://localhost:8000`
3. **Database** properly configured and migrations applied

## Setup Instructions

### 1. Import the Collection

1. Open Postman
2. Click "Import" button
3. Select the `customer_api_postman_collection.json` file
4. The collection will be imported with all endpoints organized in folders

### 2. Create Environment Variables

1. In Postman, go to **Environments** → **Create Environment**
2. Name it "Customer API Environment"
3. Add the following variables:

| Variable          | Initial Value               | Current Value | Description                              |
| ----------------- | --------------------------- | ------------- | ---------------------------------------- |
| `base_url`        | `http://localhost:8000/api` |               | API base URL                             |
| `username`        | `your_username`             |               | Django user username for login           |
| `password`        | `your_password`             |               | Django user password                     |
| `access_token`    |                             |               | JWT access token (auto-set after login)  |
| `refresh_token`   |                             |               | JWT refresh token (auto-set after login) |
| `customer_id`     |                             |               | Customer ID for CRUD operations          |
| `delivery_id`     |                             |               | Delivery ID for delivery operations      |
| `tracking_number` |                             |               | Tracking number for order tracking       |

### 3. Authentication Flow

#### Option A: Using Existing User Account

1. Set `username` and `password` variables in your environment
2. Run the "Login - Obtain JWT Token" request
3. Tokens will be automatically stored in variables

#### Option B: Create New User via API

1. First, run "Register Customer" to create a new customer account
2. This creates both a Django user and customer profile
3. Use the created credentials to login

### 4. Using the Collection

#### Authentication Endpoints

- **Login**: Get JWT tokens for authenticated requests
- **Refresh Token**: Refresh expired access tokens

#### Customer Management

- **Register Customer**: Create new customer account
- **Get Customer Portal**: View customer profile and order history
- **Create Order**: Create new delivery orders
- **Track Order**: Track orders by tracking number (public endpoint)

#### CRUD Operations

- **Customer CRUD**: Full create, read, update, delete operations
- **Delivery Management**: List deliveries, update status, view details

### 5. Testing Workflow

#### Basic Customer Flow

1. Register a new customer
2. Login to get JWT tokens
3. Access customer portal
4. Create a new order
5. Track the order using tracking number

#### Admin/Driver Flow

1. Login with admin/driver credentials
2. List all deliveries
3. Update delivery status
4. View dashboard statistics

### 6. Response Handling

- All requests include automated token storage
- Failed authentication responses are logged
- Order creation automatically sets tracking number variable
- Error responses include detailed error messages

### 7. Common Use Cases

#### Testing Order Creation

```json
{
  "package": {
    "description": "Test Package",
    "weight": 1.5,
    "dimensions": "20x15x10",
    "package_type": "parcel",
    "value": 1000,
    "special_instructions": "Handle with care"
  },
  "delivery": {
    "pickup_address": "Nairobi CBD",
    "delivery_address": "Westlands, Nairobi",
    "estimated_pickup": "2025-12-13T10:00:00Z",
    "estimated_delivery": "2025-12-13T16:00:00Z",
    "priority": 1
  },
  "payment": {
    "amount": 150.0,
    "payment_method": "cash"
  }
}
```

#### Testing Status Updates

```json
{
  "status": "in_transit",
  "location": "Nairobi CBD",
  "notes": "Package picked up successfully"
}
```

### 8. Environment-Specific URLs

Update the `base_url` variable for different environments:

- **Development**: `http://localhost:8000/api`
- **Staging**: `https://staging-api.yourdomain.com/api`
- **Production**: `https://api.yourdomain.com/api`

### 9. Security Notes

- JWT tokens are automatically managed by the collection
- Sensitive data should be stored in environment variables, not in the collection
- Use HTTPS URLs in production environments
- Refresh tokens are automatically handled

### 10. Troubleshooting

#### Authentication Issues

- Ensure Django server is running
- Verify username/password are correct
- Check if user account exists and is active

#### CORS Issues

- Verify CORS settings in Django settings.py
- Ensure proper headers are sent

#### Database Issues

- Ensure database migrations are applied
- Check database connection settings

### 11. API Documentation

For detailed API documentation, refer to the Django REST Framework browsable API at:
`http://localhost:8000/api/`

### 12. Collection Structure

```
Customer Portal API Collection
├── Authentication
│   ├── Login - Obtain JWT Token
│   └── Refresh Token
├── Customer Management
│   ├── Register Customer
│   ├── Get Customer Portal
│   ├── Create Order
│   └── Track Order
├── Customer CRUD Operations
│   ├── List Customers
│   ├── Get Customer by ID
│   ├── Create Customer
│   ├── Update Customer
│   └── Delete Customer
├── Delivery Management
│   ├── List Deliveries
│   ├── Get Delivery by ID
│   ├── Update Delivery Status
│   └── Get Dashboard Stats
└── Additional Resources
    ├── List Packages
    ├── List Drivers
    ├── List Payments
    └── List Status Updates
```

This collection provides comprehensive testing coverage for all customer-related API endpoints and can be easily extended for additional functionality.
