#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150713
#  @date          20150813 - Enhance feature for applying form API
#  @version       0.2
"""Error handling list

I derive error handling design from status code design of source code of django restframework.

Each of error handling is a dictionary contains code and message.
It will return error message if program detects error.

Attributes:
    ERR_NUM_NAME (dict): It bases on my exprience about handling frequent errors and
        I establish a private regulation to manage them.

.. _Django Restframework Guide:
    https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/status.py

"""
import json


def customize_form_errors(form):
    """Return a dict contains `detail` key and includes a number of error handling as a list

    It's customization for form API. It can return my personal expected error handling format
    When receiving and processing submitted forms and data from the client detects error.

    Example:
        >>> forms.ValidationError(**ERR_1001_INEXISTENT_ACC)

    According to ValidationError in Django documentation, the exception function can receive
    code and message to customize specific exception.
    """
    customizing_errors = {'detail': []}
    filed_errors = json.loads(form.errors.as_json())
    # Validation process: In the first stage verify form by each field whether it's valid or not
    if not form.is_valid() and not '__all__' in filed_errors:
        for fieldname, errors in filed_errors.items():
            # Data process: Make ERR_0000_INVALID_FIELD list
            error_list = map(lambda error: {
                "code": 0,
                "message": "Invalid {} - {}".format(fieldname, error['message'])
            }, errors)
            customizing_errors['detail'].extend(error_list)
    # Validation process: In the second stage verify form by models whether it's valid or not
    elif '__all__' in filed_errors:
        customizing_errors['detail'] = filed_errors['__all__']
    # Validation process: Return none when it's sure to be valid
    else:
        customizing_errors['detail'] = None
    return customizing_errors


def is_user_app_error(err_dict):
    code = err_dict['code']
    return code >= 1000 and code <= 1999


# user list
ERR_1001_INEXISTENT_ACC = {"code": 1001,
                           "message": "Account doesn't exist"}
ERR_1002_INCORRECT_PWD = {"code": 1002,
                          "message": "Incorrect password"}
ERR_1003_REGISTERED_ACC = {"code": 1003,
                           "message": "Account is invalid or already taken"}
ERR_1004_INCORRECT_FORMAT = {"code": 1004,
                             "error_msg": "Incorrect account or password"}
