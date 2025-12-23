# api/views.py
import uuid
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.utils import timezone
from delivery.models import Customer, Driver, Package, Delivery, DeliveryStatusUpdate, Payment
from .serializers import *

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated]

class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [permissions.IsAuthenticated]

class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Filter based on user role
        if user.groups.filter(name='Drivers').exists():
            # Drivers see only their assigned deliveries
            try:
                driver = Driver.objects.get(user=user)
                return queryset.filter(driver=driver)
            except Driver.DoesNotExist:
                return queryset.none()
        else:
            # Admins/managers see all deliveries
            return queryset

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        delivery = self.get_object()
        status = request.data.get('status')
        location = request.data.get('location', '')
        notes = request.data.get('notes', '')
        
        if status:
            DeliveryStatusUpdate.objects.create(
                delivery=delivery,
                status=status,
                location=location,
                notes=notes,
                updated_by=request.user
            )
            delivery.status = status
            delivery.save()
            
            return Response({'message': 'Status updated successfully'})
        
        return Response({'error': 'Status is required'}, status=400)

    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        total = Delivery.objects.count()
        delivered = Delivery.objects.filter(status='delivered').count()
        in_transit = Delivery.objects.filter(status='in_transit').count()
        pending = Delivery.objects.filter(status='pending').count()
        
        return Response({
            'total': total,
            'delivered': delivered,
            'in_transit': in_transit,
            'pending': pending,
            'completion_rate': (delivered / total * 100) if total > 0 else 0
        })

class DeliveryStatusUpdateViewSet(viewsets.ModelViewSet):
    queryset = DeliveryStatusUpdate.objects.all()
    serializer_class = DeliveryStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

class CustomerRegistrationView(APIView):
    """Customer registration endpoint"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = CustomerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return Response({
                'message': 'Customer registered successfully',
                'customer': CustomerSerializer(customer).data
            }, status=201)
        return Response(serializer.errors, status=400)

class RiderRegistrationView(APIView):
    """Rider registration endpoint"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        # Manually validate required fields
        required_fields = ['name', 'email', 'phone', 'address', 'license_number', 'vehicle_type', 'vehicle_plate', 'password']
        for field in required_fields:
            if not request.data.get(field):
                return Response({'error': f'{field} is required'}, status=400)
        
        # Check if email already exists
        if Customer.objects.filter(email=request.data.get('email')).exists():
            return Response({'error': 'User with this email already exists'}, status=400)
        
        try:
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
            import uuid
            username = customer_data['email'].split('@')[0] + str(uuid.uuid4())[:8]
            user = User.objects.create_user(
                username=username,
                email=customer_data['email'],
                password=request.data.get('password'),
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
            driver_data = {k: v for k, v in driver_data.items() if v is not None and v != ''}
            
            driver = Driver.objects.create(**driver_data)
            
            return Response({
                'message': 'Rider registered successfully. Awaiting approval.',
                'driver': DriverSerializer(driver).data
            }, status=201)
            
        except Exception as e:
            return Response({'error': f'Failed to register rider: {str(e)}'}, status=400)

class UnifiedRegistrationView(APIView):
    """Unified registration endpoint for both customers and riders"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        user_type = request.data.get('user_type', 'customer')
        
        if user_type == 'rider':
            serializer = RiderRegistrationSerializer(data=request.data)
        else:
            serializer = CustomerRegistrationSerializer(data=request.data)
            
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': f'{user_type.capitalize()} registered successfully',
                'user': CustomerSerializer(user).data if user_type != 'rider' else DriverSerializer(user).data
            }, status=201)
        return Response(serializer.errors, status=400)

class CustomerPortalView(APIView):
    """Customer portal API for customers to manage their orders"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Get or create customer profile for authenticated user
        try:
            customer = Customer.objects.get(email=request.user.email)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer profile not found'}, status=404)
        
        # Get customer orders
        orders = Delivery.objects.filter(
            Q(customer=customer) | Q(sender=customer)
        ).order_by('-created_at')
        
        orders_data = []
        for order in orders:
            order_data = DeliverySerializer(order).data
            try:
                payment = Payment.objects.get(delivery=order)
                order_data['payment'] = PaymentSerializer(payment).data
            except Payment.DoesNotExist:
                order_data['payment'] = None
            orders_data.append(order_data)
        
        return Response({
            'customer': CustomerSerializer(customer).data,
            'orders': orders_data,
            'stats': {
                'total_orders': orders.count(),
                'pending_orders': orders.filter(status='pending').count(),
                'completed_orders': orders.filter(status='delivered').count(),
                'total_spent': Payment.objects.filter(
                    delivery__in=orders,
                    status='paid'
                ).aggregate(Sum('amount'))['amount__sum'] or 0
            }
        })
    
    def post(self, request):
        """Create new delivery order"""
        try:
            customer = Customer.objects.get(email=request.user.email)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer profile not found'}, status=404)
        
        # Validate order data
        package_data = request.data.get('package', {})
        delivery_data = request.data.get('delivery', {})
        payment_data = request.data.get('payment', {})
        
        if not all([package_data, delivery_data, payment_data]):
            return Response({'error': 'Package, delivery, and payment data are required'}, status=400)
        
        try:
            # Create package
            package = Package.objects.create(
                description=package_data.get('description'),
                weight=package_data.get('weight'),
                dimensions=package_data.get('dimensions'),
                package_type=package_data.get('package_type'),
                value=package_data.get('value', 0),
                special_instructions=package_data.get('special_instructions', '')
            )
            
            # Generate tracking number
            tracking_number = f"PKG{uuid.uuid4().hex[:12].upper()}"
            
            # Calculate delivery fee (basic calculation)
            delivery_fee = float(package_data.get('weight', 1)) * 10  # 10 currency units per kg
            
            # Create delivery
            delivery = Delivery.objects.create(
                tracking_number=tracking_number,
                customer=customer,
                sender=customer,
                package=package,
                pickup_address=delivery_data.get('pickup_address'),
                delivery_address=delivery_data.get('delivery_address'),
                estimated_pickup=delivery_data.get('estimated_pickup'),
                estimated_delivery=delivery_data.get('estimated_delivery'),
                priority=delivery_data.get('priority', 1),
                delivery_fee=delivery_fee,
                created_by=request.user
            )
            
            # Create payment record
            payment = Payment.objects.create(
                delivery=delivery,
                amount=payment_data.get('amount', delivery_fee),
                payment_method=payment_data.get('payment_method', 'cash'),
                status='pending'
            )
            
            return Response({
                'message': 'Order created successfully',
                'order': DeliverySerializer(delivery).data,
                'payment': PaymentSerializer(payment).data,
                'tracking_number': tracking_number
            }, status=201)
            
        except Exception as e:
            return Response({'error': f'Failed to create order: {str(e)}'}, status=400)

class OrderTrackingView(APIView):
    """Track order by tracking number"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        tracking_number = request.GET.get('tracking_number')
        
        if not tracking_number:
            return Response({'error': 'Tracking number is required'}, status=400)
        
        try:
            delivery = Delivery.objects.get(tracking_number=tracking_number)
            
            delivery_data = DeliverySerializer(delivery).data
            
            # Add status updates
            status_updates = DeliveryStatusUpdate.objects.filter(delivery=delivery)
            delivery_data['status_updates'] = DeliveryStatusUpdateSerializer(status_updates, many=True).data
            
            # Add payment info
            try:
                payment = Payment.objects.get(delivery=delivery)
                delivery_data['payment'] = PaymentSerializer(payment).data
            except Payment.DoesNotExist:
                delivery_data['payment'] = None
            
            return Response(delivery_data)
            
        except Delivery.DoesNotExist:
            return Response({'error': 'Delivery not found'}, status=404)

class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        if user.groups.filter(name='Drivers').exists():
            try:
                driver = Driver.objects.get(user=user)
                deliveries = Delivery.objects.filter(driver=driver)
                
                stats = {
                    'assigned': deliveries.filter(status='assigned').count(),
                    'in_transit': deliveries.filter(status='in_transit').count(),
                    'delivered_today': deliveries.filter(
                        status='delivered',
                        actual_delivery__date=timezone.now().date()
                    ).count(),
                }
            except Driver.DoesNotExist:
                stats = {}
        else:
            stats = {
                'total_customers': Customer.objects.count(),
                'total_drivers': Driver.objects.count(),
                'active_deliveries': Delivery.objects.exclude(
                    status__in=['delivered', 'cancelled']
                ).count(),
                'revenue_today': Payment.objects.filter(
                    status='paid',
                    paid_at__date=timezone.now().date()
                ).aggregate(Sum('amount'))['amount__sum'] or 0,
            }
        
        return Response(stats)

class MobileAPIVersionView(APIView):
    """Mobile API version information"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        return Response({
            'api_version': '1.0.0',
            'api_name': 'PinDrop Delivery API',
            'supported_features': [
                'customer_registration',
                'rider_registration', 
                'order_tracking',
                'push_notifications',
                'real_time_location'
            ]
        })

class MobileUserProfileView(APIView):
    """Mobile app user profile management"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get current user profile"""
        try:
            # Try to get customer profile first
            customer = Customer.objects.get(email=request.user.email)
            return Response({
                'profile': CustomerSerializer(customer).data,
                'user_type': 'customer'
            })
        except Customer.DoesNotExist:
            try:
                # Try to get driver profile
                driver = Driver.objects.get(user=request.user)
                return Response({
                    'profile': DriverSerializer(driver).data,
                    'user_type': 'rider'
                })
            except Driver.DoesNotExist:
                return Response({'error': 'User profile not found'}, status=404)
    
    def put(self, request):
        """Update current user profile"""
        try:
            customer = Customer.objects.get(email=request.user.email)
            serializer = CustomerSerializer(customer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Customer.DoesNotExist:
            try:
                driver = Driver.objects.get(user=request.user)
                serializer = DriverSerializer(driver, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=400)
            except Driver.DoesNotExist:
                return Response({'error': 'User profile not found'}, status=404)

class MobileDeviceTokenView(APIView):
    """Register/update device token for push notifications"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Register device token"""
        token = request.data.get('device_token')
        user_type = request.data.get('user_type', 'customer')
        
        if not token:
            return Response({'error': 'Device token is required'}, status=400)
        
        try:
            if user_type == 'rider':
                driver = Driver.objects.get(user=request.user)
                driver.device_token = token
                driver.save()
            else:
                customer = Customer.objects.get(email=request.user.email)
                customer.device_token = token
                customer.save()
                
            return Response({'message': 'Device token registered successfully'})
        except (Customer.DoesNotExist, Driver.DoesNotExist):
            return Response({'error': 'User profile not found'}, status=404)