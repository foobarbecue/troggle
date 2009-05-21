import os
import time
import settings
os.environ['PYTHONPATH'] = settings.PYTHON_PATH
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.core import management
from django.db import connection
from django.contrib.auth.models import User
from django.http import HttpResponse

logfile=settings.LOGFILE

def reload_db():
    cursor = connection.cursor()
    cursor.execute("drop database %s" % settings.DATABASE_NAME)
    cursor.execute("create database %s" % settings.DATABASE_NAME)
    cursor.execute("ALTER DATABASE %s CHARACTER SET=utf8" % settings.DATABASE_NAME)
    cursor.execute("USE %s" % settings.DATABASE_NAME)
    management.call_command('syncdb', interactive=False)
    user = User.objects.create_user('m', 'm@m.com', 'm')
    user.is_staff = True
    user.is_superuser = True
    user.save()

def make_dirs():
    """Make directories that troggle requires"""
    #should also deal with permissions here.
    if not os.path.isdir(settings.PHOTOS_ROOT):
        os.mkdir(settings.PHOTOS_ROOT)

def import_cavetab():
    import parsers.cavetab
    parsers.cavetab.LoadCaveTab()

def import_people():
    import parsers.people
    parsers.people.LoadPersonsExpos()

def import_logbooks():
    logfile.write('\nBegun importing logbooks at ' + time.asctime() +'\n'+'-'*60)
    import parsers.logbooks
    parsers.logbooks.LoadLogbooks()

def import_survex():
    import parsers.survex
    parsers.survex.LoadAllSurvexBlocks()

def import_QMs():
    import parsers.QMs

def import_surveys():
    import parsers.surveys
    parsers.surveys.parseSurveys(logfile=settings.LOGFILE)

def reset():
    """ Wipe the troggle database and import everything from legacy data
    """
    reload_db()
    make_dirs()
    import_cavetab()
    import_people()
    import_logbooks()
    import_survex()
    import_QMs()
    import_surveys()

def export_cavetab():
    from export import tocavetab
    outfile=file(os.path.join(settings.EXPOWEB, "noinfo", "CAVETAB2.CSV"),'w')
    tocavetab.writeCaveTab(outfile)
    outfile.close()
    


    
    