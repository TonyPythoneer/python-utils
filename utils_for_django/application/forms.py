#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150813
#  @date          20150813 - Build sample of `forms.py`
#  @version       0.1
"""Establish a sample for forms.py

Django handles three distinct parts of the work involved in forms:

    1. preparing and restructuring data to make it ready for rendering
    2. creating HTML forms for the data
    3. receiving and processing submitted forms and data from the client

Form API has many built-in functions. Not only having above features but also
handling validation is very convience for me.
"""
from django import forms
from django.core.validators import EmailValidator, MinLengthValidator
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from utils import error_handling


class ExampleForm(forms.Form):
    email = forms.CharField(label='email',
                            max_length=100,
                            validators=[EmailValidator()])
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput,
                               validators=[MinLengthValidator(6)])

    def _verify_by_models(self, data):
        """Verify by models
        """
        error_list = []
        VDE = forms.ValidationError

        # Validation process: Verity by relative models
        # do something

        # Validation end: It will submit exception report about logic error if needed.
        if error_list:
            raise VDE(error_list)

    def clean(self):
        """Two stage validation util data is real valid.
        """
        # Validation process : In the first stage verify form by fields whether it's valid or not
        cleaned_data = super(ExampleForm, self).clean()

        # Validation process : In the second stage verify form by models whether it's valid or not
        if self.is_valid():
            self._verify_by_models(cleaned_data)
        return cleaned_data



class SignupForm(forms.Form):
    email = forms.CharField(label='email',
                            max_length=100,
                            validators=[EmailValidator()])
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput,
                               validators=[MinLengthValidator(6)])

    def _verify_by_models(self, data):
        """Verify by models

        In the second stage form verities by models
        """
        error_list = []
        VDE = forms.ValidationError

        # Validation process: Verity by relative models
        if User.objects.filter(username=data['email'],
                               email=data['email']).exists():
            error_list.append(VDE(**error_handling.ERR_1003_REGISTERED_ACC))

        # Validation end: It will submit exception report about logic error if needed.
        if error_list:
            raise VDE(error_list)

    def clean(self):
        """Two stage validation util data is real valid.

        It will make advanced validation of second stage when it has done basic validation
        of each field of form and it's valid.

        Workflow:
            1. Form gets data from request
            2. In the first stage form is verified by each field
            3. In the second stage form is verified by models
            4. Finally, service sends data of form to model

        Design reason:
            User fill a form out and send out to service. Service has two stage validation.

            First, if any field on form has validation error, user will watch warning,
            for example, inputting blank field, violating regulation of field. But service
            can't inform whether the email and password are valid or not.

            Second, if each field on form has been indeed filled out, user will watch warning,
            for example, invalid email, registered email, invalid password, etc.

            Finally, service sends data of form to model if it is real valid data on form.
        """
        # Validation process : In the first stage verify form by fields whether it's valid or not
        cleaned_data = super(SignupForm, self).clean()

        # Validation process : In the second stage verify form by models whether it's valid or not
        if self.is_valid():
            self._verify_by_models(cleaned_data)
        return cleaned_data
