# coding=utf-8

from django.template import Library
from django.core.urlresolvers import NoReverseMatch

register = Library()

@register.simple_tag
def active(request, name):
    try:

        path = filter(None, request.path.split('/'))
        if len(path) == 2:
            if name == path[1]:
                return ' class="active" '
            else:
                return ' '
        else:
            if name == path[0]:
                return ' class="active" '
    except NoReverseMatch:
        return ' '
