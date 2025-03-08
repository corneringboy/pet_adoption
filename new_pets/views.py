from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_protect  # ✅ Added CSRF protection
from .models import CustomUser, BuyerProfile, SellerProfile, Pet
from .forms import CustomUserCreationForm, CustomUserForm, PetForm  # ✅ Added PetForm

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
        country_code = request.POST.get("country_code")
        phone = request.POST.get("phone")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        role = request.POST.get("role") or role  # ✅ Ensure role is set correctly
        
        # Seller fields
        business_name = request.POST.get("business_name")
        business_type = request.POST.get("business_type")
        registration_number = request.POST.get("registration_number")
        tax_id = request.POST.get("tax_id")
        business_address = request.POST.get("business_address")
        business_description = request.POST.get("business_description")
        gov_id = request.FILES.get("gov_id")
        license = request.FILES.get("license")
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup", role=role)

        # ✅ Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect("signup", role=role)

        # ✅ Check if phone number already exists
        if CustomUser.objects.filter(phone_number=phone).exists():
            messages.error(request, "Phone number is already in use.")
            return redirect("signup", role=role)

        # ✅ Ensure role is properly assigned
        user = CustomUser.objects.create(
            email=email,
            full_name=full_name,  # ✅ Fix field name
            phone_number=phone,
            password=make_password(password1),
            role=role  # ✅ Ensure role is saved correctly
        )
        
        if role == "buyer":
            BuyerProfile.objects.create(user=user, phone=phone, address=business_address)
        elif role == "seller":
            SellerProfile.objects.create(
                user=user,
                gov_id=gov_id,
                business_license=license,
                store_location=business_address
            )

        messages.success(request, "Account created successfully! Please log in.")
        return redirect("login")  # ✅ Ensure redirection works

    return render(request, "new_pets/signup.html", {"role": role})

# ✅ Alternative signup method using CustomUserForm
def simple_signup_view(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # ✅ Redirect after signup
    else:
        form = CustomUserForm()
    return render(request, 'signup.html', {'form': form})

# ✅ Fixed login view (Buyers go to pet_list.html, Sellers go to add_pet.html)
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
            login(request, auth_user)  # ✅ Log the user in immediately
            messages.success(request, "Login successful!")

            # ✅ Redirect buyers to pet_list.html, sellers to add_pet.html
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
    return redirect("pet_list")  # ✅ Redirect buyer dashboard to pet_list.html

@login_required
def seller_dashboard(request):
    return render(request, "new_pets/seller_dashboard.html")

# ✅ Ensured pet_list passes pet data correctly
def pet_list(request):
    pets = Pet.objects.all().select_related("seller")  # ✅ Ensure related seller info is loaded
    return render(request, "new_pets/pet_list.html", {"pets": pets})

def search_results(request):
    query = request.GET.get("q")
    pets = Pet.objects.filter(name__icontains=query) if query else []
    return render(request, "new_pets/search_results.html", {"pets": pets, "query": query})

# ✅ New Add Pet Function (Sellers Add Pets Automatically with CSRF Protection)
@csrf_protect  # ✅ Added CSRF protection to prevent CSRF errors
@login_required
def add_pet(request):
    if request.user.role != "seller":
        messages.error(request, "Only sellers can add pets.")
        return redirect("home")  # ✅ Redirect buyers away

    seller_profile = SellerProfile.objects.get(user=request.user)  # ✅ Get seller details

    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.seller = seller_profile  # ✅ Automatically set the seller
            pet.save()
            messages.success(request, "Pet added successfully!")
            return redirect("add_pet")  # ✅ Reload page to show the new pet
    else:
        form = PetForm()

    # ✅ Fetch only pets added by this seller
    pets = Pet.objects.filter(seller=seller_profile)

    return render(request, "new_pets/add_pet.html", {"form": form, "pets": pets})

# ✅ New Edit Pet Function (Sellers Can Edit Pets)
@login_required
def edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, seller=request.user.sellerprofile)

    if request.method == "POST":
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, "Pet details updated successfully!")
            return redirect("add_pet")  # ✅ Redirect back to seller dashboard
    else:
        form = PetForm(instance=pet)

    return render(request, "new_pets/edit_pet.html", {"form": form, "pet": pet})

# ✅ New Delete Pet Function (Sellers Can Remove Their Pets)
@login_required
def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, seller=request.user.sellerprofile)
    pet.delete()
    messages.success(request, "Pet deleted successfully!")
    return redirect("add_pet")  # ✅ Redirect back to the seller dashboard
