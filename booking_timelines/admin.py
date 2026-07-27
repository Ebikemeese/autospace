from django.contrib import admin
from .models import BookingTimeline

@admin.register(BookingTimeline)
class BookingTimelineAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'status', 'manager', 'valet', 'timestamp')
    search_fields = ('booking__id', 'manager__display_name', 'valet__display_name')
    list_filter = ('status', 'timestamp')
