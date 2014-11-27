from django.conf.urls import patterns, include, url
from accounts.views import thank_you, login_register


urlpatterns = patterns('',
    url(r'^$', login_register),
    url(r'thank-you/$', thank_you),
    )
