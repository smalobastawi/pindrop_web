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
        name = request.data.get('name')
        email = request.data.get('email')
        phone = request.data.get('phone')
        address = request.data.get('address')
        password = request.data.get('password')
        
        if not all([name, email, phone, address, password]):
            return Response({'error': 'All fields are required'}, status=400)
        
        # Check if customer with email already exists
        if Customer.objects.filter(email=email).exists():
            return Response({'error': 'Customer with this email already exists'}, status=400)
        
        # Create user account
        username = email.split('@')[0] + str(uuid.uuid4())[:8]
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Create customer profile
        customer = Customer.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address
        )
        
        return Response({
            'message': 'Customer registered successfully',
            'customer': CustomerSerializer(customer).data
        }, status=201)

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