from datalogging.models import Timeseries, DataPoint
import csv
import datetime

def export_to_csv(outfile, date_range, timeseries_set, samples_per_ts=100):
    outwriter=csv.writer(outfile)

    for ts in timeseries_set:
        ts_data, ts_times=ts.data_cropped_resampled(num_samples=samples_per_ts,time_range_crop=date_range)
        print '%s has %s samples' % (ts, len(ts_data))
#        out_line.insert(0, unicode(ts))
        outwriter.writerow(('Following lines are the %s samples for %s' % (ts, len(ts_data)),))
        outwriter.writerow(ts_times)
        outwriter.writerow(ts_data)
      

    return outwriter

def sample_rate(ts):
    td=ts.datapoint_set.all()[0].time-ts.datapoint_set.reverse()[0].time
    duration=(td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6
    tot_samples=ts.datapoint_set.all().count()
    print samples
    print duration
    return tot_samples/duration
