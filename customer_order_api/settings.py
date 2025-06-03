from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-6k@4vy!e31i-k9ger!y9z=^0zt2j!)mt3%#b3d+ub_t(0eov')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'mptt',
    'mozilla_django_oidc',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'mozilla_django_oidc.middleware.SessionRefresh',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'customer_order_api.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'customer_order_api.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'mozilla_django_oidc': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'core': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        '': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

AUTHENTICATION_BACKENDS = [
    'mozilla_django_oidc.auth.OIDCAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# OIDC settings
OIDC_RP_CLIENT_ID = config('OIDC_RP_CLIENT_ID', default='vYAuFF9NqJUcVFkt0xFmyRxy0Rzkb8vI')
OIDC_RP_CLIENT_SECRET = config('OIDC_RP_CLIENT_SECRET', default='R7buwtiSOi5KALVNY4AXszTbMYJmSY8qrXp5FXY0QByW03oZ6GKrg5q_GHr22ceI')
OIDC_OP_AUTHORIZATION_ENDPOINT = 'https://customerorder.us.auth0.com/authorize'
OIDC_OP_TOKEN_ENDPOINT = 'https://customerorder.us.auth0.com/oauth/token'
OIDC_OP_USER_ENDPOINT = 'https://customerorder.us.auth0.com/userinfo'
OIDC_OP_JWKS_ENDPOINT = 'https://customerorder.us.auth0.com/.well-known/jwks.json'
OIDC_OP_LOGOUT_URL = 'https://customerorder.us.auth0.com/v2/logout'
OIDC_RP_SIGN_ALGO = 'RS256'
OIDC_RP_SCOPES = 'openid profile email'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'http://localhost:8000'
OIDC_EXEMPT_URLS = ['/api/']
OIDC_AUTHENTICATE_CLASS = 'mozilla_django_oidc.views.OIDCAuthenticationRequestView'
OIDC_CALLBACK_CLASS = 'mozilla_django_oidc.views.OIDCAuthenticationCallbackView'

# Authentication settings
LOGIN_URL = '/oidc/authenticate/'

# Auth0 logout configuration
USE_AUTH0_LOGOUT = False  # Disable Auth0 logout until configuration is fixed


# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_COOKIE_SECURE = not DEBUG  # False in DEBUG mode
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_SAVE_EVERY_REQUEST = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'mozilla_django_oidc.contrib.drf.OIDCAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='wenbusale383@gmail.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='zgku hxbz qyyq wuxd')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='wenbusale383@gmail.com')
ADMIN_EMAIL = config('ADMIN_EMAIL', default='wenbusale383@gmail.com')

AFRICASTALKING_USERNAME = config('AFRICASTALKING_USERNAME', default='sandbox')
AFRICASTALKING_API_KEY = config('AFRICASTALKING_API_KEY', default='atsk_d79fb34dbb23b82fe6c4f326dbf70891423f4f5f9aec67d0645b2767f3e51a82290ecd6a')

TESTING = False