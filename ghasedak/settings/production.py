from ghasedak.settings.base import *

ALLOWED_HOSTS = ['*']
SECRET_KEY = env.str('DJANGO_SECRET_KEY')
DEBUG = True


DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('DB_NAME'),
        'USER': env.str('DB_USER'),
        'PASSWORD': env.str('DB_PASSWORD'),
        'HOST': env.str('DB_HOST'),
        'PORT': env.str('DB_PORT')

    }
}