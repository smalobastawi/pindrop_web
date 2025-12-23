# delivery/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Customer(models.Model):
    """Customer/Client model"""
    USER_TYPES = [
        ('customer', 'Customer'),
        ('rider', 'Rider'),
        ('both', 'Both Customer and Rider')
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('pending_approval', 'Pending Approval')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    profile_image = models.ImageField(upload_to='customer_profiles/', blank=True, null=True)
    
    # Additional fields for mobile app
    device_token = models.CharField(max_length=500, blank=True, null=True)
    push_enabled = models.BooleanField(default=True)
    preferred_language = models.CharField(max_length=10, default='en')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def is_rider(self):
        return self.user_type in ['rider', 'both']
    
    @property
    def is_customer(self):
        return self.user_type in ['customer', 'both']

class Driver(models.Model):
    """Delivery driver model"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('pending_approval', 'Pending Approval')
    ]
    
    VEHICLE_TYPES = [
        ('bicycle', 'Bicycle'),
        ('motorcycle', 'Motorcycle'),
        ('car', 'Car'),
        ('van', 'Van'),
        ('truck', 'Truck')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=True, blank=True)
    
    # Driver information
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry = models.DateField(null=True, blank=True)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    vehicle_plate = models.CharField(max_length=20)
    vehicle_model = models.CharField(max_length=100, blank=True)
    vehicle_color = models.CharField(max_length=50, blank=True)
    vehicle_year = models.IntegerField(null=True, blank=True)
    
    # Status and availability
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_approval')
    is_available = models.BooleanField(default=True)
    current_location = models.CharField(max_length=200, blank=True)
    last_location_update = models.DateTimeField(null=True, blank=True)
    
    # Rating and performance
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    total_ratings = models.IntegerField(default=0)
    completed_deliveries = models.IntegerField(default=0)
    
    # Additional fields for mobile app
    device_token = models.CharField(max_length=500, blank=True, null=True)
    push_enabled = models.BooleanField(default=True)
    preferred_language = models.CharField(max_length=10, default='en')
    
    # Working hours
    working_hours_start = models.TimeField(null=True, blank=True)
    working_hours_end = models.TimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        full_name = self.user.get_full_name() or self.user.username
        return f"{full_name} - {self.vehicle_plate}"
    
    @property
    def is_approved(self):
        return self.status == 'active'

class Package(models.Model):
    """Package/delivery item model"""
    PACKAGE_TYPES = [
        ('document', 'Document'),
        ('parcel', 'Parcel'),
        ('fragile', 'Fragile'),
        ('perishable', 'Perishable'),
    ]
    
    description = models.CharField(max_length=500)
    weight = models.DecimalField(max_digits=6, decimal_places=2)  # in kg
    dimensions = models.CharField(max_length=100)  # LxWxH in cm
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPES)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    special_instructions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.description[:50]} ({self.get_package_type_display()})"

class Delivery(models.Model):
    """Main delivery model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned to Driver'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('failed', 'Delivery Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    tracking_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='deliveries')
    sender = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sent_deliveries')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    package = models.OneToOneField(Package, on_delete=models.CASCADE)
    
    pickup_address = models.TextField()
    delivery_address = models.TextField()
    estimated_pickup = models.DateTimeField()
    estimated_delivery = models.DateTimeField()
    actual_pickup = models.DateTimeField(null=True, blank=True)
    actual_delivery = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.IntegerField(default=1)  # 1=Normal, 2=Express, 3=Urgent
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery #{self.tracking_number} - {self.get_status_display()}"

class DeliveryStatusUpdate(models.Model):
    """Track status updates for a delivery"""
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='status_updates')
    status = models.CharField(max_length=20, choices=Delivery.STATUS_CHOICES)
    location = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.delivery.tracking_number} - {self.get_status_display()} at {self.created_at}"

class Payment(models.Model):
    """Payment information"""
    PAYMENT_METHODS = [
        ('cash', 'Cash on Delivery'),
        ('card', 'Credit/Debit Card'),
        ('bank', 'Bank Transfer'),
        ('mobile', 'Mobile Money'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Delivery #{self.delivery.tracking_number}"