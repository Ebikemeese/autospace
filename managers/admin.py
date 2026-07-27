from django.contrib import admin
from .models import Manager

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('uid', 'display_name', 'company', 'created_at', 'updated_at')
    search_fields = ('uid', 'display_name', 'company__display_name')
    list_filter = ('company',)
