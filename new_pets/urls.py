from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views  # Import all views from views.py

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Static pages
    path('about/', views.about, name='about'),  # About page
    path('contact/', views.contact, name='contact'),  # Contact page

    # Authentication
    path('logout/', views.custom_logout, name='logout'),  # Logout functionality

    # Role-based signup and login
    path('signup/<str:role>/', views.signup_view, name='signup'),  # Signup for buyer/seller
    path('login/<str:role>/', views.login_view, name='login'),  # Login for buyer/seller

    # Separate login routes for buyers and sellers
    path('buyer-login/', views.login_view, {'role': 'buyer'}, name='buyer_login'),  # Buyer Login
    path('seller-login/', views.seller_login_view, name='seller_login'),  # Seller Login

    # Dashboards
    path('buyer-dashboard/', views.buyer_dashboard, name='buyer_dashboard'),  # Buyer Dashboard
    path('seller-dashboard/', views.seller_dashboard, name='seller_dashboard'),  # Seller Dashboard

    # Search results (keep this if the function exists in views.py)
    path('search-results/', views.search_results, name='search_results'),

    # Pets listing page
    path('pets/', views.pet_list, name='pet_list'),  # Ensure pet_list view is correctly referenced
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



