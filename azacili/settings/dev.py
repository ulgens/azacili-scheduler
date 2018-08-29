from .common import *


DEBUG = True
ALLOWED_HOSTS = ["*"]

SECRET_KEY = 'developer'

INSTALLED_APPS.insert(0, "sslserver")
