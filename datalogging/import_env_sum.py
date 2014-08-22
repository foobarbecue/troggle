from django.conf import settings
from datalogging.models import *
from core.models import *
import csv, os, itertools
from django.template.defaultfilters import slugify
import datetime

data_type_dict={'m/s\n':'w_speed',
                'V\n':'v',
                'A\n':'a',
                'C\n':'air_deg_c',
                'uR\n':'ur',
                'ppm\n':'co2_ppmv',
                'Dir\n':'w_azmth',
                'hPa\n':'press_hpa',
                }

def date_generator(startDate,reverse=False):
    """
    Returns a 
    """
    from_date = startDate
    while True:
        yield from_date
        if reverse:
            from_date = from_date - datetime.timedelta(days=1)
        else:
            from_date = from_date + datetime.timedelta(days=1)

def import_env_summary(dat_path, verbose=False):
    env_sum=open(dat_path, 'r')
#    env_sum=csv.reader(env_sum, delimiter=' ')
    ts=0
    for line in env_sum:
        try:
            #if there is actually data in this line
	    line=line.split(' ')
            if len(line)>=5 and float(line[4])!='0.0':
                if ts==0 or ts.location_in_cave!=line[0]:
                    try:
                        ts=Timeseries.objects.get(location_in_cave=line[0])
                    except Timeseries.DoesNotExist:
                        cave_slug=slugify(line[0])
                        cave, created=Cave.objects.get_or_create(official_name=line[0][0:3], defaults={'type':'unknown', 'slug':cave_slug})
                        lbe_title='%s environmental' % line[0]
                        lbe, created=LogbookEntry.objects.get_or_create(
                                                       title=lbe_title,
                                                       date=line[1],
                                                       text='From env_summary.dat at %s' % dat_path,
                                                       slug=slugify(lbe_title), cave=cave)

                        ts=Timeseries(sensor=EquipmentItem.objects.get(pk=5), location_in_cave=line[0], data_type=data_type_dict[line[5]], logbook_entry=lbe)
                        ts.save()
                new_dp, created=DataPoint.objects.get_or_create(parent_timeseries=ts, time='%s %s' % (line[1],line[2]), defaults={'value':line[4],})
                if verbose and created:
                    print 'created %s' % new_dp
                elif verbose:
                    print '%s already existed' % new_dp
        except:
            print 'ignoring %s' % line
    env_sum.close()

def import_all_env_summaries():
    """
    Attempts to import all env_summary.dat files in the directory tree by
    walking the tree. Superseeded by import_daily_env_summaries(), which is
    a better way of doing it.
    """
    for yy in range(1,11):
        yearpaths='/data/Erebus/Erebus_%s/Archive' % ('%02d' % yy)[-2:]
    print 'read paths, starting to read files in to database'
    for yearpath in yearpaths:
        import_daily_env_summaries(yearpath)

def import_daily_env_summaries(startDate,numDays,reverse=False, verbose=False):
    """
    Reads in the env_summary.dat files for each day going backwards in time
    starting at startDate.
    """
    dates=itertools.islice(date_generator(startDate,reverse),numDays)
    for day in dates:
        filepath=day.strftime('/data/Erebus/Erebus_%y/Archive/%Y%m%d/env_summary.dat')
        print 'About to process %s' % filepath
        try:
            import_env_summary(filepath, verbose=verbose)
        except IOError:
            print day.strftime('No .dat file for %Y%m%d')

#def import_daily_env_summaries(yearpath):
#    for root, dirs, files in os.walk(yearpath):
#        if 'env_summary.dat' in files:
#            filepath=os.path.join(root,'env_summary.dat')
#            if len(filepath)==55:
#                print 'About to process %s' % filepath
#                import_dat_file(filepath)

