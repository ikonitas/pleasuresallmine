# coding=utf-8

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from deliveries.models import Delivery
from orders.utils import create_order, update_order
from orders.models import Order
from paypal.standard.forms import PayPalEncryptedPaymentsForm
from products.models import Product

from baskets.cart import Cart

@require_POST
def add_to_basket(request):
    try:
        request.META['HTTP_REFERER']
    except KeyError:
        raise Http404

    product_pk = request.POST.get('product_pk','')
    quantity = int(request.POST.get("quantity",1))
    color = request.POST.get('product_color', None)
    size = request.POST.get('product_size', None)
    if color:
        color = int(color)
    if size:
        size = int(size)

    product = get_object_or_404(Product, pk=int(product_pk))
    cart = Cart(request, 'cart')
    cart.append(product, quantity, color, size)
    cart.save()

    next_url = request.GET.get('next',request.META['HTTP_REFERER'])
    message = messages.success(request,
            "You have successfully added {0} to your bag, click <a href='/basket/checkout/'>here to checkout.</a>".format(product.name))

    message
    return HttpResponseRedirect(next_url)


@require_POST
def remove_from_basket(request):
    if not 'checkout' in request.META['HTTP_REFERER']:
        raise Http404
    product_pk = request.POST.get('product_pk')
    cart = Cart(request, 'cart')
    cart.remove(product_pk)
    cart.save()
    return HttpResponseRedirect('/basket/checkout/')

def augment_quantity(request, product_pk):
    if not 'checkout' in request.META.get('HTTP_REFERER'):
        raise Http404
    cart = Cart(request)
    cart.append(product_pk)
    cart.save()
    return HttpResponseRedirect('/basket/checkout/')

def decrease_quantity(request, product_pk):
    if not 'checkout' in request.META.get('HTTP_REFERER'):
        raise Http404
    cart = Cart(request)
    cart.decrease(product_pk)
    cart.save()
    return HttpResponseRedirect('/basket/checkout/')

def checkout(request):
    if not request.user.is_authenticated():
        messages.info(request, "Please login or register before continue.")
        return HttpResponseRedirect('%s?next=%s' % (reverse('accounts.views.login_register'), reverse('baskets.views.checkout')))
    if request.user.is_staff:
        messages.info(request, "You are logged in as adminstrator, please logout and login with your customer accounts")
        referer = request.META.get('HTTP_REFERER','/')
        return HttpResponseRedirect(referer)

    delivery = None
    note = None

    deliveries = Delivery.objects.all()
    cart = Cart(request, 'cart')
    cart_subtotal = cart.total_price
    if not cart.items:
        messages.info(request, 'Your shopping bag is empty.')
        return HttpResponseRedirect('/')


    if request.method == "POST":
        if request.POST.has_key('note'):
            note = request.POST.get('note')

    delivery = Delivery.objects.all()[0]

    order_pk = request.session.get('order_pk', '')
    if order_pk:
        try:
            order = Order.objects.get(pk=order_pk)
            order = update_order(request, order, cart, delivery, note)
        except Order.DoesNotExist:
            order = create_order(request, cart)
    else:
        order = create_order(request, cart)

    paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'return_url': settings.PAYPAL_RETURN_URL,
            'invoice': '{0}'.format(order.pk),
            'notify_url': settings.PAYPAL_NOTIFY_URL,
    }
    form = PayPalEncryptedPaymentsForm(cart,
                                       order=order,
                                       initial=paypal_dict)
    if settings.SERVER_STATUS == "LIVE":
        form_type = form.render()
    else:
        form_type = form.render()

    orderlines = order.orderline_set.all()

    return render_to_response('baskets/checkout.html', {
             'cart':cart,
             'cart_subtotal':cart_subtotal,
             'deliveries': deliveries,
             'delivery': delivery,
             'order':order,
             'orderlines': orderlines,
             'form': form_type
             },
             context_instance=RequestContext(request))

def remove_all_session(request):
    del request.session['cart']
    del request.session['order_pk']
    cart = Cart(request, 'cart')
    cart.empty()
    cart.save()
    return HttpResponse("")

def color_change(request):
    color = request.POST.get('color', '')
    product_pk = request.POST.get('product_pk', '')
    order_pk = request.POST.get('order_pk', '')
    if order_pk:
        order = Order.objects.get(pk=int(order_pk))
    if product_pk:
        product = Product.objects.get(pk=int(product_pk))
    cart = Cart(request, 'cart')
    cart.change_color(product, color)
    cart.save()

    update_order(request, order, cart)
    return HttpResponse("boom")

def size_change(request):
    size = request.POST.get('size', '')
    product_pk = request.POST.get('product_pk', '')
    order_pk = request.POST.get('order_pk', '')
    if order_pk:
        order = Order.objects.get(pk=int(order_pk))
    if product_pk:
        product = Product.objects.get(pk=int(product_pk))
    cart = Cart(request, 'cart')
    cart.change_size(product, size)
    cart.save()

    update_order(request, order, cart)
    return HttpResponse("boom")
