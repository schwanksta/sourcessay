# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Author.slug'
        db.add_column('sourcessay_author', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default=None, max_length=255, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Author.slug'
        db.delete_column('sourcessay_author', 'slug')


    models = {
        'sourcessay.author': {
            'Meta': {'object_name': 'Author'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'news_outlet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sourcessay.Outlet']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': 'None', 'max_length': '255', 'null': 'True'})
        },
        'sourcessay.item': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Item'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sourcessay.Author']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_used': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'news_outlet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sourcessay.Outlet']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'source_feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sourcessay.Source']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'sourcessay.outlet': {
            'Meta': {'object_name': 'Outlet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'sourcessay.source': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Source'},
            'feed_handler': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'feed_url': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['sourcessay']