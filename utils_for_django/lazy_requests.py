#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150813
#  @date          20150813 - Establish lazy_requests
#  @version       0.0
from django.conf import settings
from requests import Request


def lazy_requests(api, method, params_or_data, **kwargs):
    """So easy requests!

    It designs for lazy person, especially he don't know any knowledage about python
    """
    url = settings.BACKEND_APPLICATION_SERVER + api
    method = method.upper()

    # Data Process: It's a fool-proof design if developer don't know HTTP protocol
    if method in ['GET', 'DELETE']:
        kwargs['params'] = params_or_data
    elif method in ['POST', 'PATCH', 'PUT']:
        kwargs['data'] = params_or_data
    req = Request(method, url, **kwargs)

    return req
