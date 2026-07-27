import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import User, UserRole, Admin
from customers.models import Customer
from managers.models import Manager
from valets.models import Valet
from garages.views import get_slot_counts

def get_per_page(request, default=6):
    try:
        val = int(request.GET.get('per_page', default))
        return min(50, max(1, val))
    except (ValueError, TypeError):
        return default

def get_redirect_url_for_user(user, next_url=None):
    if next_url and next_url != '/' and next_url != '/login/' and next_url != '/register/':
        return next_url
    if user.role == UserRole.MANAGER:
        return '/managers/dashboard/'
    elif user.role == UserRole.VALET:
        return '/valets/dashboard/'
    elif user.role == UserRole.ADMIN:
        return '/admins/dashboard/'
    return '/'

def login_view(request):
    if request.user.is_authenticated:
        return redirect(get_redirect_url_for_user(request.user))

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
                    next_url = request.GET.get('next')
                    return redirect(get_redirect_url_for_user(user, next_url))
                else:
                    error = 'This account has been disabled.'
            else:
                error = 'Invalid email or password.'

    return render(request, 'login.html', {'error': error})


def register_view(request):
    if request.user.is_authenticated:
        return redirect(get_redirect_url_for_user(request.user))

    error = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirmPassword', '')
        display_name = request.POST.get('displayName', '').strip()
        role = request.POST.get('role', UserRole.CUSTOMER)

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
                role=role,
                uid=user_uid
            )

            if role == UserRole.CUSTOMER:
                Customer.objects.get_or_create(uid=user_uid, defaults={'display_name': display_name})
            elif role == UserRole.MANAGER:
                Manager.objects.get_or_create(uid=user_uid, defaults={'display_name': display_name})
            elif role == UserRole.VALET:
                Valet.objects.get_or_create(uid=user_uid, defaults={'display_name': display_name})
            elif role == UserRole.ADMIN:
                Admin.objects.get_or_create(uid=user_uid, defaults={'display_name': display_name})

            login(request, user)
            return redirect(get_redirect_url_for_user(user))

    return render(request, 'register.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def admin_dashboard(request):
    if request.user.role != UserRole.ADMIN and not request.user.is_staff:
        return redirect('home')
    
    from garages.models import Garage
    garages_list = list(Garage.objects.select_related('company', 'address', 'verification').prefetch_related('slots').order_by('-id'))
    for g in garages_list:
        g.slot_counts = get_slot_counts(g)

    per_page = get_per_page(request, 6)
    paginator = Paginator(garages_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard.html', {
        'page_obj': page_obj,
        'garages': page_obj.object_list,
        'per_page': per_page
    })
