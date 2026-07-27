from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'duration', 'garage', 'booking', 'created_at')
    search_fields = ('name', 'description', 'garage__display_name')
    list_filter = ('garage',)
