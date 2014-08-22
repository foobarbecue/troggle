
from south.db import db
from django.db import models
from core.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Entrance.equipment'
        db.add_column('core_entrance', 'equipment', orm['core.entrance:equipment'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Entrance.equipment'
        db.delete_column('core_entrance', 'equipment')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
        'core.caveandentrance': {
            'cave': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Cave']"}),
            'entrance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Entrance']"}),
            'entrance_letter': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'core.cavedescription': {
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linked_entrances': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Entrance']", 'null': 'True', 'blank': 'True'}),
            'linked_qms': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.QM']", 'null': 'True', 'blank': 'True'}),
            'linked_subcaves': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.NewSubCave']", 'null': 'True', 'blank': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'core.entrance': {
            'approach': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'bearings': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'entrance_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'equipment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'exact_station': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'exact_station'", 'null': 'True', 'to': "orm['core.SurveyStation']"}),
            'explorers': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'findability': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'findability_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'location_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'map_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'marking': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'marking_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'other_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'other_station': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'other_station'", 'null': 'True', 'to': "orm['core.SurveyStation']"}),
            'photo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tag_station': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tag_station'", 'null': 'True', 'to': "orm['core.SurveyStation']"}),
            'underground_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
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
        'core.newsubcave': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'core.othercavename': {
            'cave': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Cave']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'core.person': {
            'affiliation': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'blurb': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'core.personexpedition': {
            'expedition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Expedition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_guest': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Person']"}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'core.persontrip': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_logbook_entry_author': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'logbook_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.LogbookEntry']"}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'personexpedition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.PersonExpedition']", 'null': 'True'}),
            'time_underground': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'core.photo': {
            'caption': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contains_cave': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Cave']", 'null': 'True', 'blank': 'True'}),
            'contains_entrance': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photo_file'", 'null': 'True', 'to': "orm['core.Entrance']"}),
            'contains_logbookentry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.LogbookEntry']", 'null': 'True', 'blank': 'True'}),
            'contains_person': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Person']", 'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_mugshot': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'nearest_QM': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.QM']", 'null': 'True', 'blank': 'True'}),
            'nearest_survey_point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurveyStation']", 'null': 'True', 'blank': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'taken_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.PersonTrip']", 'null': 'True', 'blank': 'True'})
        },
        'core.qm': {
            'area': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'completion_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'found_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'QMs_found'", 'null': 'True', 'to': "orm['core.LogbookEntry']"}),
            'grade': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'nearest_station': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'nearest_station_description': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'ticked_off_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'QMs_ticked_off'", 'null': 'True', 'to': "orm['core.LogbookEntry']"})
        },
        'core.scannedimage': {
            'contents': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'number_in_wallet': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'scanned_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Person']", 'null': 'True', 'blank': 'True'}),
            'scanned_on': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Survey']"})
        },
        'core.survexblock': {
            'begin_char': ('django.db.models.fields.IntegerField', [], {}),
            'cave': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Cave']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'expedition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Expedition']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurvexBlock']", 'null': 'True', 'blank': 'True'}),
            'survexfile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurvexFile']", 'null': 'True', 'blank': 'True'}),
            'survexpath': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'survexscansfolder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurvexScansFolder']", 'null': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'totalleglength': ('django.db.models.fields.FloatField', [], {})
        },
        'core.survexdirectory': {
            'cave': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Cave']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'primarysurvexfile': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'primarysurvexfile'", 'null': 'True', 'to': "orm['core.SurvexFile']"})
        },
        'core.survexequate': {
            'cave': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Cave']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'core.survexfile': {
            'cave': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Cave']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'survexdirectory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurvexDirectory']", 'null': 'True', 'blank': 'True'})
        },
        'core.survexleg': {
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurvexBlock']"}),
            'clino': ('django.db.models.fields.FloatField', [], {}),
            'compass': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stationfrom': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stationfrom'", 'to': "orm['core.SurvexStation']"}),
            'stationto': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stationto'", 'to': "orm['core.SurvexStation']"}),
            'tape': ('django.db.models.fields.FloatField', [], {})
        },
        'core.survexpersonrole': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nrole': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Person']", 'null': 'True', 'blank': 'True'}),
            'personexpedition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.PersonExpedition']", 'null': 'True', 'blank': 'True'}),
            'personname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'persontrip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.PersonTrip']", 'null': 'True', 'blank': 'True'}),
            'survexblock': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurvexBlock']"})
        },
        'core.survexscansfolder': {
            'fpath': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'walletname': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.survexscansingle': {
            'ffile': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'survexscansfolder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurvexScansFolder']", 'null': 'True'})
        },
        'core.survexstation': {
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurvexBlock']"}),
            'equate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurvexEquate']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'core.survextitle': {
            'cave': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Cave']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'survexblock': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurvexBlock']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.survey': {
            'centreline_printed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'centreline_printed_by'", 'null': 'True', 'to': "orm['core.Person']"}),
            'centreline_printed_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'expedition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Expedition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'integrated_into_main_sketch_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'integrated_into_main_sketch_by'", 'null': 'True', 'to': "orm['core.Person']"}),
            'integrated_into_main_sketch_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'logbook_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.LogbookEntry']"}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'rendered_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'subcave': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.NewSubCave']", 'null': 'True', 'blank': 'True'}),
            'survex_block': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.SurvexBlock']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'tunnel_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tunnel_main_sketch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Survey']", 'null': 'True', 'blank': 'True'}),
            'wallet_letter': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'wallet_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'core.surveystation': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'core.tunnelfile': {
            'bfontcolours': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'filesize': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'npaths': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'survexblocks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.SurvexBlock']"}),
            'survexscans': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.SurvexScanSingle']"}),
            'survexscansfolders': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.SurvexScansFolder']"}),
            'survextitles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.SurvexTitle']"}),
            'tunnelcontains': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.TunnelFile']"}),
            'tunnelname': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tunnelpath': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }
    
    complete_apps = ['core']
