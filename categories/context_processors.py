# coding=utf-8

from django.core.cache import cache

from models import Category


def list_categories(request):
    categories = cache.get('list_categories')
    if not categories:
        categories = Category.objects.filter(
            is_active=True).order_by('sort_order')
        cache.set('list_categories', categories, 60)
    return {'list_categories': categories}
