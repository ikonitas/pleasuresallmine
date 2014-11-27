from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'core.views.home', name='home'),
    #url(r'^pleasuresallmine/', include('pleasuresallmine.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', include('accounts.urls')),
    url(r'^basket/', include('baskets.urls')),
    url(r'^logout/$', 'accounts.views.logout_view'),
    url(r'^search/$', 'search.views.search_products'),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^filebrowser/', include('filebrowser.urls')),
    url(r'^infopage/', include('infopages.urls')),
    url(r'^my-orders/$', 'orders.views.my_orders'),
    url(r'^thank-you/$', direct_to_template, {'template': 'thank_you.html'}),
    url(r'notifying/', 'paypal.standard.ipn.views.ipn', name='paypal-ipn'),
    url(r'(?P<slug>[-\w]+)/', include('categories.urls')),
    url('', include('products.urls'))
)


from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
   )
