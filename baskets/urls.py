from django.conf.urls import patterns, url


urlpatterns = patterns(
    'baskets.views',
    url(r'checkout/$', 'checkout',),
    url(r'add/$','add_to_basket',),
    url(r'remove/$','remove_from_basket', name="basket_remove"),
    url(r'augment/(\d+)/$', 'augment_quantity', name="augment"),
    url(r'decrease/(\d+)/$', 'decrease_quantity', name="decrease"),
    url(r'color-change/$', 'color_change', name="color_change"),
    url(r'size-change/$', 'size_change', name="size_change"),
    url(r'ajax/session/', 'remove_all_session',),
    )
