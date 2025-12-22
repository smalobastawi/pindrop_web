# Customer Portal Implementation Guide

## Overview

This implementation adds a complete customer portal to the RiderApp delivery management system, allowing customers to:

- Register and create accounts
- Place package delivery orders
- Make payments for deliveries
- Track their packages in real-time
- View order history and statistics

## Architecture

### Backend (Django + Django REST Framework)

#### New API Endpoints

1. **Customer Registration**

   - `POST /api/customer/register/`
   - Creates customer profile and user account
   - Returns success message and customer data

2. **Customer Portal**

   - `GET /api/customer/portal/`
   - Returns customer data, orders, and statistics
   - Requires authentication

   - `POST /api/customer/portal/`
   - Creates new delivery order
   - Includes package, delivery, and payment information

3. **Order Tracking**
   - `GET /api/customer/track/?tracking_number=XXX`
   - Returns order details and status updates
   - Public endpoint (no auth required)

#### Database Models

The existing models support customer functionality:

- `Customer` - Customer profile information
- `Delivery` - Order/delivery details
- `Package` - Package specifications
- `Payment` - Payment tracking
- `DeliveryStatusUpdate` - Status history

### Frontend (Vue 3 + Pinia)

#### New Components

1. **CustomerRegister.vue**

   - Customer registration form
   - Validates input and creates accounts

2. **CustomerLogin.vue**

   - Customer authentication
   - JWT token management

3. **CustomerPortal.vue**

   - Main customer dashboard
   - Order statistics and management

4. **CreateOrderForm.vue**

   - Multi-step order creation form
   - Package, delivery, and payment details

5. **TrackOrder.vue**
   - Order tracking interface
   - Timeline view of status updates

#### API Service

- `frontend/src/api/customers.js`
- Handles customer-specific API calls
- Token management and error handling

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
- Timeline view of delivery progress
- Payment status tracking
- Package and delivery details

### Customer Dashboard

- Order statistics
- Order history
- Quick actions (create order, track package)
- Responsive design

## Usage Instructions

### For Customers

1. **Registration**

   - Visit customer portal: `http://localhost:5173/customer-register`
   - Fill out registration form
   - Verify account details

2. **Login**

   - Use registered email and password
   - Access customer portal dashboard

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
   - Or directly: `http://localhost:5173/customer-login`

2. **Monitor Customer Orders**
   - Admin dashboard shows delivery statistics
   - Customer orders appear in delivery management
   - Payment status tracked in payments section

## Technical Details

### Authentication Flow

1. Customer registers → User account created + Customer profile
2. Customer logs in → JWT tokens issued
3. API calls include Authorization header
4. Token refresh handled automatically

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

## Testing

Run the test script to verify functionality:

```bash
python test_customer_api.py
```

This tests:

- Customer registration
- Authentication
- Order creation
- Order tracking

## API Examples

### Register Customer

```bash
curl -X POST http://localhost:8000/api/customer/register/ \
  -H "Content-Type: application/json" \
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
curl -X POST http://localhost:8000/api/customer/portal/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
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
      "estimated_pickup": "2025-12-14T10:00:00Z",
      "estimated_delivery": "2025-12-15T16:00:00Z"
    },
    "payment": {
      "payment_method": "cash",
      "amount": 25.00
    }
  }'
```

### Track Order

```bash
curl "http://localhost:8000/api/customer/track/?tracking_number=PKG123456789ABC"
```

## File Structure

```
pindrop_web/
├── api/
│   ├── views.py              # Added customer views
│   ├── urls.py               # Added customer endpoints
│   └── serializers.py        # Existing serializers
├── delivery/
│   └── models.py             # Existing models
├── frontend/src/
│   ├── api/
│   │   └── customers.js      # Customer API service
│   ├── views/
│   │   ├── CustomerRegister.vue
│   │   ├── CustomerLogin.vue
│   │   └── CustomerPortal.vue
│   ├── components/
│   │   ├── CreateOrderForm.vue
│   │   └── TrackOrder.vue
│   └── router/
│       └── index.js          # Updated with customer routes
├── templates/
│   ├── base.html             # Added customer portal link
│   └── main/
│       └── home.html         # Added customer portal section
└── test_customer_api.py      # Test script
```

## Security Considerations

- JWT token authentication
- Password validation
- Input sanitization
- CORS configuration
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
