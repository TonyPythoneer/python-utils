#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150709
#  @date          20150709 - build api_response
#  @version       0.0
from django.conf import settings
from rest_framework.response import Response
'''
If developing api services in Django REST framework, 
let developer save time to code response of view and focus to write comment of view.
'''


HEADER = {'X-XSS-Protection': '1;mode=block',
          'X-Content-Type-Options': 'nosniff'}


def simple_response(api_result, success_status, error_status):
    """Simplify rest api design in view.

    Args:
        api_result (Dict): return value when api completes to evaluate
        success_status (Int): return status code if api is successful to evaluate
        error_status (Int): return status code if api does error handling

    Returns:
        Response (List): list of responses include api result and success/error status.

    Example:
        >>> from rest_framework import status
        >>> from simple_response import simple_response
        >>> class RestView(APIView):
        ...    def post(self, request, format=None):
        ...        return simple_response(api_result=api_account.user_creation(request.DATA),
        ...                               success_status=status.HTTP_201_CREATED,
        ...                               error_status=status.HTTP_401_UNAUTHORIZED)
    """
    # example:
    # 200 means HTTP_200_OK
    # 201 means HTTP_201_CREATED
    if "error_msg" not in api_result:
        return Response(api_result,
                        headers=HEADER,
                        status=success_status)

    # example:
    # 400 means HTTP_400_BAD_REQUEST
    # 401 means HTTP_401_UNAUTHORIZED
    return Response(api_result,
                    status=error_status)
