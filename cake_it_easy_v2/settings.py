import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api

load_dotenv()

# --- Base paths ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security / Hosts ---
# Read from env in production; keep a safe default for local dev
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Comma-separated list in env, e.g.
# ALLOWED_HOSTS="cake-it-easy-7700e2082546.herokuapp.com,localhost,127.0.0.1"
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if h.strip()]

# Django 4+ CSRF: set trusted HTTPS origins (comma-separated)
# CSRF_TRUSTED_ORIGINS="https://cake-it-easy-7700e2082546.herokuapp.com,https://*.herokuapp.com"
_csrf_origins = os.getenv('CSRF_TRUSTED_ORIGINS', '')
if _csrf_origins:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_origins.split(',') if o.strip()]
else:
    CSRF_TRUSTED_ORIGINS = ['https://*.herokuapp.com']

# If behind a proxy (Heroku), this helps Django detect HTTPS correctly
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# --- Applications ---
INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third-party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'cloudinary',
    'cloudinary_storage',
    'whitenoise.runserver_nostatic',

    # Local apps
    'home',
    'products',
    'custom_cake',
    'bag',        
    'checkout',
    'profiles.apps.ProfilesConfig', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cake_it_easy_v2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'allauth'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'bag.context_processors.bag_totals',  # <— added for header counts
            ],
        },
    },
]

WSGI_APPLICATION = 'cake_it_easy_v2.wsgi.application'

# --- Database ---
if os.getenv('USE_SQLITE', 'True') == 'True':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
    }

# --- Authentication / Allauth ---
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_MIN_LENGTH = 4
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

# --- Password validators ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# --- I18N ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Static & Media ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Use Cloudinary for media files (uploads)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Use WhiteNoise for static files in production (hashed filenames, gzip/brotli)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Cloudinary (env-based) ---
_cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
_api_key = os.getenv('CLOUDINARY_API_KEY')
_api_secret = os.getenv('CLOUDINARY_API_SECRET')
_cloudinary_url = os.getenv('CLOUDINARY_URL')

cloudinary_config = {'secure': True}
if _cloud_name and _api_key and _api_secret:
    cloudinary_config.update({
        'cloud_name': _cloud_name,
        'api_key': _api_key,
        'api_secret': _api_secret,
    })
elif _cloudinary_url:
    cloudinary_config['cloudinary_url'] = _cloudinary_url

cloudinary.config(**cloudinary_config)
CLOUDINARY_STORAGE = {
    'UPLOAD_PREFIX': os.getenv('CLOUDINARY_UPLOAD_PREFIX', 'cake-it-easy'),
    'MEDIA_OPTIONS': {
        'use_filename': True,
        'unique_filename': False,
        'folder': os.getenv('CLOUDINARY_UPLOAD_PREFIX', 'cake-it-easy'),
    }
}

# --- Stripe (env-based) ---
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_CURRENCY = os.getenv('STRIPE_CURRENCY', 'eur')
# Add webhook secret in production
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')

# Email (console in dev)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@cakeiteasy.local")


# --- Primary key type ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Emit errors to Heroku logs so 500s are visible
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO"},
        "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": False},
    },
}

