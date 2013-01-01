from base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'finance_website',
        'USER': 'webuser',
        'PASSWORD': 'webpass',
        'HOST': '',
        'PORT': ''
    }
}

DEBUG = True