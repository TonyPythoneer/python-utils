#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150713
#  @date          20150713 - build msg
#  @version       0.1
'''
Error handling is a dictionary includes code and error message keys.
It will return description of a dictionary if program detects error.

I follow the example of django restframework about status code design.

Attributes:
    ERROR_EVENTNUM_EVENTNAME (dict): It express more clear error message to
        acknowledge developer it.

.. Django Restframework Guide:
https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/status.py
'''

ERROR_001_NO_ACCOUNT_EXIST = {"code": -1,
                              "error_msg": "Account doesn't exist"}
ERROR_002_INCORRECT_FORMAT = {"code": -2,
                              "error_msg": "Incorrect account or password"}
ERROR_003_INVALID_ACCOUNT = {"code": -3,
                             "error_msg": "Account is invalid or already taken"}
ERROR_004_CHANGE_PASSWORD = {"code": -4,
                             "error_msg": "Welcome new comer, Please change your password"}
