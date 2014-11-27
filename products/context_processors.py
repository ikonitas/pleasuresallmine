# coding=utf-8

from django.core.cache import cache

from models import Product


def special_offers(request):
    special_offers = None #cache.get('special_offers')
    if not special_offers:
        special_offers = Product.objects.filter(
                special_offer=True).order_by('?')[:4]
        cache.set('special_offers', special_offers, 60 * 60)

    return {'special_offers': special_offers }

