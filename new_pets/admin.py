from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, BuyerProfile, SellerProfile, Pet

# ✅ Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["email", "full_name", "phone_number", "role", "is_staff", "is_active"]  # ✅ Updated to avoid username error
    list_filter = ["role", "is_staff", "is_active"]
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("full_name", "phone_number")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Business Info", {"fields": ("business_name", "business_type", "business_address")}),
    )  

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "phone_number", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ["email", "full_name"]
    ordering = ["email"]

# ✅ Register CustomUser only if not already registered
if not admin.site.is_registered(CustomUser):
    admin.site.register(CustomUser, CustomUserAdmin)

# ✅ Register other models
admin.site.register(BuyerProfile)
admin.site.register(SellerProfile)

# ✅ Enhanced Custom User Admin
class EnhancedCustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'phone_number', 'is_staff', 'is_active']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('phone_number',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2')},
        ),
    )
    
    search_fields = ('email',)
    ordering = ('email',)

# ✅ Ensure CustomUserAdmin is properly registered
admin.site.unregister(CustomUser)
admin.site.register(CustomUser, EnhancedCustomUserAdmin)

# ✅ Pet Admin - Allows searching by animal name
class PetAdmin(admin.ModelAdmin):
    list_display = ('animal', 'breed', 'age', 'adoption_status', 'seller')
    search_fields = ('animal', 'breed', 'seller__user__email')  # ✅ Now you can search by animal name

admin.site.register(Pet, PetAdmin)
