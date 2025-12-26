# delivery/serializers.py
from rest_framework import serializers
from .models import Package, Delivery, Payment, UserProfile


class PackageSerializer(serializers.ModelSerializer):
    """Serializer for Package model"""
    dimensions = serializers.CharField(read_only=True)

    class Meta:
        model = Package
        fields = [
            'id', 'description', 'weight', 'length', 'width', 'height',
            'package_type', 'size_category', 'declared_value', 'requires_insurance',
            'insurance_amount', 'special_instructions', 'is_fragile', 'is_perishable',
            'requires_signature', 'dimensions', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'dimensions', 'created_at', 'updated_at']


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model"""
    total_amount = serializers.ReadOnlyField()

    class Meta:
        model = Payment
        fields = [
            'id', 'amount', 'currency', 'payment_method', 'status',
            'transaction_id', 'payment_gateway', 'gateway_reference',
            'cod_amount', 'cod_collected', 'cod_handover_amount',
            'paid_at', 'refunded_at', 'total_amount', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'paid_at', 'refunded_at', 'created_at', 'updated_at']


class DeliverySerializer(serializers.ModelSerializer):
    """Serializer for Delivery model"""
    package = PackageSerializer()
    payment = PaymentSerializer()
    sender_details = serializers.SerializerMethodField()
    rider_details = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)

    class Meta:
        model = Delivery
        fields = [
            'id', 'tracking_number', 'sender', 'sender_details', 'recipient_name',
            'recipient_phone', 'rider', 'rider_details', 'package', 'payment',
            'pickup_address', 'pickup_latitude', 'pickup_longitude',
            'delivery_address', 'delivery_latitude', 'delivery_longitude',
            'estimated_pickup', 'estimated_delivery', 'actual_pickup', 'actual_delivery',
            'status', 'status_display', 'priority', 'priority_display',
            'delivery_fee', 'distance_km', 'estimated_duration_minutes',
            'notes', 'cancellation_reason', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'tracking_number', 'actual_pickup', 'actual_delivery',
            'distance_km', 'estimated_duration_minutes', 'created_at', 'updated_at'
        ]

    def get_sender_details(self, obj):
        return {
            'id': obj.sender.id,
            'name': obj.sender.user.get_full_name() or obj.sender.user.username,
            'phone': obj.sender.phone,
            'email': obj.sender.user.email
        }

    def get_rider_details(self, obj):
        if obj.rider:
            return {
                'id': obj.rider.id,
                'name': obj.rider.user.get_full_name() or obj.rider.user.username,
                'phone': obj.rider.phone,
                'vehicle_type': obj.rider.vehicle_type,
                'vehicle_plate': obj.rider.vehicle_plate
            }
        return None


class DeliveryCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating deliveries from admin"""

    # Sender details
    sender_name = serializers.CharField(max_length=200, write_only=True)
    sender_phone = serializers.CharField(max_length=20, write_only=True)
    sender_email = serializers.EmailField(required=False, write_only=True)
    sender_address = serializers.CharField(write_only=True)

    # Recipient details
    recipient_name = serializers.CharField(max_length=200, write_only=True)
    recipient_phone = serializers.CharField(max_length=20, write_only=True)
    recipient_address = serializers.CharField(write_only=True)

    # Package details
    package_description = serializers.CharField(write_only=True)
    package_weight = serializers.DecimalField(max_digits=6, decimal_places=2, write_only=True)
    package_length = serializers.DecimalField(max_digits=6, decimal_places=2, required=False, allow_null=True, write_only=True)
    package_width = serializers.DecimalField(max_digits=6, decimal_places=2, required=False, allow_null=True, write_only=True)
    package_height = serializers.DecimalField(max_digits=6, decimal_places=2, required=False, allow_null=True, write_only=True)
    package_type = serializers.ChoiceField(choices=Package.PACKAGE_TYPES, write_only=True)
    declared_value = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, write_only=True)
    special_instructions = serializers.CharField(required=False, allow_blank=True, write_only=True)
    is_fragile = serializers.BooleanField(default=False, write_only=True)
    is_perishable = serializers.BooleanField(default=False, write_only=True)
    requires_signature = serializers.BooleanField(default=False, write_only=True)

    # Delivery details
    pickup_address = serializers.CharField(write_only=True)
    delivery_address = serializers.CharField(write_only=True)
    estimated_pickup = serializers.DateTimeField(write_only=True)
    estimated_delivery = serializers.DateTimeField(write_only=True)
    priority = serializers.ChoiceField(choices=[(1, 'Normal'), (2, 'Express'), (3, 'Urgent'), (4, 'Same Day')], write_only=True)
    delivery_fee = serializers.DecimalField(max_digits=8, decimal_places=2, write_only=True)

    # Payment details
    payment_amount = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)
    payment_method = serializers.ChoiceField(choices=Payment.PAYMENT_METHODS, write_only=True)
    cod_amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, write_only=True)

    # Optional rider assignment
    rider_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)

    class Meta:
        model = Delivery
        fields = [
            'sender_name', 'sender_phone', 'sender_email', 'sender_address',
            'recipient_name', 'recipient_phone', 'recipient_address',
            'package_description', 'package_weight', 'package_length', 'package_width', 'package_height',
            'package_type', 'declared_value', 'special_instructions', 'is_fragile', 'is_perishable', 'requires_signature',
            'pickup_address', 'delivery_address', 'estimated_pickup', 'estimated_delivery', 'priority', 'delivery_fee',
            'payment_amount', 'payment_method', 'cod_amount', 'rider_id'
        ]

    def create(self, validated_data):
        # Extract data
        sender_data = {
            'name': validated_data['sender_name'],
            'phone': validated_data['sender_phone'],
            'email': validated_data.get('sender_email', ''),
            'address': validated_data['sender_address']
        }

        recipient_data = {
            'name': validated_data['recipient_name'],
            'phone': validated_data['recipient_phone'],
            'address': validated_data['recipient_address']
        }

        package_data = {
            'description': validated_data['package_description'],
            'weight': validated_data['package_weight'],
            'length': validated_data.get('package_length'),
            'width': validated_data.get('package_width'),
            'height': validated_data.get('package_height'),
            'package_type': validated_data['package_type'],
            'declared_value': validated_data['declared_value'],
            'special_instructions': validated_data.get('special_instructions', ''),
            'is_fragile': validated_data['is_fragile'],
            'is_perishable': validated_data['is_perishable'],
            'requires_signature': validated_data['requires_signature']
        }

        delivery_data = {
            'pickup_address': validated_data['pickup_address'],
            'delivery_address': validated_data['delivery_address'],
            'estimated_pickup': validated_data['estimated_pickup'],
            'estimated_delivery': validated_data['estimated_delivery'],
            'priority': validated_data['priority'],
            'delivery_fee': validated_data['delivery_fee']
        }

        payment_data = {
            'amount': validated_data['payment_amount'],
            'payment_method': validated_data['payment_method'],
            'cod_amount': validated_data['cod_amount']
        }

        rider_id = validated_data.get('rider_id')

        # Get or create sender UserProfile
        # For simplicity, we'll create a dummy user if sender doesn't exist
        # In production, you'd want to search existing users or create properly
        from django.contrib.auth.models import User
        from django.db import transaction

        with transaction.atomic():
            # Create or get sender user
            sender_username = f"sender_{sender_data['phone']}"
            sender_user, created = User.objects.get_or_create(
                username=sender_username,
                defaults={
                    'email': sender_data.get('email', ''),
                    'first_name': sender_data['name'].split()[0] if sender_data['name'] else '',
                    'last_name': ' '.join(sender_data['name'].split()[1:]) if len(sender_data['name'].split()) > 1 else ''
                }
            )

            sender_profile, created = UserProfile.objects.get_or_create(
                user=sender_user,
                defaults={
                    'user_type': 'customer',
                    'phone': sender_data['phone'],
                    'address': sender_data['address']
                }
            )

            # Create package
            package = Package.objects.create(**package_data)

            # Create delivery
            delivery = Delivery.objects.create(
                sender=sender_profile,
                recipient_name=recipient_data['name'],
                recipient_phone=recipient_data['phone'],
                package=package,
                **delivery_data,
                created_by=self.context['request'].user
            )

            if rider_id:
                try:
                    rider = UserProfile.objects.get(id=rider_id, user_type__in=['rider', 'both'])
                    delivery.rider = rider
                    delivery.status = 'assigned'
                    delivery.save()
                except UserProfile.DoesNotExist:
                    pass  # Ignore invalid rider

            # Create payment
            Payment.objects.create(
                delivery=delivery,
                **payment_data
            )

            return delivery