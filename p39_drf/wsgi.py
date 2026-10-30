"""WSGI config for p39_drf project."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p39_drf.settings')

application = get_wsgi_application()