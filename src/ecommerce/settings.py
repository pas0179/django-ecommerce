"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os


# Import du module python-decouple qui a ete fait avant avec PIP
# pour les variables d'environnements
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG")

# ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '4239-2a02-8440-c127-a2be-9894-d3f7-1689-d0f8.ngrok-free.app']
ALLOWED_HOSTS = ["*"]

# Sans ce paramètre le cookie reste actif pendant 1 an et provoque
# une erreur de csrf_token dans les formulaire sur certain navigateur.
CSRF_COOKIE_AGE = None

# Application definition

INSTALLED_APPS = [
    # app account
    'account',
    'crispy_forms',
    "crispy_bootstrap5",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # App utiles pour django
    'django_extensions',
    # app store
    'store',
    # app product
    'product',
    # app contact
    'contact',
    # app cart
    'cart', 
    # app order
    'order',
    # app payment
    'payment',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Ajout de cart contect processor
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = ['static/']

STATIC_ROOT = BASE_DIR / 'static_files'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Variable pour le panier
CART_SESSION_ID = "cart"

# Authentification par une adresse mail
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    # Fichier authentication.py dans account avec fonction EmailAuthBackend
    "account.authentication.EmailAuthBackend",
]

# Pour aprês l'authentification des utilisateurs si authentifié
LOGIN_REDIRECT_URL = "home"
LOGIN_URL = "login"
LOGOUT_URL = "logout"

# Utilisation de bootstrap pour les messages
# On surcharge la méthode
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Parametre pour utilisation d'un dossier pour recevoir les liens de reinitialisation
# en attendant d'avoir un serveur smtp local ou distant
# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_FILE_PATH = BASE_DIR / "sent_emails"

# Config pour l'envoi de mail avec serveur smtp
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST=config("EMAIL_HOST")
EMAIL_PORT=config("EMAIL_PORT")
EMAIL_USE_TLS=config("EMAIL_USE_TLS")
# EMAIL_USE_SSL=config("EMAIL_USE_SSL")
EMAIL_HOST_USER=config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD=config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL=config("DEFAULT_FROM_EMAIL")


# Stripe paiement en ligne

STRIPE_PUBLISHABLE_KEY = config("STRIPE_PUBLISHABLE_KEY ")
STRIPE_SECRET_KEY =config("STRIPE_SECRET_KEY")
STRIPE_API_VERSION = config("STRIPE_API_VERSION")

# Webhook stripe: permet de récupérer l'info sur le paiement: payer ou refusé
# A récupérer sur stripe dans fichier de config webhook, endpoint_secret = ''
STRIPE_WEBHOOK_SECRET=config("STRIPE_WEBHOOK_SECRET")