from ghasedak.settings.base import *

SECRET_KEY = "django-insecure-xf787mwonq2s5*i%npk!-tqu8qgsn_g0fe*%vgsrfel7zvr_s1"
ALLOWED_HOSTS = ['*']
DEBUG = True

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ghasedak',
        'USER': 'ghasedak',
        'PASSWORD': 'Password',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}


