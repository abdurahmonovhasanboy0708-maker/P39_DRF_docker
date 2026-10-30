"""ASGI config for p39_drf project."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p39_drf.settings')

application = get_asgi_application()