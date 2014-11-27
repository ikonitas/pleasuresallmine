from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from orders.choice_lists import ORDER_LINE_STATUS_CHOICES
from orders.choice_lists import ORDER_LINE_STATUS_ORDERED
from orders.choice_lists import ORDER_LINE_STATUS_RETURNED
from orders.choice_lists import ORDER_LINE_STATUS_ADDED
from deliveries.models import Delivery
from products.models import Product, Color, Size

class Order(models.Model):
    user = models.ForeignKey(User,null=True, blank=True)
    purchased_at = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=250,null=True, blank=True)
    payer_email = models.EmailField(null=True, blank=True)
    payer_full_name = models.CharField(max_length=100, null=True,blank=True)
    delivery = models.ForeignKey(Delivery)
    note = models.TextField(null=True, blank=True)
    payment_status = models.CharField(max_length=20, null=True, blank=True,
                                      default="Uncompleted")

    def __unicode__(self):
        return "{0:0>5}".format(self.pk)

    @property
    def number(self):
        return "%05d" % self.pk

    def get_total(self):
        total = 0
        for line in self.orderline_set.all():
            if line.status == ORDER_LINE_STATUS_ORDERED:
                total += line.line_price
            if line.status == ORDER_LINE_STATUS_ADDED:
                total += line.line_price

        total += Decimal(self.delivery.price)
        return total

    def get_returned(self):
        added_price = 0
        return_price = 0
        for line in self.orderline_set.all():
            if line.status == ORDER_LINE_STATUS_RETURNED:
                return_price -= line.line_price
            if line.status == ORDER_LINE_STATUS_ADDED:
                added_price += line.line_price

        return added_price + return_price


class OrderLine(models.Model):
    """Orderline relating to a specific order."""
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()
    color = models.ForeignKey(Color, null=True, blank=True)
    size = models.ForeignKey(Size, null=True, blank=True)
    status = models.IntegerField(
            choices=ORDER_LINE_STATUS_CHOICES,
            null=True,
            blank=True,
            default=1,
    )
    line_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __unicode__(self):
        return str(self.pk)


class OrderNone(models.Model):
    order = models.ForeignKey(Order)
    note = models.TextField()
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
