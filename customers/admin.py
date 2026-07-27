from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('uid', 'display_name', 'created_at', 'updated_at')
    search_fields = ('uid', 'display_name')
    ordering = ('-created_at',)
