import json
from django.shortcuts import render_to_response
from django.http import HttpResponse
from viewers.classes import Viewer

def verify(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponse('invalid request to /verify')
        
    user = Viewer(jtv_handle=request.POST['username'])
    is_verified = user.verify(request.POST['password'])
    request.session['jtv_verified'] = is_verified
    
    if is_verified:
        response = {
            'success': True,
            'message': 'You are for suresies subscribed to Day9!',
            'username': user.jtv_handle
        }
    else:
        response = {
            'success': False,
            'message': 'Unable to verify JTV credentials. Check your username/password and try again.',
        }
    
    return HttpResponse(json.dumps(response))