from decouple import config

ghasedak_settings = config('GHASEDAK_SETTINGS', default='').lower()

if ghasedak_settings == 'production':
    from .production import *
elif ghasedak_settings == 'testing':
    from .testing import *
else:
    from .development import *
