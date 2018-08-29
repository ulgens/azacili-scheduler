import raven

from .common import *


DEBUG = False
ALLOWED_HOSTS = ["www.azacili.com"]

SECRET_KEY = config["django"]["secret_key"]

INSTALLED_APPS.insert(0, 'raven.contrib.django.raven_compat')
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

RAVEN_CONFIG = {
    'dsn': config["sentry"]["dsn"],
    'release': raven.fetch_git_sha(BASE_DIR),
}
