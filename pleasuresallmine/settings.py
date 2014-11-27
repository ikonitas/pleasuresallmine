import os
import socket


HOSTNAME = socket.gethostname()
if HOSTNAME == "edvinas-pc":
    SERVER_STATUS = "LOCAL"
    DEBUG = True
    COMPRESS_ENABLED = False
else:
    SERVER_STATUS = "LIVE"
    DEBUG = False
    COMPRESS_ENABLED = False


INTERNAL_IPS = ('192.168.1.29',)
DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False}

PROJECT_ROOT = os.path.join(os.path.dirname(__file__).decode('utf-8'), ('..'))

TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

ADMINS = (
    ('Edvinas Jurevicius', 'ikonitas@gmail.com'),
)

SERVER_EMAIL = ""

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pleasuresallminedb',                      # Or path to database file if using sqlite3.
        'USER': 'zatan',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-uk'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = PROJECT_ROOT + '/media'
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = PROJECT_ROOT + '/static/'
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_ROOT + '/pleasuresallmine/static',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'kgnpc!ya52x+oxcjo-$29nw37i_^4r5#p^&amp;uyu)z)ay$sd+p+l'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'baskets.middleware.SimpleCartMiddleware',
    #'core.middleware.StaffMember',
)

ROOT_URLCONF = 'pleasuresallmine.urls'

APPEND_SLASH = True

## Python dotted path to the WSGI application used by Django's runserver.
#WSGI_APPLICATION = 'pleasuresallmine.wsgi.application'

TEMPLATE_DIRS = (
    PROJECT_ROOT + '/templates/'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'debug_toolbar',
    'south',
    'sorl.thumbnail',
    'accounts',
    'automated_emails',
    'baskets',
    'categories',
    'core',
    'compressor',
    'deliveries',
    'filebrowser',
    'haystack',
    'infopages',
    'orders',
    'paypal.standard.ipn',
    'products',
    'search',
    'tinymce',
    'messages',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGIN_REDIRECT_URL = '/'
AUTH_PROFILE_MODULE = 'accounts.userprofile'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'accounts.email_auth.EmailBackend',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'baskets.context_processors.carts',
    'categories.context_processors.list_categories',
    'infopages.context_processors.list_infopages',
    'infopages.context_processors.list_infopages_menu',
    'messages.context_processors.promotion_messages',
    'deliveries.context_processors.deliveries',
    'products.context_processors.special_offers',
)


PAYPAL_RECEIVER_EMAIL = ''
PAYPAL_RETURN_URL = ''
PAYPAL_NOTIFY_URL = ''
PAYPAL_CANCEL_RETURN = ''
PAYPAL_PRIVATE_CERT = PROJECT_ROOT + ''
PAYPAL_PUBLIC_CERT = PROJECT_ROOT + ''
PAYPAL_CERT = PROJECT_ROOT + ''
PAYPAL_CERT_ID = ''

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""


HAYSTACK_SITECONF = 'pleasuresallmine.search_sites'
HAYSTACK_SEARCH_ENGINE = "whoosh"
HAYSTACK_WHOOSH_PATH = PROJECT_ROOT + '/whoosh/index'


TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'plugins': "spellchecker",
    'theme_advanced_buttons3_add': "|,spellchecker",
    'theme_advanced_toolbar_location': "top",
    'theme_advanced_toolbar_align': "left",
    'theme_advanced_buttons2': "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code,|,insertdate,inserttime,preview,|,forecolor,backcolor",
    'theme_advanced_buttons1': "save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,styleselect,formatselect,fontselect,fontsizeselect",
    'content_css': "/static/admin/css/tiny_mce.css,http://fonts.googleapis.com/css?family=Source+Sans+Pro",
}
