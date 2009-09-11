import os
import time
import settings
os.environ['PYTHONPATH'] = settings.PYTHON_PATH
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.core import management
from django.db import connection
from django.contrib.auth.models import User
from django.http import HttpResponse



def reload_db():
    cursor = connection.cursor()
    cursor.execute("drop database %s" % settings.DATABASE_NAME)
    cursor.execute("create database %s" % settings.DATABASE_NAME)
    cursor.execute("ALTER DATABASE %s CHARACTER SET=utf8" % settings.DATABASE_NAME)
    cursor.execute("USE %s" % settings.DATABASE_NAME)
    management.call_command('syncdb', interactive=False)
    user = User.objects.create_user('expo', 'goatchurch@gmail.com', 'gosser')
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
    print "importing cavetab"
    parsers.cavetab.LoadCaveTab()

def import_people():
    import parsers.people
    parsers.people.LoadPersonsExpos()

def import_logbooks():
    # The below line was causing errors I didn't understand (it said LOGFILE was a string), and I couldn't be bothered to figure
    # what was going on so I just catch the error with a try. - AC 21 May
    try:
        settings.LOGFILE.write('\nBegun importing logbooks at ' + time.asctime() +'\n'+'-'*60)
    except:
        pass
    
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

def import_surveyscans():
    import parsers.surveys
    parsers.surveys.LoadListScans(settings.SURVEY_SCANS)

    
def import_descriptions():
    import parsers.descriptions
    parsers.descriptions.getDescriptions()

def parse_descriptions():
    import parsers.descriptions
    parsers.descriptions.parseDescriptions()
    parsers.descriptions.parseDescriptionsOnCaveObjects()

def import_tunnelfiles():
    import parsers.surveys
    parsers.surveys.LoadTunnelFiles(settings.TUNNEL_DATA)


def reset():
    """ Wipe the troggle database and import everything from legacy data
    """
    reload_db()
    make_dirs()
    import_cavetab()
    import_people()
    import_surveyscans()
    import_survex()
    import_logbooks()
    import_QMs()
    import_tunnelfiles()
    #import_surveys()
    import_descriptions()
    parse_descriptions()

def resetdesc():
    """ Wipe the troggle database and import descriptions
    """
    import core.models
    for desc in core.models.CaveDescription.objects.all():
        desc.delete()
    import_descriptions()
    parse_descriptions()
    
def export_cavetab():
    from export import tocavetab
    outfile=file(os.path.join(settings.EXPOWEB, "noinfo", "CAVETAB2.CSV"),'w')
    tocavetab.writeCaveTab(outfile)
    outfile.close()

if __name__ == "__main__":
    import core.models
    import sys
    if "desc" in sys.argv:
        resetdesc()
    elif "scans" in sys.argv:
        import_surveyscans()
    elif "tunnel" in sys.argv:
        import_tunnelfiles()
    elif "reset" in sys.argv:
        reset()
    elif "survex" in sys.argv:
        management.call_command('syncdb', interactive=False)  # this sets the path so that import settings works in import_survex
        import_survex()
    
    elif "logbooks" in sys.argv:
        management.call_command('syncdb', interactive=False)  # this sets the path so that import settings works in import_survex
        import_logbooks()
    else:
        print "Do 'python databaseReset.py reset'"


    
    
