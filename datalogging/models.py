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
        get_latest_by=('time',)

class Timeseries(TroggleModel):
    logbook_entry=models.ForeignKey(LogbookEntry, blank=True, null=True)
    notes=models.TextField(blank=True, null=True)
    sensor=models.ForeignKey(EquipmentItem, related_name='sensor')
    logger_timeseries_id=models.IntegerField(blank=True, null=True)
    logger=models.ForeignKey(EquipmentItem, related_name='logger', blank=True, null=True)
    logger_channel=models.IntegerField(blank=True, null=True)
    location_in_cave=models.CharField(blank=True, null=True, max_length=500)
    import_file=models.FileField(upload_to='datalogging_files', blank=True, null=True)
    sibling_timeseries_for_file=models.ForeignKey('Timeseries', blank=True, null=True)
    csv_column=models.IntegerField(blank=True, null=True)
    start_time=models.DateTimeField(blank=True, null=True)
    end_time=models.DateTimeField(blank=True, null=True)
    UNITS_CHOICES=(
        ('air_deg_c','Air Temperature Degrees Celsius',),
        ('deg_k','Air Temperature Degrees Kelvin'),
        ('w_azmth','Wind azimuth in degrees'),
        ('w_incl','Wind inclination in degrees'),
        ('w_speed','Wind speed in meters per second'),
        ('deg_k','Air Temperature in Degrees Kelvin'),
        ('press_hpa','Air Pressure in hectopascals'),
        ('rain','Rain depth (check units)'),
        ('co2_wt_perc','Weight percent CO2'),
        ('co2_mass_perc','Mass percent CO2'),
        ('rh_perc','Relative humidity'),
        ('co2_ppmv', 'Parts per million by volume CO2'),
        ('co2_pptv','Parts per thousand by volume CO2'),
        ('v','Volts'),
        ('ma','Milliamps'),
        )
    data_type=models.CharField(choices=UNITS_CHOICES, max_length=15)

    def auto_date_range(self):
        if self.start_time:
            start=self.start_time
        else:
            start=self.datapoint_set.all()[0].time

        if self.end_time:
            end=self.end_time
        else:
            end=self.datapoint_set.all().reverse()[0].time

        return((start,end))

    def __unicode__(self):
	if self.logger_timeseries_id:
	    return "%s on run %s of logger %s (%s)" % (self.sensor, self.logger_timeseries_id, self.logger, self.data_type)
        else:
            return "%s on logger %s (%s)" % (self.sensor, self.logger, self.data_type)
    
    def plot(self):
        return render_to_string('timeseries_plot.html',{'timeseries':self})
    
    def data(self, start_time=start_time, end_time=end_time, max_samples=1000):
        try:
            cropped_ts=self.datapoint_set.filter(time__gte=start_time, time__lte=end_time)
        except:
            cropped_ts=self.datapoint_set.all()
        if len(cropped_ts) > max_samples:
            return cropped_ts.extra(where=['MOD(id,%s)=0' % (len(cropped_ts)/max_samples)])
        else:
            return cropped_ts

    def import_csv_hobo(self):
        if self.import_file:
            import_file_reader = csv.reader(self.import_file.file)
        else:
            import_file_reader = csv.reader(self.sibling_timeseries_for_file.import_file.file)            
        
        for line in import_file_reader:
            try:
                DataPoint.objects.get_or_create(parent_timeseries=self, time=datetime.datetime.strptime(line[1],'%m/%d/%y %I:%M:%S %p'), defaults={'value':line[1+self.logger_channel]})
            except:
               logging.debug('could not import line:' + str(line))
        logging.debug('imported data for:' + unicode(self))   

    def import_csv_campbell(self):
        import_file_reader = csv.reader(self.import_file.file)
        for line in import_file_reader:
            try:
                DataPoint.objects.get_or_create(parent_timeseries=self, time=datetime.datetime.strptime(line[0],'%Y-%m-%d %H:%M:%S'), defaults={'value':line[self.csv_column]})
            except:
                logging.debug('could not import line:' + str(line))
        logging.debug('imported data for:' + unicode(self))  

    def import_spawar_aws(self, import_file_path):
        import_file_reader = csv.reader(open(import_file_path),dialect='excel-tab')
        import_file_reader.next()
        import_file_reader.next()
        month_year=datetime.datetime.strptime(import_file_reader.next()[0],'%B %Y')
        print month_year
        for line in import_file_reader:
            try:
                time=month_year+datetime.timedelta(days=int(line[0])-1,hours=int(line[1][0:2]),minutes=int(line[1][2:4]))
                DataPoint.objects.get_or_create(parent_timeseries=self, time=time, defaults={'value':line[self.csv_column-1]})
                logging.debug('imported data for:' + str(line))
                print 'imported data for:' + str(line)
            except:
                logging.debug('could not import line:' + str(line))
                print 'could not import line:' + str(line)
 

       
    def import_csv_simple(self):
        import_file_reader = csv.reader(self.import_file.file)
        if self.logger.equipment_type.model_number=='U12-008':
            self.import_csv_hobo()
        elif self.logger.equipment_type.model_number=='CR1000':
            self.import_csv_campbell()
        else:
            for line in import_file_reader:
                try:
                    #DataPoint.objects.get_or_create(parent_timeseries=self, time=line[1], defaults={'value':line[2]})
                    DataPoint.objects.get_or_create(parent_timeseries=self, time=datetime.datetime.strptime(line[1],'%Y-%m-%d %H:%M:%S'), defaults={'value':line[2].split(' ')[0]})
                except:
                    logging.debug('could not import line:' + str(line))
            logging.debug('imported data for:' + unicode(self))

    def cave(self):
        return self.logbook_entry.cave
            
            
class DataAquisitionSystem(TroggleModel):
    name=models.CharField(max_length=100)
    component=models.ManyToManyField(EquipmentItem)
    description=models.TextField(blank=True, null=True)
    
    def total_watts(self):
        pass
        #need to write this
    
    def __unicode__(self):
        return str(self.pk)
