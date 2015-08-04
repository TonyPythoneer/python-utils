#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150804
#  @date          20150804
#  @version       0.0
'''Assist front-end developer to fast solve python design problem

Example:

    datas = {
        "acc": "1234567890@gmail.com",
    }

    res = requests.post("http://127.0.0.1:8000/setUserAccount",
                        data= data,
                        headers = get_token_from_req(request))

    if "www-authenticate" in res.headers:
        return redirect_to_login(request)
'''

from django.shortcuts import redirect


def get_token_from_req(req):
    return {"Authorization": "token %s" % (req.session.get('token', '')}


def redirect_to_login(req, clear_list=['userName', 'user', 'lastLogin', 'isSuper', 'token']):
    for element in clear_list:
        del request.session[element]
    return redirect("login url")
