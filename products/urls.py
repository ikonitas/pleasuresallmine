# coding=utf-8

from django.conf.urls import patterns, url


urlpatterns = patterns(
    'products.views',
    url(r'^([\w\-]+)/([\w\-]+)/([\w\-]+)/$',
        'view_product',
        name='view-product',
    ),
)
