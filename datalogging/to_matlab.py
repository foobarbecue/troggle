from datalogging.models import *
import datetime
from time import mktime
from scipy import io

ts_pk_list=[34,33,35,4,11,9,8,3,12,6,29,30,37,38]
date_range=(datetime.datetime(2009,12,24),datetime.datetime(2010,12,30))

def make_mat(mat_file_path, ts_pk_list=ts_pk_list, date_range=date_range, samples_per_ts=100):
#    out={}
    out=[]
    varnames=[]
    for pk in ts_pk_list:
        ts=Timeseries.objects.get(pk=pk)
        ts_data, ts_times=ts.data_cropped_resampled(num_samples=samples_per_ts,time_range_crop=date_range)
        #convert times to matlab serial datetimes
        ts_times=[mktime(timestamp.timetuple())/(60*60*24)+719529 for timestamp in ts_times]
        out.append(ts_times)
        out.append(ts_data)
        varname='%d:%s %s' % (pk,ts.cave(),ts.data_type.replace('_',' '))
        varnames.append('Times for %s' % varname)
        varnames.append(varname)
        #out.update({'timeseries_%d' % ts.pk : ts.data_cropped_resampled(num_samples=samples_per_ts,time_range_crop=date_range)[0]})
        print('Data for %s loaded' % ts)
    io.savemat(mat_file_path, {'timeserieses':out,'categories':varnames})

def make_mat_nofourier(mat_file_path, ts_pk_list=ts_pk_list, date_range=date_range):
    out=[]
    out_times=[]
    varnames=[]
    samples_per_ts=None
    for pk in ts_pk_list:
        ts=Timeseries.objects.get(pk=pk)
        ts_data=ts.datapoint_set.filter(time__range=date_range).values_list('value',flat=True)
        #if this doesn't match the number of samples in the last timeseries, resample it
        if samples_per_ts and samples_per_ts!=len(ts_data):
            ts_data, ts_times=ts.data_cropped_resampled(num_samples=samples_per_ts,time_range_crop=date_range)
            print 'had to resample %s' % ts
        #convert times to matlab serial datetimes
        ts_times=[mktime(timestamp.timetuple())/(60*60*24)+719529 for timestamp in ts_times]
        samples_per_ts=len(ts_data)
        out.append(ts_times)
        out.append(ts_data)
        varname='%d:%s %s' % (pk,ts.cave(),ts.data_type.replace('_',' '))
        varnames.append(varname)
        varnames.append('Times for %s' % varname)
        #out.update({'timeseries_%d' % ts.pk : ts.data_cropped_resampled(num_samples=samples_per_ts,time_range_crop=date_range)[0]})
        print('Data for %s loaded, with %s points' % (ts, len(ts_data)))
    io.savemat(mat_file_path, {'timeserieses':out,'categories':varnames})
