import os, datetime, re, sys
from string import maketrans, translate

sys.path.append('/home/aaron/troggle_erebus')
from datalogging.models import *

#Get the albertometer
albertometer=EquipmentItem.objects.get(pk='AB1')

sbd_config=(
    (Timeseries.objects.get(logger=albertometer, data_type='v'), '.*Vs=([\d\.]*)V'),
    (Timeseries.objects.get(logger=albertometer, data_type='co2_ppmv'), '.*CO2=([\d\.]*)ppm.*' ),
    (Timeseries.objects.get(logger=albertometer, data_type='air_deg_c'), '.*Ta=(-*[\d\.]*)C.*' ),
    (Timeseries.objects.get(logger=albertometer, data_type='w_azmth'), '.*Dm=([\d\.]*)#.*' ),
    (Timeseries.objects.get(logger=albertometer, data_type='w_speed'), '.*Sm=([\d\.]*)#.*' ),
    (Timeseries.objects.get(logger=albertometer, data_type='press_hpa'), '.*Pa=([\d\.]*)H.*' ),
    (Timeseries.objects.get(logger=albertometer, data_type='rain'), '.*Ua=([\d\.]*)P.*' ),
    )

def parse_all_sbds(sbd_config=sbd_config, directory='/home/aaron/troggle_erebus/media/datalogging_files/sbd'):
    for line in sbd_config:
	timeseries, re_ptn=line
        initial_count=timeseries.datapoint_set.count()
        parse_sbds(directory=directory, re_ptn=re_ptn, timeseries=timeseries)
	added_count=timeseries.datapoint_set.count()-initial_count
	print "Added %s datapoints to %s" % (added_count, timeseries)

def parse_sbds(directory, re_ptn, timeseries):
    for filename in os.listdir(directory):
        if 'sbd' in filename:
            curfile=open(os.path.join(directory, filename),'r').read()
            curtime=datetime.datetime.strptime(curfile[0:15], 'T%H:%MD%m/%d/%y')
	    curfile=unicode(curfile, errors='ignore')
            value=re.match(re_ptn, curfile).groups()[0]
            DataPoint.objects.get_or_create(time=curtime, value=value, parent_timeseries=timeseries)
        else:
            print "not importing" + filename

def make_single_csv(directory, outfile_path):
    of=open(outfile_path,'w')
    for filename in os.listdir(directory):
        of.write(open(os.path.join(directory, filename),'r').read()+'\n')

inp=sys.__stdin__.read()
if len(inp)>1:
    for line in sbd_config:
        curfile=unicode(inp, errors='ignore')
        curtime=datetime.datetime.strptime(curfile[0:15], 'T%H:%MD%m/%d/%y')
        value=re.match(line[1], curfile).groups()[0]

        #workaround for bug where co2 values put the decimal point one to the left of where it should be
        if (int(line[0])==19 and float(value) < 75):
            value=value*10

        dp, created = DataPoint.objects.get_or_create(time=curtime, value=value, parent_timeseries=line[0])
        print dp
        if created:
            print "created"
else:
    pass
        
