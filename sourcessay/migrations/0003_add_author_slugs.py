# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.template.defaultfilters import slugify

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        for author in orm.Author.objects.all():
            author.slug = slugify(author.name)
            author.save()

    def backwards(self, orm):
        "Write your backwards methods here."
        pass

    models = {
        'sourcessay.author': {
            'Meta': {'object_name': 'Author'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'news_outlet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sourcessay.Outlet']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
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
    symmetrical = True
