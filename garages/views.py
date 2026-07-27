from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from authentication.models import UserRole
from .models import Garage
from companies.models import Company
from addresses.models import Address

def get_slot_counts(garage):
    counts = {}
    type_icons = {
        'CAR': {'icon': '🚗', 'label': 'Car'},
        'BIKE': {'icon': '🏍️', 'label': 'Bike'},
        'HEAVY': {'icon': '🚚', 'label': 'Heavy Vehicle'},
        'BICYCLE': {'icon': '🚲', 'label': 'Bicycle'},
    }
    for s in garage.slots.all():
        stype = s.type
        info = type_icons.get(stype, {'icon': '🅿️', 'label': stype})
        if stype not in counts:
            counts[stype] = {
                'type': stype,
                'label': info['label'],
                'icon': info['icon'],
                'count': 0,
                'min_price': s.price_per_hour,
            }
        counts[stype]['count'] += 1
        if s.price_per_hour < counts[stype]['min_price']:
            counts[stype]['min_price'] = s.price_per_hour
    return list(counts.values())


def get_location_images(garage):
    imgs = []
    
    if hasattr(garage, 'address') and garage.address and garage.address.lat and garage.address.lng:
        lat = garage.address.lat
        lng = garage.address.lng
        
        sat_view = f"https://static-maps.yandex.ru/1.x/?ll={lng},{lat}&z=16&l=sat,skl&size=650,450&pt={lng},{lat},pm2rdm"
        road_view = f"https://static-maps.yandex.ru/1.x/?ll={lng},{lat}&z=16&l=map&size=650,450&pt={lng},{lat},pm2rdm"
        street_view = f"https://maps.googleapis.com/maps/api/streetview?size=1000x600&location={lat},{lng}&fov=90&heading=90&pitch=0"
        
        imgs.extend([sat_view, road_view, street_view])

    if hasattr(garage, 'images') and garage.images and isinstance(garage.images, list):
        for img in garage.images:
            if img and isinstance(img, str) and img not in imgs and 'unsplash.com' not in img:
                imgs.append(img)

    if not imgs:
        imgs = ['https://images.unsplash.com/photo-1506521781263-d8422e82f27a?auto=format&fit=crop&w=1000&q=80']

    seen = set()
    deduped = []
    for item in imgs:
        if item not in seen:
            seen.add(item)
            deduped.append(item)

    return deduped


def garage_detail(request, garage_id):
    garage = get_object_or_404(
        Garage.objects.select_related('address', 'company', 'verification')
        .prefetch_related('slots', 'reviews', 'reviews__customer'),
        id=garage_id
    )
    
    reviews = garage.reviews.all()
    avg_rating = sum([r.rating for r in reviews]) / len(reviews) if reviews else 5.0
    location_images = get_location_images(garage)
    slot_counts = get_slot_counts(garage)

    return render(request, 'garage_detail.html', {
        'garage': garage,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'location_images': location_images,
        'slot_counts': slot_counts
    })


@login_required
def create_garage(request):
    if request.user.role != UserRole.MANAGER and not request.user.is_staff:
        return redirect('home')

    error = None
    if request.method == 'POST':
        display_name = request.POST.get('displayName', '').strip()
        description = request.POST.get('description', '').strip()
        address_str = request.POST.get('address', '').strip()
        lat = request.POST.get('lat', 0.0)
        lng = request.POST.get('lng', 0.0)

        if not display_name or not address_str:
            error = 'Garage name and address are required.'
        else:
            company, _ = Company.objects.get_or_create(display_name=f"{request.user.display_name or 'Manager'}'s Company")
            garage = Garage.objects.create(
                display_name=display_name,
                description=description,
                company=company
            )
            Address.objects.create(
                garage=garage,
                address=address_str,
                lat=float(lat) if lat else 0.0,
                lng=float(lng) if lng else 0.0
            )
            return redirect('garage_detail', garage_id=garage.id)

    return render(request, 'create_garage.html', {'error': error})
