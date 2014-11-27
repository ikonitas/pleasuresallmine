from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from accounts.models import UserProfile
from products.models import Product, Size, Color
from orders.choice_lists import ORDER_LINE_STATUS_CHOICES
from orders.choice_lists import ORDER_LINE_STATUS_ADDED
from orders.models import Order, OrderLine

def my_orders(request):
    if request.user.is_anonymous():
        messages.info(request, "Please login or register first.")
        return HttpResponseRedirect('/login/')
    if request.user.is_staff:
        messages.info(request, "You are logged in as administrator, please logout and login with your customer account.")
        return HttpResponseRedirect('/')
    else:
        userprofile = UserProfile.objects.get(user_id=request.user.pk)
        orders =  Order.objects.filter(user=request.user, payment_status="Completed")
        try:
            address = userprofile.user.address_set.all()[0]
        except:
            address = None
    return render_to_response('orders/my_orders.html',
            {'userprofile': userprofile,
             'orders': orders,
             'address': address}, context_instance=RequestContext(request))


@staff_member_required
def view_order(request, order_pk):
    products = Product.objects.all()
    order = Order.objects.get(pk=order_pk)
    if request.method == "POST":
        if "change_line_status" in request.POST:
            line = request.POST.get('line', '')
            line_status = request.POST.get('line_status', '')
            if "line" and "line_status" in request.POST:
                orderline = order.orderline_set.get(pk=line)
                orderline.status = line_status
                orderline.save()
            else:
                messages.warning(request, "Please make sure that you have \
                ticked a line and choosed a orderline")

        if "add_orderline" in request.POST:
            product_pk = request.POST.get("orderline_product", "")
            quantity = request.POST.get("orderline_quantity", "")
            color = request.POST.get('product_color', "")
            size = request.POST.get('product_size', "")

            if color:
                color = Color.objects.get(pk=int(color))
            if size:
                size = Size.objects.get(pk=int(size))

            price = request.POST.get("orderline_price", "")
            if product_pk and quantity and price:
                orderline = OrderLine()
                orderline.order = order
                orderline.product = Product.objects.get(pk=product_pk)
                orderline.quantity = quantity
                if color:
                    orderline.color = color
                if size:
                    orderline.size = size
                orderline.line_price = price
                orderline.status = ORDER_LINE_STATUS_ADDED
                orderline.save()
            else:
                messages.warning(request, """Something missing please double \
                check""")

        if "delete_order_line" in request.POST:
            line = request.POST.get("line", "")
            order.orderline_set.get(pk=line).delete()


    userprofile = UserProfile.objects.get(user=order.user)
    orderline_status_choices = ORDER_LINE_STATUS_CHOICES
    try:
        address = userprofile.user.address_set.all()[0]
    except:
        address = None
    colors = Color.objects.all()
    sizes = Size.objects.all()
    return render_to_response('admin/orders/view_order.html',
            {'order': order,
             'products':products,
             'orderline_status_choices': orderline_status_choices,
             'userprofile': userprofile,
             'address': address,
             'colors': colors,
             'sizes': sizes,
             'root_path': '/admin/',
             }, RequestContext(request))


def view_invoice(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)

    # authorised?
    if not(request.user.is_staff or request.user == order.user):
        return HttpResponseForbidden()

    try:
        address = order.user.address_set.all()[0]
    except:
        address = None

    return render_to_response(
        'admin/orders/view_invoice.html',
        {
            'order' : order,
            'address': address,
        },
        RequestContext(request)
    )
