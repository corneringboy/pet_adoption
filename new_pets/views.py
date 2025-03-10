from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse
from django.middleware.csrf import get_token
from .models import CustomUser, BuyerProfile, SellerProfile, Pet
from .forms import CustomUserCreationForm, CustomUserForm, PetForm
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    return render(request, "new_pets/home.html")

def about(request):
    return render(request, "new_pets/about.html")

def contact(request):
    return render(request, "new_pets/contact.html")

def signup_view(request, role=None):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        address = request.POST.get("address", "").strip()  # Ensure address is collected
        store_location = request.POST.get("store_location", "").strip()
        role = request.POST.get("role") or role

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup", role=role)

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect("signup", role=role)

        if CustomUser.objects.filter(phone_number=phone).exists():
            messages.error(request, "Phone number is already in use.")
            return redirect("signup", role=role)

        user = CustomUser.objects.create(
            email=email,
            full_name=full_name,
            phone_number=phone,
            password=make_password(password1),
            role=role
        )

        if role == "buyer":
            BuyerProfile.objects.get_or_create(user=user, phone=phone, address=address)  # Address added
        elif role == "seller":
            SellerProfile.objects.get_or_create(user=user, store_location=store_location)  # Ensure store location is saved

        messages.success(request, "Account created successfully! Please log in.")
        return redirect("login")

    return render(request, "new_pets/signup.html", {"role": role})

def login_view(request, role=None):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found!")
            return render(request, "new_pets/login.html", {"role": role})

        auth_user = authenticate(request, email=email, password=password)

        if auth_user is not None:
            login(request, auth_user)
            messages.success(request, "Login successful!")

            if auth_user.role == "buyer":
                return redirect("pet_list")
            elif auth_user.role == "seller":
                return redirect("add_pet")
            else:
                return redirect("home")
        else:
            messages.error(request, "Invalid email or password!")

    return render(request, "new_pets/login.html", {"role": role})

def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")

@login_required
def buyer_dashboard(request):
    return redirect("pet_list")

@login_required
def seller_dashboard(request):
    return render(request, "new_pets/seller_dashboard.html")

def pet_list(request):
    pets = Pet.objects.select_related("seller", "seller__user")
    
    buyer_profile = None
    if request.user.is_authenticated and request.user.role == "buyer":
        try:
            buyer_profile = BuyerProfile.objects.get(user=request.user)
        except BuyerProfile.DoesNotExist:
            buyer_profile = None

    for pet in pets:
        pet.seller_address = pet.seller.store_location if pet.seller and pet.seller.store_location else "Address not provided"

    return render(request, "new_pets/pet_list.html", {"pets": pets, "buyer_profile": buyer_profile})

def search_results(request):
    query = request.GET.get("q")
    pets = Pet.objects.filter(name__icontains=query) if query else []
    return render(request, "new_pets/search_results.html", {"pets": pets, "query": query})

@csrf_protect  
@login_required
def add_pet(request):
    if request.user.role != "seller":
        messages.error(request, "Only sellers can add pets.")
        return redirect("home")

    seller_profile = get_object_or_404(SellerProfile, user=request.user)

    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.seller = seller_profile
            pet.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "Invalid form data"}, status=400)

    form = PetForm()
    pets = Pet.objects.filter(seller=seller_profile)
    return render(request, "new_pets/add_pet.html", {"form": form, "pets": pets})

@login_required
def edit_pet(request, pet_id):
    seller_profile = get_object_or_404(SellerProfile, user=request.user)
    pet = get_object_or_404(Pet, id=pet_id, seller=seller_profile)

    if request.method == "POST":
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, "Pet details updated successfully!")
            return redirect("add_pet")
    else:
        form = PetForm(instance=pet)
    return render(request, "new_pets/edit_pet.html", {"form": form, "pet": pet})

@login_required
def delete_pet(request, pet_id):
    seller_profile = get_object_or_404(SellerProfile, user=request.user)
    pet = get_object_or_404(Pet, id=pet_id, seller=seller_profile)
    pet.delete()
    messages.success(request, "Pet deleted successfully!")
    return redirect("add_pet")

def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

@csrf_exempt
@login_required
def express_interest(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.user.role != "buyer":
        return JsonResponse({"error": "Only buyers can express interest."}, status=403)
    if request.method == "POST":
        pet.interested_buyers.add(request.user)
        return JsonResponse({"message": "Interest recorded!"})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def edit_seller_profile(request):
    seller_profile, created = SellerProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        seller_profile.store_location = request.POST.get("store_location", seller_profile.store_location)
        seller_profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("seller_dashboard")
    return render(request, "new_pets/edit_seller_profile.html", {"seller_profile": seller_profile})
