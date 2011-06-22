import rpdb2
from django.shortcuts import render_to_response
from viewers.models import Viewer
from django.template import RequestContext

def index(request):
    rpdb2.start_embedded_debugger('abc123')
    me = Viewer(jtv_handle='harblrbl')
    return render_to_response('viewers/index.html',
        {'me': me },
        context_instance=RequestContext(request)
    )