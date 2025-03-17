from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Pet

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

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'password1', 'password2']

class PetForm(forms.ModelForm):
    animal = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter the type of pet (e.g., Dog, Cat, Bird)"
        })
    )
    breed = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter breed (optional)"
        })
    )
    age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            "placeholder": "Enter age in years"
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "Provide a short description about the pet",
            "rows": 3
        }),
        required=False
    )
    image = forms.ImageField(required=False)

    class Meta:
        model = Pet
        fields = ["animal", "breed", "age", "image", "description", "adoption_status"]
