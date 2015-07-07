from django import forms
from django.core.validators import EmailValidator, MinLengthValidator

class SignupForm(forms.Form):
    email = forms.CharField(label='email',
                            max_length=100,
                            validators=[EmailValidator()])
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput,
                               validators=[MinLengthValidator(6)])

