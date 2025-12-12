# test_customer_api.py
"""
Test script for customer functionality
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"

def test_customer_registration():
    """Test customer registration"""
    print("Testing customer registration...")
    
    customer_data = {
        "name": "John Doe",
        "email": "john.doe.test@example.com",
        "phone": "+1234567890",
        "address": "123 Test Street, Test City, TC 12345",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/customer/register/", json=customer_data)
    
    if response.status_code == 201:
        print("✅ Customer registration successful")
        return response.json()
    else:
        print(f"❌ Customer registration failed: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def test_customer_login(email, password):
    """Test customer login"""
    print("Testing customer login...")
    
    login_data = {
        "email": email,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/token/", json=login_data)
    
    if response.status_code == 200:
        print("✅ Customer login successful")
        return response.json()
    else:
        print(f"❌ Customer login failed: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def test_order_creation(access_token):
    """Test order creation"""
    print("Testing order creation...")
    
    order_data = {
        "package": {
            "description": "Test Package - Electronics",
            "weight": 2.5,
            "dimensions": "30x20x10",
            "package_type": "parcel",
            "value": 150.00,
            "special_instructions": "Handle with care"
        },
        "delivery": {
            "pickup_address": "456 Sender Street, Sender City, SC 67890",
            "delivery_address": "789 Receiver Avenue, Receiver City, RC 13579",
            "estimated_pickup": (datetime.now() + timedelta(hours=2)).isoformat(),
            "estimated_delivery": (datetime.now() + timedelta(days=1)).isoformat(),
            "priority": 1
        },
        "payment": {
            "payment_method": "cash",
            "amount": 25.00
        }
    }
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(f"{BASE_URL}/customer/portal/", json=order_data, headers=headers)
    
    if response.status_code == 201:
        print("✅ Order creation successful")
        return response.json()
    else:
        print(f"❌ Order creation failed: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def test_order_tracking(tracking_number):
    """Test order tracking"""
    print("Testing order tracking...")
    
    response = requests.get(f"{BASE_URL}/customer/track/", params={"tracking_number": tracking_number})
    
    if response.status_code == 200:
        print("✅ Order tracking successful")
        return response.json()
    else:
        print(f"❌ Order tracking failed: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def main():
    """Run all tests"""
    print("Starting customer functionality tests...\n")
    
    # Test 1: Customer Registration
    registration_result = test_customer_registration()
    if not registration_result:
        print("Stopping tests due to registration failure")
        return
    
    print()
    
    # Test 2: Customer Login
    email = "john.doe.test@example.com"
    password = "testpassword123"
    login_result = test_customer_login(email, password)
    if not login_result:
        print("Stopping tests due to login failure")
        return
    
    access_token = login_result['access']
    print()
    
    # Test 3: Order Creation
    order_result = test_order_creation(access_token)
    if not order_result:
        print("Stopping tests due to order creation failure")
        return
    
    tracking_number = order_result['tracking_number']
    print()
    
    # Test 4: Order Tracking
    tracking_result = test_order_tracking(tracking_number)
    if not tracking_result:
        print("Stopping tests due to tracking failure")
        return
    
    print("\n🎉 All tests completed successfully!")
    print(f"Created tracking number: {tracking_number}")

if __name__ == "__main__":
    main()