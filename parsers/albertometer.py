import os, datetime, re
from string import maketrans, translate
from datalogging.models import *

sbd_config=(
    (Timeseries.objects.get(pk=18), '.*Vs=([\d\.]*)V'),
    (Timeseries.objects.get(pk=19), '.*CO2=(\d*)ppm.*' )
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
    
