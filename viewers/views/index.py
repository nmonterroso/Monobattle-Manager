from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms

def index(request):
    params = {}
    if 'jtv_verified' in request.session and request.session['jtv_verified'] == True:
        params['jtv_verified'] = True
    else:
        params['jtv_verified'] = False
    
    params['verify_form'] = VerifyForm()
    params['submit_form'] = SubmitForm()
        
    return render_to_response('viewers/index.html',
        params,
        context_instance=RequestContext(request)
    )
    
class VerifyForm(forms.Form):
    username = forms.CharField(label='justin.tv username', required=True)
    password = forms.CharField(label='justin.tv password', required=True, widget=forms.widgets.PasswordInput)
    
class SubmitForm(forms.Form):
    sc2name = forms.CharField()
    sc2code = forms.CharField()