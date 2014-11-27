# coding=utf-8

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from categories.models import Category
from products.models import Product


def view_product(request, parent_slug, category_slug, product_slug):
    parent_category = get_object_or_404(Category, slug=parent_slug)
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=product_slug)

    return render_to_response('products/view_product.html',
                              {'product': product,
                               'parent_category': parent_category,
                               'category': category,
                               }, context_instance=RequestContext(request))
