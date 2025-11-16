# !Configuracion global del sistema
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/


SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', 'False') == 'True'


CSRF_TRUSTED_ORIGINS = [
    'https://*.ngrok-free.app', 
    'https://*.ngrok-free.dev', 
]

ALLOWED_HOSTS = ['127.0.0.1', 'localhost','.ngrok-free.app','*']

# Application definition

# !DEFINIR LAS APLICACIONES
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'store.apps.StoreConfig',
    'core',
    'control',
    'cart',
    'quote',
    'accounts',
    'coment',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'sipstore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.totales_carrito',
            ],
        },
    },
]

WSGI_APPLICATION = 'sipstore.wsgi.application'


# !Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'SIPstoreDB',
        'USER': 'root',
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}




# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/


TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

LANGUAGE_CODE = 'es'

LANGUAGES = [
    ('es', 'Español'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# !Archivos estáticos (CSS, JS, imágenes)
STATIC_URL = 'static/'

# !Carpeta statica Global
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# !Media para las imagenes
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# !API KEYS

MERCADOPAGO_PUBLIC_KEY = os.getenv('MERCADOPAGO_PUBLIC_KEY')

MERCADOPAGO_ACCESS_TOKEN = os.getenv('MERCADOPAGO_ACCESS_TOKEN')

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "apikey"  # palabra literal
EMAIL_HOST_PASSWORD = os.getenv("SENDGRID_API_KEY")
DEFAULT_FROM_EMAIL = "tonopanelessip@gmail.com"


# ! LOGIN Y LOGOUT

LOGIN_URL = 'login' 

LOGIN_REDIRECT_URL = 'control'

LOGOUT_REDIRECT_URL = 'logged_out_confirm'

AUTH_USER_MODEL = 'accounts.CustomUser'

PASSWORD_RESET_TTL = 120