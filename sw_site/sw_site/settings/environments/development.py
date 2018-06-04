from sw_site.settings.components import BASE_DIR, config

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fx)pch!nnzo-5ng@q04fi6v0c0h&q#&^1$tf(@zdy%618tdeor'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
