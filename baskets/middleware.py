from baskets.cart import Cart

class SimpleCartMiddleware(object):
    '''Middleware to support only a single cart, for the simple case '''
    def process_request(self, request):
        request.cart = Cart(request, 'cart')
        return None

    def process_response(self, request, response):
        if hasattr(request, "cart"):
            request.cart.save()
        return response
