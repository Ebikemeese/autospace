from django.urls import path
from . import views

app_name = 'booking_timeslines'

urlpatterns = [
    path("", views.getBookingTimelines, name="booking_timeslines"),
]