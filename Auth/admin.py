from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    def profile_pic_preview(self, obj):
        if obj.profile_pic:
            return format_html('<img src="{}" width="150" height="150" />'.format(obj.profile_pic.url))
        return ""
    profile_pic_preview.short_description = 'Profile Picture Preview'

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'birth_date', 'country', 'phone_no', 'profile_pic', 'profile_pic_preview')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'birth_date', 'country', 'phone_no', 'profile_pic')}
        ),
    )

    readonly_fields = ('profile_pic_preview',)

admin.site.register(CustomUser, CustomUserAdmin)