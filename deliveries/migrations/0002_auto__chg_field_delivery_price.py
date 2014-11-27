# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Delivery.price'
        db.alter_column('deliveries_delivery', 'price', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

    def backwards(self, orm):

        # Changing field 'Delivery.price'
        db.alter_column('deliveries_delivery', 'price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2))

    models = {
        'deliveries.delivery': {
            'Meta': {'object_name': 'Delivery'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'price': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['deliveries']