# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Content.show_on_home'
        db.alter_column(u'core_content', 'show_on_home', self.gf('django.db.models.fields.BooleanField')())

    def backwards(self, orm):

        # Changing field 'Content.show_on_home'
        db.alter_column(u'core_content', 'show_on_home', self.gf('django.db.models.fields.NullBooleanField')(null=True))

    models = {
        u'core.audio': {
            'Meta': {'object_name': 'Audio', '_ormbases': [u'core.Content']},
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'core.brand': {
            'Meta': {'object_name': 'Brand'},
            'bg_color': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'bg_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'core.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'city': ('django.db.models.fields.CharField', [], {'default': "'Bangalore'", 'max_length': '100'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'Karnataka'", 'max_length': '100'})
        },
        u'core.content': {
            'Meta': {'object_name': 'Content'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contents'", 'to': u"orm['core.ContentType']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'no_of_people_rated': ('django.db.models.fields.BigIntegerField', [], {'default': '1'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'show_on_home': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contents'", 'null': 'True', 'to': u"orm['core.Store']"}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'core.contenttype': {
            'Meta': {'object_name': 'ContentType'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'core.device': {
            'Meta': {'object_name': 'Device'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'device_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mac_address': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'devices'", 'null': 'True', 'to': u"orm['core.Store']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'core.image': {
            'Meta': {'object_name': 'Image'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'target_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'core.slideshow': {
            'Meta': {'object_name': 'SlideShow', '_ormbases': [u'core.Content']},
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'slideshow'", 'symmetrical': 'False', 'to': u"orm['core.Image']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'core.store': {
            'Meta': {'object_name': 'Store'},
            'address_first_line': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'address_second_line': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stores'", 'to': u"orm['core.Brand']"}),
            'city': ('django.db.models.fields.CharField', [], {'default': "'Bangalore'", 'max_length': '50'}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stores'", 'null': 'True', 'to': u"orm['core.Cluster']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pin_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'Karnataka'", 'max_length': '50'})
        },
        u'core.video': {
            'Meta': {'object_name': 'Video', '_ormbases': [u'core.Content']},
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'core.wallpaper': {
            'Meta': {'object_name': 'Wallpaper', '_ormbases': [u'core.Content']},
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'core.web': {
            'Meta': {'object_name': 'Web', '_ormbases': [u'core.Content']},
            'content': ('django.db.models.fields.TextField', [], {}),
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['core']