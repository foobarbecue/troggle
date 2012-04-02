from localsettings import EXPOWEB #inital localsettings call so that urljoins work
import os
import urlparse
# Django settings for troggle project.

DEBUG = False
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
#PHOTOS_ROOT = os.path.join(EXPOWEB, 'photos')

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

TEMPLATE_CONTEXT_PROCESSORS = ( "django.core.context_processors.auth", "core.context.troggle_context", ) 

LOGIN_REDIRECT_URL = '/'

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'middleware.SmartAppendSlashMiddleware'
)

ROOT_URLCONF = 'urls'

ACCOUNT_ACTIVATION_DAYS=3

AUTH_PROFILE_MODULE = 'core.person'

QM_PATTERN="\[\[\s*[Qq][Mm]:([ABC]?)(\d{4})-(\d*)-(\d*)\]\]"

from localsettings import * #localsettings needs to take precedence. Call it to override any existing vars.
