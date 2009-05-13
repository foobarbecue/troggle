import os
import settings
os.environ['PYTHONPATH'] = settings.PYTHON_PATH
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.core import management
from django.db import connection

cursor = connection.cursor()
cursor.execute("drop database %s" % settings.DATABASE_NAME)
cursor.execute("create database %s" % settings.DATABASE_NAME)
cursor.execute("ALTER DATABASE %s CHARACTER SET=utf8" % settings.DATABASE_NAME)
cursor.execute("USE %s" % settings.DATABASE_NAME)
management.call_command('syncdb')
from django.contrib.auth.models import User
user = User.objects.create_user('m', 'm@m.com', 'm')
user.is_staff = True
user.is_superuser = True
user.save()

import parsers.cavetab
import parsers.logbooks
import parsers.QMs
import parsers.survex
import parsers.surveys