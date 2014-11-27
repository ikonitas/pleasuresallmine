from decimal import Decimal

from django.db import models
from django.core.urlresolvers import reverse

from categories.models import Category

class Size(models.Model):
    title = models.CharField(max_length=30)

    def __unicode__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=30)

    def __unicode__(self):
        return self.title


class Product(models.Model):
    page_title_help = 'The title to be shown at the top of your browser window.'
    meta_keywords_help = 'This should be a comma separated list of keywords/keyphrases that are relevant to this page.'
    meta_description_help = 'This should be a brief description of the content of this page.'
    is_active_help = "Should this product show in category listings ?"
    name = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category)
    is_in_stock = models.NullBooleanField(default=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    margin = models.DecimalField(
            max_digits=10,
            decimal_places=2,
            default=100.00,
    )
    size = models.ManyToManyField(Size, null=True, blank=True)
    color = models.ManyToManyField(Color, null=True, blank=True)
    product_number = models.CharField(max_length=20, null=True, blank=True)
    special_offer = models.NullBooleanField(
            null=True,
            blank=True,
            default=False
    )
    is_active = models.BooleanField(default=True, help_text=is_active_help)
    slug = models.SlugField(unique=True)
    page_title = models.CharField(max_length=200, null=True,
                                  blank=True, help_text=page_title_help)
    meta_description = models.CharField(max_length=250, null=True,
                                        blank=True, help_text=meta_description_help)
    meta_keywords = models.CharField(max_length=300, null=True,
                                     blank=True, help_text=meta_keywords_help)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def total_price(self):
        total_price = (self.price * self.margin) / 100
        total_price = self.price + total_price
        return Decimal("%.2f" % total_price)

    def get_absolute_url(self):
        return reverse('products.views.view_product', args=[
                self.category.parent.slug,
                self.category.slug,
                self.slug
        ])

    def get_image(self):
        try:
          image = self.productimage_set.all()[0].image
          if image.file:
              return self.productimage_set.all()[0].image
        except:
          return None


class ProductImage(models.Model):
    image = models.ImageField(null=True,
                              blank=True,
                              upload_to="uploads/%Y/%m/%d")
    product = models.ForeignKey(Product)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __unicode__(self):
        return self.product.name
