#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150810
#  @date          20150812 - Build customize_form_errors
#  @version       0.1
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
# Number 0 that error handling is relative to form instance or interface
ERR_0000_FIELD_ERROR = {"code": 0,
                        "message": "Invalid {filedname} - {message}"}

# Number 1 that the error handlings are relative to user instance
ERR_1001_INEXISTENT_ACC = {"code": 1001,
                           "message": "Account doesn't exist"}
ERR_1002_INCORRECT_PWD = {"code": 1002,
                          "message": "Incorrect password"}
ERR_1003_REGISTERED_ACC = {"code": 1003,
                           "message": "Account is invalid or already taken"}
ERR_1004_INCORRECT_FORMAT = {"code": 1004,
                             "message": "Incorrect account or password"}
