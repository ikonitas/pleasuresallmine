import json

from django.http import HttpResponse

from products.models import Product

def get_price(request):
    price = 0
    if request.method == "GET":
        product_pk = request.GET.get('product_pk', '')
        if product_pk:
            product = Product.objects.get(pk=product_pk)
            if request.GET.has_key('quantity'):
                quantity = request.GET.get('quantity', 1)
                price =  int(quantity) * product.total_price()
    resp = {'price': str(price)}
    return HttpResponse(json.dumps(resp),
            mimetype="application/javascript")
