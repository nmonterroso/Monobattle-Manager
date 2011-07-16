import json
from django.shortcuts import render_to_response
from django.http import HttpResponse
from variables.models import Variable
from viewers.models import ViewerSubmission
from time import time

def submit(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponse('invalid request to /submit')
    elif not 'jtv_verified' in request.session or request.session['jtv_verified'] != True:
        return HttpResponse(json.dumps({
            'success': False,
            'message': 'You have not verified your JTV account! Please do that before signing up for monobattles!'
        }))
    elif not Variable.get_bool('monobattles_enabled'):
        return HttpResponse(json.dumps({
            'success': False,
            'message': 'Monobattles are currently disabled'
        }))
    elif not request.POST['sc2_name'] or not request.POST['sc2_charcode'] or not request.POST['sc2_charcode'].isdigit():
        return HttpResponse(json.dumps({
            'success': False,
            'message': 'Please fill out your sc2 character name and code'
        }))
        
    submission = ViewerSubmission(
        sc2_name=request.POST['sc2_name'],
        sc2_charcode=request.POST['sc2_charcode'],
        submit_time=time()
    )
    submission.save()
    
    return HttpResponse(json.dumps({
        'success': True,
        'message': 'You signed up for monobattles!'
    }))