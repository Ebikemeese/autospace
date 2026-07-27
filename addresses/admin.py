from django.contrib import admin
from .models import Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'garage', 'address', 'lat', 'lng', 'created_at')
    search_fields = ('address', 'garage__display_name')
