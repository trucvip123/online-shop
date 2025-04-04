import os
import sys
from dotenv import load_dotenv
from urllib.parse import urlparse


load_dotenv()
tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

SECRET_KEY = "uey!i4x26n!$d-73cs%blri)09#xfud_e361ne2h(#s2uj7)l!"

DEBUG = True

ALLOWED_HOSTS = ["14.225.23.223", "localhost", "127.0.0.1", "dienthanhliem.com", "www.dienthanhliem.com"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "df_cart",
    "df_goods",
    "df_user",
    "df_order",
    "tinymce",
    'social_django'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "daily_fresh_demo.urls"

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
                "django.template.context_processors.media",
            ],
        },
    },
]

WSGI_APPLICATION = "daily_fresh_demo.wsgi.application"

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#     },
#     "OPTIONS": {
#         "TIMEOUT": 20,
#     },
# }


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "thanhliemdb",
#         "USER": "postgres",
#         "PASSWORD": "123",
#         "HOST": "localhost",
#         "PORT": "5432",
#     }
# }

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": tmpPostgres.path.replace("/", ""),
#         "USER": tmpPostgres.username,
#         "PASSWORD": tmpPostgres.password,
#         "HOST": tmpPostgres.hostname,
#         "PORT": 5432,
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME", "default_db"),
        "USER": os.getenv("DB_USER", "default_user"),
        "PASSWORD": os.getenv("DB_PASSWORD", "default_password"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

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

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("GOOGLE_CLIENT_ID", "<your-client-id>")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "<your-client-secret>")

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

USE_I18N = True

USE_L10N = True

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Ho_Chi_Minh"

USE_TZ = False

# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"
# This is where you store static files manually (DO NOT use STATIC_ROOT here)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # ✅ Ensure this directory exists
]

# This is where collectstatic collects all static files for deployment
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # ✅ Separate directory

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")


TINYMCE_DEFAULT_CONFIG = {
    "theme": "advanced",
    "width": 600,
    "height": 400,
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATA_UPLOAD_MAX_MEMORY_SIZE = 209715200