"""
URL configuration for autospace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('authentication.urls')),
    path('address/', include("addresses.urls")),
    path('booking/timelines/', include("booking_timelines.urls")),
    path('bookings', include("bookings.urls")),
    path('companies/', include("companies.urls")),
    path('customers/', include("customers.urls")),
    path('garages/', include("garages.urls")),
    path('managers/', include("managers.urls")),
    path('reviews/', include("reviews.urls")),
    path('services/', include("services.urls")),
    path('slots/', include("slots.urls")),
    path('valet/assignments/', include("valet_assignments.urls")),
    path('valets/', include("valets.urls")),
    path('verification/', include("verification.urls")),
]
