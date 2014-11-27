from haystack.query import SearchQuerySet
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

def search_products(request):
    try:
        search_term = request.GET['q']
    except:
        return HttpResponseRedirect('/')

    results = SearchQuerySet().auto_query(search_term)
    products = []
    for product in results:
        products.append(product.object)
    return render_to_response('search/results.html',
                             {'products': products,
                              'search_term': search_term,},
                             context_instance=RequestContext(request))

