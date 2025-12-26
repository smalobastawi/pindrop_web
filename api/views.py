# api/views.py - Simplified version
import uuid
import requests
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from delivery.models import UserProfile, Package, Delivery, DeliveryStatusUpdate, Payment
from .serializers import *
from core.logging_utils import log_api_error, log_app_error, log_db_error
from core.permissions import HasRolePermission, has_permission

class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for managing user profiles with filtering"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'user__email', 'phone', 'user__first_name', 'user__last_name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user_type = self.request.query_params.get('user_type', None)
        
        if user_type:
            queryset = queryset.filter(user_type=user_type)
        
        return queryset

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

        try:
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.user_type in ['rider', 'both']:
                return queryset.filter(rider=user_profile)
            else:
                return queryset.filter(sender=user_profile)
        except UserProfile.DoesNotExist:
            return queryset.none()

    def create(self, request, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.user_type in ['rider']:
                return Response({'error': 'Riders are not allowed to create deliveries'}, status=403)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=404)

        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        delivery = self.get_object()
        status_value = request.data.get('status')
        location = request.data.get('location', '')
        notes = request.data.get('notes', '')
        
        if status_value:
            DeliveryStatusUpdate.objects.create(
                delivery=delivery,
                status=status_value,
                location=location,
                notes=notes,
                updated_by=request.user
            )
            delivery.status = status_value
            delivery.save()
            return Response({'message': 'Status updated successfully'})
        
        return Response({'error': 'Status is required'}, status=400)

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
        try:
            serializer = CustomerRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                customer = serializer.save()
                log_api_error(f'Customer registration successful for {customer.user.email}')
                return Response({
                    'message': 'Customer registered successfully',
                    'customer': CustomerSerializer(customer).data
                }, status=201)
            log_api_error(f'Customer registration failed: {serializer.errors}')
            return Response(serializer.errors, status=400)
        except Exception as e:
            log_api_error(f'Error during customer registration: {str(e)}')
            return Response({'error': str(e)}, status=400)

class RiderRegistrationView(APIView):
    """Rider registration endpoint"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        try:
            # Handle both JSON and FormData submissions
            data = request.data.copy()

            # Debug: Log what we're receiving
            log_app_error(f'Rider registration request data: {dict(data)}')
            log_app_error(f'Request content type: {request.content_type}')
            log_app_error(f'Request POST: {dict(request.POST) if hasattr(request, "POST") else "No POST"}')
            log_app_error(f'Request FILES: {dict(request.FILES) if hasattr(request, "FILES") else "No FILES"}')

            # Handle different field structures:
            # - JSON API calls might send 'name' instead of 'first_name' and 'last_name'
            # - FormData calls send 'first_name' and 'last_name' separately

            # Flatten list values that come from FormData to strings
            flattened_data = {}
            for key, value in data.items():
                if isinstance(value, list) and len(value) == 1:
                    # If it's a single-item list, extract the first element
                    flattened_data[key] = value[0]
                elif isinstance(value, list) and len(value) > 1:
                    # If it's a multi-item list, keep as is (for multi-select fields)
                    flattened_data[key] = value
                else:
                    # Keep non-list values as they are
                    flattened_data[key] = value

            # Handle 'name' field for JSON API calls - split into first_name and last_name
            if 'name' in flattened_data and ('first_name' not in flattened_data or 'last_name' not in flattened_data):
                # Split name into first and last name
                name_parts = flattened_data['name'].strip().split(' ', 1)
                if len(name_parts) >= 1:
                    flattened_data['first_name'] = name_parts[0]
                if len(name_parts) >= 2:
                    flattened_data['last_name'] = name_parts[1]
                else:
                    flattened_data['last_name'] = ''  # Default empty last name if only one name provided

            # Ensure we have all required fields from either request.data or request.POST
            required_fields = ['first_name', 'last_name', 'email', 'password', 'phone', 'address',
                              'license_number', 'vehicle_type', 'vehicle_plate']

            for field in required_fields:
                if field not in flattened_data or not flattened_data[field]:
                    # Try to get from POST if not in data
                    if hasattr(request, 'POST') and field in request.POST:
                        post_value = request.POST[field]
                        flattened_data[field] = post_value[0] if isinstance(post_value, list) and len(post_value) == 1 else post_value
                    elif field == 'password' and hasattr(request, 'POST') and 'password' in request.POST:
                        post_value = request.POST['password']
                        flattened_data[field] = post_value[0] if isinstance(post_value, list) and len(post_value) == 1 else post_value

            # Debug: Log the final data being sent to serializer
            log_app_error(f'Final data for serializer: {flattened_data}')

            serializer = RiderRegistrationSerializer(data=flattened_data)
            if serializer.is_valid():
                rider = serializer.save()
                log_api_error(f'Rider registration successful for {rider.user.email}')
                return Response({
                    'message': 'Rider registered successfully',
                    'rider': RiderSerializer(rider).data
                }, status=201)
            log_api_error(f'Rider registration failed: {serializer.errors}')
            return Response(serializer.errors, status=400)
        except Exception as e:
            log_api_error(f'Error during rider registration: {str(e)}')
            return Response({'error': str(e)}, status=400)

class UnifiedRegistrationView(APIView):
    """Unified registration endpoint for both customers and riders"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        # Handle both JSON and FormData submissions
        data = request.data.copy()
        
        # Handle 'name' field for JSON API calls - split into first_name and last_name
        if 'name' in data and ('first_name' not in data or 'last_name' not in data):
            # Split name into first and last name
            name_parts = data['name'].strip().split(' ', 1)
            if len(name_parts) >= 1:
                data['first_name'] = name_parts[0]
            if len(name_parts) >= 2:
                data['last_name'] = name_parts[1]
            else:
                data['last_name'] = ''  # Default empty last name if only one name provided
        
        user_type = data.get('user_type', 'customer')
        
        if user_type == 'rider':
            # For rider registration, provide default values for optional fields if not provided
            if 'identity_type' not in data:
                data['identity_type'] = 'national_id'  # Default identity type
            if 'identity_number' not in data:
                data['identity_number'] = ''  # Default empty identity number
            
            serializer = RiderRegistrationSerializer(data=data)
        else:
            serializer = CustomerRegistrationSerializer(data=data)
             
        if serializer.is_valid():
            user_profile = serializer.save()
            if user_type == 'rider':
                return Response({
                    'message': 'Rider registered successfully',
                    'user': RiderSerializer(user_profile).data
                }, status=201)
            else:
                return Response({
                    'message': 'Customer registered successfully',
                    'user': CustomerSerializer(user_profile).data
                }, status=201)
        return Response(serializer.errors, status=400)

class CustomerPortalView(APIView):
    """Customer portal API for customers to manage their orders"""
    permission_classes = [permissions.IsAuthenticated, HasRolePermission(['view_own_orders', 'create_orders'])]

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.user_type not in ['customer', 'both']:
                return Response({'error': 'User is not a customer'}, status=403)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=404)

        # Get customer orders
        orders = Delivery.objects.filter(
            sender=user_profile
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
            'customer': CustomerSerializer(user_profile).data,
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
        log_app_error(f'POST request data: {dict(request.data)}')
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.user_type not in ['customer', 'both']:
                return Response({'error': 'User is not a customer'}, status=403)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=404)

        # Validate order data
        package_data = request.data.get('package', {})
        delivery_data = request.data.get('delivery', {})
        payment_data = request.data.get('payment', {})

        log_app_error(f'Package data: {package_data}')
        log_app_error(f'Delivery data: {delivery_data}')
        log_app_error(f'Payment data: {payment_data}')

        if not all([package_data, delivery_data, payment_data]):
            return Response({'error': 'Package, delivery, and payment data are required'}, status=400)

        try:
            # Parse dimensions if provided
            dimensions = package_data.get('dimensions', '')
            length = width = height = None
            if dimensions and 'x' in dimensions:
                try:
                    dims = dimensions.split('x')
                    if len(dims) == 3:
                        length = float(dims[0])
                        width = float(dims[1])
                        height = float(dims[2])
                except ValueError:
                    pass  # Ignore parsing errors

            log_app_error(f'Creating package with data: {package_data}')
            # Create package
            package = Package.objects.create(
                description=package_data.get('description'),
                weight=float(package_data.get('weight', 0)),
                length=length,
                width=width,
                height=height,
                package_type=package_data.get('package_type'),
                declared_value=float(package_data.get('value', 0)),
                special_instructions=package_data.get('special_instructions', '')
            )

            # Generate tracking number
            tracking_number = f"PKG{uuid.uuid4().hex[:12].upper()}"

            # Calculate delivery fee (basic calculation)
            delivery_fee = float(package_data.get('weight', 1)) * 10  # 10 currency units per kg

            log_app_error(f'Creating delivery with data: {delivery_data}')
            # Parse datetimes
            estimated_pickup = parse_datetime(delivery_data.get('estimated_pickup'))
            estimated_delivery = parse_datetime(delivery_data.get('estimated_delivery'))

            if not estimated_pickup or not estimated_delivery:
                raise ValueError("Invalid datetime format for estimated_pickup or estimated_delivery")

            # Create delivery
            delivery = Delivery.objects.create(
                tracking_number=tracking_number,
                sender=user_profile,
                recipient_name=delivery_data.get('recipient_name'),
                recipient_phone=delivery_data.get('recipient_phone'),
                package=package,
                pickup_address=delivery_data.get('pickup_address'),
                delivery_address=delivery_data.get('delivery_address'),
                estimated_pickup=estimated_pickup,
                estimated_delivery=estimated_delivery,
                priority=delivery_data.get('priority', 1),
                delivery_fee=delivery_fee,
                created_by=request.user
            )

            log_app_error(f'Creating payment with data: {payment_data}')
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
            log_app_error(f'Error creating order: {str(e)}')
            return Response({'error': f'Failed to create order: {str(e)}'}, status=400)


class RiderPortalView(APIView):
    """Rider portal API for riders to manage their deliveries"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.user_type not in ['rider', 'both']:
                return Response({'error': 'User is not a rider'}, status=403)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=404)

        # Get rider deliveries
        deliveries = Delivery.objects.filter(
            rider=user_profile
        ).order_by('-created_at')

        deliveries_data = []
        for delivery in deliveries:
            delivery_data = DeliverySerializer(delivery).data
            try:
                payment = Payment.objects.get(delivery=delivery)
                delivery_data['payment'] = PaymentSerializer(payment).data
            except Payment.DoesNotExist:
                delivery_data['payment'] = None
            deliveries_data.append(delivery_data)

        # Calculate earnings
        completed_deliveries = deliveries.filter(status='delivered')
        total_earnings = Payment.objects.filter(
            delivery__in=completed_deliveries,
            status='paid'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        return Response({
            'rider': RiderSerializer(user_profile).data,
            'deliveries': deliveries_data,
            'stats': {
                'total_deliveries': deliveries.count(),
                'pending_deliveries': deliveries.filter(status='assigned').count(),
                'in_transit': deliveries.filter(status='in_transit').count(),
                'completed_deliveries': completed_deliveries.count(),
                'total_earnings': total_earnings,
                'rating': float(user_profile.rating),
                'is_available': user_profile.is_available,
            }
        })


class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=404)

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
        
        try:
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.user_type in ['rider', 'both']:
                # Rider dashboard
                deliveries = Delivery.objects.filter(rider=user_profile)
                
                stats = {
                    'assigned': deliveries.filter(status='assigned').count(),
                    'in_transit': deliveries.filter(status='in_transit').count(),
                    'delivered_today': deliveries.filter(
                        status='delivered',
                        actual_delivery__date=timezone.now().date()
                    ).count(),
                    'total_completed': user_profile.completed_deliveries,
                    'rating': float(user_profile.rating),
                    'is_available': user_profile.is_available,
                }
            else:
                # Admin/customer dashboard
                stats = {
                    'total_customers': UserProfile.objects.filter(user_type='customer').count(),
                    'total_riders': UserProfile.objects.filter(user_type__in=['rider', 'both']).count(),
                    'active_deliveries': Delivery.objects.exclude(
                        status__in=['delivered', 'cancelled']
                    ).count(),
                    'revenue_today': Payment.objects.filter(
                        status='paid',
                        paid_at__date=timezone.now().date()
                    ).aggregate(Sum('amount'))['amount__sum'] or 0,
                }
            return Response(stats)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=404)

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
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(user_profile)
            return Response({
                'profile': serializer.data,
                'user_type': user_profile.user_type
            })
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=404)
    
    def put(self, request):
        """Update current user profile"""
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=404)

class MobileDeviceTokenView(APIView):
    """Register/update device token for push notifications"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Register device token"""
        token = request.data.get('device_token')
        
        if not token:
            return Response({'error': 'Device token is required'}, status=400)
        
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.device_token = token
            user_profile.save()
                
            return Response({'message': 'Device token registered successfully'})
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=404)

class RiderAvailabilityView(APIView):
    """Manage rider availability"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Update rider availability status"""
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.user_type not in ['rider', 'both']:
                return Response({'error': 'User is not a rider'}, status=403)
            
            is_available = request.data.get('is_available')
            current_location = request.data.get('current_location')
            
            if is_available is not None:
                user_profile.is_available = is_available
            
            if current_location:
                user_profile.current_location = current_location
                user_profile.last_location_update = timezone.now()
            
            user_profile.save()
            
            return Response({
                'message': 'Availability updated successfully',
                'is_available': user_profile.is_available,
                'current_location': user_profile.current_location
            })
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=404)


class GoogleLoginView(APIView):
    """Google Sign-In authentication"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        credential = request.data.get('credential')
        if not credential:
            return Response({'error': 'Credential is required'}, status=400)

        try:
            # Verify the token with Google
            response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={credential}')
            if response.status_code != 200:
                return Response({'error': 'Invalid token'}, status=400)

            google_data = response.json()

            # Check if user exists
            try:
                user = User.objects.get(email=google_data['email'])
                user_profile = UserProfile.objects.get(user=user)
            except (User.DoesNotExist, UserProfile.DoesNotExist):
                # Create new user with random password
                random_password = uuid.uuid4().hex[:12]  # Generate random password

                # Parse name
                given_name = google_data.get('given_name', '')
                family_name = google_data.get('family_name', '')
                full_name = google_data.get('name', '')
                if not given_name and not family_name and full_name:
                    name_parts = full_name.split(' ', 1)
                    given_name = name_parts[0]
                    family_name = name_parts[1] if len(name_parts) > 1 else ''

                user = User.objects.create_user(
                    username=google_data['email'],
                    email=google_data['email'],
                    password=random_password,
                    first_name=given_name,
                    last_name=family_name
                )

                user_profile = UserProfile.objects.create(
                    user=user,
                    user_type='customer',
                    phone='Not provided',
                    address='Not provided'
                )

                # Assign customer role
                try:
                    from main.models import Role, UserRole
                    customer_role = Role.objects.get(name='customer')
                    UserRole.objects.create(user=user, role=customer_role)
                except Role.DoesNotExist:
                    pass  # Role not found, continue without assigning

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'user_type': user_profile.user_type
                }
            })

        except requests.RequestException as e:
            log_api_error(f'Google token verification failed: {str(e)}')
            return Response({'error': 'Token verification failed'}, status=400)
        except Exception as e:
            log_api_error(f'Google login error: {str(e)}')
            return Response({'error': str(e)}, status=400)