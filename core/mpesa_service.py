import os
import base64
import requests
from datetime import datetime, timedelta
from core.logging_utils import log_app_error

class MpesaService:
    """
    M-Pesa Daraja API Service for STK Push payments.
    Uses live credentials from environment variables.
    """
    
    def __init__(self):
        # Use live credentials from environment variables
        self.consumer_key = os.getenv('MPESA_CONSUMER_KEY')
        self.consumer_secret = os.getenv('MPESA_CONSUMER_SECRET')
        self.shortcode = os.getenv('MPESA_LIPA_NA_MPESA_SHORTCODE')
        self.passkey = os.getenv('MPESA_LIPA_NA_MPESA_PASSKEY')
        
        # Determine environment - default to 'production' for live credentials
        # Set MPESA_ENVIRONMENT=sandbox in .env to use sandbox
        self.environment = os.getenv('MPESA_ENVIRONMENT', 'production')
        
        # Set API URLs based on environment
        if self.environment == 'sandbox':
            self.base_url = 'https://sandbox.safaricom.co.ke'
        else:
            self.base_url = 'https://api.safaricom.co.ke'
        
        self._access_token = None
        self._token_expiry = None
        
        # Log initialization
        log_app_error(f'MPESA_SERVICE: Initialized with environment={self.environment}, shortcode={self.shortcode}, base_url={self.base_url}')
        log_app_error(f'MPESA_SERVICE: Consumer key present={bool(self.consumer_key)}, Consumer secret present={bool(self.consumer_secret)}')
        log_app_error(f'MPESA_SERVICE: Passkey present={bool(self.passkey)}')

    def get_access_token(self):
        """
        Get OAuth access token from M-Pesa API.
        Caches token until expiry.
        """
        # Check if we have a valid cached token
        if self._access_token and self._token_expiry:
            if datetime.now() < self._token_expiry:
                log_app_error(f'MPESA_SERVICE: Using cached access token')
                return self._access_token
        
        url = f'{self.base_url}/oauth/v1/generate?grant_type=client_credentials'
        
        # Create Base64 encoded credentials
        credentials = f'{self.consumer_key}:{self.consumer_secret}'
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }
        
        log_app_error(f'MPESA_SERVICE: Requesting access token from {url}')
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            log_app_error(f'MPESA_SERVICE: Access token response status={response.status_code}')
            log_app_error(f'MPESA_SERVICE: Access token response body={response.text}')
            
            response.raise_for_status()
            
            data = response.json()
            self._access_token = data.get('access_token')
            
            # Token expires in 3599 seconds (approximately 1 hour)
            # Cache it for 50 minutes to be safe
            self._token_expiry = datetime.now() + timedelta(minutes=50)
            
            log_app_error(f'MPESA_SERVICE: Access token obtained successfully')
            return self._access_token
            
        except requests.RequestException as e:
            log_app_error(f'MPESA_SERVICE: Failed to get access token - {str(e)}')
            if hasattr(e, 'response') and e.response is not None:
                log_app_error(f'MPESA_SERVICE: Error response body={e.response.text}')
            raise Exception(f"Failed to get M-Pesa access token: {str(e)}")

    def generate_password(self):
        """
        Generate the password for STK Push request.
        Password = Base64 encoded (BusinessShortCode + PassKey + Timestamp)
        """
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        data_to_encode = f'{self.shortcode}{self.passkey}{timestamp}'
        encoded = base64.b64encode(data_to_encode.encode()).decode()
        log_app_error(f'MPESA_SERVICE: Generated password with timestamp={timestamp}')
        return encoded, timestamp

    def initiate_stk_push(self, phone_number, amount, account_reference, transaction_desc, callback_url):
        """
        Initiate STK Push for M-Pesa payment.
        
        Args:
            phone_number: Customer phone number (format: 254XXXXXXXXX)
            amount: Amount to charge
            account_reference: Reference for the transaction (e.g., order number)
            transaction_desc: Description of the transaction
            callback_url: URL to receive payment result
            
        Returns:
            dict: M-Pesa API response
        """
        log_app_error(f'MPESA_SERVICE: Initiating STK Push - phone={phone_number}, amount={amount}, ref={account_reference}')
        log_app_error(f'MPESA_SERVICE: Callback URL={callback_url}')
        
        try:
            access_token = self.get_access_token()
        except Exception as e:
            log_app_error(f'MPESA_SERVICE: STK Push aborted - could not get access token: {str(e)}')
            raise
            
        password, timestamp = self.generate_password()
        
        url = f'{self.base_url}/mpesa/stkpush/v1/processrequest'
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Ensure phone number is in correct format (254XXXXXXXXX)
        phone = str(phone_number).strip()
        if phone.startswith('0'):
            phone = '254' + phone[1:]
        elif phone.startswith('+'):
            phone = phone[1:]
        
        # Ensure amount is an integer
        amount_int = int(float(amount))
        
        # Truncate strings to M-PESA limits
        account_ref = account_reference[:12] if len(str(account_reference)) > 12 else str(account_reference)
        trans_desc = transaction_desc[:13] if len(str(transaction_desc)) > 13 else str(transaction_desc)
        
        payload = {
            'BusinessShortCode': self.shortcode,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount_int,
            'PartyA': phone,
            'PartyB': self.shortcode,
            'PhoneNumber': phone,
            'CallBackURL': callback_url,
            'AccountReference': account_ref,
            'TransactionDesc': trans_desc
        }
        
        log_app_error(f'MPESA_SERVICE: STK Push request URL={url}')
        log_app_error(f'MPESA_SERVICE: STK Push payload (without password)={dict((k, v) for k, v in payload.items() if k != "Password")}')
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            log_app_error(f'MPESA_SERVICE: STK Push response status={response.status_code}')
            log_app_error(f'MPESA_SERVICE: STK Push response body={response.text}')
            
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('ResponseCode') == '0':
                log_app_error(f'MPESA_SERVICE: STK Push successful - CheckoutRequestID={result.get("CheckoutRequestID")}')
            else:
                log_app_error(f'MPESA_SERVICE: STK Push failed - ResponseCode={result.get("ResponseCode")}, ResponseDescription={result.get("ResponseDescription")}')
            
            return result
            
        except requests.RequestException as e:
            log_app_error(f'MPESA_SERVICE: STK Push request failed - {str(e)}')
            if hasattr(e, 'response') and e.response is not None:
                log_app_error(f'MPESA_SERVICE: Error response body={e.response.text}')
            raise Exception(f"STK Push failed: {str(e)}")

    def query_stk_status(self, checkout_request_id):
        """
        Query the status of an STK Push transaction.
        
        Args:
            checkout_request_id: The CheckoutRequestID from the STK Push response
            
        Returns:
            dict: M-Pesa API response with transaction status
        """
        log_app_error(f'MPESA_SERVICE: Querying STK status for CheckoutRequestID={checkout_request_id}')
        
        access_token = self.get_access_token()
        password, timestamp = self.generate_password()
        
        url = f'{self.base_url}/mpesa/stkpushquery/v1/query'
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'BusinessShortCode': self.shortcode,
            'Password': password,
            'Timestamp': timestamp,
            'CheckoutRequestID': checkout_request_id
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            log_app_error(f'MPESA_SERVICE: STK Query response status={response.status_code}')
            log_app_error(f'MPESA_SERVICE: STK Query response body={response.text}')
            
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            log_app_error(f'MPESA_SERVICE: STK Query failed - {str(e)}')
            raise Exception(f"STK Query failed: {str(e)}")

    def process_callback(self, callback_data):
        """
        Process the callback from M-Pesa.
        
        Args:
            callback_data: The callback data from M-Pesa
            
        Returns:
            dict: Parsed callback information
        """
        log_app_error(f'MPESA_SERVICE: Processing callback data={callback_data}')
        
        try:
            if 'Body' in callback_data and 'stkCallback' in callback_data['Body']:
                stk_callback = callback_data['Body']['stkCallback']
                
                result = {
                    'merchant_request_id': stk_callback.get('MerchantRequestID'),
                    'checkout_request_id': stk_callback.get('CheckoutRequestID'),
                    'result_code': stk_callback.get('ResultCode'),
                    'result_desc': stk_callback.get('ResultDesc'),
                    'success': stk_callback.get('ResultCode') == 0
                }
                
                # Parse callback metadata if payment was successful
                if result['success']:
                    metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
                    for item in metadata:
                        name = item.get('Name')
                        value = item.get('Value')
                        
                        if name == 'Amount':
                            result['amount'] = value
                        elif name == 'MpesaReceiptNumber':
                            result['receipt_number'] = value
                        elif name == 'TransactionDate':
                            result['transaction_date'] = value
                        elif name == 'PhoneNumber':
                            result['phone_number'] = value
                
                log_app_error(f'MPESA_SERVICE: Callback processed - result={result}')
                return result
            
            log_app_error(f'MPESA_SERVICE: Invalid callback format')
            return {'success': False, 'result_desc': 'Invalid callback format'}
            
        except Exception as e:
            log_app_error(f'MPESA_SERVICE: Callback processing error - {str(e)}')
            return {'success': False, 'result_desc': str(e)}
