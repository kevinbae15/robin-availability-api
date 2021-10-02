#
# These are settings for local development
#
from rest_framework.settings import api_settings
from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

SECRET_KEY = "71f!(pb*@k)7s7%0_lt(h^qs_*2tkmp_%$&)&9ihd60e8rm#i9"

# The necessary information for connecting to the
# the postgres database running on our local machine
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "mabledb",
        "USER": "mableadmin",
        "PASSWORD": "mableadmin",
        "HOST": "localhost",
        "PORT": "",
    }
}

DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
    "rest_framework.renderers.BrowsableAPIRenderer",
)

REST_FRAMEWORK = {"DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES}
