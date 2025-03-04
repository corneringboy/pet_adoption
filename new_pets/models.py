from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# ✅ Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, full_name, phone_number, password, **extra_fields)

# ✅ Custom User Model
class CustomUser(AbstractUser):
    username = None  # ❌ Remove default username
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)  
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)

    ROLE_CHOICES = [
        ("buyer", "Buyer"),
        ("seller", "Seller"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="buyer")

    # ✅ Business details (only for sellers)
    business_name = models.CharField(max_length=255, blank=True, null=True)
    business_type = models.CharField(max_length=255, blank=True, null=True)
    is_company = models.BooleanField(default=False)
    business_registration_number = models.CharField(max_length=100, blank=True, null=True)
    vat_tax_id = models.CharField(max_length=100, blank=True, null=True)
    business_address = models.TextField(blank=True, null=True)
    business_description = models.TextField(blank=True, null=True)

    # ✅ File uploads (KYC & Business License)
    government_id = models.FileField(upload_to="kyc_documents/", blank=True, null=True)
    business_license = models.FileField(upload_to="business_licenses/", blank=True, null=True)

    USERNAME_FIELD = "email"  # ✅ Use email as the unique identifier
    REQUIRED_FIELDS = ["full_name", "phone_number"]  # ✅ Required fields for superuser creation

    objects = CustomUserManager()  # ✅ Use custom manager

    def __str__(self):
        return self.email

# ✅ Buyer Profile
class BuyerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.email

# ✅ Seller Profile
class SellerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gov_id = models.FileField(upload_to="kyc_documents/", blank=True, null=True)
    business_license = models.FileField(upload_to="business_licenses/", blank=True, null=True)
    store_location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.email

# ✅ Pet Model
class Pet(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"








