from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from authentication.models import UserRole
from garages.models import Garage
from valets.models import Valet
from bookings.models import Booking

def get_per_page(request, default=6):
    try:
        val = int(request.GET.get('per_page', default))
        return min(50, max(1, val))
    except (ValueError, TypeError):
        return default

@login_required
def manager_dashboard(request):
    if request.user.role != UserRole.MANAGER and not request.user.is_staff:
        return redirect('home')
    
    garages_list = Garage.objects.select_related('company', 'address', 'verification').prefetch_related('slots').order_by('-id')
    valets = Valet.objects.all()
    bookings = Booking.objects.all().select_related('slot', 'customer')

    per_page = get_per_page(request, 6)
    paginator = Paginator(garages_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'manager_dashboard.html', {
        'page_obj': page_obj,
        'garages': page_obj.object_list,
        'total_garages_count': garages_list.count(),
        'valets': valets,
        'bookings': bookings,
        'per_page': per_page
    })

@login_required
def manage_valets(request):
    if request.user.role != UserRole.MANAGER and not request.user.is_staff:
        return redirect('home')

    valets = Valet.objects.all()
    return render(request, 'manage_valets.html', {'valets': valets})
