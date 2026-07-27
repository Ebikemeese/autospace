from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_name', 'created_at', 'updated_at')
    search_fields = ('display_name', 'description')
    ordering = ('-created_at',)
