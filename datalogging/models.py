from django.db import models
from core.models import TroggleModel, LogbookEntry
from django.template.loader import render_to_string
import time

class Manufacturer(TroggleModel):
    name=models.CharField(max_length=160, primary_key=True )
    website=models.URLField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name

class EquipmentType(TroggleModel):
    manufacturer=models.ForeignKey(Manufacturer)
    model_number=models.CharField(max_length=100,  primary_key=True)
    description=models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return "%s %s" % (self.manufacturer, self.model_number)

class EquipmentItem(TroggleModel):
    serial_number=models.CharField(max_length=100, primary_key=True)
    equipment_type=models.ForeignKey(EquipmentType)
    notes=models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return "%s %s" % (self.equipment_type, self.serial_number)

class Timeseries(TroggleModel):
    logbook_entry=models.ForeignKey(LogbookEntry)
    sensor=models.ForeignKey(EquipmentItem, related_name='sensor')
    logger_timeseries_id=models.IntegerField(blank=True, null=True)
    logger=models.ForeignKey(EquipmentItem, related_name='logger')
    logger_channel=models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return "%s on run %s of logger %s" % (self.sensor, self.logger_timeseries_id, self.logger)
    
    def plot(self):
        return render_to_string('timeseries_plot.html',{'timeseries':self})

class DataPoint(TroggleModel):
    time=models.DateTimeField()
    value=models.FloatField()
    parent_timeseries=models.ForeignKey(Timeseries)

    def epoch_time(self):
        return time.mktime(res.timetuple(self.time))*1000
    
    def __unicode__(self):
        return "data point taken at %s from %s" % (self.time, self.parent_timeseries)
    

# Create your models here.
