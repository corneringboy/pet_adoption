from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, BuyerProfile, SellerProfile, Pet

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
admin.site.register(Pet)

