from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Company

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'role', 'company', 'is_staff')
    list_filter = ('company', 'role', 'is_staff', 'is_superuser')
    search_fields = ('email', 'name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'phone')}),
        ('Company & Role', {'fields': ('company', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email')
