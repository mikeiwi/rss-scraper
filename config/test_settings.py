import logging

from .settings import *  # NOQA

logging.disable(logging.CRITICAL)


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "HOST": "db",
        "PORT": 5432,
    }
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
DEBUG = False
TEMPLATE_DEBUG = False

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]


class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

IGNORE_NOTI_ERRORS = False
