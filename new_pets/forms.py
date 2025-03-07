from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Pet  # ✅ Added Pet model

class CustomUserCreationForm(UserCreationForm):
    business_name = forms.CharField(required=False)
    business_type = forms.CharField(required=False)
    is_company = forms.BooleanField(required=False)
    business_registration_number = forms.CharField(required=False)
    vat_tax_id = forms.CharField(required=False)
    business_address = forms.CharField(widget=forms.Textarea, required=False)
    business_description = forms.CharField(widget=forms.Textarea, required=False)
    government_id = forms.FileField(required=False)
    business_license = forms.FileField(required=False)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'phone_number', 'password1', 'password2', 'role',  
                  'business_name', 'business_type', 'is_company', 'business_registration_number', 
                  'vat_tax_id', 'business_address', 'business_description', 
                  'government_id', 'business_license']

# ✅ Added CustomUserForm without removing any existing code
class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'password1', 'password2']  # No 'username'

# ✅ New Pet Form for Adding Pets
class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ["name", "breed", "age", "image", "description", "adoption_status"]
