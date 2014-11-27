from infopages.models import InfoPage
from django.shortcuts import render_to_response
from django.template import RequestContext

def view_page(request, slug):
    infopage = InfoPage.objects.get(url=slug)

    return render_to_response('infopages/infopage.html', {'infopage': infopage,}, context_instance=RequestContext(request))
