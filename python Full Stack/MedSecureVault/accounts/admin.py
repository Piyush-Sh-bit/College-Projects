from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_approved_doctor', 'is_staff', 'is_active')
    list_filter = ('role', 'is_approved_doctor', 'is_staff', 'is_active', 'date_joined')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_approved_doctor', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'is_approved_doctor', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    actions = ['approve_doctors', 'disapprove_doctors']
    
    def approve_doctors(self, request, queryset):
        updated = queryset.filter(role='doctor').update(is_approved_doctor=True)
        self.message_user(request, f'{updated} doctor accounts approved.')
    approve_doctors.short_description = "Approve selected doctor accounts"
    
    def disapprove_doctors(self, request, queryset):
        updated = queryset.filter(role='doctor').update(is_approved_doctor=False)
        self.message_user(request, f'{updated} doctor accounts disapproved.')
    disapprove_doctors.short_description = "Disapprove selected doctor accounts"

admin.site.register(CustomUser, CustomUserAdmin)