from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from .models import CustomUser, BuyerProfile, SellerProfile, Pet
from .forms import CustomUserCreationForm

# 🏠 Home Page
def home(request):
    return render(request, "new_pets/home.html")

# 📄 About Page
def about(request):
    return render(request, "new_pets/about.html")

# 📞 Contact Page
def contact(request):
    return render(request, "new_pets/contact.html")

# 🔐 Signup View for Buyer and Seller
def signup_view(request, role=None):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to DB yet
            user.set_password(form.cleaned_data.get("password"))  # ✅ Hash password before saving

            # Assign role if passed in URL
            if role:
                user.role = role

            # Save business-related fields
            user.business_name = form.cleaned_data.get("business_name", "")
            user.business_type = form.cleaned_data.get("business_type", "")
            user.is_company = form.cleaned_data.get("is_company", False)
            user.business_registration_number = form.cleaned_data.get("business_registration_number", "")
            user.vat_tax_id = form.cleaned_data.get("vat_tax_id", "")
            user.business_address = form.cleaned_data.get("business_address", "")
            user.business_description = form.cleaned_data.get("business_description", "")

            # Handle file uploads
            user.government_id = request.FILES.get("government_id", None)
            user.business_license = request.FILES.get("business_license", None)

            user.save()  # ✅ Save user to database

            # Create profile based on role
            if user.role == "buyer":
                BuyerProfile.objects.create(user=user, phone=user.phone_number, address=user.business_address)
            elif user.role == "seller":
                SellerProfile.objects.create(
                    user=user, gov_id=user.government_id, business_license=user.business_license, store_location=user.business_address
                )

            messages.success(request, "Signup successful! Please log in.")
            return redirect("login", role=user.role)

        else:
            print(form.errors)  # Debugging: Print form errors to terminal

    else:
        form = CustomUserCreationForm()

    return render(request, "new_pets/signup.html", {"form": form, "role": role})

# 🔑 Login View (Handles both Buyer & Seller)
def login_view(request, role=None):  
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(email=email)  # ✅ Find user by email
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found!")
            return render(request, "new_pets/login.html", {"role": role})

        # ✅ Authenticate using email instead of username
        auth_user = authenticate(request, username=email, password=password)

        if auth_user is not None:
            if role and auth_user.role != role:  
                messages.error(request, "Invalid role for this login page!")
                return redirect("login", role=role)

            login(request, auth_user)
            messages.success(request, "Login successful!")

            # ✅ Redirect based on user role
            if auth_user.role == "buyer":
                return redirect("buyer_dashboard")
            elif auth_user.role == "seller":
                return redirect("seller_dashboard")
            else:
                return redirect("home")  # ✅ Default fallback

        else:
            messages.error(request, "Invalid email or password!")

    return render(request, "new_pets/login.html", {"role": role})

# 🚪 Logout View
def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")

# 📊 Buyer Dashboard
@login_required
def buyer_dashboard(request):
    return render(request, "new_pets/buyer_dashboard.html")

# 🏪 Seller Dashboard
@login_required
def seller_dashboard(request):
    return render(request, "new_pets/seller_dashboard.html")

# 🐶 Pet Listings Page
def pet_list(request):
    pets = Pet.objects.all()
    return render(request, "new_pets/pet_list.html", {"pets": pets})

# 🔎 Search Results Page
def search_results(request):
    query = request.GET.get("q")
    pets = Pet.objects.filter(name__icontains=query) if query else []
    return render(request, "new_pets/search_results.html", {"pets": pets, "query": query})












