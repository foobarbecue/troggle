
from south.db import db
from django.db import models
from datalogging.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Manufacturer'
        db.create_table('datalogging_manufacturer', (
            ('new_since_parsing', orm['datalogging.Manufacturer:new_since_parsing']),
            ('non_public', orm['datalogging.Manufacturer:non_public']),
            ('name', orm['datalogging.Manufacturer:name']),
            ('website', orm['datalogging.Manufacturer:website']),
        ))
        db.send_create_signal('datalogging', ['Manufacturer'])
        
        # Adding model 'EquipmentItem'
        db.create_table('datalogging_equipmentitem', (
            ('new_since_parsing', orm['datalogging.EquipmentItem:new_since_parsing']),
            ('non_public', orm['datalogging.EquipmentItem:non_public']),
            ('serial_number', orm['datalogging.EquipmentItem:serial_number']),
            ('equipment_type', orm['datalogging.EquipmentItem:equipment_type']),
            ('notes', orm['datalogging.EquipmentItem:notes']),
        ))
        db.send_create_signal('datalogging', ['EquipmentItem'])
        
        # Adding model 'DataPoint'
        db.create_table('datalogging_datapoint', (
            ('id', orm['datalogging.DataPoint:id']),
            ('new_since_parsing', orm['datalogging.DataPoint:new_since_parsing']),
            ('non_public', orm['datalogging.DataPoint:non_public']),
            ('time', orm['datalogging.DataPoint:time']),
            ('value', orm['datalogging.DataPoint:value']),
            ('parent_timeseries', orm['datalogging.DataPoint:parent_timeseries']),
        ))
        db.send_create_signal('datalogging', ['DataPoint'])
        
        # Adding model 'EquipmentType'
        db.create_table('datalogging_equipmenttype', (
            ('new_since_parsing', orm['datalogging.EquipmentType:new_since_parsing']),
            ('non_public', orm['datalogging.EquipmentType:non_public']),
            ('manufacturer', orm['datalogging.EquipmentType:manufacturer']),
            ('model_number', orm['datalogging.EquipmentType:model_number']),
            ('description', orm['datalogging.EquipmentType:description']),
            ('voltage', orm['datalogging.EquipmentType:voltage']),
            ('current', orm['datalogging.EquipmentType:current']),
            ('amp_hours', orm['datalogging.EquipmentType:amp_hours']),
            ('data_storage_capacity', orm['datalogging.EquipmentType:data_storage_capacity']),
            ('manual', orm['datalogging.EquipmentType:manual']),
        ))
        db.send_create_signal('datalogging', ['EquipmentType'])
        
        # Adding model 'Timeseries'
        db.create_table('datalogging_timeseries', (
            ('id', orm['datalogging.Timeseries:id']),
            ('new_since_parsing', orm['datalogging.Timeseries:new_since_parsing']),
            ('non_public', orm['datalogging.Timeseries:non_public']),
            ('logbook_entry', orm['datalogging.Timeseries:logbook_entry']),
            ('notes', orm['datalogging.Timeseries:notes']),
            ('sensor', orm['datalogging.Timeseries:sensor']),
            ('logger_timeseries_id', orm['datalogging.Timeseries:logger_timeseries_id']),
            ('logger', orm['datalogging.Timeseries:logger']),
            ('logger_channel', orm['datalogging.Timeseries:logger_channel']),
            ('location_in_cave', orm['datalogging.Timeseries:location_in_cave']),
            ('import_file', orm['datalogging.Timeseries:import_file']),
            ('data_type', orm['datalogging.Timeseries:data_type']),
        ))
        db.send_create_signal('datalogging', ['Timeseries'])
        
        # Adding model 'DataAquisitionSystem'
        db.create_table('datalogging_dataaquisitionsystem', (
            ('id', orm['datalogging.DataAquisitionSystem:id']),
            ('new_since_parsing', orm['datalogging.DataAquisitionSystem:new_since_parsing']),
            ('non_public', orm['datalogging.DataAquisitionSystem:non_public']),
            ('name', orm['datalogging.DataAquisitionSystem:name']),
            ('description', orm['datalogging.DataAquisitionSystem:description']),
        ))
        db.send_create_signal('datalogging', ['DataAquisitionSystem'])
        
        # Adding ManyToManyField 'DataAquisitionSystem.component'
        db.create_table('datalogging_dataaquisitionsystem_component', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dataaquisitionsystem', models.ForeignKey(orm.DataAquisitionSystem, null=False)),
            ('equipmentitem', models.ForeignKey(orm.EquipmentItem, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Manufacturer'
        db.delete_table('datalogging_manufacturer')
        
        # Deleting model 'EquipmentItem'
        db.delete_table('datalogging_equipmentitem')
        
        # Deleting model 'DataPoint'
        db.delete_table('datalogging_datapoint')
        
        # Deleting model 'EquipmentType'
        db.delete_table('datalogging_equipmenttype')
        
        # Deleting model 'Timeseries'
        db.delete_table('datalogging_timeseries')
        
        # Deleting model 'DataAquisitionSystem'
        db.delete_table('datalogging_dataaquisitionsystem')
        
        # Dropping ManyToManyField 'DataAquisitionSystem.component'
        db.delete_table('datalogging_dataaquisitionsystem_component')
        
    
    
    models = {
        'core.area': {
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Area']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'core.cave': {
            'area': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Area']", 'null': 'True', 'blank': 'True'}),
            'depth': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'description_file': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'equipment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'explorers': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extent': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kataster_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'kataster_status': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'length': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'official_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '160'}),
            'references': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'survex_file': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'survey': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'underground_centre_line': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'underground_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'unofficial_number': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'})
        },
        'core.expedition': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'core.logbookentry': {
            'cave': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Cave']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'expedition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Expedition']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'datalogging.dataaquisitionsystem': {
            'component': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['datalogging.EquipmentItem']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'datalogging.datapoint': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'parent_timeseries': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datalogging.Timeseries']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'datalogging.equipmentitem': {
            'equipment_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datalogging.EquipmentType']"}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'})
        },
        'datalogging.equipmenttype': {
            'amp_hours': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'current': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'data_storage_capacity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'manual': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datalogging.Manufacturer']"}),
            'model_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'voltage': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'datalogging.manufacturer': {
            'name': ('django.db.models.fields.CharField', [], {'max_length': '160', 'primary_key': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'datalogging.timeseries': {
            'data_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'import_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'location_in_cave': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'logbook_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.LogbookEntry']", 'null': 'True', 'blank': 'True'}),
            'logger': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'logger'", 'null': 'True', 'to': "orm['datalogging.EquipmentItem']"}),
            'logger_channel': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'logger_timeseries_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sensor'", 'to': "orm['datalogging.EquipmentItem']"})
        }
    }
    
    complete_apps = ['datalogging']
