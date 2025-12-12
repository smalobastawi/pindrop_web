# api/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from delivery.models import Customer, Driver, Package, Delivery, DeliveryStatusUpdate, Payment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Driver
        fields = '__all__'

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