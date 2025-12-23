#!/usr/bin/env python
"""
Simple test script to verify the updated API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_api_endpoints():
    """Test the new API endpoints"""
    print("Testing PinDrop API Endpoints...")
    print("=" * 50)
    
    # Test 1: Mobile API Version
    try:
        response = requests.get(f"{BASE_URL}/mobile/version/")
        if response.status_code == 200:
            print("[OK] Mobile API Version: Working")
            data = response.json()
            print(f"   Version: {data.get('api_version')}")
            print(f"   Features: {', '.join(data.get('supported_features', []))}")
        else:
            print(f"[FAIL] Mobile API Version: Failed ({response.status_code})")
    except Exception as e:
        print(f"[ERROR] Mobile API Version: {e}")
    
    print()
    
    # Test 2: Customer Registration (Unified)
    try:
        customer_data = {
            "name": "Test Customer",
            "email": "customer@test.com",
            "phone": "+1234567890",
            "address": "123 Test St, Test City",
            "user_type": "customer",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/register/", json=customer_data)
        if response.status_code == 201:
            print("[OK] Customer Registration: Working")
            data = response.json()
            print(f"   Message: {data.get('message')}")
        else:
            print(f"[FAIL] Customer Registration: Failed ({response.status_code})")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"[ERROR] Customer Registration: {e}")
    
    print()
    
    # Test 3: Rider Registration
    try:
        rider_data = {
            "name": "Test Rider",
            "email": "rider@test.com",
            "phone": "+1234567891",
            "address": "456 Test St, Test City",
            "license_number": "TEST123456",
            "vehicle_type": "motorcycle",
            "vehicle_plate": "TR001",
            "vehicle_model": "Yamaha FZ",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/register/rider/", json=rider_data)
        if response.status_code == 201:
            print("[OK] Rider Registration: Working")
            data = response.json()
            print(f"   Message: {data.get('message')}")
        else:
            print(f"[FAIL] Rider Registration: Failed ({response.status_code})")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"[ERROR] Rider Registration: {e}")
    
    print()
    
    # Test 4: Order Tracking (without authentication)
    try:
        response = requests.get(f"{BASE_URL}/customer/track/", params={"tracking_number": "INVALID"})
        if response.status_code == 404:
            print("[OK] Order Tracking: Working (Correctly returns 404 for invalid tracking)")
        elif response.status_code == 400:
            print("[OK] Order Tracking: Working (Correctly returns 400 for missing tracking number)")
        else:
            print(f"[FAIL] Order Tracking: Unexpected status ({response.status_code})")
    except Exception as e:
        print(f"[ERROR] Order Tracking: {e}")
    
    print()
    print("=" * 50)
    print("API Testing Complete!")

if __name__ == "__main__":
    test_api_endpoints()