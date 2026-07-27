from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Admin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'display_name', 'role', 'uid', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'display_name', 'username', 'uid')
    list_filter = ('role', 'is_staff', 'is_active')
    ordering = ('-date_joined',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Autospace Extra Profile Info', {'fields': ('uid', 'display_name', 'role')}),
    )

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('uid', 'display_name', 'created_at', 'updated_at')
    search_fields = ('uid', 'display_name')
