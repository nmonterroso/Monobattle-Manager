from django.shortcuts import render_to_response
from viewers.models import Viewer

def index(req):
    me = Viewer(jtv_handle='harblrbl')
    return render_to_response('viewers/index.html', {'me': me})