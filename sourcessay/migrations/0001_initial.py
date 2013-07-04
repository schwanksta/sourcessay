# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Source'
        db.create_table('sourcessay_source', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('feed_url', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('feed_handler', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('sourcessay', ['Source'])

        # Adding model 'Outlet'
        db.create_table('sourcessay_outlet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('sourcessay', ['Outlet'])

        # Adding model 'Author'
        db.create_table('sourcessay_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('news_outlet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sourcessay.Outlet'])),
        ))
        db.send_create_signal('sourcessay', ['Author'])

        # Adding model 'Item'
        db.create_table('sourcessay_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sourcessay.Source'])),
            ('news_outlet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sourcessay.Outlet'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('line_used', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('sourcessay', ['Item'])

        # Adding M2M table for field authors on 'Item'
        m2m_table_name = db.shorten_name('sourcessay_item_authors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm['sourcessay.item'], null=False)),
            ('author', models.ForeignKey(orm['sourcessay.author'], null=False))
        ))
        db.create_unique(m2m_table_name, ['item_id', 'author_id'])


    def backwards(self, orm):
        # Deleting model 'Source'
        db.delete_table('sourcessay_source')

        # Deleting model 'Outlet'
        db.delete_table('sourcessay_outlet')

        # Deleting model 'Author'
        db.delete_table('sourcessay_author')

        # Deleting model 'Item'
        db.delete_table('sourcessay_item')

        # Removing M2M table for field authors on 'Item'
        db.delete_table(db.shorten_name('sourcessay_item_authors'))


    models = {
        'sourcessay.author': {
            'Meta': {'object_name': 'Author'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'news_outlet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sourcessay.Outlet']"})
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