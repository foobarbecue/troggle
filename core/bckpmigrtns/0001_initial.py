
from south.db import db
from django.db import models
from core.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Expedition'
        db.create_table('core_expedition', (
            ('id', orm['core.Expedition:id']),
            ('new_since_parsing', orm['core.Expedition:new_since_parsing']),
            ('non_public', orm['core.Expedition:non_public']),
            ('year', orm['core.Expedition:year']),
            ('name', orm['core.Expedition:name']),
        ))
        db.send_create_signal('core', ['Expedition'])
        
        # Adding model 'LogbookEntry'
        db.create_table('core_logbookentry', (
            ('id', orm['core.LogbookEntry:id']),
            ('new_since_parsing', orm['core.LogbookEntry:new_since_parsing']),
            ('non_public', orm['core.LogbookEntry:non_public']),
            ('date', orm['core.LogbookEntry:date']),
            ('expedition', orm['core.LogbookEntry:expedition']),
            ('title', orm['core.LogbookEntry:title']),
            ('cave', orm['core.LogbookEntry:cave']),
            ('place', orm['core.LogbookEntry:place']),
            ('text', orm['core.LogbookEntry:text']),
            ('slug', orm['core.LogbookEntry:slug']),
        ))
        db.send_create_signal('core', ['LogbookEntry'])
        
        # Adding model 'QM'
        db.create_table('core_qm', (
            ('id', orm['core.QM:id']),
            ('new_since_parsing', orm['core.QM:new_since_parsing']),
            ('non_public', orm['core.QM:non_public']),
            ('found_by', orm['core.QM:found_by']),
            ('ticked_off_by', orm['core.QM:ticked_off_by']),
            ('number', orm['core.QM:number']),
            ('grade', orm['core.QM:grade']),
            ('location_description', orm['core.QM:location_description']),
            ('nearest_station_description', orm['core.QM:nearest_station_description']),
            ('nearest_station', orm['core.QM:nearest_station']),
            ('area', orm['core.QM:area']),
            ('completion_description', orm['core.QM:completion_description']),
            ('comment', orm['core.QM:comment']),
        ))
        db.send_create_signal('core', ['QM'])
        
        # Adding model 'Survey'
        db.create_table('core_survey', (
            ('id', orm['core.Survey:id']),
            ('new_since_parsing', orm['core.Survey:new_since_parsing']),
            ('non_public', orm['core.Survey:non_public']),
            ('expedition', orm['core.Survey:expedition']),
            ('wallet_number', orm['core.Survey:wallet_number']),
            ('wallet_letter', orm['core.Survey:wallet_letter']),
            ('comments', orm['core.Survey:comments']),
            ('location', orm['core.Survey:location']),
            ('subcave', orm['core.Survey:subcave']),
            ('survex_block', orm['core.Survey:survex_block']),
            ('logbook_entry', orm['core.Survey:logbook_entry']),
            ('centreline_printed_on', orm['core.Survey:centreline_printed_on']),
            ('centreline_printed_by', orm['core.Survey:centreline_printed_by']),
            ('tunnel_file', orm['core.Survey:tunnel_file']),
            ('tunnel_main_sketch', orm['core.Survey:tunnel_main_sketch']),
            ('integrated_into_main_sketch_on', orm['core.Survey:integrated_into_main_sketch_on']),
            ('integrated_into_main_sketch_by', orm['core.Survey:integrated_into_main_sketch_by']),
            ('rendered_image', orm['core.Survey:rendered_image']),
        ))
        db.send_create_signal('core', ['Survey'])
        
        # Adding model 'SurvexScanSingle'
        db.create_table('core_survexscansingle', (
            ('id', orm['core.SurvexScanSingle:id']),
            ('ffile', orm['core.SurvexScanSingle:ffile']),
            ('name', orm['core.SurvexScanSingle:name']),
            ('survexscansfolder', orm['core.SurvexScanSingle:survexscansfolder']),
        ))
        db.send_create_signal('core', ['SurvexScanSingle'])
        
        # Adding model 'ScannedImage'
        db.create_table('core_scannedimage', (
            ('id', orm['core.ScannedImage:id']),
            ('new_since_parsing', orm['core.ScannedImage:new_since_parsing']),
            ('file', orm['core.ScannedImage:file']),
            ('scanned_by', orm['core.ScannedImage:scanned_by']),
            ('scanned_on', orm['core.ScannedImage:scanned_on']),
            ('survey', orm['core.ScannedImage:survey']),
            ('contents', orm['core.ScannedImage:contents']),
            ('number_in_wallet', orm['core.ScannedImage:number_in_wallet']),
        ))
        db.send_create_signal('core', ['ScannedImage'])
        
        # Adding model 'SurvexDirectory'
        db.create_table('core_survexdirectory', (
            ('id', orm['core.SurvexDirectory:id']),
            ('path', orm['core.SurvexDirectory:path']),
            ('cave', orm['core.SurvexDirectory:cave']),
            ('primarysurvexfile', orm['core.SurvexDirectory:primarysurvexfile']),
        ))
        db.send_create_signal('core', ['SurvexDirectory'])
        
        # Adding model 'Cave'
        db.create_table('core_cave', (
            ('id', orm['core.Cave:id']),
            ('new_since_parsing', orm['core.Cave:new_since_parsing']),
            ('non_public', orm['core.Cave:non_public']),
            ('official_name', orm['core.Cave:official_name']),
            ('slug', orm['core.Cave:slug']),
            ('kataster_code', orm['core.Cave:kataster_code']),
            ('kataster_number', orm['core.Cave:kataster_number']),
            ('unofficial_number', orm['core.Cave:unofficial_number']),
            ('explorers', orm['core.Cave:explorers']),
            ('underground_description', orm['core.Cave:underground_description']),
            ('equipment', orm['core.Cave:equipment']),
            ('references', orm['core.Cave:references']),
            ('survey', orm['core.Cave:survey']),
            ('kataster_status', orm['core.Cave:kataster_status']),
            ('underground_centre_line', orm['core.Cave:underground_centre_line']),
            ('notes', orm['core.Cave:notes']),
            ('length', orm['core.Cave:length']),
            ('depth', orm['core.Cave:depth']),
            ('extent', orm['core.Cave:extent']),
            ('survex_file', orm['core.Cave:survex_file']),
            ('description_file', orm['core.Cave:description_file']),
        ))
        db.send_create_signal('core', ['Cave'])
        
        # Adding model 'PersonTrip'
        db.create_table('core_persontrip', (
            ('id', orm['core.PersonTrip:id']),
            ('new_since_parsing', orm['core.PersonTrip:new_since_parsing']),
            ('non_public', orm['core.PersonTrip:non_public']),
            ('personexpedition', orm['core.PersonTrip:personexpedition']),
            ('time_underground', orm['core.PersonTrip:time_underground']),
            ('logbook_entry', orm['core.PersonTrip:logbook_entry']),
            ('is_logbook_entry_author', orm['core.PersonTrip:is_logbook_entry_author']),
        ))
        db.send_create_signal('core', ['PersonTrip'])
        
        # Adding model 'SurvexBlock'
        db.create_table('core_survexblock', (
            ('id', orm['core.SurvexBlock:id']),
            ('name', orm['core.SurvexBlock:name']),
            ('parent', orm['core.SurvexBlock:parent']),
            ('text', orm['core.SurvexBlock:text']),
            ('cave', orm['core.SurvexBlock:cave']),
            ('date', orm['core.SurvexBlock:date']),
            ('expedition', orm['core.SurvexBlock:expedition']),
            ('survexfile', orm['core.SurvexBlock:survexfile']),
            ('begin_char', orm['core.SurvexBlock:begin_char']),
            ('survexpath', orm['core.SurvexBlock:survexpath']),
            ('survexscansfolder', orm['core.SurvexBlock:survexscansfolder']),
            ('totalleglength', orm['core.SurvexBlock:totalleglength']),
        ))
        db.send_create_signal('core', ['SurvexBlock'])
        
        # Adding model 'TunnelFile'
        db.create_table('core_tunnelfile', (
            ('id', orm['core.TunnelFile:id']),
            ('tunnelpath', orm['core.TunnelFile:tunnelpath']),
            ('tunnelname', orm['core.TunnelFile:tunnelname']),
            ('bfontcolours', orm['core.TunnelFile:bfontcolours']),
            ('filesize', orm['core.TunnelFile:filesize']),
            ('npaths', orm['core.TunnelFile:npaths']),
        ))
        db.send_create_signal('core', ['TunnelFile'])
        
        # Adding model 'Person'
        db.create_table('core_person', (
            ('id', orm['core.Person:id']),
            ('new_since_parsing', orm['core.Person:new_since_parsing']),
            ('non_public', orm['core.Person:non_public']),
            ('first_name', orm['core.Person:first_name']),
            ('last_name', orm['core.Person:last_name']),
            ('affiliation', orm['core.Person:affiliation']),
            ('blurb', orm['core.Person:blurb']),
            ('user', orm['core.Person:user']),
        ))
        db.send_create_signal('core', ['Person'])
        
        # Adding model 'SurvexTitle'
        db.create_table('core_survextitle', (
            ('id', orm['core.SurvexTitle:id']),
            ('survexblock', orm['core.SurvexTitle:survexblock']),
            ('title', orm['core.SurvexTitle:title']),
            ('cave', orm['core.SurvexTitle:cave']),
        ))
        db.send_create_signal('core', ['SurvexTitle'])
        
        # Adding model 'NewSubCave'
        db.create_table('core_newsubcave', (
            ('id', orm['core.NewSubCave:id']),
            ('new_since_parsing', orm['core.NewSubCave:new_since_parsing']),
            ('non_public', orm['core.NewSubCave:non_public']),
            ('name', orm['core.NewSubCave:name']),
        ))
        db.send_create_signal('core', ['NewSubCave'])
        
        # Adding model 'Entrance'
        db.create_table('core_entrance', (
            ('id', orm['core.Entrance:id']),
            ('new_since_parsing', orm['core.Entrance:new_since_parsing']),
            ('non_public', orm['core.Entrance:non_public']),
            ('location', orm['core.Entrance:location']),
            ('name', orm['core.Entrance:name']),
            ('entrance_description', orm['core.Entrance:entrance_description']),
            ('explorers', orm['core.Entrance:explorers']),
            ('map_description', orm['core.Entrance:map_description']),
            ('location_description', orm['core.Entrance:location_description']),
            ('approach', orm['core.Entrance:approach']),
            ('underground_description', orm['core.Entrance:underground_description']),
            ('photo', orm['core.Entrance:photo']),
            ('marking', orm['core.Entrance:marking']),
            ('marking_comment', orm['core.Entrance:marking_comment']),
            ('findability', orm['core.Entrance:findability']),
            ('findability_description', orm['core.Entrance:findability_description']),
            ('tag_station', orm['core.Entrance:tag_station']),
            ('exact_station', orm['core.Entrance:exact_station']),
            ('other_station', orm['core.Entrance:other_station']),
            ('other_description', orm['core.Entrance:other_description']),
            ('bearings', orm['core.Entrance:bearings']),
        ))
        db.send_create_signal('core', ['Entrance'])
        
        # Adding model 'SurveyStation'
        db.create_table('core_surveystation', (
            ('id', orm['core.SurveyStation:id']),
            ('new_since_parsing', orm['core.SurveyStation:new_since_parsing']),
            ('non_public', orm['core.SurveyStation:non_public']),
            ('name', orm['core.SurveyStation:name']),
        ))
        db.send_create_signal('core', ['SurveyStation'])
        
        # Adding model 'SurvexPersonRole'
        db.create_table('core_survexpersonrole', (
            ('id', orm['core.SurvexPersonRole:id']),
            ('survexblock', orm['core.SurvexPersonRole:survexblock']),
            ('nrole', orm['core.SurvexPersonRole:nrole']),
            ('personname', orm['core.SurvexPersonRole:personname']),
            ('person', orm['core.SurvexPersonRole:person']),
            ('personexpedition', orm['core.SurvexPersonRole:personexpedition']),
            ('persontrip', orm['core.SurvexPersonRole:persontrip']),
        ))
        db.send_create_signal('core', ['SurvexPersonRole'])
        
        # Adding model 'SurvexEquate'
        db.create_table('core_survexequate', (
            ('id', orm['core.SurvexEquate:id']),
            ('cave', orm['core.SurvexEquate:cave']),
        ))
        db.send_create_signal('core', ['SurvexEquate'])
        
        # Adding model 'Area'
        db.create_table('core_area', (
            ('id', orm['core.Area:id']),
            ('new_since_parsing', orm['core.Area:new_since_parsing']),
            ('non_public', orm['core.Area:non_public']),
            ('name', orm['core.Area:name']),
            ('slug', orm['core.Area:slug']),
            ('description', orm['core.Area:description']),
            ('parent', orm['core.Area:parent']),
        ))
        db.send_create_signal('core', ['Area'])
        
        # Adding model 'CaveDescription'
        db.create_table('core_cavedescription', (
            ('id', orm['core.CaveDescription:id']),
            ('new_since_parsing', orm['core.CaveDescription:new_since_parsing']),
            ('non_public', orm['core.CaveDescription:non_public']),
            ('short_name', orm['core.CaveDescription:short_name']),
            ('long_name', orm['core.CaveDescription:long_name']),
            ('description', orm['core.CaveDescription:description']),
        ))
        db.send_create_signal('core', ['CaveDescription'])
        
        # Adding model 'Photo'
        db.create_table('core_photo', (
            ('id', orm['core.Photo:id']),
            ('new_since_parsing', orm['core.Photo:new_since_parsing']),
            ('caption', orm['core.Photo:caption']),
            ('contains_logbookentry', orm['core.Photo:contains_logbookentry']),
            ('file', orm['core.Photo:file']),
            ('is_mugshot', orm['core.Photo:is_mugshot']),
            ('contains_cave', orm['core.Photo:contains_cave']),
            ('contains_entrance', orm['core.Photo:contains_entrance']),
            ('nearest_survey_point', orm['core.Photo:nearest_survey_point']),
            ('nearest_QM', orm['core.Photo:nearest_QM']),
            ('location', orm['core.Photo:location']),
            ('slug', orm['core.Photo:slug']),
        ))
        db.send_create_signal('core', ['Photo'])
        
        # Adding model 'SurvexFile'
        db.create_table('core_survexfile', (
            ('id', orm['core.SurvexFile:id']),
            ('path', orm['core.SurvexFile:path']),
            ('survexdirectory', orm['core.SurvexFile:survexdirectory']),
            ('cave', orm['core.SurvexFile:cave']),
        ))
        db.send_create_signal('core', ['SurvexFile'])
        
        # Adding model 'PersonExpedition'
        db.create_table('core_personexpedition', (
            ('id', orm['core.PersonExpedition:id']),
            ('new_since_parsing', orm['core.PersonExpedition:new_since_parsing']),
            ('non_public', orm['core.PersonExpedition:non_public']),
            ('expedition', orm['core.PersonExpedition:expedition']),
            ('person', orm['core.PersonExpedition:person']),
            ('is_guest', orm['core.PersonExpedition:is_guest']),
            ('position', orm['core.PersonExpedition:position']),
            ('nickname', orm['core.PersonExpedition:nickname']),
        ))
        db.send_create_signal('core', ['PersonExpedition'])
        
        # Adding model 'SurvexLeg'
        db.create_table('core_survexleg', (
            ('id', orm['core.SurvexLeg:id']),
            ('block', orm['core.SurvexLeg:block']),
            ('stationfrom', orm['core.SurvexLeg:stationfrom']),
            ('stationto', orm['core.SurvexLeg:stationto']),
            ('tape', orm['core.SurvexLeg:tape']),
            ('compass', orm['core.SurvexLeg:compass']),
            ('clino', orm['core.SurvexLeg:clino']),
        ))
        db.send_create_signal('core', ['SurvexLeg'])
        
        # Adding model 'SurvexScansFolder'
        db.create_table('core_survexscansfolder', (
            ('id', orm['core.SurvexScansFolder:id']),
            ('fpath', orm['core.SurvexScansFolder:fpath']),
            ('walletname', orm['core.SurvexScansFolder:walletname']),
        ))
        db.send_create_signal('core', ['SurvexScansFolder'])
        
        # Adding model 'CaveAndEntrance'
        db.create_table('core_caveandentrance', (
            ('id', orm['core.CaveAndEntrance:id']),
            ('new_since_parsing', orm['core.CaveAndEntrance:new_since_parsing']),
            ('non_public', orm['core.CaveAndEntrance:non_public']),
            ('cave', orm['core.CaveAndEntrance:cave']),
            ('entrance', orm['core.CaveAndEntrance:entrance']),
            ('entrance_letter', orm['core.CaveAndEntrance:entrance_letter']),
        ))
        db.send_create_signal('core', ['CaveAndEntrance'])
        
        # Adding model 'SurvexStation'
        db.create_table('core_survexstation', (
            ('id', orm['core.SurvexStation:id']),
            ('name', orm['core.SurvexStation:name']),
            ('block', orm['core.SurvexStation:block']),
            ('equate', orm['core.SurvexStation:equate']),
        ))
        db.send_create_signal('core', ['SurvexStation'])
        
        # Adding model 'OtherCaveName'
        db.create_table('core_othercavename', (
            ('id', orm['core.OtherCaveName:id']),
            ('new_since_parsing', orm['core.OtherCaveName:new_since_parsing']),
            ('non_public', orm['core.OtherCaveName:non_public']),
            ('name', orm['core.OtherCaveName:name']),
            ('cave', orm['core.OtherCaveName:cave']),
        ))
        db.send_create_signal('core', ['OtherCaveName'])
        
        # Adding ManyToManyField 'TunnelFile.survexscansfolders'
        db.create_table('core_tunnelfile_survexscansfolders', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tunnelfile', models.ForeignKey(orm.TunnelFile, null=False)),
            ('survexscansfolder', models.ForeignKey(orm.SurvexScansFolder, null=False))
        ))
        
        # Adding ManyToManyField 'TunnelFile.survexblocks'
        db.create_table('core_tunnelfile_survexblocks', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tunnelfile', models.ForeignKey(orm.TunnelFile, null=False)),
            ('survexblock', models.ForeignKey(orm.SurvexBlock, null=False))
        ))
        
        # Adding ManyToManyField 'CaveDescription.linked_subcaves'
        db.create_table('core_cavedescription_linked_subcaves', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cavedescription', models.ForeignKey(orm.CaveDescription, null=False)),
            ('newsubcave', models.ForeignKey(orm.NewSubCave, null=False))
        ))
        
        # Adding ManyToManyField 'Cave.area'
        db.create_table('core_cave_area', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cave', models.ForeignKey(orm.Cave, null=False)),
            ('area', models.ForeignKey(orm.Area, null=False))
        ))
        
        # Adding ManyToManyField 'CaveDescription.linked_entrances'
        db.create_table('core_cavedescription_linked_entrances', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cavedescription', models.ForeignKey(orm.CaveDescription, null=False)),
            ('entrance', models.ForeignKey(orm.Entrance, null=False))
        ))
        
        # Adding ManyToManyField 'CaveDescription.linked_qms'
        db.create_table('core_cavedescription_linked_qms', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cavedescription', models.ForeignKey(orm.CaveDescription, null=False)),
            ('qm', models.ForeignKey(orm.QM, null=False))
        ))
        
        # Adding ManyToManyField 'TunnelFile.survexscans'
        db.create_table('core_tunnelfile_survexscans', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tunnelfile', models.ForeignKey(orm.TunnelFile, null=False)),
            ('survexscansingle', models.ForeignKey(orm.SurvexScanSingle, null=False))
        ))
        
        # Adding ManyToManyField 'TunnelFile.survextitles'
        db.create_table('core_tunnelfile_survextitles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tunnelfile', models.ForeignKey(orm.TunnelFile, null=False)),
            ('survextitle', models.ForeignKey(orm.SurvexTitle, null=False))
        ))
        
        # Adding ManyToManyField 'TunnelFile.tunnelcontains'
        db.create_table('core_tunnelfile_tunnelcontains', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_tunnelfile', models.ForeignKey(orm.TunnelFile, null=False)),
            ('to_tunnelfile', models.ForeignKey(orm.TunnelFile, null=False))
        ))
        
        # Adding ManyToManyField 'Photo.contains_person'
        db.create_table('core_photo_contains_person', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('photo', models.ForeignKey(orm.Photo, null=False)),
            ('person', models.ForeignKey(orm.Person, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Expedition'
        db.delete_table('core_expedition')
        
        # Deleting model 'LogbookEntry'
        db.delete_table('core_logbookentry')
        
        # Deleting model 'QM'
        db.delete_table('core_qm')
        
        # Deleting model 'Survey'
        db.delete_table('core_survey')
        
        # Deleting model 'SurvexScanSingle'
        db.delete_table('core_survexscansingle')
        
        # Deleting model 'ScannedImage'
        db.delete_table('core_scannedimage')
        
        # Deleting model 'SurvexDirectory'
        db.delete_table('core_survexdirectory')
        
        # Deleting model 'Cave'
        db.delete_table('core_cave')
        
        # Deleting model 'PersonTrip'
        db.delete_table('core_persontrip')
        
        # Deleting model 'SurvexBlock'
        db.delete_table('core_survexblock')
        
        # Deleting model 'TunnelFile'
        db.delete_table('core_tunnelfile')
        
        # Deleting model 'Person'
        db.delete_table('core_person')
        
        # Deleting model 'SurvexTitle'
        db.delete_table('core_survextitle')
        
        # Deleting model 'NewSubCave'
        db.delete_table('core_newsubcave')
        
        # Deleting model 'Entrance'
        db.delete_table('core_entrance')
        
        # Deleting model 'SurveyStation'
        db.delete_table('core_surveystation')
        
        # Deleting model 'SurvexPersonRole'
        db.delete_table('core_survexpersonrole')
        
        # Deleting model 'SurvexEquate'
        db.delete_table('core_survexequate')
        
        # Deleting model 'Area'
        db.delete_table('core_area')
        
        # Deleting model 'CaveDescription'
        db.delete_table('core_cavedescription')
        
        # Deleting model 'Photo'
        db.delete_table('core_photo')
        
        # Deleting model 'SurvexFile'
        db.delete_table('core_survexfile')
        
        # Deleting model 'PersonExpedition'
        db.delete_table('core_personexpedition')
        
        # Deleting model 'SurvexLeg'
        db.delete_table('core_survexleg')
        
        # Deleting model 'SurvexScansFolder'
        db.delete_table('core_survexscansfolder')
        
        # Deleting model 'CaveAndEntrance'
        db.delete_table('core_caveandentrance')
        
        # Deleting model 'SurvexStation'
        db.delete_table('core_survexstation')
        
        # Deleting model 'OtherCaveName'
        db.delete_table('core_othercavename')
        
        # Dropping ManyToManyField 'TunnelFile.survexscansfolders'
        db.delete_table('core_tunnelfile_survexscansfolders')
        
        # Dropping ManyToManyField 'TunnelFile.survexblocks'
        db.delete_table('core_tunnelfile_survexblocks')
        
        # Dropping ManyToManyField 'CaveDescription.linked_subcaves'
        db.delete_table('core_cavedescription_linked_subcaves')
        
        # Dropping ManyToManyField 'Cave.area'
        db.delete_table('core_cave_area')
        
        # Dropping ManyToManyField 'CaveDescription.linked_entrances'
        db.delete_table('core_cavedescription_linked_entrances')
        
        # Dropping ManyToManyField 'CaveDescription.linked_qms'
        db.delete_table('core_cavedescription_linked_qms')
        
        # Dropping ManyToManyField 'TunnelFile.survexscans'
        db.delete_table('core_tunnelfile_survexscans')
        
        # Dropping ManyToManyField 'TunnelFile.survextitles'
        db.delete_table('core_tunnelfile_survextitles')
        
        # Dropping ManyToManyField 'TunnelFile.tunnelcontains'
        db.delete_table('core_tunnelfile_tunnelcontains')
        
        # Dropping ManyToManyField 'Photo.contains_person'
        db.delete_table('core_photo_contains_person')
        
    
    
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
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
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
