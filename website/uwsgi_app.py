import sys
import os

sys.path.append(os.path.abspath("{0}/{1}".format(
    os.path.dirname(__file__),
    "finance"
)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi

app = django.core.handlers.wsgi.WSGIHandler()