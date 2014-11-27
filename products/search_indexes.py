from django.db import models
from haystack.indexes import RealTimeSearchIndex, CharField
from haystack import site
from products.models import Product


class ProductIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    name = CharField(model_attr="name")
    description = CharField(model_attr="description")
    product_number = CharField(model_attr="product_number")
    category = CharField(model_attr="category")

    def index_queryset(self):
        return Product.objects.filter(is_active=True)

site.register(Product, ProductIndex)
