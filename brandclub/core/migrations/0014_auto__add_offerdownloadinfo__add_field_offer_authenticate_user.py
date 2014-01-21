# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OfferDownloadInfo'
        db.create_table(u'core_offerdownloadinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('offer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='offer_download_info', to=orm['core.Offer'])),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email_id', self.gf('django.db.models.fields.EmailField')(max_length=100, null=True)),
            ('mobile_number', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
        ))
        db.send_create_signal(u'core', ['OfferDownloadInfo'])

        # Adding field 'Offer.authenticate_user'
        db.add_column(u'core_offer', 'authenticate_user',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'OfferDownloadInfo'
        db.delete_table(u'core_offerdownloadinfo')

        # Deleting field 'Offer.authenticate_user'
        db.delete_column(u'core_offer', 'authenticate_user')


    models = {
        u'core.audio': {
            'Meta': {'object_name': 'Audio', '_ormbases': [u'core.Content']},
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'core.brand': {
            'Meta': {'object_name': 'Brand'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'bg_color': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'bg_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'competitors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'competitors_rel_+'", 'null': 'True', 'to': u"orm['core.Brand']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'footfall': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'core.city': {
            'Meta': {'object_name': 'City'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clusters'", 'to': u"orm['core.City']"}),
            'content': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'clusters'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['core.Content']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'map_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clusters'", 'to': u"orm['core.State']"})
        },
        u'core.content': {
            'Meta': {'object_name': 'Content'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content_location': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contents'", 'to': u"orm['core.ContentType']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 2, 19, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'no_of_people_rated': ('django.db.models.fields.BigIntegerField', [], {'default': '1'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'store': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'contents'", 'to': u"orm['core.Store']", 'through': u"orm['core.OrderedStoreContent']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'core.contenttype': {
            'Meta': {'object_name': 'ContentType'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'core.country': {
            'Meta': {'object_name': 'Country'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'name': ('django.db.models.fields.CharField', [], {'default': "'Image_for_slideshow'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'target_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'core.offer': {
            'Meta': {'object_name': 'Offer', '_ormbases': [u'core.Content']},
            'authenticate_user': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'core.offerdownloadinfo': {
            'Meta': {'object_name': 'OfferDownloadInfo'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'email_id': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'offer_download_info'", 'to': u"orm['core.Offer']"}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'core.orderedstorecontent': {
            'Meta': {'ordering': "['order']", 'object_name': 'OrderedStoreContent'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'store_contents'", 'to': u"orm['core.Content']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Store']"})
        },
        u'core.slideshow': {
            'Meta': {'object_name': 'SlideShow', '_ormbases': [u'core.Content']},
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'slideshow'", 'symmetrical': 'False', 'through': u"orm['core.SlideShowImage']", 'to': u"orm['core.Image']"})
        },
        u'core.slideshowimage': {
            'Meta': {'ordering': "['order']", 'object_name': 'SlideShowImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Image']"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slideshow': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.SlideShow']"})
        },
        u'core.state': {
            'Meta': {'object_name': 'State'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.store': {
            'Meta': {'object_name': 'Store'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address_first_line': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'address_second_line': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stores'", 'to': u"orm['core.Brand']"}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stores'", 'to': u"orm['core.City']"}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stores'", 'null': 'True', 'to': u"orm['core.Cluster']"}),
            'contact_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'demo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '6'}),
            'mail_id': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'map_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pin_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '100'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stores'", 'to': u"orm['core.State']"})
        },
        u'core.storefeedback': {
            'Meta': {'object_name': 'StoreFeedback'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'email_id': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'feedback'", 'to': u"orm['core.Store']"})
        },
        u'core.video': {
            'Meta': {'object_name': 'Video', '_ormbases': [u'core.Content']},
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'file': ('core.helpers.ContentTypeRestrictedFileField', [], {'max_length': '100'})
        },
        u'core.wallpaper': {
            'Meta': {'object_name': 'Wallpaper', '_ormbases': [u'core.Content']},
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'core.web': {
            'Meta': {'object_name': 'Web', '_ormbases': [u'core.Content']},
            'content': ('ckeditor.fields.RichTextField', [], {}),
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'core.webcontent': {
            'Meta': {'object_name': 'WebContent', '_ormbases': [u'core.Content']},
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['core']