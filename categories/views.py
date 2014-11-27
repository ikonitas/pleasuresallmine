from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.contrib import messages
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from categories.models import Category


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    categories = []
    if not category.parent:
        if category.category_set.all():
            for child in category.category_set.all():
                if child.is_active:
                    categories.append(child)

    return render_to_response('categories/list_categories.html',
            {'category': category,
             'categories':categories,
             } ,
             context_instance=RequestContext(request))

def list_products(request, slug, children_slug):
    parent_category = get_object_or_404(Category, slug=slug)
    category = get_object_or_404(Category, slug=children_slug)

    products = cache.get("{0}_{1}".format(slug, children_slug))
    if not products:
        products = [ product for product in category.product_set.all()]
        cache.set('{0}_{1}'.format(slug, children_slug), products, 60 * 60)

    if not products:
        messages.warning(request, "{0} COMMING SOON!".format(
                category.name.upper()))
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render_to_response('categories/list_products.html',
                              {'products': products,
                               'category': category,
                               'parent_category': parent_category,
                              }, context_instance=RequestContext(request))
