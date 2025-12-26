# delivery/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid

class UserProfile(models.Model):
    """Unified user profile that can be both customer and rider"""
    USER_TYPES = [
        ('customer', 'Customer Only'),
        ('rider', 'Rider Only'),
        ('both', 'Customer & Rider'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('pending_approval', 'Pending Approval'),
    ]
    
    VEHICLE_TYPES = [
        ('bicycle', 'Bicycle'),
        ('motorcycle', 'Motorcycle'),
        ('car', 'Car'),
        ('van', 'Van'),
        ('truck', 'Truck'),
        ('none', 'No Vehicle'),
    ]
    
    IDENTITY_TYPES = [
        ('passport', 'Passport'),
        ('national_id', 'National ID'),
        ('drivers_license', 'Driver\'s License'),
        ('other', 'Other'),
    ]
    
    # Core user info
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Contact info
    phone = models.CharField(max_length=20)
    address = models.TextField()
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    # ===== RIDER-SPECIFIC FIELDS =====
    license_number = models.CharField(max_length=50, blank=True, null=True)
    license_expiry = models.DateField(null=True, blank=True)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES, default='none')
    vehicle_plate = models.CharField(max_length=20, blank=True, null=True)
    vehicle_model = models.CharField(max_length=100, blank=True, null=True)
    vehicle_color = models.CharField(max_length=50, blank=True, null=True)
    vehicle_year = models.IntegerField(null=True, blank=True)
    
    # Identity verification
    identity_type = models.CharField(max_length=20, choices=IDENTITY_TYPES, blank=True, null=True)
    identity_number = models.CharField(max_length=50, blank=True, null=True)
    identity_document = models.ImageField(upload_to='identity_documents/', blank=True, null=True)
    license_document = models.ImageField(upload_to='license_documents/', blank=True, null=True)
    
    # Rider status and availability
    is_available = models.BooleanField(default=False)
    current_location = models.CharField(max_length=200, blank=True, null=True)
    last_location_update = models.DateTimeField(null=True, blank=True)
    
    # Rating and performance
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_ratings = models.IntegerField(default=0)
    completed_deliveries = models.IntegerField(default=0)
    
    # Working hours
    working_hours_start = models.TimeField(null=True, blank=True)
    working_hours_end = models.TimeField(null=True, blank=True)
    
    # Preferences and settings
    device_token = models.CharField(max_length=500, blank=True, null=True)
    push_enabled = models.BooleanField(default=True)
    preferred_language = models.CharField(max_length=10, default='en')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        indexes = [
            models.Index(fields=['user_type', 'status']),
            models.Index(fields=['is_available', 'user_type']),
        ]
    
    def __str__(self):
        full_name = self.user.get_full_name() or self.user.username
        return f"{full_name} ({self.get_user_type_display()})"
    
    def clean(self):
        """Validate data based on user type"""
        super().clean()
        
        if self.user_type in ['rider', 'both']:
            # Riders MUST have these fields
            required_fields = [
                ('license_number', 'License number is required for riders'),
                ('vehicle_plate', 'Vehicle plate is required for riders'),
                ('vehicle_type', 'Riders must have a vehicle type'),
                ('identity_type', 'Identity type is required for riders'),
                ('identity_number', 'Identity number is required for riders'),
            ]
            
            for field, error_message in required_fields:
                if not getattr(self, field):
                    raise ValidationError({field: error_message})
            
            if self.vehicle_type == 'none':
                raise ValidationError({'vehicle_type': 'Riders must have a vehicle type'})
            
            # Validate license expiry
            if self.license_expiry and self.license_expiry < timezone.now().date():
                raise ValidationError({'license_expiry': 'License has expired'})
        
        elif self.user_type == 'customer':
            # Customers shouldn't have vehicle info
            if self.vehicle_type != 'none':
                raise ValidationError({'vehicle_type': 'Customers should not have a vehicle type'})
            if self.vehicle_plate or self.license_number:
                raise ValidationError('Customers should not have vehicle or license information')
    
    def save(self, *args, **kwargs):
        """Override save to run full_clean"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def is_rider_approved(self):
        """Check if rider is approved and active"""
        return (
            self.user_type in ['rider', 'both'] and 
            self.status == 'active' and 
            self.license_number and 
            self.vehicle_plate and
            self.identity_number
        )
    
    @property
    def can_receive_deliveries(self):
        """Check if user can receive deliveries"""
        return self.user_type in ['customer', 'both'] and self.status == 'active'
    
    @property
    def can_make_deliveries(self):
        """Check if user can make deliveries as rider"""
        return self.is_rider_approved and self.is_available
    
    @property
    def is_online(self):
        """Check if rider is online and available"""
        if not self.is_available:
            return False
        
        # Check working hours if set
        if self.working_hours_start and self.working_hours_end:
            now = timezone.now().time()
            return self.working_hours_start <= now <= self.working_hours_end
        
        return True

class Package(models.Model):
    """Package/delivery item model"""
    PACKAGE_TYPES = [
        ('document', 'Document'),
        ('parcel', 'Parcel'),
        ('fragile', 'Fragile'),
        ('perishable', 'Perishable'),
        ('electronic', 'Electronic'),
        ('clothing', 'Clothing'),
        ('food', 'Food'),
        ('other', 'Other'),
    ]
    
    SIZE_CATEGORIES = [
        ('small', 'Small (≤ 0.5kg)'),
        ('medium', 'Medium (0.5-5kg)'),
        ('large', 'Large (5-20kg)'),
        ('xlarge', 'Extra Large (>20kg)'),
    ]
    
    # Package details
    description = models.CharField(max_length=500)
    weight = models.DecimalField(max_digits=6, decimal_places=2, help_text="Weight in kg")
    length = models.DecimalField(max_digits=6, decimal_places=2, help_text="Length in cm", null=True, blank=True)
    width = models.DecimalField(max_digits=6, decimal_places=2, help_text="Width in cm", null=True, blank=True)
    height = models.DecimalField(max_digits=6, decimal_places=2, help_text="Height in cm", null=True, blank=True)
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPES)
    size_category = models.CharField(max_length=20, choices=SIZE_CATEGORIES, default='medium')
    
    # Value and insurance
    declared_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    requires_insurance = models.BooleanField(default=False)
    insurance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    # Special handling
    special_instructions = models.TextField(blank=True)
    is_fragile = models.BooleanField(default=False)
    is_perishable = models.BooleanField(default=False)
    requires_signature = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Package'
        verbose_name_plural = 'Packages'
    
    def __str__(self):
        return f"{self.description[:50]} ({self.get_package_type_display()})"
    
    @property
    def dimensions(self):
        """Get formatted dimensions string"""
        if all([self.length, self.width, self.height]):
            return f"{self.length}x{self.width}x{self.height}cm"
        return "Not specified"
    
    @property
    def volume(self):
        """Calculate volume in cubic cm"""
        if all([self.length, self.width, self.height]):
            return self.length * self.width * self.height
        return None

class Delivery(models.Model):
    """Main delivery model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('searching', 'Searching for Rider'),
        ('assigned', 'Assigned to Rider'),
        ('accepted', 'Accepted by Rider'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('arrived', 'Arrived at Destination'),
        ('delivered', 'Delivered'),
        ('failed', 'Delivery Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        (1, 'Normal (24-48 hours)'),
        (2, 'Express (12-24 hours)'),
        (3, 'Urgent (2-6 hours)'),
        (4, 'Same Day (1-2 hours)'),
    ]
    
    # Tracking and identification
    tracking_number = models.CharField(max_length=50, unique=True)
    
    # Parties involved
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_deliveries')
    recipient_name = models.CharField(max_length=200)
    recipient_phone = models.CharField(max_length=20)
    rider = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, 
                             related_name='assigned_deliveries', limit_choices_to={'user_type__in': ['rider', 'both']})
    
    # Package details
    package = models.OneToOneField(Package, on_delete=models.CASCADE)
    
    # Address information
    pickup_address = models.TextField()
    pickup_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    pickup_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    delivery_address = models.TextField()
    delivery_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    delivery_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Timestamps
    estimated_pickup = models.DateTimeField()
    estimated_delivery = models.DateTimeField()
    actual_pickup = models.DateTimeField(null=True, blank=True)
    actual_delivery = models.DateTimeField(null=True, blank=True)
    
    # Status and priority
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)
    
    # Financials
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2)
    distance_km = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    estimated_duration_minutes = models.IntegerField(null=True, blank=True)
    
    # Metadata
    notes = models.TextField(blank=True)
    cancellation_reason = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['tracking_number']),
            models.Index(fields=['sender', 'status']),
            models.Index(fields=['rider', 'status']),
        ]
    
    def __str__(self):
        return f"Delivery #{self.tracking_number} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = f"DLV-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)
    
    @property
    def is_active(self):
        """Check if delivery is still active (not completed/cancelled)"""
        return self.status not in ['delivered', 'failed', 'cancelled']
    
    @property
    def delivery_time_minutes(self):
        """Calculate actual delivery time in minutes"""
        if self.actual_pickup and self.actual_delivery:
            delta = self.actual_delivery - self.actual_pickup
            return delta.total_seconds() / 60
        return None

class DeliveryStatusUpdate(models.Model):
    """Track status updates for a delivery"""
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='status_updates')
    status = models.CharField(max_length=20, choices=Delivery.STATUS_CHOICES)
    location = models.CharField(max_length=200, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    notes = models.TextField(blank=True)
    image = models.ImageField(upload_to='delivery_updates/', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Status Update'
        verbose_name_plural = 'Status Updates'
    
    def __str__(self):
        return f"{self.delivery.tracking_number} - {self.get_status_display()} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class Payment(models.Model):
    """Payment information"""
    PAYMENT_METHODS = [
        ('cash', 'Cash on Delivery'),
        ('card', 'Credit/Debit Card'),
        ('bank', 'Bank Transfer'),
        ('mobile', 'Mobile Money'),
        ('wallet', 'Wallet Balance'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('partially_refunded', 'Partially Refunded'),
    ]
    
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('KES', 'Kenyan Shilling'),
        ('NGN', 'Nigerian Naira'),
        ('GHS', 'Ghanaian Cedi'),
    ]
    
    # Relationships
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE, related_name='payment')
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    
    # Transaction details
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_gateway = models.CharField(max_length=50, blank=True)
    gateway_reference = models.CharField(max_length=200, blank=True)
    
    # COD specific
    cod_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, help_text="Cash on Delivery amount")
    cod_collected = models.BooleanField(default=False)
    cod_handover_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    # Timestamps
    paid_at = models.DateTimeField(null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        indexes = [
            models.Index(fields=['status', 'payment_method']),
            models.Index(fields=['transaction_id']),
        ]
    
    def __str__(self):
        return f"Payment for {self.delivery.tracking_number} - {self.get_status_display()}"
    
    @property
    def total_amount(self):
        """Calculate total amount including COD if applicable"""
        return self.amount + self.cod_amount
    
    @property
    def is_cod(self):
        """Check if this is a Cash on Delivery payment"""
        return self.payment_method == 'cash' and self.cod_amount > 0

class RiderRating(models.Model):
    """Ratings for riders"""
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE, related_name='rating')
    rider = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ratings_received')
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ratings_given')
    
    # Ratings (1-5)
    punctuality = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    handling = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    communication = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    professionalism = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    
    # Overall
    overall_rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    comments = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['delivery', 'rider', 'customer']
        verbose_name = 'Rider Rating'
        verbose_name_plural = 'Rider Ratings'
    
    def __str__(self):
        return f"{self.overall_rating}/5 for {self.rider.user.get_full_name()}"

class DeliveryProof(models.Model):
    """Proof of delivery"""
    PROOF_TYPES = [
        ('signature', 'Signature'),
        ('photo', 'Photo'),
        ('both', 'Signature and Photo'),
    ]
    
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE, related_name='proof')
    proof_type = models.CharField(max_length=20, choices=PROOF_TYPES)
    
    # Signature details
    signature_image = models.ImageField(upload_to='signatures/', null=True, blank=True)
    signature_name = models.CharField(max_length=200, blank=True)
    
    # Photo details
    delivery_photo = models.ImageField(upload_to='delivery_photos/', null=True, blank=True)
    
    # Additional proof
    recipient_id_type = models.CharField(max_length=50, blank=True)
    recipient_id_number = models.CharField(max_length=50, blank=True)
    
    notes = models.TextField(blank=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Delivery Proof'
        verbose_name_plural = 'Delivery Proofs'
    
    def __str__(self):
        return f"Proof for {self.delivery.tracking_number}"