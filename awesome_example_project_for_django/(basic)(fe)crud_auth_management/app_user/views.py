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
                'context': {'form': SignupForm()},
                'context_instance': RequestContext(req)}

    # Call index.html when method is GET
    if req.method == 'GET':
        return rtr(**rtr_args)

    # Processing when method is POST
    if req.method == 'POST':
        # Verify: Processing POST data by form
        sf = SignupForm(req.POST)

        m_fields = {field: sf.data[field] for field in sf.fields}
        print m_fields

        # Verify: the form has set validators
        if not sf.is_valid():
            # keep user's inputting data
            rtr_args['context']['form'] = SignupForm(req.POST)
            return rtr(**rtr_args)

        # it needs to add in validator of form
        if User.objects.filter(email=sf.data["email"]).exists():
            rtr_args['context']['err_msg'] = {"User": ["The username/email is registered."]}.items()
            return rtr(**rtr_args)

        m_fields['username'] = m_fields['email']
        user = User.objects.create_user(**m_fields)
        user.save()

        return redirect_with_querystring("home", {"msg": "Successful registration!"})


def login(req):
    if req.method == 'GET':
        email = req.POST.get('email', '')
        password = req.POST.get('password', '')
    if req.method == 'POST':
        email = req.POST.get('email', '')
        password = req.POST.get('password', '')
        user = authenticate(username=email, password=password)
