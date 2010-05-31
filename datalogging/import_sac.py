from obspy.core import read
from datalogging.models import DataPoint, Timeseries
import datetime, os
from scipy.signal import resample

def transfcontm1(con_raw):
    return 100*(con_raw*-322.5*0.000001)-200

#conestm1=Timeseries.objects.get(logbook_entry__cave__slug='cones', data_type='air_deg_c')
#ts=read('/fs/scratch/aaron/Erebus_10/Archive/20100106/20100106020000/CON.TM1.ER')

 

def import_sac_trace(trace, timeseries):
    assert trace[0].stats['sampling_rate']==4.0
    start_time=trace[0].stats['starttime'].getDateTime()
    time=start_time
    sampling_interval=datetime.timedelta(minutes=10)

    resampled_trace=resample(trace[0].data, len(trace[0])/2400)

    for dp in resampled_trace:
        obj,created=DataPoint.objects.get_or_create(parent_timeseries=timeseries,time=time,defaults={'value':transfcontm1(dp)})
        if created:
            print 'just made: '+str(obj)
        else:
            print 'already existed: '+str(obj)
        time+=sampling_interval

def import_sac_files(directory, timeseries):
    walker=os.walk(directory)

    for step in walker:
        if 'CON.TM1.ER' in step[2]:
            sacpath=os.path.join(step[0],'CON.TM1.ER')
            print "about to process: " + sacpath
            try:
                trace=read(sacpath)
                import_sac_trace(trace, timeseries)
            except TypeError:
                print "looks like it wasn't a SAC file."


