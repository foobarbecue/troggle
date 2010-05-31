#log# Automatic Logger file. *** THIS MUST BE THE FIRST LINE ***
#log# DO NOT CHANGE THIS LINE OR THE TWO BELOW
#log# opts = Struct({'__allownew': True, 'logfile': 'regresslog.py', 'pylab': 1})
#log# args = []
#log# It is safe to make manual edits below here.
#log#-----------------------------------------------------------------------
from datalogging import data_plot 
from datalogging import data_plot 
data_plot.time_domain_by_cave()
res=Cave.objects.annotate(num_ts=Count('logbookentry__timeseries')).filter(num_ts__gt=0)
from core.models import *
res=Cave.objects.annotate(num_ts=Count('logbookentry__timeseries')).filter(num_ts__gt=0)
from scipy import linspace, polyval, polyfit, sqrt, stats, randn
from pylab import plot, title, show , legend
_ip.magic("logstate ")
_ip.magic("logon regresslog")
_ip.magic("logstart ")
_ip.magic("logstop ")
_ip.magic("logstart regresslog")
_ip.magic("logstart regresslog.py")
_ip.magic("logoff ")
_ip.magic("logstart regresslog.py")
_ip.magic("logstop ")
_ip.magic("logstart regresslog.py")

_ip.magic("logon ")
from scipy import linspace, polyval, polyfit, sqrt, stats, randn
from pylab import plot, title, show , legend
from core.models import *
from datalogging.models import *
#? polyval
#? polyfit
xinput=Timeseries.objects.get(logbook_entry__cave__official_name='Derodome')
yinput=Timeseries.objects.get(logbook_entry__cave__official_name='Derodome')
yinput=Timeseries.objects.get(logbook_entry__cave__slug='Heroin Tower')
yinput=Timeseries.objects.get(logbook_entry__cave__official_name='Heroin Tower')
(x,y)=polyfit(xinput.values_list('value',flat=True), yinput.values_list('value',flat=True),1)
(x,y)=polyfit(xinput.datapoint_set.values_list('value',flat=True), yinput.datapoint_set.values_list('value',flat=True),1)
(x,y)=polyfit(xinput.datapoint_set.filter(time__range=('2009-12-10','2010-01-02')).values_list('value',flat=True), yinput.datapoint_set.filter(time__range=('2009-12-10','2010-01-02')).values_list('value',flat=True),1)
len(x)
x
#? polyfit
y
(slope,intercept)=polyfit(xinput.datapoint_set.filter(time__range=('2009-12-10','2010-01-02')).values_list('value',flat=True), yinput.datapoint_set.filter(time__range=('2009-12-10','2010-01-02')).values_list('value',flat=True),1)
(slope,intercept, r, rr, stderr)=stats.linregress(xinput.datapoint_set.filter(time__range=('2009-12-10','2010-01-02')).values_list('value',flat=True), yinput.datapoint_set.filter(time__range=('2009-12-10','2010-01-02')).values_list('value',flat=True),1)
title('Linear Regression Example')
plot(xinput.datapoint_set.filter(time__range=('2009-12-10','2010-01-02')).values_list('value',flat=True), yinput.datapoint_set.filter(time__range=('2009-12-10','2010-01-02')).values_list('value',flat=True))
plot(xinput.datapoint_set.filter(time__range=('2009-12-10','2010-01-02')).values_list('value',flat=True), yinput.datapoint_set.filter(time__range=('2009-12-10','2010-01-02')).values_list('value',flat=True),'k.')
#? xlabel
xlabel('Derodome Temperature')
Ylabel('Heroin Tower Temperature')
ylabel('Heroin Tower Temperature')
#? polyfit
#? linalg.lstsq
#? linalg.lstsq
#? linregress
#? stats.linregress
#? stats.pearsonr
title('Linear Regression Example')
(c,b,a)=polyfit(xinput.datapoint_set.filter(time__range=('2009-12-10','2010-01-02')).values_list('value',flat=True), yinput.datapoint_set.filter(time__range=('2009-12-10','2010-01-02')).values_list('value',flat=True),2)
xr=polyval((c,b,a),xinput.datapoint_set.filter(time__range=('2009-12-10','2010-01-02')).values_list('value',flat=True))
plot(xinput.datapoint_set.filter(time__range=('2009-12-10','2010-01-02')).values_list('value',flat=True),xr,'r.-')
(c,b,a)=polyfit(xinput.datapoint_set.filter(time__range=('2009-12-10','2010-01-02')).values_list('value',flat=True), yinput.datapoint_set.filter(time__range=('2009-12-10','2010-01-02')).values_list('value',flat=True),3)
(a,b,c,d)=polyfit(xinput.datapoint_set.filter(time__range=('2009-12-10','2010-01-02')).values_list('value',flat=True), yinput.datapoint_set.filter(time__range=('2009-12-10','2010-01-02')).values_list('value',flat=True),3)
xr=polyval((a,b,c,d),xinput.datapoint_set.filter(time__range=('2009-12-10','2010-01-02')).values_list('value',flat=True))
plot(xinput.datapoint_set.filter(time__range=('2009-12-10','2010-01-02')).values_list('value',flat=True),xr,'r.-')
f=gcf()
f.lines()
f.lines
ax=gca()
ax.lines()
ax.lines
ax.lines[0]
lines=ax.lines[0]
lines.set_color('red')
lines.set_color('blue')
lines.set_color('green')
show()
ax.lines[1].set_visible(False)
show()
ax.lines[2].set_visible(False)
show()
_ip.magic("logoff ")
