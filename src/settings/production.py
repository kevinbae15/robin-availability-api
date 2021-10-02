# settings for the deployed environment which will have different database connection

from .base import *
import dj_database_url

DEBUG = False
AUTH_SWITCH = True
EMAIL_SWITCH = True
FORCE_HTTPS = True
SECRET_KEY = os.environ.get("SECRET_KEY")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


ALLOWED_HOSTS = ["api.textbookexchangenetwork.com", "localhost", "127.0.0.1"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "127.0.0.1:11211",
    }
}

EMAIL_LINK = "https://email.textbookexchangenetwork.com/emailingService"
AUTH_HOST = "https://auth.textbookexchangenetwork.com/authService/validateJWT/"

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": "5432",
    }
}

# Logging module configurations
LOGGING["loggers"]["ten.server"]["level"] = "INFO"
LOGGING["handlers"]["console"]["level"] = "INFO"
LOGGING["formatters"]["verbose"][
    "format"
] = "API   %(levelname)-8s %(module)-12s %(lineno)-4d %(process)d: %(message)s"
LOGGING["formatters"]["django.server"]["format"] = "API   %(levelname)-32s: %(message)s"
