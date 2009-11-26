from django.db import models
from core.models import TroggleModel, LogbookEntry
from django.template.loader import render_to_string
import time, csv

class Manufacturer(TroggleModel):
    name=models.CharField(max_length=160, primary_key=True )
    website=models.URLField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name

class EquipmentType(TroggleModel):
    manufacturer=models.ForeignKey(Manufacturer)
    model_number=models.CharField(max_length=100,  primary_key=True)
    description=models.TextField(blank=True, null=True)
    voltage=models.FloatField(blank=True, null=True, )
    current=models.FloatField(blank=True, null=True, )
    amp_hours=models.FloatField(blank=True, null=True, )
    data_storage_capacity=models.FloatField(blank=True, null=True, )
    manual=models.FileField(upload_to="equipment_manuals")
    
    def __unicode__(self):
        return "%s %s" % (self.manufacturer, self.model_number)

class EquipmentItem(TroggleModel):
    serial_number=models.CharField(max_length=100, primary_key=True)
    equipment_type=models.ForeignKey(EquipmentType)
    notes=models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return "%s %s" % (self.equipment_type, self.serial_number)

class DataPoint(TroggleModel):
    time=models.DateTimeField()
    value=models.FloatField()
    parent_timeseries=models.ForeignKey('Timeseries')

    def epoch_time(self):
        return time.mktime(self.time.timetuple())*1000
    
    def __unicode__(self):
        return "data point taken at %s from %s" % (self.time, self.parent_timeseries)

class Timeseries(TroggleModel):
    logbook_entry=models.ForeignKey(LogbookEntry, blank=True, null=True)
    sensor=models.ForeignKey(EquipmentItem, related_name='sensor')
    logger_timeseries_id=models.IntegerField(blank=True, null=True)
    logger=models.ForeignKey(EquipmentItem, related_name='logger', blank=True, null=True)
    logger_channel=models.IntegerField(blank=True, null=True)
    import_file=models.FileField(upload_to='datalogging_files')
    UNITS_CHOICES=(
        ('Air Temperature Degrees Celsius', 'air_deg_c'),
        ('Air Temperature Degrees Kelvin', 'deg_k'),
        ('Weight percent CO2', 'co2_wt_perc'),
        ('Mass percent CO2', 'co2_mass_perc'),
        ('Relative humidity', 'rh_perc'),
        ('Parts per million by volume CO2', 'co2_ppmv'),
        ('Parts per thousand by volume CO2', 'co2_pptv'),
        ('Volts', 'v'),
        ('Milliamps', 'ma'),
        )
    data_type=models.CharField(choices=UNITS_CHOICES, max_length=15)

    def __unicode__(self):
        return "sensor %s on run %s of logger %s" % (self.sensor, self.logger_timeseries_id, self.logger)
    
    def plot(self):
        return render_to_string('timeseries_plot.html',{'timeseries':self})
    
    def import_csv_simple(self):
        import_file_reader = csv.reader(self.import_file.file)
        for line in import_file_reader:
            try:
                DataPoint.objects.get_or_create(parent_timeseries=self, time=line[1], defaults={'value':line[2]})
            except:
                print 'could not import line:' + str(line)

class DataAquisitionSystem(TroggleModel):
    component=models.ManyToManyField(EquipmentItem)
    description=models.TextField(blank=True, null=True)
    
    def total_watts(self):
        pass
        #need to write this
    
    def __unicode__(self):
        return str(self.pk)