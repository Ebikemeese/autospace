from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle_number', 'customer', 'slot', 'status', 'start_time', 'end_time', 'total_price')
    search_fields = ('vehicle_number', 'customer__display_name', 'phone_number', 'passcode')
    list_filter = ('status', 'start_time', 'end_time')
