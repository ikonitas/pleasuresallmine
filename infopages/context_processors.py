# coding=utf-8

from infopages.models import InfoPage


def list_infopages(request):
    infopages = InfoPage.objects.filter(
            is_active=True,
            show_menu=False,
            ).order_by(
            'sort_order'
    )
    return {'list_infopages': infopages,}

def list_infopages_menu(request):
    infopages = InfoPage.objects.filter(
            is_active=True,
            show_menu=True,
            ).order_by(
            'sort_order'
    )
    return {'list_infopages_menu': infopages,}
