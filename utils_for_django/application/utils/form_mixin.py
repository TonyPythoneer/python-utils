#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150901
#  @date          20150908 - TwoStageFormValidationMixin adds new function
#  @version       0.1.2
"""Offer form class that it can inherit Mixin object and simplify codes
"""
import json


class TwoStageFormValidationMixin(object):
    def _verify_by_models(self, data):
        """Verify by model instance in the second validation stage

        Example:
            Althought it can't be inherited, it's valuable to be referred as below.

            It offers form class not only inherit but also can go a step further to focus
            data validation; This therefore will separate API into data validation and
            data process clearly.

            class SignupForm(TwoStageFormValidationMixin, forms.Form):
                email = forms.CharField(label='email',
                                        max_length=100,
                                        validators=[EmailValidator()])
                password = forms.CharField(label='password',
                                           widget=forms.PasswordInput,
                                           validators=[MinLengthValidator(6)])

                def _verify_by_models(self, data):
                    error_list = []
                    VDE = forms.ValidationError

                    # Validation process: Verity by relative models
                    if User.objects.filter(username=data['email'],
                                           email=data['email']).exists():
                        error_list.append(VDE(**error_handling.ERR_1003_REGISTERED_ACC))

                    # Validation end: It will submit exception report about logic error if needed.
                    if error_list:
                        raise VDE(error_list)
        """
        pass

    def clean(self):
        """Two-stage validation util data is real valid and clean.

        It will be verified by two-stage validation: form and model instance

        Workflow:
            1. Form gets data from request
            2. Verify by form instance in the first validation stage
            3. Verify by model instance in the second validation stage
            4. Finally, form data outputs cleaned data

        Example:
            When form instance calls `is_valid`, it will trigger `clean` and be verified
            by form field validations. If it's valid, form instance will make `clean_data`
            as callable function -- otherwise it will do error handling.

            It supposes it's valid. Form instance can call `clean_data` to do bussiness
            logic.

            def signup(req):
                if req.method == 'POST':
                    # Verification process: Store raw data in form
                    sf = SignupForm(req.POST)

                    # Verification process: Verify by form's validators
                    if not sf.is_valid():
                        # do something
                        return False

                    # Model process: Create a new user
                    user = User.objects.create_user(username=sf.cleaned_data['email'],
                                                    email=sf.cleaned_data['email'],
                                                    password=sf.cleaned_data['password'])
                    user.save()
                    return True
        """
        # Validation process : First, form data is verified by form instance
        cleaned_data = super(TwoStageFormValidationMixin, self).clean()

        # Validation process : Later, form data is verified by model instance
        if self.is_valid():
            self._verify_by_models(cleaned_data)
        return cleaned_data

    def error_handling(self):
        """Return a dict contains `detail` key and includes a number of error handling as a list

        Example:
            Each field validation or model validation contains message and code when it
            outputs json format as below.

            >>> form_instance.errors.as_json()
            '{"platform": [{"message": "This field is required.", "code": "required"}],
              "user_o": [{"message": "This field is required.", "code": "required"}],
              "deivce_name": [{"message": "This field is required.", "code": "required"}]}'

            I can go a further step to tidy the json and make a dictionary object.
            It clearly lists every error statement in list object as dictionary object's value.

            >>> form_instance.error_handling()
            {'detail': [{'code': 0,
                         'message': 'Invalid platform - This field is required.'},
                        {'code': 0,
                         'message': 'Invalid user_o - This field is required.'},
                        {'code': 0,
                         'message': 'Invalid deivce_name - This field is required.'}]}
        """
        # Local variables: These are necessary local variables for this function.
        detail = None
        field_errors = json.loads(self.errors.as_json())

        # Validation process: Check the form's validity
        if not self.is_valid():
            # Data process: Get field errors when from is invalid in the first stage
            if not '__all__' in field_errors:
                detail = []
                for fieldname, errors in field_errors.items():
                    for error in errors:
                        message = "Invalid {} - {}".format(fieldname, error['message'])
                        detail.append({'code': 0, 'message': message})
            # Data process: Get bussiness logic errors when from is invalid in the second stage
            else:
                detail = filed_errors['__all__']

        return {'detail': detail}
