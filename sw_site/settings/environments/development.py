# from sw_site.settings.components import BASE_DIR, config

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = config('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CORS_ORIGIN_WHITELIST = (
    'localhost:8000',
    '127.0.0.1:8000',
    'localhost:8080',
    '127.0.0.1:8080',
)
