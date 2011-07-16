import json
from time import time

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from variables.models import Variable
from viewers.models import ViewerSubmission

def manage(request):
    params = {}
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/manage')
        else:
            params['error'] = "Invalid username or password"
    
    if request.user.is_authenticated() and request.user.has_perm('variables.add_variable'):
        template = 'viewers/manage.html'
        params['is_enabled'] = Variable.get_bool('monobattles_enabled')
    else:
        params['login_form'] = AuthenticationForm()
        template = 'viewers/manage_login.html'
    
    return render_to_response(template,
        params,
        context_instance=RequestContext(request)
    )
    
def manage_action(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponse('invalid request to /manage-action')
    elif not request.user.is_authenticated() or not request.user.has_perm('variables.add_variable'):
        return HttpResponse(json.dumps({
            'success': False,
            'message': 'You are not allowed to enable/disable monobattles'
        }))
        
    if request.POST['action'] == 'enable':
        Variable.set('monobattles_enabled', True)
        Variable.set('monobattles_last_enabled_time', time())
        return HttpResponse(json.dumps({
            'success': True,
            'message': 'Monobattles are ON!'
        }))

    Variable.set('monobattles_enabled', False)
    last_enabled = Variable.get_decimal('monobattles_last_enabled_time', time())
    submissions_query = ViewerSubmission.objects.filter(
        submit_time__gte=last_enabled
    ).order_by('submit_time')
    submissions = []
    for s in submissions_query:
        submissions.append({
            'name': s.sc2_name,
            'code': s.sc2_charcode,
            'time': s.__unicode__()
        })
    
    return HttpResponse(json.dumps({
        'success': True,
        'message': 'Monobattles have been disabled',
        'submissions': submissions
    }))