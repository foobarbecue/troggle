import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import mlab
from matplotlib.ticker import MaxNLocator

from datalogging.models import *

years    = mdates.YearLocator()   # every year
months   = mdates.MonthLocator()  # every month

days   = mdates.DayLocator()
monthsFmt = mdates.DateFormatter('%B %Y')
daysFmt = mdates.DateFormatter('%D')

fig=plt.figure()
tsnum=0

datemin=None
datemax=None

dataset=Timeseries.objects.filter(data_type='air_deg_c')[2:13]
axes=[]
lastax=None

for ts in dataset:
    tsnum+=1
    tsls=ts.data()
    if lastax:
        ax=fig.add_subplot(len(dataset),1,tsnum, sharex=(lastax or None))
    else:
        ax=fig.add_subplot(len(dataset),1,tsnum)

    #ax.xaxis.set_major_locator(months)
    #ax.xaxis.set_major_formatter(monthsFmt)
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(daysFmt)
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=4,prune='top'))
    print unicode(ts)
    if ts.location_in_cave:
        ax.set_ylabel(unicode(ts.logbook_entry.cave)+': '+ts.location_in_cave, rotation='horizontal')
    else:
        ax.set_ylabel(unicode(ts.logbook_entry.cave), rotation='horizontal')

    if not datemin or datemin > min(tsls[0]):
        datemin = min(tsls)
    
    if not datemax or datemax < max(tsls[0]):
        datemax = max(tsls)

    ax.set_xlim(datemin, datemax)
    ax.plot(tsls[0], tsls[1])
    lastax=ax
    

fig.autofmt_xdate()
plt.show()
