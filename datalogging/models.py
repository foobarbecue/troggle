from django.conf import settings
from django.db import models
from core.models import TroggleModel, LogbookEntry
from django.template.loader import render_to_string
import datetime, time, csv, logging
logging.basicConfig(filename=settings.LOGFILE,level=logging.DEBUG)

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
    manual=models.FileField(upload_to="equipment_manuals", blank=True, null=True, )
    
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

    class Meta:
        ordering=('time',)

class Timeseries(TroggleModel):
    logbook_entry=models.ForeignKey(LogbookEntry, blank=True, null=True)
    notes=models.TextField(blank=True, null=True)
    sensor=models.ForeignKey(EquipmentItem, related_name='sensor')
    logger_timeseries_id=models.IntegerField(blank=True, null=True)
    logger=models.ForeignKey(EquipmentItem, related_name='logger', blank=True, null=True)
    logger_channel=models.IntegerField(blank=True, null=True)
    import_file=models.FileField(upload_to='datalogging_files', blank=True, null=True)
    UNITS_CHOICES=(
        ('air_deg_c','Air Temperature Degrees Celsius',),
        ('deg_k','Air Temperature Degrees Kelvin'),
        ('co2_wt_perc','Weight percent CO2'),
        ('co2_mass_perc','Mass percent CO2'),
        ('rh_perc','Relative humidity'),
        ('co2_ppmv', 'Parts per million by volume CO2'),
        ('co2_pptv','Parts per thousand by volume CO2'),
        ('v','Volts'),
        ('ma','Milliamps'),
        )
    data_type=models.CharField(choices=UNITS_CHOICES, max_length=15)

    def __unicode__(self):
	if self.logger_timeseries_id:
	    return "%s on run %s of logger %s" % (self.sensor, self.logger_timeseries_id, self.logger)
        else:
            return "%s on logger %s" % (self.sensor, self.logger)
    
    def plot(self):
        return render_to_string('timeseries_plot.html',{'timeseries':self})

    def import_csv_hobo(self):
        import_file_reader = csv.reader(self.import_file.file)
        for line in import_file_reader:
            try:
                DataPoint.objects.get_or_create(parent_timeseries=self, time=datetime.datetime.strptime(line[1],'%m/%d/%y %I:%M:%S %p'), defaults={'value':line[1+self.logger_channel]})
            except:
               logging.debug('could not import line:' + str(line))
        logging.debug('imported data for:' + unicode(self))   

    def import_csv_simple(self):
        import_file_reader = csv.reader(self.import_file.file)
	if self.logger.equipment_type.model_number=='U12-008':
            self.import_csv_hobo()
        else:
            for line in import_file_reader:
                try:
                    #DataPoint.objects.get_or_create(parent_timeseries=self, time=line[1], defaults={'value':line[2]})
                    DataPoint.objects.get_or_create(parent_timeseries=self, time=datetime.datetime.strptime(line[1],'%Y-%m-%d %H:%M:%S'), defaults={'value':line[2].split(' ')[0]})
                except:
                    logging.debug('could not import line:' + str(line))
            logging.debug('imported data for:' + unicode(self))
            
            
class DataAquisitionSystem(TroggleModel):
    name=models.CharField(max_length=100)
    component=models.ManyToManyField(EquipmentItem)
    description=models.TextField(blank=True, null=True)
    
    def total_watts(self):
        pass
        #need to write this
    
    def __unicode__(self):
        return str(self.pk)
