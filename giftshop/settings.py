import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = os.environ['ENVIRONMENT'] == 'debug'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'rest_framework',
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'giftshop.urls'

WSGI_APPLICATION = 'giftshop.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

TIME_ZONE = 'UTC'

USE_I18N = False

USE_TZ = True

REST_FRAMEWORK = {
    "DATE_FORMAT": "%d.%m.%Y",
    "DATE_INPUT_FORMATS": ["%d.%m.%Y"],
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'UNAUTHENTICATED_USER': None,
}
