from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views  # Added for password reset functionality
from .views import (
    home, about, contact, login_view, signup_view, 
    buyer_dashboard, seller_dashboard, custom_logout, 
    search_results, pet_list
)

urlpatterns = [
    # 🏠 Home Page
    path('', home, name='home'),

    # 📄 Static Pages
    path('about/', about, name='about'),  # About page
    path('contact/', contact, name='contact'),  # Contact page

    # 🔐 Authentication
    path('logout/', custom_logout, name='logout'),  # Logout functionality

    # 🆕 Role-Based Signup & Login
    path('signup/<str:role>/', signup_view, name='signup'),  # Role-based signup: /signup/buyer/ & /signup/seller/
    path('login/<str:role>/', login_view, name='login'),  # Role-based login: /login/buyer/ & /login/seller/

    # ➕ General Signup & Login (if role not specified)
    path('signup/', signup_view, name='signup'),
    path('login/', LoginView.as_view(template_name='new_pets/login.html'), name='login'),

    # 📊 User Dashboards
    path('buyer-dashboard/', buyer_dashboard, name='buyer_dashboard'),  # Buyer Dashboard
    path('seller-dashboard/', seller_dashboard, name='seller_dashboard'),  # Seller Dashboard

    # 🔎 Search & Pets
    path('search-results/', search_results, name='search_results'),  # Search results page
    path('pets/', pet_list, name='pet_list'),  # Pet listing page

    # 🔑 Password Reset (Newly Added)
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

# 📂 Serve Media Files in Development Mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






