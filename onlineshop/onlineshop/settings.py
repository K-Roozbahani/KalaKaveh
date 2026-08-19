"""
تنظیمات پروژه OnlineShop.

این فایل تنظیمات اصلی Django را برای محیط‌های Development و Production
مدیریت می‌کند.

تنظیمات حساس و وابسته به محیط از فایل .env خوانده می‌شوند.
"""

from datetime import timedelta
from pathlib import Path

from environ import Env
from kombu import Exchange, Queue


# ==========================================================
# Base Configuration
# ==========================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()

ENV_DIR = PROJECT_DIR / "deployment/env/"
env.read_env(ENV_DIR / ".env")


# ==========================================================
# Logging
# ==========================================================

from .config.logging import LOGGING


# ==========================================================
# Security
# ==========================================================

# کلید Secret نباید داخل سورس‌کد قرار داشته باشد.
# مقدار آن باید از Environment خوانده شود.
SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool(
    "DEBUG",
    default=False,
)

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=[
        "127.0.0.1",
        "localhost",
    ],
)


# ==========================================================
# Application Definition
# ==========================================================

INSTALLED_APPS = [
    # ------------------------------------------------------
    # Django
    # ------------------------------------------------------
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # ------------------------------------------------------
    # Third Party
    # ------------------------------------------------------
    "django_ckeditor_5",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "django_filters",
    "corsheaders",

    # ------------------------------------------------------
    # Local Apps
    # ------------------------------------------------------
    "utils",
    "users",
    "home",
    "products",
    "discounts",
    "carts",
    "addresses",
    "orders",
    "payments",
    "shipping",
    "checkout",
    "health",
]


# ==========================================================
# Middleware
# ==========================================================

MIDDLEWARE = [
    # ------------------------------------------------------
    # Security
    # ------------------------------------------------------
    "django.middleware.security.SecurityMiddleware",

    # ------------------------------------------------------
    # CORS
    # ------------------------------------------------------
    "corsheaders.middleware.CorsMiddleware",

    # ------------------------------------------------------
    # Session
    # ------------------------------------------------------
    "django.contrib.sessions.middleware.SessionMiddleware",

    # ------------------------------------------------------
    # Common
    # ------------------------------------------------------
    "django.middleware.common.CommonMiddleware",

    # ------------------------------------------------------
    # CSRF
    # ------------------------------------------------------
    "django.middleware.csrf.CsrfViewMiddleware",

    # ------------------------------------------------------
    # Authentication
    # ------------------------------------------------------
    "django.contrib.auth.middleware.AuthenticationMiddleware",

    # ------------------------------------------------------
    # Messages
    # ------------------------------------------------------
    "django.contrib.messages.middleware.MessageMiddleware",

    # ------------------------------------------------------
    # Clickjacking Protection
    # ------------------------------------------------------
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "onlineshop.urls"

WSGI_APPLICATION = "onlineshop.wsgi.application"


# ==========================================================
# Templates
# ==========================================================

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


# ==========================================================
# Database
# ==========================================================

DB_SQLITE = env.bool(
    "DB_SQLITE",
    default=True,
)

if DB_SQLITE:

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

else:

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("POSTGRES_DB"),
            "USER": env("POSTGRES_USER"),
            "PASSWORD": env("POSTGRES_PASSWORD"),
            "HOST": env(
                "POSTGRES_HOST",
                default="postgres",
            ),
            "PORT": env.int(
                "POSTGRES_PORT",
                default=5432,
            ),

            # نگه داشتن Connection برای افزایش Performance
            "CONN_MAX_AGE": env.int(
                "POSTGRES_CONN_MAX_AGE",
                default=600,
            ),

            # بررسی سلامت Connectionهای Persistent
            "CONN_HEALTH_CHECKS": True,

            "OPTIONS": {
                "connect_timeout": 10,
            },
        }
    }


# ==========================================================
# Password Validation
# ==========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator",
    },
]


# ==========================================================
# Internationalization
# ==========================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Tehran"

USE_I18N = True

USE_TZ = True


# ==========================================================
# Static & Media
# ==========================================================

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR.parent / "static_root"

MEDIA_ROOT = BASE_DIR.parent / "media_root"

MEDIA_URL = "media/"


# ==========================================================
# Authentication
# ==========================================================

AUTH_USER_MODEL = "users.User"


# ==========================================================
# Django REST Framework
# ==========================================================

REST_FRAMEWORK = {

    # ------------------------------------------------------
    # Permission
    # ------------------------------------------------------

    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],

    # ------------------------------------------------------
    # Authentication
    #
    # فعلاً JWTAuthentication استاندارد را نگه می‌داریم.
    # پس از پیاده‌سازی CookieJWTAuthentication این مقدار
    # به Authentication Class اختصاصی پروژه تغییر خواهد کرد.
    # ------------------------------------------------------

    "DEFAULT_AUTHENTICATION_CLASSES": (
        "users.authentication.jwt.CookieJWTAuthentication",
    ),

    # ------------------------------------------------------
    # Pagination
    # ------------------------------------------------------

    "DEFAULT_PAGINATION_CLASS":
        "rest_framework.pagination.PageNumberPagination",

    "PAGE_SIZE": 10,

    # ------------------------------------------------------
    # OpenAPI / Swagger
    # ------------------------------------------------------

    "DEFAULT_SCHEMA_CLASS":
        "drf_spectacular.openapi.AutoSchema",

    # ------------------------------------------------------
    # Exception Handler
    # ------------------------------------------------------

    "EXCEPTION_HANDLER":
        "onlineshop.config.exceptions.handlers.custom_exception_handler",
}


# ==========================================================
# Simple JWT
# ==========================================================

SIMPLE_JWT = {

    # ------------------------------------------------------
    # Access Token
    # ------------------------------------------------------

    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=10,
    ),

    # ------------------------------------------------------
    # Refresh Token
    # ------------------------------------------------------

    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=7,
    ),

    # ------------------------------------------------------
    # Refresh Token Rotation
    #
    # پس از Refresh، Refresh Token جدید صادر می‌شود.
    # ------------------------------------------------------

    "ROTATE_REFRESH_TOKENS": True,

    # ------------------------------------------------------
    # Blacklist
    #
    # Refresh Token قبلی پس از Rotation باطل می‌شود.
    # ------------------------------------------------------

    "BLACKLIST_AFTER_ROTATION": True,

    # ------------------------------------------------------
    # Authentication Header
    #
    # فعلاً برای حفظ سازگاری با Simple JWT نگه داشته شده.
    # بعداً Cookie Authentication روی آن قرار می‌گیرد.
    # ------------------------------------------------------

    "AUTH_HEADER_TYPES": (
        "Bearer",
    ),
}


# ==========================================================
# Cache - Redis
# ==========================================================

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("CACHE_REDIS_URL"),

        "TIMEOUT": 300,

        "OPTIONS": {
            "socket_connect_timeout": 5,
            "socket_timeout": 5,
        },
    }
}


# ==========================================================
# Celery
# ==========================================================

CELERY_BROKER_URL = env(
    "CELERY_BROKER_URL",
)

CELERY_RESULT_BACKEND = env(
    "CELERY_RESULT_BACKEND",
)

CELERY_ACCEPT_CONTENT = [
    "json",
]

CELERY_TASK_SERIALIZER = "json"

CELERY_RESULT_SERIALIZER = "json"

CELERY_TIMEZONE = TIME_ZONE

CELERY_ENABLE_UTC = False

CELERY_TASK_TRACK_STARTED = True

CELERY_TASK_TIME_LIMIT = 60 * 30

CELERY_TASK_SOFT_TIME_LIMIT = 60 * 25

CELERY_TASK_ACKS_LATE = True

CELERY_WORKER_PREFETCH_MULTIPLIER = 1

CELERY_TASK_REJECT_ON_WORKER_LOST = True

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CELERY_RESULT_EXPIRES = 60 * 60 * 24


HEALTH_CHECK_CELERY = env.bool(
    "HEALTH_CHECK_CELERY",
    default=False,
)


# ==========================================================
# Celery Default Queue
# ==========================================================

CELERY_TASK_DEFAULT_QUEUE = "notification"

CELERY_TASK_DEFAULT_EXCHANGE = "notification"

CELERY_TASK_DEFAULT_ROUTING_KEY = "notification"


# ==========================================================
# Celery Queues
# ==========================================================

CELERY_TASK_QUEUES = (
    Queue(
        "notification",
        Exchange("notification"),
        routing_key="notification",
    ),

    Queue(
        "pricing",
        Exchange("pricing"),
        routing_key="pricing",
    ),
)


# ==========================================================
# Celery Routes
# ==========================================================

CELERY_TASK_ROUTES = {

    # ------------------------------------------------------
    # Price Engine
    # ------------------------------------------------------

    "discounts.refresh_variant_price": {
        "queue": "pricing",
    },

    "discounts.refresh_product_variants_price": {
        "queue": "pricing",
    },

    "discounts.refresh_all_variant_prices": {
        "queue": "pricing",
    },

    # ------------------------------------------------------
    # Notifications
    # ------------------------------------------------------

    "accounts.send_otp": {
        "queue": "notification",
    },
}


# ==========================================================
# CORS
# ==========================================================

CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
)

# اجازه ارسال Cookie همراه Requestهای Cross-Origin
CORS_ALLOW_CREDENTIALS = True


# ==========================================================
# CSRF
# ==========================================================

# Originهای مجاز برای درخواست‌های حساس به CSRF.
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
)

# Frontend باید بتواند مقدار CSRF Cookie را بخواند
# تا آن را در Header با نام X-CSRFToken ارسال کند.
CSRF_COOKIE_HTTPONLY = env.bool(
    "CSRF_COOKIE_HTTPONLY",
    default=False,
)

# در Production فقط روی HTTPS ارسال شود.
CSRF_COOKIE_SECURE = env.bool(
    "CSRF_COOKIE_SECURE",
    default=not DEBUG,
)

# جلوگیری از ارسال Cookie در Cross-Site Requestهای ناخواسته.
CSRF_COOKIE_SAMESITE = env(
    "CSRF_COOKIE_SAMESITE",
    default="Lax",
)


# ==========================================================
# Session Cookie
# ==========================================================

# Session برای Guest Cart پروژه استفاده می‌شود.
SESSION_COOKIE_HTTPONLY = True

# در Production فقط روی HTTPS ارسال شود.
SESSION_COOKIE_SECURE = not DEBUG

SESSION_COOKIE_SAMESITE = "Lax"


# ==========================================================
# JWT Cookie Configuration
# ==========================================================

# نام Cookie مربوط به Access Token
AUTH_COOKIE_ACCESS = env(
    "AUTH_COOKIE_ACCESS",
    default="access_token",
)

# نام Cookie مربوط به Refresh Token
AUTH_COOKIE_REFRESH = env(
    "AUTH_COOKIE_REFRESH",
    default="refresh_token",
)

# Cookieهای JWT در Production فقط روی HTTPS ارسال می‌شوند.
AUTH_COOKIE_SECURE = env.bool(
    "AUTH_COOKIE_SECURE",
    default=not DEBUG,
)

# سیاست SameSite برای JWT Cookieها.
AUTH_COOKIE_SAMESITE = env(
    "AUTH_COOKIE_SAMESITE",
    default="Lax",
)


# ==========================================================
# Security Headers
# ==========================================================

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"

SECURE_REFERRER_POLICY = (
    "strict-origin-when-cross-origin"
)

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)


# ----------------------------------------------------------
# HTTPS Redirect
#
# در Production فعال می‌شود.
# در صورتی که HTTPS توسط Nginx مدیریت شود، باید Header
# X-Forwarded-Proto به درستی Forward شده باشد.
# ----------------------------------------------------------

SECURE_SSL_REDIRECT = env.bool(
    "SECURE_SSL_REDIRECT",
    default=not DEBUG,
)


# ==========================================================
# Django CKEditor 5
# ==========================================================

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "underline",
            "link",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "insertTable",
            "blockQuote",
            "|",
            "imageUpload",
            "|",
            "undo",
            "redo",
        ]
    }
}


# ==========================================================
# DRF Spectacular
# ==========================================================

SPECTACULAR_SETTINGS = {

    "TITLE": "Online Shop API",

    "DESCRIPTION": "REST API Documentation",

    "VERSION": "1.0.0",

    "SERVE_INCLUDE_SCHEMA": False,

    "COMPONENT_SPLIT_REQUEST": True,

    # فعلاً تا زمان پیاده‌سازی کامل Cookie Authentication
    # برای حفظ سازگاری Swagger نگه داشته شده است.
    "SECURITY": [
        {
            "Bearer": [],
        },
    ],

    "SECURITY_SCHEMES": {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    },
}