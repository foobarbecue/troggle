from datalogging.models import *
from core.models import *
from django.conf import settings
import csv
from django.template.defaultfilters import slugify

data_type_dict={'m/s\n':'w_speed',
                'V\n':'v',
                'A\n':'a',
                'C\n':'air_deg_c',
                'uR\n':'ur',
                'ppm\n':'co2_ppmv',
                'Dir\n':'w_azmth',
                'hPa\n':'press_hpa',
                }

def import_dat_file(dat_path):
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
#                if created:
#                    print 'created %s' % new_dp
        except:
            print 'ignoring %s' % line
