
import environ
import os
from datetime import timedelta

env = environ.Env()
environ.Env.read_env()

from pathlib import Path
from mailjet_rest import Client

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'church.middleware.Church.check_authenticated_user',
    # 'church.middleware.ClassBasedMiddlewareWhiteListViews.ChurchAuthMiddlewareWhiteList',
    'church.middleware.ClassBasedMiddleware.ChurchAuthMiddleware',
    'church.middleware.ChurchSetup.church_setup_middleware',
]
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',
    'django_resized',
    'sorl.thumbnail',
    'crispy_forms',
    'dashboard',
    'membership.apps.MembershipConfig',
    'welfare',
    'donations',
    'groups',
    'pledges',
    'cevents',
    'levy',
    'announcement',
    'offerings',
    'church_services',
    'projects',
    'expenses',
    'accounts',
    'church',
    'cashbook',
    # 'django_countries'
]

# CRISPY_TEMPLATE_PACK = 'bootstrap4'
ROOT_URLCONF = 'churchclicks.urls'
DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


DATETIME_INPUT_FORMATS = [
        '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
]

WSGI_APPLICATION = 'churchclicks.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

X_FRAME_OPTIONS = '*'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'churchflow',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5433',
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
AUTH_USER_MODEL = 'accounts.User'

LOGIN_REDIRECT_URL = 'dashboard/'
LOGOUT_REDIRECT_URL = '/'

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# CUSTOM SETTINGS

EMAIL_CONFIRMATION_PERIOD_DAYS = 7
SIMPLE_EMAIL_CONFIRMATION_PERIOD = timedelta(days=EMAIL_CONFIRMATION_PERIOD_DAYS)
SIMPLE_EMAIL_CONFIRMATION_KEY_LENGTH = 16
SIMPLE_EMAIL_CONFIRMATION_EMAIL_ADDRESS_MODEL = 'helloralph@vineboard.com'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Directory where uploaded media is saved.
# MEDIA_URL = '/media/' # Public URL at the browser
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field


# mailjet settings_
mailjet = Client(auth=(env('MAILJET_API_KEY'), env('MAILJET_SECRET_KEY')), version='v3.1')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'