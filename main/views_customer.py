# main/views_customer.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import uuid
from delivery.models import Customer, Package, Delivery, Payment

def customer_register(request):
    """Customer registration page"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone')
            address = data.get('address')
            password = data.get('password')
            
            # Check if customer exists
            if Customer.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Customer with this email already exists'}, status=400)
            
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
            
            return JsonResponse({'message': 'Customer registered successfully'})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return render(request, 'main/customer_register.html')

def customer_login(request):
    """Customer login page"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            # Simple authentication (in production, use proper auth)
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    # Create session
                    request.session['customer_email'] = email
                    return JsonResponse({'message': 'Login successful'})
                else:
                    return JsonResponse({'error': 'Invalid credentials'}, status=400)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=400)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return render(request, 'main/customer_login.html')

def customer_portal(request):
    """Customer portal dashboard"""
    if 'customer_email' not in request.session:
        return redirect('customer_login')
    
    email = request.session['customer_email']
    try:
        customer = Customer.objects.get(email=email)
        orders = Delivery.objects.filter(
            customer=customer
        ).order_by('-created_at')
        
        context = {
            'customer': customer,
            'orders': orders,
            'stats': {
                'total_orders': orders.count(),
                'pending_orders': orders.filter(status='pending').count(),
                'completed_orders': orders.filter(status='delivered').count(),
            }
        }
        return render(request, 'main/customer_portal.html', context)
    except Customer.DoesNotExist:
        return redirect('customer_login')

@csrf_exempt
def create_order(request):
    """Create new order"""
    if 'customer_email' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = request.session['customer_email']
            customer = Customer.objects.get(email=email)
            
            # Create package
            package = Package.objects.create(
                description=data['package']['description'],
                weight=data['package']['weight'],
                dimensions=data['package']['dimensions'],
                package_type=data['package']['package_type'],
                value=data['package'].get('value', 0),
                special_instructions=data['package'].get('special_instructions', '')
            )
            
            # Calculate delivery fee
            delivery_fee = float(data['package']['weight']) * 10
            
            # Create delivery
            delivery = Delivery.objects.create(
                tracking_number=f"PKG{uuid.uuid4().hex[:12].upper()}",
                customer=customer,
                sender=customer,
                package=package,
                pickup_address=data['delivery']['pickup_address'],
                delivery_address=data['delivery']['delivery_address'],
                estimated_pickup=data['delivery']['estimated_pickup'],
                estimated_delivery=data['delivery']['estimated_delivery'],
                priority=data['delivery'].get('priority', 1),
                delivery_fee=delivery_fee,
                created_by=customer.user if hasattr(customer, 'user') else None
            )
            
            # Create payment
            payment = Payment.objects.create(
                delivery=delivery,
                amount=data['payment'].get('amount', delivery_fee),
                payment_method=data['payment']['payment_method'],
                status='pending'
            )
            
            return JsonResponse({
                'message': 'Order created successfully',
                'tracking_number': delivery.tracking_number
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def track_order(request):
    """Track order by tracking number"""
    if request.method == 'GET':
        tracking_number = request.GET.get('tracking_number')
        if not tracking_number:
            return JsonResponse({'error': 'Tracking number required'}, status=400)
        
        try:
            delivery = Delivery.objects.get(tracking_number=tracking_number)
            
            order_data = {
                'tracking_number': delivery.tracking_number,
                'status': delivery.status,
                'package': {
                    'description': delivery.package.description,
                    'weight': delivery.package.weight,
                    'package_type': delivery.package.package_type
                },
                'delivery_address': delivery.delivery_address,
                'estimated_delivery': delivery.estimated_delivery,
                'created_at': delivery.created_at
            }
            
            # Add payment info
            try:
                payment = Payment.objects.get(delivery=delivery)
                order_data['payment'] = {
                    'amount': payment.amount,
                    'payment_method': payment.payment_method,
                    'status': payment.status
                }
            except Payment.DoesNotExist:
                order_data['payment'] = None
            
            return JsonResponse(order_data)
            
        except Delivery.DoesNotExist:
            return JsonResponse({'error': 'Delivery not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def customer_logout(request):
    """Customer logout"""
    if 'customer_email' in request.session:
        del request.session['customer_email']
    return redirect('customer_login')