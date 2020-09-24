from .common import *


DEBUG = True
ALLOWED_HOSTS = ["*"]

SECRET_KEY = 'developer'

INSTALLED_APPS = [
    "django_migration_vis",
    "debug_toolbar",
    "sslserver",
] + INSTALLED_APPS

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

INTERNAL_IPS = ("127.0.0.1", )
