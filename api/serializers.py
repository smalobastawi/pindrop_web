# api/serializers.py
import uuid
from rest_framework import serializers
from django.contrib.auth.models import User
from delivery.models import Customer, Driver, Package, Delivery, DeliveryStatusUpdate, Payment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active')

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Customer
        fields = '__all__'

class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    
    class Meta:
        model = Driver
        fields = '__all__'
        
class CustomerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = Customer
        fields = ('name', 'email', 'phone', 'address', 'user_type', 'password')
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        customer = Customer.objects.create(**validated_data)
        
        # Create user account if needed
        if not customer.user:
            username = validated_data['email'].split('@')[0] + str(uuid.uuid4())[:8]
            user = User.objects.create_user(
                username=username,
                email=validated_data['email'],
                password=password,
                first_name=validated_data['name'].split()[0] if validated_data['name'] else '',
                last_name=' '.join(validated_data['name'].split()[1:]) if len(validated_data['name'].split()) > 1 else ''
            )
            customer.user = user
            customer.save()
            
        return customer
        
class RiderRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = Driver
        fields = ('password',)
        
    def create(self, validated_data):
        # Extract password
        password = validated_data.pop('password')
        
        # Get the request data
        request = self.context.get('request')
        if request:
            # Create customer first
            customer_data = {
                'name': request.data.get('name'),
                'email': request.data.get('email'),
                'phone': request.data.get('phone'),
                'address': request.data.get('address'),
                'user_type': 'rider'
            }
            customer = Customer.objects.create(**customer_data)
            
            # Create user account
            username = customer_data['email'].split('@')[0] + str(uuid.uuid4())[:8]
            user = User.objects.create_user(
                username=username,
                email=customer_data['email'],
                password=password,
                first_name=customer_data['name'].split()[0] if customer_data['name'] else '',
                last_name=' '.join(customer_data['name'].split()[1:]) if len(customer_data['name'].split()) > 1 else ''
            )
            customer.user = user
            customer.save()
            
            # Create driver profile
            driver_data = {
                'user': user,
                'customer': customer,
                'license_number': request.data.get('license_number'),
                'vehicle_type': request.data.get('vehicle_type'),
                'vehicle_plate': request.data.get('vehicle_plate'),
                'vehicle_model': request.data.get('vehicle_model', ''),
                'vehicle_color': request.data.get('vehicle_color', ''),
                'vehicle_year': request.data.get('vehicle_year')
            }
            
            # Filter out None values
            driver_data = {k: v for k, v in driver_data.items() if v is not None}
            
            driver = Driver.objects.create(**driver_data)
            
            return driver
        
        raise serializers.ValidationError("Request context is required")

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'

class DeliveryStatusUpdateSerializer(serializers.ModelSerializer):
    updated_by = UserSerializer(read_only=True)
    
    class Meta:
        model = DeliveryStatusUpdate
        fields = '__all__'

class DeliverySerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    sender = CustomerSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)
    package = PackageSerializer(read_only=True)
    status_updates = DeliveryStatusUpdateSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Delivery
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'