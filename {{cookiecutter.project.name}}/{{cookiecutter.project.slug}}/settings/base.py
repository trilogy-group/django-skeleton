"""
Django settings for {{cookiecutter.project.slug}} project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from email.policy import default
from decouple import config
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default="django-insecure-976gl!=dg_9^upz%)7mbgzi78@d&nprrwk38psuh&zb_716cwn")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',

    {%- if cookiecutter.authentication.rest is defined %}
    "rest_framework",
    "rest_framework.authtoken",
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    {%- endif %}

    {%- if cookiecutter.authentication.social is defined %}
    'allauth.socialaccount',
    'social_django',
    'rest_social_auth',
    {% endif %}
    'corsheaders',
    
    {%- if cookiecutter.documentation.swagger is defined %}
    'drf_yasg',
    {% endif %}
    # 'health_check',
    {%- if cookiecutter.prometheus is defined %}
    # 'django_prometheus',
    {%- endif %}
    # {%- if cookiecutter.worker.django_q is defined %}
    # 'django-q',
    # {%- endif %}
    
    "accounts",
]

MIDDLEWARE = [
    {%- if cookiecutter.prometheus is defined %}
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    {%- endif %}
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.disable_csrf.DisableCSRF',
    {%- if cookiecutter.prometheus is defined %}
    'django_prometheus.middleware.PrometheusAfterMiddleware'
    {%- endif %}
]

ROOT_URLCONF = '{{cookiecutter.project.slug}}.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = '{{cookiecutter.project.slug}}.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SOCIAL_AUTH_JSONFIELD_ENABLED = True

# ---- allauth and rest-auth settings ----
SITE_ID = 1
AUTH_USER_MODEL = "accounts.User"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'

AUTHENTICATION_BACKENDS = (
    {%- if cookiecutter.authentication.social is defined %}
    {%- if cookiecutter.authentication.social.google is defined %}
    'social_core.backends.google.GoogleOAuth2',
    {%- endif %}
    {%- if cookiecutter.authentication.social.github is defined %}
    'social_core.backends.github.GithubOAuth2',
    {%- endif %}
    {%- if cookiecutter.authentication.social.aws_cognito is defined %}
    'social_core.backends.cognito.CognitoOAuth2',
    {%- endif %}
    {%- endif %}
    # and maybe some others ...
    'django.contrib.auth.backends.ModelBackend',
    # allauth specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

{%- if cookiecutter.authentication.social is defined %}
{%- if cookiecutter.authentication.social.google is defined %}
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '{{ cookiecutter.authentication.social.google.oauth2_key }}'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '{{ cookiecutter.authentication.social.google.oauth2_secret }}'
REST_SOCIAL_OAUTH_ABSOLUTE_REDIRECT_URI = '{{ cookiecutter.authentication.social.google.oauth_absolute_redirect_uri}}'

SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]
{%- endif %}
{%- if cookiecutter.authentication.social.github is defined %}
SOCIAL_AUTH_GITHUB_KEY = config('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = config('SOCIAL_AUTH_GITHUB_SECRET')
REST_SOCIAL_OAUTH_ABSOLUTE_REDIRECT_URI = config('REST_SOCIAL_OAUTH_ABSOLUTE_REDIRECT_URI')
{%- endif %}
{%- if cookiecutter.authentication.social.aws_cognito is defined %}
SOCIAL_AUTH_COGNITO_KEY = config('SOCIAL_AUTH_COGNITO_KEY')
SOCIAL_AUTH_COGNITO_SECRET = config('SOCIAL_AUTH_COGNITO_SECRET')
SOCIAL_AUTH_COGNITO_POOL_DOMAIN = config('SOCIAL_AUTH_COGNITO_POOL_DOMAIN')
{%- endif %}
{%- endif %}

{%- if cookiecutter.worker.celery is defined %}
# CELERY
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_EVENT_QUEUE_PREFIX = 'sakshammittal'
{%- endif %}


{%- if cookiecutter.email.sendgrid is defined %}
EMAIL_URL = os.environ.get("EMAIL_URL")
SENDGRID_USERNAME = os.environ.get("SENDGRID_USERNAME")
SENDGRID_PASSWORD = os.environ.get("SENDGRID_PASSWORD")
if not EMAIL_URL and SENDGRID_USERNAME and SENDGRID_PASSWORD:
    EMAIL_URL = "smtp://%s:%s@smtp.sendgrid.net:587/?tls=True" % (
        SENDGRID_USERNAME,
        SENDGRID_PASSWORD,
    )
{%- endif %}

{%- if cookiecutter.email.default is defined %}
# EMAIL
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_USE_SSL = config('EMAIL_USE_SSL')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
{%- endif %}
