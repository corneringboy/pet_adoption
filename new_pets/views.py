from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from .models import CustomUser, BuyerProfile, SellerProfile, Pet

# Home Page
def home(request):
    return render(request, "new_pets/home.html")

# About Page
def about(request):
    return render(request, "new_pets/about.html")

# Contact Page
def contact(request):
    return render(request, "new_pets/contact.html")

# Signup View for Buyer and Seller
def signup_view(request, role):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect(reverse("signup", args=[role]))

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect(reverse("signup", args=[role]))

        user = CustomUser.objects.create(
            username=email,
            email=email,
            password=make_password(password1),
            role=role
        )

        if role == "buyer":
            phone = request.POST.get("phone")
            address = request.POST.get("address")
            BuyerProfile.objects.create(user=user, phone=phone, address=address)
        elif role == "seller":
            gov_id = request.FILES.get("gov_id")
            license = request.FILES.get("license")
            store_location = request.POST.get("store_location")
            SellerProfile.objects.create(user=user, gov_id=gov_id, business_license=license, store_location=store_location)

        login(request, user)
        return redirect("buyer_dashboard" if role == "buyer" else "seller_dashboard")

    return render(request, "new_pets/signup.html", {"role": role})

# Login View (Handles both Buyer & Seller)
def login_view(request, role):  # Accepts 'role' parameter
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(email=email)
            auth_user = authenticate(request, username=user.username, password=password)

            if auth_user is not None:
                if auth_user.role == role:  # Ensure role matches
                    login(request, auth_user)
                    messages.success(request, "Login successful!")

                    # Redirect user based on role
                    return redirect("buyer_dashboard" if role == "buyer" else "seller_dashboard")
                else:
                    messages.error(request, "Invalid role for this login page!")
            else:
                messages.error(request, "Invalid credentials!")
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found!")

    return render(request, "new_pets/login.html", {"role": role})

# Logout View
def custom_logout(request):
    logout(request)
    return redirect("home")

# Buyer Dashboard
@login_required
def buyer_dashboard(request):
    return render(request, "new_pets/buyer_dashboard.html")

# Seller Dashboard
@login_required
def seller_dashboard(request):
    return render(request, "new_pets/seller_dashboard.html")

# Pet Listings Page
def pet_list(request):
    pets = Pet.objects.all()
    return render(request, "new_pets/pet_list.html", {"pets": pets})

# Search Results Page
def search_results(request):
    query = request.GET.get("q")
    pets = Pet.objects.filter(name__icontains=query) if query else []
    return render(request, "new_pets/search_results.html", {"pets": pets, "query": query})






