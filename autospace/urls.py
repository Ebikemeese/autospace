from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('authentication.urls')),
    path('', include('managers.urls')),
    path('', include('valets.urls')),
    path('', include('garages.urls')),
    path('', include('verification.urls')),
    path('address/', include("addresses.urls")),
    path('booking/timelines/', include("booking_timelines.urls")),
    path('bookings/', include("bookings.urls")),
    path('companies/', include("companies.urls")),
    path('customers/', include("customers.urls")),
    path('reviews/', include("reviews.urls")),
    path('services/', include("services.urls")),
    path('slots/', include("slots.urls")),
    path('valet/assignments/', include("valet_assignments.urls")),
]
