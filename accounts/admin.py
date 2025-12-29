# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'full_name', 'phone_number', 'email', 'date_joined', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'phone_number', 'email', 'full_name')
    ordering = ('-date_joined',)

    # Muhim: readonly field’larni aniq belgilab beramiz
    readonly_fields = ('date_joined', 'last_login')

    # Standart fieldsets ni to‘g‘ri o‘zgartiramiz
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Shaxsiy ma\'lumotlar', {
            'fields': ('full_name', 'email', 'phone_number', 'avatar')
        }),
        ('Ruxsatlar', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Muhim sanalar', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)  # yopiq bo‘lib ochiladi
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'full_name', 'password1', 'password2'),
        }),
    )

    def has_delete_permission(self, request, obj=None):
        return False  # Hech kim o‘chira olmaydi

    # Yangi user yaratganda majburiy field’lar
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['email'].required = True
        form.base_fields['phone_number'].required = True
        return form
