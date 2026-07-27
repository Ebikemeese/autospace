from django.contrib import admin
from .models import Garage

@admin.register(Garage)
class GarageAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_name', 'company', 'created_at', 'updated_at')
    search_fields = ('display_name', 'description', 'company__display_name')
    list_filter = ('company',)
