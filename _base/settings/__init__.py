from decouple import config

kaftaar_settings = config('GHASEDAK_SETTINGS', default='').lower()

if kaftaar_settings == 'production':
    from .production import *
elif kaftaar_settings == 'testing':
    from .testing import *
else:
    from .development import *
