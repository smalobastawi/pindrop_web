# Postman Login and Registration Collection Guide

This guide explains how to use the Postman collection for testing the login and registration APIs.

## Files Created

- [`login_registration_postman_collection.json`](login_registration_postman_collection.json) - Main Postman collection
- [`login_registration_environment.json`](login_registration_environment.json) - Environment variables

## Collection Overview

This collection includes:

### 1. Authentication Endpoints

- **Login - Obtain JWT Token**: Authenticate users and get access/refresh tokens
- **Refresh Token**: Refresh expired access tokens

### 2. Account Registration Endpoints

- **Register Customer**: Create new customer accounts
- **Register Rider**: Create new rider accounts (requires admin approval)
- **Unified Registration**: Single endpoint for both customer and rider registration

## Setup Instructions

### 1. Import Collection and Environment

1. Open Postman
2. Click **Import** button
3. Select the [`login_registration_postman_collection.json`](login_registration_postman_collection.json) file
4. Also import the [`login_registration_environment.json`](login_registration_environment.json) file
5. Select the "Login and Registration Environment" from the environment dropdown

### 2. Configure Environment Variables

The collection uses the following variables (all configurable in the environment):

- `base_url`: API base URL (default: `http://localhost:8000/api`)
- `email`: Test email (default: `test@example.com`)
- `password`: Test password (default: `testpassword123`)
- `access_token`: JWT access token (auto-populated after login)
- `refresh_token`: JWT refresh token (auto-populated after login)
- `customer_name`, `customer_phone`, `customer_address`: Customer details
- `rider_license_number`, `rider_vehicle_type`, `rider_vehicle_plate`, `rider_identity_type`, `rider_identity_number`: Rider details

### 3. Usage Workflow

#### Registration Flow

1. **Register Customer**: Use the "Register Customer" request to create a new customer account
2. **Register Rider**: Use the "Register Rider" request to create a new rider account
3. **Unified Registration**: Use the "Unified Registration" for a single endpoint approach

#### Login Flow

1. **Login**: Use the "Login - Obtain JWT Token" request with valid credentials
2. The response will automatically populate the `access_token` and `refresh_token` variables
3. Subsequent authenticated requests will use the bearer token automatically

#### Token Management

1. When your access token expires, use the "Refresh Token" request
2. This will automatically update the `access_token` variable

## API Endpoints Details

### Login

- **URL**: `{{base_url}}/token/`
- **Method**: POST
- **Body**: `{"email": "{{email}}", "password": "{{password}}"}`
- **Success Response**: Returns `access` and `refresh` tokens

### Register Customer

- **URL**: `{{base_url}}/register/customer/`
- **Method**: POST
- **Body**: Customer details including name, email, phone, address, and password
- **Success Response**: Returns customer details and ID

### Register Rider

- **URL**: `{{base_url}}/register/rider/`
- **Method**: POST
- **Body**: Rider details including license, vehicle info, identity documents, and password
- **Success Response**: Returns rider details and ID (requires admin approval)

### Refresh Token

- **URL**: `{{base_url}}/token/refresh/`
- **Method**: POST
- **Body**: `{"refresh": "{{refresh_token}}"}`
- **Success Response**: Returns new `access` token

## Testing the Collection

1. Start your Django development server: `python manage.py runserver`
2. Open Postman and select the collection
3. Run requests in this order:
   - Register Customer (or Register Rider)
   - Login - Obtain JWT Token
   - Refresh Token (when needed)

## Troubleshooting

- **401 Unauthorized**: Check if you're logged in and have valid tokens
- **400 Bad Request**: Verify your request body matches the expected format
- **500 Server Error**: Check your Django server logs for details

## Best Practices

- Use different email addresses for testing to avoid conflicts
- Reset your database between test runs if needed
- Monitor the Postman console for debug logs and token updates
- The collection includes test scripts that automatically handle token storage
