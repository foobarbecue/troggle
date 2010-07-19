import numpy
import datetime
from datalogging.models import *
date_range=(datetime.datetime(2009,12,24),datetime.datetime(2009,12,30))

def parallel_comp(component_dir, azimuth, speed):
    """
    Calculates the effective speed of wind movement parallel to
    component_dir, given the speed and azimuth of wind.
    """
    return speed*numpy.cos(azimuth-component_dir)

def new_parallel_ts(component_dir, speed_ts, azimuth_ts):
    """
    Creates a new timeseries with values that are the component
    parallel to component_dir.
    """    
    speeds, times=speed_ts.data_cropped_resampled(num_samples=100, time_range_crop=date_range)
    azimuths=azimuth_ts.data_cropped_resampled(num_samples=100, time_range_crop=date_range)[0]
    comp_ts=Timeseries(data_type='w_speed',sensor=EquipmentItem.objects.get(pk=5))
    speed_ts.logbook_entry.timeseries_set.add(comp_ts)
    for speed, azimuth, time in zip(speeds, azimuths, times):
        new_dp=DataPoint(value=parallel_comp(component_dir,speed,azimuth),time=time)
        comp_ts.datapoint_set.add(new_dp)
        comp_ts.save()
    return comp_ts
