from localsettings import *
import os
import urlparse
# Django settings for troggle project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-uk'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/troggle/media-admin/'
PHOTOS_ROOT = os.path.join(EXPOWEB, 'photos')

MEDIA_URL = urlparse.urljoin(URL_ROOT , '/site_media/')
SURVEYS_URL = urlparse.urljoin(URL_ROOT , '/survey_scans/')
PHOTOS_URL  = urlparse.urljoin(URL_ROOT , '/photos/')
SVX_URL = urlparse.urljoin(URL_ROOT , '/survex/')

APPEND_SLASH = False
SMART_APPEND_SLASH = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'a#vaeozn0)uz_9t_%v5n#tj)m+%ace6b_0(^fj!355qki*v)j2'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#   'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = ( "django.core.context_processors.auth", "expo.context.settings_context", ) 

LOGIN_REDIRECT_URL = '/'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'troggle.middleware.SmartAppendSlashMiddleware'
)

ROOT_URLCONF = 'troggle.urls'

ACCOUNT_ACTIVATION_DAYS=3

AUTH_PROFILE_MODULE = 'expo.person'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.redirects',
    #'troggle.photologue',
    #'troggle.reversion',
    #'django_evolution',
    'troggle.registration',
    'troggle.profiles',
    'troggle.expo',
    'troggle.imagekit', 
)