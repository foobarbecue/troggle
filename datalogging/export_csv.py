from datalogging.models import Timeseries, DataPoint
import csv
import datetime

def export_to_csv(path, date_range, timeseries_set):
    outfile=open(path,'w')
    outwriter=csv.writer(outfile)

    for ts in timeseries_set:
        out_line=ts.datapoint_set.filter(time__range=date_range).values_list('value',flat=True)
        out_line=list(out_line)
        print '%s has %s samples' % (ts, len(out_line))
        out_line.insert(0, unicode(ts))
        outwriter.writerow(out_line)
      

    return outwriter

def sample_rate(ts):
    td=ts.datapoint_set.all()[0].time-ts.datapoint_set.reverse()[0].time
    duration=(td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6
    tot_samples=ts.datapoint_set.all().count()
    print samples
    print duration
    return tot_samples/duration
