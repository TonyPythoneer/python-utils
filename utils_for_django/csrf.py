#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150713
#  @date          20150713
#  @version       0.1
"""
It inherits TokenAuthentication of django-rest-framework/rest_framework/authentication.py and
customizes authentication class which has token will expire of feature.

requirements:
djangorestframework==2.4.2
"""
import datetime

from django.utils.timezone import utc
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication, get_authorization_header


class ExpiringTokenAuthentication(TokenAuthentication):
    """Add timeliness token feature in TokenAuthentication

    In short, the only two differences being:
        1. request has to include a Authenticate header
        2. Inspect created time of token

    The rest of parts is the same TokenAuthentication.

    Examples:
        class ExampleView(APIView):
            authentication_classes = (ExpiringTokenAuthentication,)
            def get(self, request, format=None):
                pass
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        """request has to include a Authenticate header
        """
        if not auth or auth[0].lower() != b'token':
            msg = 'Invalid token header. No token provided.'
            raise exceptions.AuthenticationFailed(msg)

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):

        try:
            token = self.model.objects.select_related('user').get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')

        """Inspect created time of token
        """
        utc_now = datetime.datetime.utcnow().replace(tzinfo=utc)
        if token.created < utc_now - datetime.timedelta(hours=24):
            token.delete()
            msg = 'Invalid token header. Token has expired.'
            raise exceptions.AuthenticationFailed(msg)

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')

        return (token.user, token)
