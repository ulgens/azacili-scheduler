from .common import *


DEBUG = True
ALLOWED_HOSTS = ["*"]

SECRET_KEY = 'developer'

INSTALLED_APPS.insert(0, "sslserver")
INSTALLED_APPS.append("debug_toolbar")

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

INTERNAL_IPS = ("127.0.0.1", )
