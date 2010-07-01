import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from datalogging.models import *
from core.models import Cave

from matplotlib import pyplot as plt
from datetime import datetime, date
from django.db.models import Count, Q

from scipy import signal
from numpy import corrcoef
import scipy

from datalogging.data_plot import crop_date_range

caves_with_timeseries=(
    Cave.objects.get(official_name__icontains='temp'),
    Cave.objects.get(slug__icontains='wind'),
    Cave.objects.get(slug__icontains='mouse'),
    Cave.objects.get(slug__icontains='2009-02'),
    Cave.objects.get(slug='heroin'),
    Cave.objects.get(slug__icontains='heroine'),
    Cave.objects.get(slug__icontains='shooting'),
    Cave.objects.get(slug__icontains='derodome'),
    Cave.objects.get(slug__icontains='kachina'),
#    Cave.objects.get(slug_icontains='helo'),
    Cave.objects.get(slug__icontains='hut'),
    Cave.objects.get(slug__icontains='warren'),
    )

#tses=Timeseries.objects.filter(logbook_entry__cave__in=caves_with_timeseries,data_type__in=('air_deg_c','w_speed','w_azmth')).exclude(location_in_cave__icontains='panel').exclude(pk__in=[13,14,16,31,7])
ts_pk_list=[34,33,35,4,11,9,8,3,12,6,29,30,37,38]
tses=[Timeseries.objects.get(pk=prim_key) for prim_key in ts_pk_list]

def correl_array(date_range, tses=tses):
    print "specifed date range is: %s to %s" % date_range    
    data=[]
    labels=[]
    for ts in tses:
        print "detected range for ts %s is: %s to %s" % (ts.pk, ts.auto_date_range()[0],ts.auto_date_range()[1])
        data.append(list(ts.datapoint_set.values_list('value',flat=True)))
        labels.append('%s: %s'%(ts.pk, ts.logbook_entry.cave))

    # Resample the data so that all timeseries have the same
    # number of elements. Use the lowest sample rate of all
    # timeseries.
    n=min([len(ts) for ts in data])
    x = 0    
    for ts in data:
        data[x]=signal.resample(data[x], n)
        x+=1

    data=scipy.asarray(data)
    data=data.transpose()
    return labels, stats.corrcoef(data)


def correl(ts1, ts2, date_range):
    
    
#    for ts in (ts1, ts2):
        # check that winddir is complete within date_range
#        cropped_dr=crop_date_range(date_range, ts)
#        if date_range!=cropped_dr:
#            print 'Cropping %s to %s' % (date_range, cropped_dr)
#            date_range=cropped_dr

    #sanity check on date ranges
    print "specifed date range is: %s to %s" % date_range
    print "detected range for ts1 is %s to %s" % ts1.auto_date_range()
    print "detected range for ts2 is %s to %s" % ts2.auto_date_range()
    ts1filtd=ts1.datapoint_set.filter(time__range=date_range)
    ts2filtd=ts2.datapoint_set.filter(time__range=date_range)
    n=min(ts1filtd.count(), ts2filtd.count())
    ts1filtd=signal.resample(list(ts1filtd.values_list('value',flat=True)), n)
    ts2filtd=signal.resample(list(ts2filtd.values_list('value',flat=True)), n)

    ans=stats.corrcoef(ts1filtd, ts2filtd)

    return ans
