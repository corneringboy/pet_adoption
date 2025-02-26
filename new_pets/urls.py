from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import get_pet_suggestions, signup_view, login_view, seller_login_view

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('about/', views.about, name='about'),  # About page
    path('contact/', views.contact, name='contact'),  # Contact page
    path('logout/', views.custom_logout, name='logout'),  # Logout functionality

    # Role-based signup and login
    path('signup/<str:role>/', signup_view, name='signup'),
    path('login/<str:role>/', login_view, name='login'),

    # Separate login routes for buyers and sellers
    path('login/', login_view, name='buyer_login'),  # Buyer Login
    path('seller-login/', seller_login_view, name='seller_login'),  # Seller Login

    # Buyer and seller dashboards
    path('buyer-dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('seller-dashboard/', views.seller_dashboard, name='seller_dashboard'),

    # Search and auto-suggestions
    path('get-pet-suggestions/', get_pet_suggestions, name='get_pet_suggestions'),
    path('search-results/', views.search_results, name='search_results'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  



