import os
from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'ci.sqlite3',
    }
}

# Evitar problemas con logs
LOGGING['handlers']['file']['filename'] = os.path.join(BASE_DIR, 'ci.log')
