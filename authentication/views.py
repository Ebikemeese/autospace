import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, UserRole
from customers.models import Customer

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    error = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            error = 'Please fill in all fields.'
        else:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    next_url = request.GET.get('next', 'home')
                    return redirect(next_url)
                else:
                    error = 'This account has been disabled.'
            else:
                error = 'Invalid email or password.'

    return render(request, 'login.html', {'error': error})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    error = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirmPassword', '')
        display_name = request.POST.get('displayName', '').strip()

        if not email or not password or not confirm_password or not display_name:
            error = 'Please fill in all required fields.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters long.'
        elif User.objects.filter(email=email).exists():
            error = 'An account with this email already exists.'
        else:
            user_uid = str(uuid.uuid4())
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                display_name=display_name,
                role=UserRole.CUSTOMER,
                uid=user_uid
            )

            # Automatically create associated Customer profile
            Customer.objects.get_or_create(
                uid=user_uid,
                defaults={'display_name': display_name}
            )

            # Log in the user immediately after successful registration
            login(request, user)
            return redirect('home')

    return render(request, 'register.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('home')
