from pathlib import Path
import environ
import logging
from datetime import timedelta
import logging.config
from django.utils.log import DEFAULT_LOGGING
from .constants import LoggingConstants

env = environ.Env(DEBUG=(bool, False))
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
environ.Env.read_env(BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-=t5t%&aaab9-3r$a+1(7%-t%qm4h#wih6wyf95+6sy_+3#!ser"


ALLOWED_HOSTS = ["*"]


# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = [
    "apps.users.apps.UsersConfig",
    "apps.core.apps.CoreConfig",
    "apps.analytics.apps.AnalyticsConfig",
    "apps.availability.apps.AvailabilityConfig",
    "apps.bookings.apps.BookingsConfig",
    "apps.notifications.apps.NotificationsConfig",
    "apps.payments.apps.PaymentsConfig",
    "apps.reviews.apps.ReviewsConfig",
    "apps.services.apps.ServicesConfig",
]

THIRD_PARTY_APPS = [
    "autoslug",
    "django_extensions",
    "django_elasticsearch_dsl",
    "allauth",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.account",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "djoser",
    "formtools",
    "djcelery_email",
    "drf_spectacular",
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

# Social Auth Settings
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "EMAIL_AUTHENTICATION": True  # authenticate user authomatically when logged in useing google
    }
}

SOCIALACCOUNT_AUTO_SIGNUP = (
    True  # Automatically creates an account if not already existing
)


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "mubaku.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mubaku.wsgi.application"

# Elastic Search
ELASTICSEARCH_DSL = {
    "default": {"hosts": "http://elasticsearch:9200"},
}


# Cors settings

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-requested-with",
    "accept",
    "origin",
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]


# Cache Settings
CACHES = {
    "default": {
        "BACKEND": env("CACHE_BACKEND"),
        "LOCATION": env("CACHE_LOCATION"),
        "OPTIONS": {
            "CLIENT_CLASS": env("OPTIONS_CLIENT_CLASS"),
        },
    }
}

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [
    "https://mubakulifestyle.com",
    "http://178.79.157.38",  # Your VPS IP address
    "http://localhost",  # If you're testing locally
    "https://leading-kite-wise.ngrok-free.app",
]


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Auth Settings

SITE_ID = 1

LOGIN_REDIRECT_URL = "/"  # Redirect after login
LOGOUT_REDIRECT_URL = "/"  # Redirect after logout

# Use email as the login field
ACCOUNT_AUTHENTICATION_METHOD = "email"

# Remove the username field from signup forms
ACCOUNT_USERNAME_REQUIRED = False

# Require the user to provide an email during signup
ACCOUNT_EMAIL_REQUIRED = True

# Enforce email uniqueness in the database
ACCOUNT_UNIQUE_EMAIL = True

# Login using the email field
ACCOUNT_EMAIL_VERIFICATION = "optional"  # or 'mandatory' if you want email verification

AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by email
    "allauth.account.auth_backends.AuthenticationBackend",
]


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    # },
]

DEFAULT_FROM_EMAIL = "electron7089@gmail.com"


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Douala"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "/staticfiles/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "NON_FIELD_ERRORS_KEY": "error",
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


# API Documentation
SPECTACULAR_SETTINGS = {
    "TITLE": "Mubaku Lifestyle API",
    "DESCRIPTION": "API documentation for authentication, users, and profiles.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

DJANGO_FILTERS_CONFIG = {
    "DEFAULT_RENDERER": None,
}


SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": (
        "Bearer",
        "JWT",
    ),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=20),
    "SIGNING_KEY": env("SIGNING_KEY"),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

DJOSER = {
    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "USERNAME_CHANGE_EMAIL_CONFIRMATION": True,
    "PASSWORD_CHANGE_EMAIL_CONFIRMATION": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "USERNAME_RESET_CONFIRM_URL": "email/reset/confirm/{uid}/{token}",
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": False,
    "SERIALIZERS": {
        "user_create": "apps.users.serializers.CreateUserSerializer",
        "user_create_password_retype": "apps.users.serializers.CreateUserSerializer",
        "user": "apps.users.serializers.UserSerializer",
        "current_user": "apps.users.serializers.UserSerializer",
        "user_delete": "djoser.serializers.UserDeleteSerializer",
    },
    "PERMISSIONS": {
        "user_create": ["rest_framework.permissions.AllowAny"],
        "user": ["rest_framework.permissions.IsAuthenticated"],
        "user_delete": ["rest_framework.permissions.IsAuthenticated"],
        "current_user": ["rest_framework.permissions.IsAuthenticated"],
        "activation": ["rest_framework.permissions.AllowAny"],
        "password_reset": ["rest_framework.permissions.AllowAny"],
        "password_reset_confirm": ["rest_framework.permissions.AllowAny"],
        "password_change": ["rest_framework.permissions.IsAuthenticated"],
        "password_change_confirm": ["rest_framework.permissions.IsAuthenticated"],
        "user_list": ["rest_framework.permissions.IsAuthenticated"],
    },
    "HIDE_USERS": False,
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": True,
}


# =============== Logging ================
logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
            },
            "file": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"},
            "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
            },
            "file": {
                "level": LoggingConstants.LOG_LEVEL,
                "class": "logging.FileHandler",
                "formatter": "file",
                "filename": f"logs/{LoggingConstants.LOG_FILE_NAME}",
            },
            "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
        },
        "loggers": {
            "": {
                "level": LoggingConstants.LOG_LEVEL,
                "handlers": ["console", "file"],
                "propagate": False,
            },
            "apps": {
                "level": LoggingConstants.LOG_LEVEL,
                "handlers": ["console", "file"],
                "propagate": False,
            },
            "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
            "channels": {
                "level": "DEBUG",  # Set to DEBUG for detailed Channels logging
                "handlers": ["console", "file"],
                "propagate": False,
            },
            "channels.layers": {
                "level": "DEBUG",  # Specific logger for Channels layers
                "handlers": ["console", "file"],
                "propagate": False,
            },
        },
    }
)
