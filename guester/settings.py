
from datetime import timedelta
import os
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = '-uda&r(n#74s#xbbqjg-n-3-e&41w%dfxb=yt(+^60=)2$@k7n'

DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = False


INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'registration',
    'el_pagination',
    'rest_framework',
    'corsheaders',
    'mailqueue',
    'drf_yasg',

    'django.contrib.gis',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'brands',
    'customers',
    'dishes',
    'general',
    'main',
    'shops',
    'staffs',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = 'guester.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.main_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'guester.wsgi.application'

GDAL_LIBRARY_PATH = ""



DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}



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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True



MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_URL = '/static/'
STATICFILES_DIRS = (BASE_DIR / 'static',)
STATIC_ROOT = (BASE_DIR / 'static'/ 'static')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = '/app/accounts/login/'
LOGOUT_URL = '/app/accounts/logout/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/app/accounts/login/'


EL_PAGINATION_PREVIOUS_LABEL = "< &nbsp;Previous"
EL_PAGINATION_NEXT_LABEL = "Next &nbsp;>"
EL_PAGINATION_USE_NEXT_PREVIOUS_LINKS = True
EL_PAGINATION_DEFAULT_CALLABLE_EXTREMES = 1
EL_PAGINATION_DEFAULT_CALLABLE_AROUNDS = 1

PASSWORD_ENCRYPTION_KEY = 'a54MqS4Re_tP6nlVYX6fBBAc025sztJw6URlW35vxCY='

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=210),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=730),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

VERSATILEIMAGEFIELD_SETTINGS = {
    'cache_length': 2592000,
    'cache_name': 'versatileimagefield_cache',
    'jpeg_resize_quality': 70,
    'sized_directory_name': '__sized__',
    'filtered_directory_name': '__filtered__',
    'placeholder_directory_name': '__placeholder__',
    'create_images_on_demand': True,
    'image_key_post_processor': None,
    'progressive_jpeg': False
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'info@tegain.com'
EMAIL_HOST_PASSWORD = '!@#infteg907'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'info@tegain.com'
DEFAULT_BCC_EMAIL = 'info@tegain.com'
DEFAULT_REPLY_TO_EMAIL = 'info@tegain.com'
