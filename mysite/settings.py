"""
Django settings for mysite project (Railway + React CORS/CSRF ready)
Django 4.0.4
"""

import os
from pathlib import Path

# ---------- Paths ----------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------- Helpers ----------
def env_bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes", "on"}

def env_list(name: str, default_list):
    raw = os.getenv(name)
    return [x.strip() for x in raw.split(",")] if raw else default_list

# ---------- Core ----------
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-rc^*w^w&6g9_(uvx#6s*bnt!w)l0rdi%!l7mv#y%uc&x%wo5pk",  # dev fallback
)
DEBUG = env_bool("DJANGO_DEBUG", True)

# Be explicit in production (avoid "*")
ALLOWED_HOSTS = env_list(
    "DJANGO_ALLOWED_HOSTS",
    [
        "server-production-3fc4.up.railway.app",  # <<< UPDATE (your Railway URL)
        "localhost",
        "127.0.0.1",
    ],
)

# CSRF: must include scheme (https://). Django 4.0.x does NOT support wildcards here.
CSRF_TRUSTED_ORIGINS = env_list(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    [
        "https://server-production-3fc4.up.railway.app",  # <<< UPDATE (your Railway URL)
        "https://frontend-mu-two-39.vercel.app",          # <<< UPDATE (your React frontend)
        "http://localhost:3000",
    ],
)

# Tell Django it’s behind Railway’s proxy so request.is_secure() works
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Secure cookies for HTTPS
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# If your React app uses Django session auth across domains, SameSite must be None
CSRF_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SAMESITE = "None"

# ---------- Apps ----------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # CORS
    "corsheaders",
]

# ---------- Middleware ----------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",          # keep directly after Security
    "django.contrib.sessions.middleware.SessionMiddleware",

    # CORS must be before CommonMiddleware
    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mysite.urls"

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

WSGI_APPLICATION = "mysite.wsgi.application"

# ---------- Database (Railway Postgres via env) ----------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ["PGDATABASE"],
        "USER": os.environ["PGUSER"],
        "PASSWORD": os.environ["PGPASSWORD"],
        "HOST": os.environ["PGHOST"],
        "PORT": os.environ["PGPORT"],
    }
}

# ---------- Password validation ----------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------- i18n ----------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------- Static files ----------
STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------- CORS (React) ----------
# Frontend origins that may call your API (must include scheme)
CORS_ALLOWED_ORIGINS = env_list(
    "DJANGO_CORS_ALLOWED_ORIGINS",
    [
        "https://frontend-react-django-8f5da9j3f-mrgbpjpygmailcoms-projects.vercel.app/",  # <<< UPDATE (your React frontend)
        "http://localhost:3000",
    ],
)
CORS_ALLOW_CREDENTIALS = True
# If you need extra headers: from corsheaders.defaults import default_headers
# CORS_ALLOW_HEADERS = list(default_headers) + ["X-CSRFToken", "Authorization"]
