from .base import *

SECRET_KEY = '_02@*fi=%habjr*f0n$é-r#rzt%g-n8)!0of%q+2ukpbyza$%e'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
