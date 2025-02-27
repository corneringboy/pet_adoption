from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import get_pet_suggestions, signup_view, login_view, seller_login_view

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Static pages
    path('about/', views.about, name='about'),  # About page
    path('contact/', views.contact, name='contact'),  # Contact page

    # Authentication
    path('logout/', views.custom_logout, name='logout'),  # Logout functionality

    # Role-based signup and login
    path('signup/<str:role>/', signup_view, name='signup'),  # Signup for buyer/seller
    path('login/<str:role>/', login_view, name='login'),  # Login for buyer/seller

    # Separate login routes for buyers and sellers
    path('buyer-login/', login_view, {'role': 'buyer'}, name='buyer_login'),  # Buyer Login
    path('seller-login/', seller_login_view, name='seller_login'),  # Seller Login

    # Dashboards
    path('buyer-dashboard/', views.buyer_dashboard, name='buyer_dashboard'),  # Buyer Dashboard
    path('seller-dashboard/', views.seller_dashboard, name='seller_dashboard'),  # Seller Dashboard

    # Search and auto-suggestions
    path('get-pet-suggestions/', get_pet_suggestions, name='get_pet_suggestions'),  # Pet suggestions
    path('search-results/', views.search_results, name='search_results'),  # Search results
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


