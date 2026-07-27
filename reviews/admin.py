from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'garage', 'customer', 'rating', 'created_at')
    search_fields = ('comment', 'garage__display_name', 'customer__display_name')
    list_filter = ('rating', 'garage')
