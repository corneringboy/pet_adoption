from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views  # Import all views from views.py

urlpatterns = [
    # 🏠 Home Page
    path('', views.home, name='home'),

    # 📄 Static Pages
    path('about/', views.about, name='about'),  # About page
    path('contact/', views.contact, name='contact'),  # Contact page

    # 🔐 Authentication
    path('logout/', views.custom_logout, name='logout'),  # Logout functionality

    # 🆕 Role-Based Signup & Login
    path('signup/<str:role>/', views.signup_view, name='signup'),  # Signup for buyer/seller
    path('login/<str:role>/', views.login_view, name='login'),  # Login for buyer/seller

    # 🚀 Separate Login Routes for Buyers & Sellers
    path('buyer-login/', views.login_view, {'role': 'buyer'}, name='buyer_login'),  # Buyer Login
    path('seller-login/', views.seller_login_view, name='seller_login'),  # Seller Login

    # 📊 User Dashboards
    path('buyer-dashboard/', views.buyer_dashboard, name='buyer_dashboard'),  # Buyer Dashboard
    path('seller-dashboard/', views.seller_dashboard, name='seller_dashboard'),  # Seller Dashboard

    # 🔎 Search & Pets
    path('search-results/', views.search_results, name='search_results'),  # Search results page
    path('pets/', views.pet_list, name='pet_list'),  # Pet listing page
]

# 📂 Serve Media Files in Development Mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




