# coding=utf-8

from django.template import Library

register = Library()

@register.simple_tag
def active(request, name):
    if name == int(request.GET.get('page', '1')):
        return 'active'
    else:
        return ''
