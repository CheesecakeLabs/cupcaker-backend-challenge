import os
from datetime import timedelta
from os.path import abspath, dirname, exists, join

import environ

# Load operating system env variables and prepare to use them
env = environ.Env()

# .env file, should load only in development environment
env_file = join(dirname(__file__), "local.env")
if exists(env_file):
    environ.Env.read_env(str(env_file))


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = dirname(dirname(abspath(__file__)))

# Quick-start development settings - unsuitable for production
SECRET_KEY = env(
    "DJANGO_SECRET_KEY", default="8#ubdv*jh_1u(6m4)^s^*pdo!&y_#jz)vv%5cp%8^*&%ztttxq"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", False)
ENVIRONMENT = env("ENV")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=[])

# CORS
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=False)
if not CORS_ALLOW_ALL_ORIGINS:
    CORS_ALLOWED_ORIGINS = env.str(
        "CORS_ALLOWED_ORIGINS", default="localhost,127.0.0.1"
    ).split(",")

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "versatileimagefield",
    "drf_spectacular",
    "django_extensions",
    "rest_framework_simplejwt.token_blacklist",
]

PROJECT_APPS = ["api.authentication", "api.core", "dashboard"]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "api.core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "api.core.wsgi.application"

# Django debug toolbar settings

if ENVIRONMENT == "development":
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INTERNAL_IPS = env.list("INTERNAL_IPS", [])
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: request.headers.get("x-requested-with")
        != "XMLHttpRequest"
    }


# Database

DATABASES = {"default": env.db()}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"}
]

# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = []

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

SITE_ID = 1

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files (uploads)

if ENVIRONMENT in ("development", "testing"):
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    MEDIA_ROOT = "uploads/"
    MEDIA_URL = "/uploads/"

# Email settings

if ENVIRONMENT in ("development", "testing"):
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "no-reply@localhost"

# Django Rest Framework Settings

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "api.authentication.helpers.tokens.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Auth

AUTH_USER_MODEL = "authentication.User"
FORGOT_TIME_EXPIRATION_TIME = timedelta(days=1)

#

SPECTACULAR_SETTINGS = {
    "TITLE": "Python Django",
    "VERSION": "1.0.0",
    "DESCRIPTION": "API Documentation",
}


# VersatileImageField
# https://django-versatileimagefield.readthedocs.io/en/latest/installation.html#settings

VERSATILEIMAGEFIELD_SETTINGS = {
    "cache_length": 2592000,
    "cache_name": "versatileimagefield_cache",
    "jpeg_resize_quality": 70,
    "sized_directory_name": "__sized__",
    "filtered_directory_name": "__filtered__",
    "placeholder_directory_name": "__placeholder__",
    "create_images_on_demand": True,
    "image_key_post_processor": None,
    "progressive_jpeg": False,
}

# The rendition key sets will be used if 'create_images_on_demand' is set to False
# It will improve the overall performance of your app by pre warming images
# These values should come from the app's design specs
# https://django-versatileimagefield.readthedocs.io/en/latest/installation.html#versatileimagefield-rendition-key-sets

# VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
#     'image_gallery': [
#         ('gallery_large', 'crop__800x450'),
#     ],
# }

# SimpleJWT Settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=int(env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=5))
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=int(env.int("REFRESH_TOKEN_EXPIRE_DAYS", default=1))
    ),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "SIGNING_KEY": env.str("JWT_SECRET_KEY", default=SECRET_KEY),
    "AUTH_HEADER_TYPES": ("Bearer", "Token"),
}

# AWS

AWS_ACCESS_KEY = env.str("AWS_ACCESS_KEY", default="")
AWS_SECRET_KEY = env.str("AWS_SECRET_KEY", default="")
AWS_REGION = env.str("AWS_REGION", default="")

# Messenger

DEFAULT_MESSENGER = "EMAIL"
