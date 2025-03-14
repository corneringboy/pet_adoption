import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings
SECRET_KEY = 'django-insecure-2op$tae6wpc#r8bl+%z(3snsf1-q5udj)p_go-x6_@9xf^_1%b'  # ❗ Replace with env var in production

DEBUG = True  # ❗ Set to False in production

ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # ✅ Added for local development

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'new_pets',  # ✅ Your app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # ✅ Ensure CSRF Middleware is enabled
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pet_adoption.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ✅ Project-level templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pet_adoption.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

### ✅ FIXED STATIC FILES CONFIGURATION ###
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'new_pets' / 'static']  # ✅ Corrected path
STATIC_ROOT = BASE_DIR / 'staticfiles'  # ✅ Static files for production

### ✅ FIXED MEDIA FILES CONFIGURATION ###
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # ✅ Corrected path for uploaded files

# ✅ Custom user model
AUTH_USER_MODEL = 'new_pets.CustomUser'  # ✅ Ensure this model exists

# ✅ Authentication URLs
LOGIN_URL = 'login'             # ✅ URL name for login page
LOGIN_REDIRECT_URL = 'home'     # ✅ Added to redirect after login
LOGOUT_REDIRECT_URL = 'home'    # ✅ Redirect after logout

# ✅ Authentication Backend
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# ✅ Added Email Backend for Account Confirmation & Password Reset
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # ✅ Prints emails to the console (for testing)
EMAIL_HOST = 'smtp.gmail.com'  # ✅ Update for real SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # ✅ Replace with your email
EMAIL_HOST_PASSWORD = 'your-email-password'  # ❗ Use environment variables in production

# ✅ CSRF Settings (Ensure Secure Handling in Production)
CSRF_COOKIE_SECURE = False  # ✅ Set to True in production with HTTPS
CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_NAME = 'csrftoken'

# ✅ Default Auto Field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
