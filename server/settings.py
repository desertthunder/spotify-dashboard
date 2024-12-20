"""Django settings for server project.

Generated by 'django-admin startproject' using Django 5.1.1.
"""

import os
import pathlib

from dotenv import load_dotenv

load_dotenv()


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

# NOTE: Used to encode and decode JWT tokens
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-oukd3fukrry=ce&7kc*itz=(%y*hphm7fq)1s^228fn4p2%%8q",
)

DEBUG = bool(os.environ.get("DEBUG", 0))

ALLOWED_HOSTS: list[str] = [
    "127.0.0.1",
    "localhost",
    "local.dashspot.dev",
]

CORS_ALLOWED_ORIGINS = [
    "https://local.dashspot.dev",  # React
    "http://localhost:5173",  # React
    "https://accounts.spotify.com",  # Spotify Redirect URI
]

CORS_ALLOWED_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "referer",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

INSTALLED_APPS = [
    "daphne",
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "corsheaders",
    "browser",
    "api",
    "core",
    "apps",
    "live",
    "library",
    "django_celery_results",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI_APPLICATION = "server.wsgi.application"
ASGI_APPLICATION = "server.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("PGDATABASE", "music_api_db"),
        "USER": os.environ.get("PGUSER", "pguser"),
        "PASSWORD": os.environ.get("PGPASSWORD", "password"),
        "HOST": os.environ.get("PGHOST", "localhost"),
        "PORT": os.environ.get("PGPORT", 5432),
    }
}

# Authentication
AUTH_USER_MODEL = "core.AppUser"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static Files
STATIC_URL = "static/"

# Default pk
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Spotify API
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", None)
SPOTIFY_BASE_URL = "https://api.spotify.com/v1/"

REST_FRAMEWORK = {
    "DEFAULT_METADATA_CLASS": "rest_framework.metadata.SimpleMetadata",
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
}

CELERY_TIMEZONE = "America/Chicago"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_RESULT_BACKEND = "django-db"
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_RESULT_EXTENDED = True
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

WEB_APP_URL = os.getenv("WEB_APP_URL", "https://local.dashspot.dev")
REDIRECT_URI = f"{WEB_APP_URL}/server/api/login"
