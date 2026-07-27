from django.contrib import admin
from .models import Valet

@admin.register(Valet)
class ValetAdmin(admin.ModelAdmin):
    list_display = ('uid', 'display_name', 'company', 'licence_id', 'created_at')
    search_fields = ('uid', 'display_name', 'licence_id', 'company__display_name')
    list_filter = ('company',)
