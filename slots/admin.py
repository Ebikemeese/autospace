from django.contrib import admin
from .models import Slot

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_name', 'garage', 'price_per_hour', 'type', 'created_at')
    search_fields = ('display_name', 'garage__display_name')
    list_filter = ('type', 'garage')
