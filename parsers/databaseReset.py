import os
os.environ['PYTHONPATH'] = 'c:\djangoprojects\verfification'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.core import management
from django.db import connection

cursor = connection.cursor()
cursor.execute("drop database verification")
cursor.execute("create database verification")
cursor.execute("use verification")
management.call_command('syncdb')
from django.contrib.auth.models import User
user = User.objects.create_user('m', 'm@m.com', 'm')
user.is_staff = True
user.is_superuser = True
user.save()
#management.call_command('runserver')
