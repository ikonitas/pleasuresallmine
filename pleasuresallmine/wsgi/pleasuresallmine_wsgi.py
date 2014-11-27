import os
import site

site.addsitedir('/var/envs/pleasuresallmine')
site.addsitedir('/var/www/pleasuresallmine')
site.addsitedir('/var/www/pleasuresallmine/pleasuresallmine')

os.environ['DJANGO_SETTINGS_MODULE'] = 'pleasuresallmine.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
