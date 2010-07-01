#log# Automatic Logger file. *** THIS MUST BE THE FIRST LINE ***
#log# DO NOT CHANGE THIS LINE OR THE TWO BELOW
#log# opts = Struct({'__allownew': True, 'logfile': 'correlation_usage.py'})
#log# args = []
#log# It is safe to make manual edits below here.
#log#-----------------------------------------------------------------------
from datalogging import data_plot
from core.models import *
_ip.magic("logstart ")
_ip.magic("logstop ")
_ip.magic("logstart correlation_usage.py")

from datalogging.models import Timeseries 
c0902=Timeseries.objects.filter(logbook_entry__cave__slug='2009-02')
c0902
c0902=c0902[0]
wdir=Timeseries.objects.filter(data_type='w_azmth')[1]
wdir
from datetime import datetime
date_range=(datetime.date(2009,12,18),datetime.date(2010,01,02))
date_range=(datetime(2009,12,18),datetime(2010,01,02))
q
from datalogging import correl_charts 
correl(c0902, wdir, date_range)
correl_charts.correl(c0902, wdir, date_range)
reload(correl_charts)
correl_charts.correl(c0902, wdir, date_range)
reload(correl_charts)
correl_charts.correl(c0902, wdir, date_range)
reload(correl_charts)
correl_charts.correl(c0902, wdir, date_range)
correl_charts.correl(c0902, wdir, date_range)
reload(correl_charts)
reload(correl_charts)
correl_charts.correl(c0902, wdir, date_range)
reload(correl_charts)
correl_charts.correl(c0902, wdir, date_range)
from scipy import stats
#? stats.corrcoef 
res=correl_charts.correl(c0902, wdir, date_range)
res.transpose 
res.transpose()
(4, *(3,4))
(4, expand(3,4))
tses=Timeseries.objects.filter(logbook_entry__cave__in=caves_with_timeseries,data_type__in=('air_deg_c','w_speed','w_azmth')).exclude(location_in_cave__icontains='panel')
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
tses=Timeseries.objects.filter(logbook_entry__cave__in=caves_with_timeseries,data_type__in=('air_deg_c','w_speed','w_azmth')).exclude(location_in_cave__icontains='panel')
tses.count()
for each in tses:
    print each.logbook_entry.cave
    
stats.corrcoef(tses.values_list('value'))
z=[1,4,2,3,4]
[print x for y in z]
[print(x) for y in z]
[print(y) for y in z]
[print('y') for y in z]
[ print('y') for y in z ]
print('y')
help(docs)
[y for x in z]
[x for x in z]
res=[ts.datapoint_set.all.values_list('value',flat=True) for ts in tses]
res=[ts.datapoint_set.values_list('value',flat=True) for ts in tses]
res[1]
date_range 
reload(correl_charts)
reload(correl_charts)
reload(correl_charts)
reload(correl_charts)
res=correl_charts.correl(date_range)
res=correl_charts.correl_array(date_range)
_ip.magic("debug ")
import scipy
bumpfump=scipy.array([1,3,4,5])
bumpfump
bumpfump.transpose()
bumpfump=[[1,2,3],[4,5,6],[7,8,9]]
bumpfump.transpose()
bumpfump=scipy.array([[1,2,3],[4,5,6],[7,8,9]])
bumpfump.transpose()
reload(correl_charts)
res=correl_charts.correl_array(date_range)
res=correl_charts.correl_array(date_range)
reload(correl_charts)
res=correl_charts.correl_array(date_range)
reload(correl_charts)
res=correl_charts.correl_array(date_range)
_ip.magic("debug ")
#? array
#? scipy.array
res=correl_charts.correl_array(date_range)
data
up
res=correl_charts.correl_array(date_range)
_ip.magic("debug ")
reload(correl_charts)
res=correl_charts.correl_array(date_range)
res=correl_charts.correl_array(date_range)
reload(correl_charts)
res=correl_charts.correl_array(date_range)
reload(correl_charts)
res=correl_charts.correl_array(date_range)
reload(correl_charts)
res=correl_charts.correl_array(date_range)
type([list(ts.datapoint_set.values_list('value',flat=True)) for ts in tses])
reload(correl_charts)
res=correl_charts.correl_array(date_range)
_ip.magic("debug ")
data=scipy.array()
data=scipy.array([])
#? scipy.array
reload(correl_charts)
reload(correl_charts)
reload(correl_charts)
res=correl_charts.correl_array(date_range)
reload(correl_charts)
res=correl_charts.correl_array(date_range)
reload(correl_charts)
res=correl_charts.correl_array(date_range)
reload(correl_charts)
res=correl_charts.correl_array(date_range)
res=correl_charts.correl_array(date_range)
#? numpy.ndarray
import numpy
#? numpy.ndarray
help(numpy.ndarray)
reload(correl_charts)
res=correl_charts.correl_array(date_range)
exit()
