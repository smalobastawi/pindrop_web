# main/views.py
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    """Home page view"""
    context = {
        'title': 'Home Page',
        'message': 'Welcome to our Django Bootstrap site!'
    }
    return render(request, 'main/home.html', context)

def about(request):
    """About page view"""
    context = {
        'title': 'About Us',
        'content': 'This is a Django project with Bootstrap integration.'
    }
    return render(request, 'main/about.html', context)

def contact(request):
    """Contact page view"""
    context = {
        'title': 'Contact Us',
        'email': 'contact@example.com',
        'phone': '+123 456 7890'
    }
    return render(request, 'main/contact.html', context)

def services(request):
    """Services page view"""
    services_list = [
        {'name': 'Web Development', 'desc': 'Custom web applications'},
        {'name': 'AI Integration', 'desc': 'Machine learning solutions'},
        {'name': 'Database Design', 'desc': 'PostgreSQL optimization'},
    ]
    context = {
        'title': 'Our Services',
        'services': services_list
    }
    return render(request, 'main/services.html', context)

def bootstrap_test(request):
    """Bootstrap testing page"""
    return render(request, 'main/bootstrap_test.html')

# Dynamic page example with URL parameters
def user_profile(request, username):
    """Example of dynamic URL with parameter"""
    context = {
        'title': f'{username}\'s Profile',
        'username': username,
        'joined': '2024-01-01'
    }
    return render(request, 'main/profile.html', context)

# Page with form example
def contact_form(request):
    """Contact form page"""
    if request.method == 'POST':
        # Process form data here
        name = request.POST.get('name', '')
        context = {
            'title': 'Thank You!',
            'message': f'Thank you {name} for contacting us!'
        }
        return render(request, 'main/thank_you.html', context)
    
    # If GET request, show empty form
    context = {'title': 'Contact Form'}
    return render(request, 'main/contact_form.html', context)