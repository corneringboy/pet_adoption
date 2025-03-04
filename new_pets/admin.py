from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, BuyerProfile, SellerProfile, Pet

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["email", "username", "role", "is_staff", "is_active"]  # Show email, username, and role
    search_fields = ["email", "username"]
    ordering = ["email"]

# ✅ Register only once
if not admin.site.is_registered(CustomUser):
    admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(BuyerProfile)
admin.site.register(SellerProfile)
admin.site.register(Pet)
