from urllib import urlencode

from django.core.urlresolvers import reverse
from django.shortcuts import redirect


def redirect_with_querystring(viewname, kwquery, args=[], kwargs={}):
    view_url = reverse(viewname, args=args, kwargs=kwargs)
    querystring = urlencode(kwquery)
    return redirect(view_url + "?" + querystring)
