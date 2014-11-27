# coding=utf-8

from deliveries.models import Delivery

def delivery_price(request):
    price = Delivery.objects.all()[0]
    return { 'delivery_price': price }

def deliveries(request):
    deliveries = Delivery.objects.all().order_by('sort_order')
    return {'deliveries': deliveries}
