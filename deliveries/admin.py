from django.contrib import admin
from deliveries.models import Delivery


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'sort_order', )

    def has_add_permission(self, request):
        return False

admin.site.register(Delivery, DeliveryAdmin)
