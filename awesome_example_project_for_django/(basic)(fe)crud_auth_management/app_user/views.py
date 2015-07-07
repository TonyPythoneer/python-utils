from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import redirect
from django.shortcuts import render_to_response as rtr

from forms import SignupForm

from utils.url_generator import redirect_with_querystring
from utils.decorators import exec_timer


@exec_timer
def home(req):
    rtr_args = {'template_name': 'index.html',
                'context': {'links': {'signup': reverse('user:signup')}}}
    if req.GET:
        rtr_args['context']['msg'] = req.GET.get('msg', '')

    return rtr(**rtr_args)


@exec_timer
def signup(req):
    rtr_args = {'template_name': 'signup.html',
                'context': {'signup_form': SignupForm()},
                'context_instance': RequestContext(req)}

    # Call index.html when method is GET
    if req.method == 'GET':
        return rtr(**rtr_args)

    # Processing when method is POST
    if req.method == 'POST':
        # Verify: Processing POST data by form
        sf = SignupForm(req.POST)
        print dir(sf)
        print sf.data
        print dir(sf["email"])
        print type(sf["email"])
        print sf["email"].data
        print sf["password"].value()
        if not sf.is_valid():
            rtr_args['context']['err_msg'] = sf.errors.items()
            return rtr(**rtr_args)


        return redirect_with_querystring("home", {"msg": "Successful registration!"})


def login(req):
    if req.method == 'GET':
        email = req.POST.get('email', '')
        password = req.POST.get('password', '')
    if req.method == 'POST':
        email = req.POST.get('email', '')
        password = req.POST.get('password', '')
        user = authenticate(username=email, password=password)
