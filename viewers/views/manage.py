from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms

def manage(request):
    if 'monobattle_manager' in request.session and request.session['monobattle_manager'] == True:
        template = 'viewers/manage.html'
    else:
        params['manage_login'] = ManageLogin()
        template = 'viewers/manage_login.html'
    
    return render_to_response(template,
        params,
        context_instance=RequestContext(request)
    )
    
class ManageLogin(forms.Form):
    username = forms.charField(label='username', required=True)
    password = forms.CharField(label='password', required=True,
                               widget=forms.widgets.PasswordInput)
    