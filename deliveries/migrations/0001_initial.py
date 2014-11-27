# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Delivery'
        db.create_table('deliveries_delivery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=3.99, null=True, max_digits=6, decimal_places=2, blank=True)),
        ))
        db.send_create_signal('deliveries', ['Delivery'])


    def backwards(self, orm):
        # Deleting model 'Delivery'
        db.delete_table('deliveries_delivery')


    models = {
        'deliveries.delivery': {
            'Meta': {'object_name': 'Delivery'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '3.99', 'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'})
        }
    }

    complete_apps = ['deliveries']