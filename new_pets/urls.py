from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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
    path('signup/<str:role>/', signup_view, name='signup'),  # Signup for buyer/seller
    path('login/<str:role>/', login_view, name='login'),  # Role-based login: /login/buyer/ & /login/seller/

    # 📊 User Dashboards
    path('buyer-dashboard/', buyer_dashboard, name='buyer_dashboard'),  # Buyer Dashboard
    path('seller-dashboard/', seller_dashboard, name='seller_dashboard'),  # Seller Dashboard

    # 🔎 Search & Pets
    path('search-results/', search_results, name='search_results'),  # Search results page
    path('pets/', pet_list, name='pet_list'),  # Pet listing page
]

# 📂 Serve Media Files in Development Mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






