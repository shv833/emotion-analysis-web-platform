"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
# from celery.schedules import crontab
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
PROJECT_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = PROJECT_DIR.parent.parent

# print(f'project dir:\n {os.listdir(PROJECT_DIR)}')
# print(f'base dir:\n {os.listdir(BASE_DIR)}')


def optional(key, default=None):
    return os.environ.get(key, default)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = optional("SECRET_KEY", "secret")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = optional("DJANGO_DEBUG", "false").lower() == "true"

ALLOWED_HOSTS = optional("ALLOWED_HOSTS", "localhost,127.0.0.1,[::1],0.0.0.0").split(",")


# Application definition

INSTALLED_APPS = [
        "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    "django_ckeditor_5",
    "drf_spectacular",
    "rest_framework",
    "rest_framework.authtoken",
    "djoser",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "backend",
    "users",
    "groups",
    "courses",
    "debug_toolbar",
    "django_hosts",
    # "django_celery_beat",
]

MIDDLEWARE = [
    "django_hosts.middleware.HostsRequestMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django_hosts.middleware.HostsResponseMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
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

WSGI_APPLICATION = "backend.wsgi.application"
ASGI_APPLICATION = "backend.asgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": optional("POSTGRES_ENGINE", "django.db.backends.postgresql_psycopg2"),
        "NAME": optional("POSTGRES_DB"),
        "USER": optional("POSTGRES_USER"),
        "PASSWORD": optional("POSTGRES_PASSWORD"),
        "HOST": optional("POSTGRES_HOST"),
        "PORT": optional("POSTGRES_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

STATIC_URL = "staticfiles/"
STATIC_ROOT = os.path.join(PROJECT_DIR, "staticfiles")


# Email

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = optional("EMAIL_HOST")
EMAIL_PORT = optional("EMAIL_PORT")
EMAIL_HOST_USER = optional("EMAIL_USER")
EMAIL_HOST_PASSWORD = optional("EMAIL_PASS")
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_SENDER = optional("EMAIL_SENDER", EMAIL_HOST_USER)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
}

DJOSER = {
    "PASSWORD_RESET_CONFIRM_URL": "auth/password/reset-password-confirmation/?uid={uid}&token={token}",
    "ACTIVATION_URL": "#/activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": False,
    "SERIALIZERS": {},
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Emotion analysis API",
    "DESCRIPTION": "Emotion analysis diploma",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
}

AUTH_USER_MODEL = "users.User"

APPEND_SLASH = True

# CKEditor

customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]

CKEDITOR_5_CONFIGS = {
    "default": {
        "language": {"ui": "en", "content": "en"},
        "blockToolbar": [
            "paragraph",
            "heading1",
            "heading2",
            "heading3",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "blockQuote",
        ],
        "toolbar": [
            "heading",
            "codeBlock",
            "|",
            "outdent",
            "indent",
            "|",
            "bold",
            "italic",
            "link",
            "underline",
            "strikethrough",
            "code",
            "subscript",
            "superscript",
            "highlight",
            "|",
            "bulletedList",
            "numberedList",
            "todoList",
            "|",
            "blockQuote",
            "insertImage",
            "|",
            "fontSize",
            "fontFamily",
            "fontColor",
            "fontBackgroundColor",
            "mediaEmbed",
            "removeFormat",
            "insertTable",
            "sourceEditing",
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignRight",
                "imageStyle:alignCenter",
                "imageStyle:side",
                "|",
                "toggleImageCaption",
                "|",
            ],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties",
            ],
            "tableProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
            "tableCellProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
        },
        "heading": {
            "options": [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading1",
                    "view": "h1",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h3",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
            ]
        },
        "list": {
            "properties": {
                "styles": True,
                "startIndex": True,
                "reversed": True,
            }
        },
        "htmlSupport": {"allow": [{"name": "/.*/", "attributes": True, "classes": True, "styles": True}]},
    },
}

# Configure subdomains
ROOT_URLCONF = "backend.urls.api"
ROOT_HOSTCONF = "backend.hosts"
DEFAULT_HOST = "api"

# Debugger
INTERNAL_IPS = [
    "127.0.0.1",
]

# # CORS and CSRF prod
# CORS_ALLOWED_ORIGINS = [f"http://{i}" for i in ALLOWED_HOSTS]
# CSRF_COOKIE_DOMAIN = optional("CSRF_COOKIE_DOMAIN", ".localhost")
# CSRF_TRUSTED_ORIGINS = [f"http://{i}" for i in ALLOWED_HOSTS]
# CSRF_COOKIE_SAMESITE = "None"
# CSRF_COOKIE_SECURE = True

# CORS and CSRF dev
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = "Lax"
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = [f"http://{i}" for i in ALLOWED_HOSTS]
CSRF_TRUSTED_ORIGINS = [f"http://{i}" for i in ALLOWED_HOSTS]


DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"


# CELERY_BROKER_URL = "redis://redis:6379/0"
# CELERY_TIMEZONE = "UTC"

# CELERY_BEAT_SCHEDULE = {
#     "delete_expired_tokens_every_week": {
#         "task": "backend.tasks.delete_expired_tokens",
#         "schedule": crontab(hour=3, minute=0),
#     },
# }


if DEBUG:
    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }
    MINIO_ACCESS_KEY = optional("MINIO_ROOT_USER")
    MINIO_SECRET_KEY = optional("MINIO_ROOT_PASSWORD")
    MINIO_BUCKET_NAME = optional("MINIO_BUCKET_NAME")
    MINIO_ENDPOINT = optional("MINIO_ENDPOINT")

    AWS_ACCESS_KEY_ID = MINIO_ACCESS_KEY
    AWS_SECRET_ACCESS_KEY = MINIO_SECRET_KEY
    AWS_STORAGE_BUCKET_NAME = MINIO_BUCKET_NAME
    AWS_S3_ENDPOINT_URL = MINIO_ENDPOINT
    AWS_S3_URL_PROTOCOL = "http:"
    AWS_S3_CUSTOM_DOMAIN = f"localhost/{MINIO_BUCKET_NAME}"
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = True
    AWS_S3_FILE_OVERWRITE = False
