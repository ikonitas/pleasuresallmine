from django.conf.urls import patterns, url


urlpatterns = patterns('',
        url(r'^$', 'categories.views.category', name='category'),
        url(r'^(?P<children_slug>[-\w]+)/$', 'categories.views.list_products',),
        )
