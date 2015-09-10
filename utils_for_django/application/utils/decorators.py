#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150902
#  @date          20150902 - Build customized_login_required
#  @version       0.1
"""Here is a collection of decorators in util
"""
import time

from django.contrib.auth.decorators import login_required


def exec_timer(func):
    """Estimate function execution time
    """
    def args_wrapper(*args, **kwargs):
        """Set timer and ouput result
        """
        # timer
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        # output
        print "=== {func_name} ===".format(func_name=func.__name__)
        print "exec_time:" + str(end-start)

        return result
    return args_wrapper


def customized_login_required(function=None):
    """If the user isn't logged in, redirect to settings.LOGIN_URL.
    """
    return login_required(function=function, redirect_field_name='pervious')
