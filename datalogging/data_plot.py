import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from datalogging.models import *
from core.models import Cave
from matplotlib import pyplot as plt
from datetime import datetime, date
from django.db.models import Count, Q
from matplotlib.ticker import MaxNLocator

default_time_range=(datetime(2009,12,8,0,0),datetime(2010,1,3,0,0))
all_temp_plots=Q(Timeseries.objects.filter(data_type='air_deg_c'))


#remove 'bogus cave' which was used for testing
#and some others we don't want displayed
#caves_with_timeseries=Cave.objects.annotate(num_ts=Count('logbookentry__timeseries')).filter(
#    Q(num_ts__gt=0)|Q(official_name__icontains='wind'),
#    ~Q(official_name__in=('Bogus Cave','LEH','Helo Cave')))

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
    )

cave_number=0

def time_domain(ts_list=all_temp_plots, date_range=default_time_range):
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

def crop_date_range(date_range_crop, ts):
    """
    Finds the intersection of the input date range with the timeseries start_time and
    end_time.
    """
    date_range_crop=list(date_range_crop)
    print "input date is:" ,
    print date_range_crop[0],
    print "to"
    print date_range_crop[1],
    if ts.start_time is not None and date_range_crop[0] < ts.start_time:
        date_range_crop[0] = ts.start_time
        print "Adjusting start time"
    else:
        print "Didn't need to adjust start time"
    if ts.end_time is not None and date_range_crop[1] > ts.end_time:
        date_range_crop[1] = ts.end_time    
        print "Adjusting end time"
    else:
        print "Didn't need to adjust end time"
      
    return date_range_crop

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
        label=unicode(ts.location_in_cave)

        if ts.data_type=='w_azmth':
            a2=ax.twinx()
            for tlabel in a2.get_yticklabels():
                tlabel.set_color('g')
            a2.plot(times, values, label=label, color='g')
            a2.legend(labels=('windspeed (m/s)','direction (degrees from true north)'))
        else:
            ax.plot(times, values, label=label)

        ax.set_xlim(date_range)
        ax.legend(loc='best')
        ax.yaxis.set_label_text(ts.logbook_entry.cave)
        ax.yaxis.label.set_rotation('horizontal')
        ax.yaxis.label.set_ha('right')
        print u'Plotted timeseries: ' + unicode(ts)

def hist_do_plot(ts_list, ax):
    """
    Handles the actual plotting for histogram data.
    """
    for ts in ts_list and ts.pk !=25:
        
        dps=ts.datapoint_set.all()
        if ts.start_time is not None:
            dps=dps.filter(time__gte=ts.start_time)
        if ts.end_time is not None:
            dps=dps.filter(time__lte=ts.end_time)       
        try:
            ax.hist(dps.values_list('value', flat=True), histtype='step', normed=True, label=ts.location_in_cave)
        except:
            pass
        ax.yaxis.set_label_text(ts.logbook_entry.cave)


def adjust(fig):
#    fig.subplots_adjust(hspace=1)
    for ax in fig.axes:
        ax.yaxis.set_major_locator(MaxNLocator(4))
    plt.setp(fig.axes[-1].get_xticklabels(), visible=True)  
    plt.show()

def time_domain_by_cave(cave_list=caves_with_timeseries, date_range=default_time_range):
    """
    Produce plots for each timeseries in each cave in cave_list (a list or tuple) over the
    range date_range (a 2-tuple of strings in YYYY-MM-DD HH:MM:SS or datetime objects).

    Caves have individual subplots within which each of the timeseries for that cave is
    displayed.
    """
    fig=plt.figure()
    cave_number=0
    ax=None
    
    #first plot the barometric pressure at LEH
#    ax=fig.add_subplot(len(cave_list),1,1)
#    LEHpress=Timeseries.objects.get(logbook_entry__cave__slug='leh',data_type='press_hpa').datapoint_set
#    ax.plot(LEHpress.values_list('time',flat=True),LEHpress.values_list('value',flat=True))
#    plt.setp(ax.get_xticklabels(), visible=False)
#    ax.set_xlim(date_range)
#    ax.yaxis.set_label_text('Barometric Pressure (hPa)')
#    ax.yaxis.label.set_rotation('horizontal')
#    ax.yaxis.label.set_ha('right')
#    ax.set_ylim(625,640)
 
    #now plot all of the temperatures
    for cave in cave_list:
        print 'Adding subplot for cave: '+unicode(cave)

        #Link every subplot to the xaxis of the LEH barometric pressure
        ax=fig.add_subplot(len(cave_list),1,cave_number+1,sharex=ax)

        #Hide the x-axis lables, except for the last one
        plt.setp(ax.get_xticklabels(), visible=False)
        if cave_number==(len(cave_list)-1):
            plt.setp(ax.get_xticklabels(), visible=True)    
        time_domain_do_plot(cave.timeseries_set().filter(data_type__in=('air_deg_c','w_speed','w_azmth')).exclude(location_in_cave__icontains='panel'), date_range, ax)
        cave_number+=1

    adjust(fig)

    return ax
    

def histograms_by_cave(cave_list=caves_with_timeseries):
    fig=plt.figure()
    cave_number=0
    ax=None
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
    
def scatterplots(xtimeseries, ytimeseries_list):
    pass
