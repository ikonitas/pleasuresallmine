# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Basket'
        db.delete_table('baskets_basket')


    def backwards(self, orm):
        # Adding model 'Basket'
        db.create_table('baskets_basket', (
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='song', to=orm['products.Product'])),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('basket_id', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('baskets', ['Basket'])


    models = {
        
    }

    complete_apps = ['baskets']