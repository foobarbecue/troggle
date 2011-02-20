from django.db.models import Avg, Max, Min, Count, StdDev
from math import sqrt

def monthly_stats_multiple(ts_list, data_type):
    #ts_list is actually a list of cave slugs!!
    from datalogging.models import DataPoint
    outp=[]
    for month in range(1,13):
        outp.append([month,
            DataPoint.objects.filter(time__month=month,
            parent_timeseries__logbook_entry__cave__slug__in=ts_list,
            parent_timeseries__data_type=data_type).exclude(value=0.0).aggregate(Avg('value'), Max('value'), Min('value'), Count('value'), StdDev('value', sample=True)),])
        try:
            outp[month-1][1].update({'confidence_interval':float(outp[month-1][1]['value__stddev'])/float(sqrt(outp[month-1][1]['value__count']))})
        except TypeError:
            outp[month-1][1].update({'confidence_interval':None})
    return outp

def monthly_stats(ts):
    outp=[]
    for month in range(1,13):
        outp.append([month,
            ts.datapoint_set.filter(time__month=month).exclude(value=0.0).aggregate(Avg('value'), Max('value'), Min('value'), Count('value'), StdDev('value', sample=True))])
        try:
            outp[month-1][1].update({'confidence_interval':float(outp[month-1][1]['value__stddev'])/float(sqrt(outp[month-1][1]['value__count']))})
        except TypeError:
            outp[month-1][1].update({'confidence_interval':None})
    return outp
