import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.mlab as mlab

from datalogging.models import *

years    = mdates.YearLocator()   # every year
months   = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y')

fig=plt.figure()
tsnum=0

for ts in Timeseries.objects.all()[0:5]:
    tsnum+=1
    
    ax=fig.add_subplot(1,1,n)
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)

    
    datemin = datetime.date(min(tsls[0]).year, 1, 1)
    datemax = datetime.date(max(tsls[0]).year+1, 1, 1)
    ax.set_xlim(datemin, datemax)

fig.autofmt_xdate()
plt.show()