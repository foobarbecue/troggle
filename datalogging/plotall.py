import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.mlab as mlab

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

dataset=Timeseries.objects.all()[2:7]

for ts in dataset:
    tsnum+=1
    tsls=ts.data()
    
    ax=fig.add_subplot(5,1,tsnum)

    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(monthsFmt)
    ax.xaxis.set_minor_locator(days)
    ax.xaxis.set_minor_formatter(daysFmt)    
    print unicode(ts)
    ax.set_title(unicode(ts.logbook_entry.cave)+' '+ts.location_in_cave)

    if not datemin or datemin > min(tsls[0]):
        datemin = min(tsls[0])
    
    if not datemax or datemax < max(tsls[0]):
        datemax = max(tsls[0])


    ax.plot(tsls[0], tsls[1])
    
    ax.set_xlim(datemin, datemax)

fig.autofmt_xdate()
plt.show()