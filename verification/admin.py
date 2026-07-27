from django.contrib import admin
from .models import Verification

@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ('garage', 'verified', 'admin', 'updated_at')
    search_fields = ('garage__display_name', 'admin__display_name')
    list_filter = ('verified',)
