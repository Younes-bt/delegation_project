from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, City, Association, Training, Center, TrainingGroup, Material

admin.site.register(City)
admin.site.register(Center)
admin.site.register(Training)
admin.site.register(Association)
admin.site.register(UserProfile)
admin.site.register(TrainingGroup)

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'room', 'center', 'situation', 'quantity', 'last_maintenance_date')
    list_filter = ('center', 'room', 'situation')
    search_fields = ('title', 'description', 'room__name', 'center__name')
    ordering = ('room', 'title')
    date_hierarchy = 'last_maintenance_date'

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'role', 'is_staff', 'is_active',)
    list_filter = ('role', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
