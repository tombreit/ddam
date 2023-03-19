"""
Django settings for ddam project.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/

See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/
"""

from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    AUTH_LDAP=(bool, False),
)
environ.Env.read_env(BASE_DIR.parent / '.env')

RUN_DIR = BASE_DIR.parent / "run"
RUN_DIR.mkdir(parents=True, exist_ok=True)

DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY', default="django-insecure-asdfasdfasdf")
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])

ADMINS = [x.split(':') for x in env.list('ADMINS')]
MANAGERS = ADMINS

CSRF_COOKIE_SECURE = False if DEBUG else True
SESSION_COOKIE_SECURE = False if DEBUG else True

# Application definition

DJANGO_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]
THIRD_PARTY_APPS = [
    'crispy_forms',
    "crispy_bootstrap5",
    'django_htmx',
    'django_filters',
]
LOCAL_APPS = [
    'ddam.apps.DDAMAdminConfig',  # replaces 'django.contrib.admin'
    'ddam.core',
    'ddam.accounts',
    'ddam.organization',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

ROOT_URLCONF = 'ddam.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ddam.organization.context_processors.branding',
            ],
        },
    },
]

WSGI_APPLICATION = 'ddam.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': RUN_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_TZ = True

# Start on Monday
# This value is only used when not using format internationalization, or when a format cannot be found for the current locale.
FIRST_DAY_OF_WEEK = 1

FORMAT_MODULE_PATH = [
    'ddam.core.formats',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_URL = 'static/'
STATIC_ROOT = RUN_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = RUN_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'accounts.CustomUser'
LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'

# Email configs
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' if DEBUG else 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SUBJECT_PREFIX = env('EMAIL_SUBJECT_PREFIX')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
SERVER_EMAIL = DEFAULT_FROM_EMAIL

if env("EMAIL_HOST"):
    EMAIL_PORT = env("EMAIL_PORT")
    EMAIL_HOST = env("EMAIL_HOST")
    EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# DDAM SETTINGS
# Asset upload settings
DDAM_ASSET_UPLOAD_DIR = 'assets'
DDAM_ASSET_VALID_FILE_EXTENSIONS = ["svg", "jpg", "jpeg", "png", "webp"]  #  Removed "avif" for now, as Willow does not support it.
DDAM_ASSET_MAX_FILESIZE = env.int("DDAM_ASSET_MAX_FILESIZE") * 1000 * 1024 if env("DDAM_ASSET_MAX_FILESIZE", default=None) else 3000 * 1024  # Bytes

# Image renditions
DDAM_RENDITION_SIZE = (600, 300)
DDAM_RENDITION_ROOT = MEDIA_ROOT / 'renditions'


if env('AUTH_LDAP'):
    from .ldap import *
    # print("[i] AUTH_LDAP enabled via .env")
else:
    # print("[i] AUTH_LDAP disabled in .env")
    pass
