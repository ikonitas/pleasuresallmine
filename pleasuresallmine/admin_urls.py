# coding=utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
from accounts.views import edit_customer, add_customer
from orders.views import view_order, view_invoice
from orders.ajax import get_price

admin.autodiscover()

urlpatterns = patterns(
        '',
        (r'', include(admin.site.urls)),
        (r'^accounts/userprofile/(\d+)/$', edit_customer),
        (r'^accounts/userprofile/add/$', add_customer),
        (r'^orders/order/(\d+)/$', view_order),
        (r'^orders/order/(\d+)/html-invoice/$', view_invoice),
        (r'^orders/order/get-price/$', get_price),
)
