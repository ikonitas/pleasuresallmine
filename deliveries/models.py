from django.db import models


class Delivery(models.Model):
    name = models.CharField(max_length=140)
    price = models.CharField(null=True, blank=True, max_length=20)
    sort_order = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return str(self.price)

    class Meta:
        verbose_name_plural = "deliveries"
