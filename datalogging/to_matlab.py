from datalogging.models import *
import datetime
from scipy import io

ts_pk_list=[34,33,35,4,11,9,8,3,12,6,29,30,37,38]
date_range=(datetime.datetime(2009,12,24),datetime.datetime(2010,12,30))

def make_mat(mat_file_path, ts_pk_list=ts_pk_list, date_range=date_range, samples_per_ts=100):
#    out={}
    out=[]
    varnames=[]
    for pk in ts_pk_list:
        ts=Timeseries.objects.get(pk=pk)
        out.append(ts.data_cropped_resampled(num_samples=samples_per_ts,time_range_crop=date_range)[0])
        varnames.append('%d:%s%s' % (pk,ts.cave(),ts.data_type.replace('_',' ')))
        #out.update({'timeseries_%d' % ts.pk : ts.data_cropped_resampled(num_samples=samples_per_ts,time_range_crop=date_range)[0]})
        print('Data for %s loaded' % ts)
    io.savemat(mat_file_path, {'timeserieses':out,'categories':varnames})
