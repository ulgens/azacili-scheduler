import raven

from .common import *


DEBUG = False
ALLOWED_HOSTS = ["www.azacili.com"]

SECRET_KEY = config["django"]["secret_key"]

INSTALLED_APPS = [
    'raven.contrib.django.raven_compat',
] + INSTALLED_APPS

RAVEN_CONFIG = {
    'dsn': config["sentry"]["dsn"],
    'release': raven.fetch_git_sha(BASE_DIR),
}
