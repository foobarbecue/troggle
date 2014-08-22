# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Sample.photo'
        db.add_column('samples_sample', 'photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Photo'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Sample.photo'
        db.delete_column('samples_sample', 'photo_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
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
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.area': {
            'Meta': {'object_name': 'Area'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Area']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'core.cave': {
            'Meta': {'object_name': 'Cave'},
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
        'core.entrance': {
            'Meta': {'object_name': 'Entrance'},
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
            'Meta': {'object_name': 'Expedition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'core.logbookentry': {
            'Meta': {'object_name': 'LogbookEntry'},
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
        'core.person': {
            'Meta': {'object_name': 'Person'},
            'affiliation': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'blurb': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'core.photo': {
            'Meta': {'object_name': 'Photo'},
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
            'taken_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photographer'", 'null': 'True', 'to': "orm['core.Person']"})
        },
        'core.qm': {
            'Meta': {'object_name': 'QM'},
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
        'core.surveystation': {
            'Meta': {'object_name': 'SurveyStation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'samples.sample': {
            'Meta': {'object_name': 'Sample'},
            'd18O': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'd2H': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'distance_from_bottom': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'logbook_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.LogbookEntry']", 'null': 'True', 'blank': 'True'}),
            'material': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'part_of': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['samples.Sample']", 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Photo']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['samples']
