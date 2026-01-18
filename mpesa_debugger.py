import os
import requests
import base64
from datetime import datetime
import json
from dotenv import load_dotenv

class MpesaDebugger:
    """
    Debug M-PESA STK Push issues step by step
    """
    
    def __init__(self):
        load_dotenv()
        self.consumer_key = os.getenv('MPESA_CONSUMER_KEY')
        self.consumer_secret = os.getenv('MPESA_CONSUMER_SECRET')
        self.shortcode = os.getenv('MPESA_LIPA_NA_MPESA_SHORTCODE')
        self.passkey = os.getenv('MPESA_LIPA_NA_MPESA_PASSKEY')
        self.environment = 'production'  # PRODUCTION environment
        
        # Set base URL based on environment
        if self.environment == 'sandbox':
            self.base_url = 'https://sandbox.safaricom.co.ke'
        else:
            self.base_url = 'https://api.safaricom.co.ke'
    
    def check_credentials(self):
        """Step 1: Verify all credentials are set"""
        print("=" * 50)
        print("STEP 1: Checking PRODUCTION Credentials")
        print("=" * 50)
        
        checks = {
            'Consumer Key': self.consumer_key,
            'Consumer Secret': self.consumer_secret,
            'Shortcode': self.shortcode,
            'Passkey': self.passkey
        }
        
        all_good = True
        for name, value in checks.items():
            if value and not value.startswith('your_'):
                print(f"[OK] {name}: {'*' * 10} (Set)")
            else:
                print(f"[FAIL] {name}: NOT SET")
                all_good = False

        if not all_good:
            print("\nTo set credentials:")
            print("1. Create a .env file in the project root")
            print("2. Add the following lines with your actual M-Pesa credentials:")
            print("   MPESA_CONSUMER_KEY=your_consumer_key_here")
            print("   MPESA_CONSUMER_SECRET=your_consumer_secret_here")
            print("   MPESA_LIPA_NA_MPESA_SHORTCODE=your_shortcode_here")
            print("   MPESA_LIPA_NA_MPESA_PASSKEY=your_passkey_here")
            print("3. Obtain credentials from Safaricom Developer Portal (https://developer.safaricom.co.ke/)")
        
        print()
        return all_good
    
    def get_access_token(self):
        """Step 2: Get OAuth access token"""
        print("=" * 50)
        print("STEP 2: Getting PRODUCTION Access Token")
        print("=" * 50)
        
        try:
            # Create basic auth header
            auth_string = f"{self.consumer_key}:{self.consumer_secret}"
            auth_bytes = auth_string.encode('ascii')
            auth_base64 = base64.b64encode(auth_bytes).decode('ascii')
            
            url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
            headers = {
                'Authorization': f'Basic {auth_base64}'
            }
            
            print(f"URL: {url}")
            print(f"Authorization: Basic {auth_base64[:20]}...")
            
            response = requests.get(url, headers=headers)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                access_token = data.get('access_token')
                print(f"[OK] Access Token: {access_token[:20]}...")
                print()
                return access_token
            else:
                print(f"[FAIL] Failed to get access token")
                print()
                return None
                
        except Exception as e:
            print(f"[FAIL] Error: {str(e)}")
            print()
            return None
    
    def generate_password(self, timestamp):
        """Generate the password for STK push"""
        password_string = f"{self.shortcode}{self.passkey}{timestamp}"
        password_bytes = password_string.encode('ascii')
        return base64.b64encode(password_bytes).decode('ascii')
    
    def initiate_stk_push(self, access_token, phone_number, amount):
        """Step 3: Initiate STK Push"""
        print("=" * 50)
        print("STEP 3: Initiating PRODUCTION STK Push")
        print("=" * 50)
        
        try:
            # Format phone number (ensure it starts with 254)
            if phone_number.startswith('0'):
                phone_number = '254' + phone_number[1:]
            elif phone_number.startswith('+'):
                phone_number = phone_number[1:]
            elif not phone_number.startswith('254'):
                phone_number = '254' + phone_number
            
            print(f"Phone Number (formatted): {phone_number}")
            
            # Generate timestamp
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            password = self.generate_password(timestamp)
            
            print(f"Timestamp: {timestamp}")
            print(f"Password: {password[:20]}...")
            
            url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            # Use ngrok or a public URL for callback
            callback_url = "https://mydomain.com/mpesa-express-simulate/"
            
            payload = {
                'BusinessShortCode': self.shortcode,
                'Password': password,
                'Timestamp': timestamp,
                'TransactionType': 'CustomerPayBillOnline',
                'Amount': int(amount),
                'PartyA': phone_number,
                'PartyB': self.shortcode,
                'PhoneNumber': phone_number,
                'CallBackURL': callback_url,
                'AccountReference': f'Order{timestamp}',
                'TransactionDesc': 'Payment for delivery'
            }
            
            print(f"\nPayload:")
            print(json.dumps(payload, indent=2))
            
            response = requests.post(url, json=payload, headers=headers)
            
            print(f"\nStatus Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ResponseCode') == '0':
                    print(f"\n[SUCCESS] STK Push sent successfully!")
                    print(f"CheckoutRequestID: {data.get('CheckoutRequestID')}")
                    return data
                else:
                    print(f"\n[FAIL] STK Push failed: {data.get('ResponseDescription')}")
                    return None
            else:
                print(f"\n[FAIL] Request failed with status {response.status_code}")
                return None
                
        except Exception as e:
            print(f"\n[FAIL] Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def run_full_test(self, phone_number='254704602809', amount=10):
        """Run complete diagnostic test - PRODUCTION"""
        print("\n" + "=" * 50)
        print("M-PESA STK PUSH DIAGNOSTIC TEST - PRODUCTION")
        print("=" * 50 + "\n")
        
        # Step 1: Check credentials
        if not self.check_credentials():
            print("[ERROR] Please set all required environment variables")
            return
        
        # Step 2: Get access token
        access_token = self.get_access_token()
        if not access_token:
            print("[ERROR] Failed to get access token. Check your credentials.")
            return
        
        # Step 3: Initiate STK push
        result = self.initiate_stk_push(access_token, phone_number, amount)
        
        if result:
            print("\n" + "=" * 50)
            print("[SUCCESS] TEST COMPLETED SUCCESSFULLY")
            print("=" * 50)
            print("\nCheck your phone for the STK push prompt!")
        else:
            print("\n" + "=" * 50)
            print("[ERROR] TEST FAILED")
            print("=" * 50)
            print("\nCommon Issues:")
            print("1. Wrong credentials (Consumer Key/Secret)")
            print("2. Wrong shortcode or passkey")
            print("3. Phone number format (should be 254XXXXXXXXX)")
            print("4. Sandbox vs Production mismatch")
            print("5. Callback URL not accessible")

# Usage
if __name__ == '__main__':
    debugger = MpesaDebugger()
    
    # Test with your phone number
    # Make sure to format it as 254XXXXXXXXX
    test_phone = '254704602809'  # Replace with your actual test number
    test_amount = 1  # Test with 1 KES
    
    debugger.run_full_test(test_phone, test_amount)