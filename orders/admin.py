from orders.models import Order, OrderLine
from django.contrib import admin

class OrderLineAdmin(admin.TabularInline):
    model = OrderLine

class OrderAdmin(admin.ModelAdmin):
    inlines = [ OrderLineAdmin, ]
    #def changelist_view(self, request, extra_context=None):
    #    if not request.GET.has_key('payment_status__exact'):
    #        qu = request.GET.copy()
    #        qu['payment_status__exact'] = 'Completed'
    #        request.GET = qu
    #        request.META['QUERY_STRING'] = request.GET.urlencode()
    #    return super(OrderAdmin,self).changelist_view(request, extra_context=extra_context)

    list_display = ('number', 'user', 'purchased_at', 'payment_status',
                    'note', 'transaction_id', 'payer_email',
                    'payer_full_name', 'get_total',)
    list_filter = ('payment_status',)

admin.site.register(Order, OrderAdmin)

