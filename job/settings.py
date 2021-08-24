"""
Django settings for job project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import django_heroku
from decouple import config
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'etdq)uvq=t0rc&ams5_ovn6w8bcwknjj0u97*(#n^(76x*+dr1'
SECRET_KEY=config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True 
DEBUG = config('DEBUG')

ALLOWED_HOSTS = ['172.17.2.127', '127.0.0.1','192.168.43.252']
# ALLOWED_HOSTS = config('ALLOWED_HOST')

# TWILIO_ACCOUNT_SID = 'AC723a890cf2f2811026ca352916d5b977'
# TWILIO_AUTH_TOKEN ='6f786b5fc935f4e24e99acbcf057d309'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'jobapp.apps.JobappConfig',
    'account.apps.AccountConfig',

    #3rd Party App
    'ckeditor',
    'taggit',
    'user_visit',
    'crispy_forms',
    'captcha',
    'smsapp',
    'widget_tweaks',
    'qrcode',
    'qr_code',
    
    
]
CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'user_visit.middleware.UserVisitMiddleware',
]

ROOT_URLCONF = 'job.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'template')],
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

WSGI_APPLICATION = 'job.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if config('MODE')== 'dev':
    DATABASES =  {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('PORT'),
    }
}
else:
   DATABASES = {
       'default': dj_database_url.config(
           default=config('DATABASE_URL')
       )
   }

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
# if config('MODE')=="dev":
#    DATABASES = {
#        'default': {
#            'ENGINE': 'django.db.backends.postgresql_psycopg2',
#            'NAME': config('DB_NAME'),
#            'USER': config('DB_USER'),
#            'PASSWORD': config('c'),
#            'HOST': config('DB_HOST'),
#            'PORT': '',
#        }
       
#    }
# # production





# Password validation


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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

AUTH_USER_MODEL = 'account.User'

# CKeditor Config
CKEDITOR_CONFIGS = {
    'default': {
        'width': '100%',
        'tabSpaces': 4,

    }
}


from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

AT_ENDPOINT_URL = "https://api.sandbox.africastalking.com/version1/messaging"

AT_API_KEY = ('a68f6931ea672ccd7f2eac764fdc92dd5938b1a7cf1e0e955c1bd15f98af05d5')


AT_USER_NAME = ('sandbox')

AT_FROM_VALUE = ('+254704099049')


# Activate Django-Heroku.
django_heroku.settings(locals())

GOOGLE_RECAPTCHA_SECRET_KEY ='6LcVGNEbAAAAAGKG4-pj9jy2EtwOlhR0QUqATcz_'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
