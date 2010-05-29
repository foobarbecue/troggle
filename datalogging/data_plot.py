import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from datalogging.models import *
from core.models import Cave
from matplotlib import pyplot as plt
from datetime import datetime
from django.db.models import Count
from matplotlib.ticker import MaxNLocator

all_temp_plots=Timeseries.objects.filter(data_type='air_deg_c')
caves_with_data=Cave.objects.all()
cave_number=0

def time_domain(ts_list=all_temp_plots, date_range=[datetime(2009,12,01),datetime(2010,03,01)]):
    """
    Produce plots for each timeseries in ts_list (a list or tuple) over the
    range date_range (a 2-tuple of strings in YYYY-MM-DD HH:MM:SS or datetime objects).
    """

    fig=plt.figure()
    ax=fig.add_subplot(111)

    time_domain_do_plot(ts_list, date_range, ax)

    plt.legend()
    adjust(plt)
    plt.show()

def crop_date_range(date_range, ts):
    """
    Finds the intersection of the input date range with the timeseries start_time and
    end_time.
    """
    if ts.start_time is not None and date_range[0] < ts.start_time:
        date_range[0] = ts.start_time
        print "Adjusting start time"
    else:
        print "Didn't need to adjust start time"
    if ts.end_time is not None and date_range[1] > ts.end_time:
        date_range[1] = ts.end_time    
        print "Adjusting end time"
    else:
        print "Didn't need to adjust end time"
      
    return date_range

def time_domain_do_plot(ts_list, date_range, ax):
    """
    Handles the actual plotting for time domain data.
    """
    for ts in ts_list:
        #Crop the data according to the start_time and end_time fields.
        #This removes extraneous data, e.g. from travelling to location.
        date_range_cropped=crop_date_range(date_range, ts)

        times=ts.datapoint_set.filter(time__range=date_range_cropped).values_list('time',flat=True)
        values=ts.datapoint_set.filter(time__range=date_range_cropped).values_list('value',flat=True)
        if ts.location_in_cave and ts.logbook_entry.cave:
            label=unicode(ts.logbook_entry.cave)+': '+ts.location_in_cave
        elif ts.location_in_cave:
            label=unicode(ts.logbook_entry.cave)
        else:
            label='unknown'

        ax.plot(times, values, label=label)
        ax.set_xlim(date_range)
        print u'Plotted timeseries: ' + unicode(ts)

def hist_do_plot(ts_list, ax):
    """
    Handles the actual plotting for histogram data.
    """
    for ts in ts_list:
        
        dps=ts.datapoint_set.all()
        if ts.start_time is not None:
            dps=dps.filter(time__gte=ts.start_time)
        if ts.end_time is not None:
            dps=dps.filter(time__lte=ts.end_time)       
        try:
            ax.hist(dps.values_list('value', flat=True), histtype='step', normed=True, label=ts.location_in_cave)
        except:
            pass
        ax.set_title(ts.logbook_entry.cave)


def adjust(fig):
#    fig.subplots_adjust(hspace=1)
    for ax in fig.axes:
        ax.yaxis.set_major_locator(MaxNLocator(2))
    plt.show()

def time_domain_by_cave(cave_list=all_caves, date_range=[datetime(2009,12,01),datetime(2010,03,01)]):
    """
    Produce plots for each timeseries in each cave in cave_list (a list or tuple) over the
    range date_range (a 2-tuple of strings in YYYY-MM-DD HH:MM:SS or datetime objects).

    Caves have individual subplots within which each of the timeseries for that cave is
    displayed.
    """
    fig=plt.figure()
    cave_number=0
    ax=None
    cave_list=Cave.objects.annotate(num_ts=Count('logbookentry__timeseries')).filter(num_ts__gt=0)
    for cave in cave_list:
        print 'Adding subplot for cave: '+unicode(cave)

        #Link every subplot to the xaxis of the first one
        if ax is not None:
            ax=fig.add_subplot(len(cave_list)-1,1,cave_number,sharex=ax)
        else:
            ax=fig.add_subplot(len(cave_list)-1,1,cave_number)

        #Hide the x-axis lables, except for the last one
        plt.setp(ax.get_xticklabels(), visible=False)
        if cave_number==(len(cave_list)-1):
            plt.setp(ax.get_xticklabels(), visible=True)
        ax.set_title(unicode(cave))            
        time_domain_do_plot(cave.timeseries_set().filter(data_type='air_deg_c'), date_range, ax)
        cave_number+=1
    
    adjust(fig)
    

def histograms_by_cave(cave_list=all_caves):
    fig=plt.figure()
    cave_number=0
    ax=None
    cave_list=Cave.objects.annotate(num_ts=Count('logbookentry__timeseries')).filter(num_ts__gt=0).exclude(official_name='Bogus Cave')
    for cave in cave_list:
        print 'Adding subplot for cave: '+unicode(cave)

        #Link every subplot to the xaxis of the first one
        if ax is not None:
            ax=fig.add_subplot(len(cave_list),1,cave_number,sharex=ax)
        else:
            ax=fig.add_subplot(len(cave_list),1,cave_number)

        #Hide the x-axis lables, except for the last subplot
        plt.setp(ax.get_xticklabels(), visible=False)
        if cave_number==(len(cave_list)-1):
            plt.setp(ax.get_xticklabels(), visible=True)
            
        hist_do_plot(cave.timeseries_set().filter(data_type='air_deg_c'), ax)
        cave_number+=1
        ax.legend(loc='best')
    
    adjust(fig)
    

