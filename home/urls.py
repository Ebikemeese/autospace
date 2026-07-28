from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),
    path('bookings/', views.bookings_page, name='bookings_page'),
    path('bookings/create/', views.create_booking, name='create_booking'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('faqs/', views.faqs, name='faqs'),
    path('contact/', views.contact, name='contact'),
    path('change-password/', views.change_password, name='change_password'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    path('cookie-policy/', views.cookie_policy, name='cookie_policy'),
    path('cookie-settings/', views.cookie_settings, name='cookie_settings'),
    path('terms/', views.terms_and_conditions, name='terms_and_conditions'),
    path('booking-failed/', views.booking_failed, name='booking_failed'),
]
