from django.contrib import admin
from .models import ValetAssignment

@admin.register(ValetAssignment)
class ValetAssignmentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'pickup_valet', 'return_valet', 'created_at')
    search_fields = ('booking__id', 'pickup_valet__display_name', 'return_valet__display_name')
    list_filter = ('pickup_valet', 'return_valet')
