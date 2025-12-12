# Django Customer Portal Implementation Guide

## Overview

This implementation adds a complete customer portal to the PinDrop delivery management system using Django templates and JavaScript, allowing customers to:

- Register and create accounts
- Place package delivery orders
- Make payments for deliveries
- Track their packages in real-time
- View order history and statistics

## Architecture

### Backend (Django)

#### New URLs and Views

1. **Customer Registration**

   - `GET/POST /customer-register/`
   - Customer registration page with form
   - Creates customer profile and user account

2. **Customer Login**

   - `GET/POST /customer-login/`
   - Customer login page
   - Session-based authentication

3. **Customer Portal**

   - `GET /customer-portal/`
   - Main customer dashboard
   - Shows orders, statistics, and actions

4. **Order Creation API**

   - `POST /api/customer/create-order/`
   - Creates new delivery order
   - Includes package, delivery, and payment information

5. **Order Tracking**

   - `GET /api/customer/track-order/?tracking_number=XXX`
   - Returns order details and status updates
   - Public endpoint (no auth required)

6. **Customer Logout**
   - `GET /customer-logout/`
   - Logs out customer and clears session

#### Database Models

The existing models support customer functionality:

- `Customer` - Customer profile information
- `Delivery` - Order/delivery details
- `Package` - Package specifications
- `Payment` - Payment tracking
- `DeliveryStatusUpdate` - Status history

### Frontend (Django Templates + JavaScript)

#### New Templates

1. **customer_register.html**

   - Customer registration form
   - Validates input and creates accounts
   - Bootstrap styling with AJAX

2. **customer_login.html**

   - Customer authentication
   - Session-based login

3. **customer_portal.html**
   - Main customer dashboard
   - Order statistics, creation, and tracking
   - Interactive modals and forms

#### JavaScript Features

- AJAX form submissions
- Dynamic cost calculation
- Order tracking functionality
- Modal management
- Real-time status updates

## Features

### Customer Registration

- Full name, email, phone, address
- Password requirements
- Duplicate email validation
- Automatic user account creation

### Order Management

- Package details (description, weight, dimensions, type)
- Delivery information (addresses, timing, priority)
- Payment processing (multiple methods)
- Automatic cost calculation

### Payment Options

- Cash on Delivery
- Credit/Debit Card
- Bank Transfer
- Mobile Money

### Order Tracking

- Real-time status updates
- Payment status tracking
- Package and delivery details
- Search by tracking number

### Customer Dashboard

- Order statistics
- Order history
- Quick actions (create order, track package)
- Responsive design

## Usage Instructions

### For Customers

1. **Registration**

   - Visit customer portal: `http://localhost:8000/customer-register/`
   - Fill out registration form
   - Verify account details

2. **Login**

   - Use registered email and password
   - Access customer portal dashboard at `http://localhost:8000/customer-portal/`

3. **Creating Orders**

   - Click "Create New Order" in dashboard
   - Fill package details (weight, dimensions, type)
   - Specify pickup and delivery addresses
   - Choose delivery priority and payment method
   - Review and submit order

4. **Tracking Orders**
   - Use tracking number from order confirmation
   - Track via dashboard or public tracking page
   - View real-time status updates

### For Administrators

1. **Access Customer Portal**

   - From main navigation: "Customer Portal"
   - Or directly: `http://localhost:8000/customer-login/`

2. **Monitor Customer Orders**
   - Admin dashboard shows delivery statistics
   - Customer orders appear in delivery management
   - Payment status tracked in payments section

## Technical Details

### Authentication Flow

1. Customer registers → User account created + Customer profile
2. Customer logs in → Session created
3. API calls include session authentication
4. Session management handled by Django

### Order Processing

1. Customer submits order → Validation → Database storage
2. Tracking number generated → Order confirmation sent
3. Payment record created → Status tracking begins
4. Delivery assigned → Status updates logged

### Cost Calculation

- Base rate: $10 per kg
- Priority multipliers:
  - Normal (1x)
  - Express (1.5x)
  - Urgent (2x)

## API Examples

### Register Customer

```bash
curl -X POST http://localhost:8000/customer-register/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: <token>" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "address": "123 Main St",
    "password": "securepass123"
  }'
```

### Create Order

```bash
curl -X POST http://localhost:8000/api/customer/create-order/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: <token>" \
  -H "Cookie: sessionid=<session_id>" \
  -d '{
    "package": {
      "description": "Electronics",
      "weight": 2.5,
      "dimensions": "30x20x10",
      "package_type": "parcel"
    },
    "delivery": {
      "pickup_address": "456 Sender St",
      "delivery_address": "789 Receiver Ave",
      "estimated_pickup": "2025-12-14T10:00:00",
      "estimated_delivery": "2025-12-15T16:00:00"
    },
    "payment": {
      "payment_method": "cash",
      "amount": 25.00
    }
  }'
```

### Track Order

```bash
curl "http://localhost:8000/api/customer/track-order/?tracking_number=PKG123456789ABC"
```

## File Structure

```
pindrop_web/
├── main/
│   ├── views_customer.py       # Customer portal views
│   ├── urls.py                 # Updated with customer URLs
│   └── templates/main/
│       ├── customer_register.html
│       ├── customer_login.html
│       └── customer_portal.html
├── templates/
│   ├── base.html               # Updated navigation
│   └── main/
│       └── home.html           # Updated with customer portal link
├── delivery/
│   └── models.py               # Existing models
├── api/
│   ├── views.py                # REST API endpoints
│   └── urls.py                 # API URLs
└── mysite/
    └── settings.py             # Django configuration
```

## Security Considerations

- Session-based authentication
- Password validation
- Input sanitization
- CSRF protection
- Rate limiting (can be added)
- HTTPS in production

## Future Enhancements

- Email notifications
- SMS notifications
- Payment gateway integration
- Real-time tracking with GPS
- Mobile app
- Multi-language support
- Advanced analytics
- Customer support chat

## Quick Start

1. **Run Django Server**

   ```bash
   python manage.py runserver
   ```

2. **Access Customer Portal**

   - Registration: `http://localhost:8000/customer-register/`
   - Login: `http://localhost:8000/customer-login/`
   - Portal: `http://localhost:8000/customer-portal/`

3. **Test Functionality**
   - Register a new customer
   - Create an order
   - Track the order using the tracking number

The customer portal is now fully integrated into the Django application and accessible through the main website navigation!
