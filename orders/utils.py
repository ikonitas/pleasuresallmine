from decimal import Decimal

from django.contrib import messages
from django.db import transaction

from paypal.standard.ipn.signals import payment_was_successful
from paypal.standard.ipn.signals import payment_was_flagged
from automated_emails.views import send_order_confirmation_email
from deliveries.models import Delivery
from orders.models import Order
from orders.models import OrderLine
from products.models import Color, Size


@transaction.commit_on_success
def create_order(request,cart, delivery=None):
    subtotal = cart.total_price

    order = Order()
    order.user = request.user

    delivery = Delivery.objects.all()[0]
    order.delivery = delivery
    order.total = subtotal + Decimal(order.delivery.price)

    order.save()

    for pro in cart:
        line = OrderLine()
        line.order = order
        line.product = pro.item
        line.quantity = pro.quantity
        if pro.color:
            line.color = Color.objects.get(pk=pro.color)
        if pro.size:
            line.size = Size.objects.get(pk=pro.size)
        line.line_price = pro.item.total_price() * pro.quantity
        line.save()

    request.session['order_pk'] = order.pk
    return order

def update_order(request, order, cart, delivery=None, note=None):
    order_lines_product_pk = [line.product_id for line in order.orderline_set.all()]

    if delivery:
        order.delivery = delivery
    if note:
        order.note = note
        messages.info(request, "Your additional delivery info has been added")

    for item in cart:
        if item.item.pk in order_lines_product_pk:
            for line in order.orderline_set.all():
                if item.item.pk == line.product_id:
                    line.quantity = item.quantity
                    if item.color:
                        line.color = Color.objects.get(pk=item.color)
                    if item.size:
                        line.size = Size.objects.get(pk=item.size)
                    line.line_price = item.quantity * item.item.total_price()
                    line.save()
        else:
            new_line = OrderLine()
            new_line.order = order
            new_line.product = item.item
            new_line.quantity = item.quantity
            new_line.line_price = item.quantity * item.item.total_price()
            new_line.save()

    order_lines_product_pk = [line.product_id for line in order.orderline_set.all()]
    if not len(cart) == len(order_lines_product_pk):
        order.orderline_set.all().delete()
        update_order(request, order, cart)

    order.total = 0

    for line in order.orderline_set.all():
        order.total += line.line_price

    order.total =+ order.total + Decimal(order.delivery.price)

    order.save()

    return order

def play_signals(sender, **kwargs):
    ipn = sender
    order = Order.objects.get(pk=ipn.invoice)
    order.transaction_id = str(ipn.txn_id)
    order.payment_status = str(ipn.payment_status)
    order.payer_email = str(ipn.payer_email)
    order.payer_full_name = "%s %s" % (ipn.first_name, ipn.last_name)
    if order.payment_status == "Completed":
        if not ipn.flag:
            send_order_confirmation_email(order)
    order.save()
    return
payment_was_successful.connect(play_signals)
payment_was_flagged.connect(play_signals)

def paypal_signal(ipn):
    pass
