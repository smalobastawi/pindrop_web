# api/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from delivery.models import UserProfile, Package, Delivery, DeliveryStatusUpdate, Payment
from main.models import Role, UserRole

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'rating', 'completed_deliveries', 'total_ratings')

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'user_type', 'status', 'phone', 'address', 
            'profile_image', 'device_token', 'push_enabled', 'preferred_language',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at', 'user_type', 'status')

class RiderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'user_type', 'status', 'phone', 'address', 'profile_image',
            'license_number', 'license_expiry', 'vehicle_type', 'vehicle_plate',
            'vehicle_model', 'vehicle_color', 'vehicle_year', 'identity_type',
            'identity_number', 'identity_document', 'license_document', 'is_available',
            'current_location', 'rating', 'completed_deliveries', 'working_hours_start',
            'working_hours_end', 'device_token', 'push_enabled', 'preferred_language',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at', 'rating', 'completed_deliveries')

class CustomerRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()
    preferred_language = serializers.CharField(default='en')
    push_enabled = serializers.BooleanField(default=True)
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value
    
    def validate_password(self, value):
        validate_password(value)
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        profile = UserProfile.objects.create(
            user=user,
            user_type='customer',
            phone=validated_data['phone'],
            address=validated_data['address']
        )

        # Assign customer role
        try:
            customer_role = Role.objects.get(name='customer')
            UserRole.objects.create(user=user, role=customer_role)
        except Role.DoesNotExist:
            pass  # Role not found, continue without assigning

        return profile

class RiderRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()
    license_number = serializers.CharField()
    license_expiry = serializers.DateField(required=False)
    vehicle_type = serializers.CharField()
    vehicle_plate = serializers.CharField()
    vehicle_model = serializers.CharField(required=False)
    vehicle_color = serializers.CharField(required=False)
    vehicle_year = serializers.IntegerField(required=False)
    identity_type = serializers.CharField(required=False)
    identity_number = serializers.CharField(required=False)
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value
    
    def validate_password(self, value):
        validate_password(value)
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        profile = UserProfile.objects.create(
            user=user,
            user_type='rider',
            status='pending_approval',
            phone=validated_data['phone'],
            address=validated_data['address'],
            license_number=validated_data['license_number'],
            license_expiry=validated_data.get('license_expiry'),
            vehicle_type=validated_data['vehicle_type'],
            vehicle_plate=validated_data['vehicle_plate'],
            vehicle_model=validated_data.get('vehicle_model', ''),
            vehicle_color=validated_data.get('vehicle_color', ''),
            vehicle_year=validated_data.get('vehicle_year'),
            identity_type=validated_data.get('identity_type', ''),
            identity_number=validated_data.get('identity_number', '')
        )

        # Assign rider role
        try:
            rider_role = Role.objects.get(name='rider')
            UserRole.objects.create(user=user, role=rider_role)
        except Role.DoesNotExist:
            pass  # Role not found, continue without assigning

        return profile

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class DeliverySerializer(serializers.ModelSerializer):
    sender = CustomerSerializer(read_only=True)
    rider = RiderSerializer(read_only=True)
    package = PackageSerializer(read_only=True)
    
    class Meta:
        model = Delivery
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'tracking_number')

class DeliveryStatusUpdateSerializer(serializers.ModelSerializer):
    updated_by = UserSerializer(read_only=True)
    
    class Meta:
        model = DeliveryStatusUpdate
        fields = '__all__'
        read_only_fields = ('created_at',)

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')