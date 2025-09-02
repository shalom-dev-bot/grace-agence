from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_admin', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_admin', 'theme_preference', 'language_preference')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('profile_picture', 'theme_preference', 'language_preference', 'is_admin')
        }),
    )