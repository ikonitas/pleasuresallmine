from django.shortcuts import render_to_response
from django.template import RequestContext

from core.models import HomeScreen

def home(request):
    screen = HomeScreen.objects.filter(is_active=True).order_by('?')[0]
    return render_to_response('core/home.html', {'screen': screen,},
                              context_instance = RequestContext(request))
