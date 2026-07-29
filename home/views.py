from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings
from garages.models import Garage
from garages.views import get_slot_counts
from garages.seeder import seed_global_parking_data
from slots.models import Slot, SlotType
from bookings.models import Booking, BookingStatus
from customers.models import Customer
import json
from datetime import datetime, timedelta

def check_auto_seed():
    if not settings.DEBUG and not Garage.objects.exists():
        try:
            seed_global_parking_data()
        except Exception:
            pass

def get_per_page(request, default=6):
    try:
        val = int(request.GET.get('per_page', default))
        return min(50, max(1, val))
    except (ValueError, TypeError):
        return default

def home(request):
    check_auto_seed()
    popular_garages = list(Garage.objects.select_related('address', 'company', 'verification').prefetch_related('slots').order_by('-id')[:6])

    for g in popular_garages:
        g.slot_counts = get_slot_counts(g)

    garages_json = []
    for g in popular_garages:
        if hasattr(g, 'address') and g.address:
            min_price = min([s.price_per_hour for s in g.slots.all()], default=15.0)
            garages_json.append({
                'id': g.id,
                'name': g.display_name or f"Garage #{g.id}",
                'address': g.address.address,
                'lat': g.address.lat,
                'lng': g.address.lng,
                'price': min_price,
            })

    return render(request, 'index.html', {
        'popular_garages': popular_garages,
        'garages_json': json.dumps(garages_json)
    })


@login_required
def about(request):
    return render(request, 'about.html')


@login_required
def search(request):
    check_auto_seed()
    location_query = request.GET.get('location', '').strip()
    slot_type = request.GET.get('type', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    garages_qs = Garage.objects.select_related('address', 'company', 'verification').prefetch_related('slots').order_by('-id')

    if location_query:
        garages_qs = garages_qs.filter(
            Q(display_name__icontains=location_query) |
            Q(description__icontains=location_query) |
            Q(address__address__icontains=location_query)
        )

    if slot_type:
        garages_qs = garages_qs.filter(slots__type=slot_type).distinct()

    if max_price:
        try:
            max_p = float(max_price)
            garages_qs = garages_qs.filter(slots__price_per_hour__lte=max_p).distinct()
        except ValueError:
            pass

    garages_list = list(garages_qs)
    for g in garages_list:
        g.slot_counts = get_slot_counts(g)

    per_page = get_per_page(request, 6)
    paginator = Paginator(garages_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    map_markers = []
    for g in page_obj:
        if hasattr(g, 'address') and g.address:
            min_price = min([s.price_per_hour for s in g.slots.all()], default=15.0)
            first_slot = g.slots.first()
            map_markers.append({
                'id': g.id,
                'name': g.display_name or f"Garage #{g.id}",
                'address': g.address.address,
                'lat': g.address.lat,
                'lng': g.address.lng,
                'price': min_price,
                'slot_id': first_slot.id if first_slot else None
            })

    slot_types = SlotType.choices

    return render(request, 'search.html', {
        'page_obj': page_obj,
        'garages': page_obj.object_list,
        'total_count': len(garages_list),
        'location_query': location_query,
        'slot_type': slot_type,
        'max_price': max_price,
        'slot_types': slot_types,
        'per_page': per_page,
        'map_markers_json': json.dumps(map_markers)
    })


@login_required
def bookings_page(request):
    customer = Customer.objects.filter(uid=request.user.uid).first() if request.user.uid else None
    user_bookings = []
    if customer:
        user_bookings = Booking.objects.filter(customer=customer).select_related('slot', 'slot__garage', 'slot__garage__address').order_by('-start_time')

    per_page = get_per_page(request, 6)
    paginator = Paginator(user_bookings, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'bookings.html', {
        'page_obj': page_obj,
        'bookings': page_obj.object_list,
        'per_page': per_page
    })


@login_required
def create_booking(request):
    if request.method == 'POST':
        slot_id = request.POST.get('slot_id')
        vehicle_number = request.POST.get('vehicle_number', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        start_str = request.POST.get('start_time')
        end_str = request.POST.get('end_time')

        if not slot_id or not vehicle_number:
            return redirect('search')

        slot = get_object_or_404(Slot, id=slot_id)
        customer, _ = Customer.objects.get_or_create(uid=request.user.uid or str(request.user.id), defaults={'display_name': request.user.display_name})

        try:
            start_time = datetime.fromisoformat(start_str) if start_str else datetime.now()
            end_time = datetime.fromisoformat(end_str) if end_str else datetime.now() + timedelta(hours=2)
        except Exception:
            start_time = datetime.now()
            end_time = datetime.now() + timedelta(hours=2)

        hours = max(1, (end_time - start_time).seconds / 3600)
        total_price = hours * slot.price_per_hour

        Booking.objects.create(
            slot=slot,
            customer=customer,
            vehicle_number=vehicle_number,
            phone_number=phone_number,
            price_per_hour=slot.price_per_hour,
            total_price=total_price,
            start_time=start_time,
            end_time=end_time,
            status=BookingStatus.BOOKED
        )
        return redirect('bookings_page')

    return redirect('search')


def how_it_works(request):
    return render(request, 'how_it_works.html')


def faqs(request):
    return render(request, 'faqs.html')


def contact(request):
    return render(request, 'contact.html')


@login_required
def change_password(request):
    error = None
    success = False
    if request.method == 'POST':
        old_password = request.POST.get('oldPassword', '')
        new_password = request.POST.get('newPassword', '')
        confirm_new_password = request.POST.get('confirmNewPassword', '')

        if not old_password or not new_password or not confirm_new_password:
            error = 'Please fill in all fields.'
        elif not request.user.check_password(old_password):
            error = 'Your current password is incorrect.'
        elif new_password != confirm_new_password:
            error = 'New passwords do not match.'
        elif len(new_password) < 6:
            error = 'New password must be at least 6 characters long.'
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            success = True

    return render(request, 'change_password.html', {'error': error, 'success': success})


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def cookie_policy(request):
    return render(request, 'cookie_policy.html')


def cookie_settings(request):
    return render(request, 'cookie_settings.html')


def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')


def booking_failed(request):
    return render(request, 'booking_failed.html')
