from django.conf.urls import patterns, url


urlpatterns = patterns('infopages.views',
    url(r'(?P<slug>[-\w]+)/$', 'view_page',),
    )
