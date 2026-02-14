from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Custom admin panel for the CustomUser model with role displayed."""
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'reader_subscriptions')}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')


