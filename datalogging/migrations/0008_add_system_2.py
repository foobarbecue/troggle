
from south.db import db
from django.db import models
from datalogging.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'EquipmentType.amp_hours'
        db.add_column('datalogging_equipmenttype', 'amp_hours', orm['datalogging.equipmenttype:amp_hours'])
        
        # Adding field 'DataAquisitionSystem.description'
        db.add_column('datalogging_dataaquisitionsystem', 'description', orm['datalogging.dataaquisitionsystem:description'])
        
        # Adding field 'EquipmentType.data_storage_capacity'
        db.add_column('datalogging_equipmenttype', 'data_storage_capacity', orm['datalogging.equipmenttype:data_storage_capacity'])
        
        # Deleting field 'EquipmentType.capacity'
        db.delete_column('datalogging_equipmenttype', 'capacity')
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'EquipmentType.amp_hours'
        db.delete_column('datalogging_equipmenttype', 'amp_hours')
        
        # Deleting field 'DataAquisitionSystem.description'
        db.delete_column('datalogging_dataaquisitionsystem', 'description')
        
        # Deleting field 'EquipmentType.data_storage_capacity'
        db.delete_column('datalogging_equipmenttype', 'data_storage_capacity')
        
        # Adding field 'EquipmentType.capacity'
        db.add_column('datalogging_equipmenttype', 'capacity', orm['datalogging.equipmenttype:capacity'])
        
    
    
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
            'kataster_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'kataster_status': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'length': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'official_name': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
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
            'manual': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
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
            'import_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'logbook_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.LogbookEntry']", 'null': 'True', 'blank': 'True'}),
            'logger': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'logger'", 'null': 'True', 'to': "orm['datalogging.EquipmentItem']"}),
            'logger_channel': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'logger_timeseries_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sensor'", 'to': "orm['datalogging.EquipmentItem']"})
        }
    }
    
    complete_apps = ['datalogging']
