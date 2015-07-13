#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150709
#  @date          20150713
#  @version       0.0.1 - api_result stores a new value with status code
"""
If developing api services in Django REST framework,
it help developer save time to code response of view and focus to write comment of view.
"""
from rest_framework.response import Response


HEADER = {'X-XSS-Protection': '1;mode=block',
          'X-Content-Type-Options': 'nosniff'}


def simple_response(api_result, success_status, error_status):
    """Simplify rest api design in view.

    When coding a view function originally needs 6 lines which exclude
    class and def declarations, the simple function just needs 3 lines
    to complete the same feature.

    Warning:
        Please be sure to check your error handling message is dictionary type and
        includes `err_msg` of key.

    Args:
        api_result (Dict): return value when api completes to evaluate
        success_status (Int): return status code if api is successful to evaluate
            200 means HTTP_200_OK when touching off function except creating new object
            201 means HTTP_201_CREATED when touching off function creates new object
        error_status (Int): return status code if api does error handling
            400 means HTTP_400_BAD_REQUEST
            401 means HTTP_401_UNAUTHORIZED when the view needs token or login

    Returns:
        Response (List): list of responses include api result and success/error status.

    Example:
        Look! It's just so easy and clear to code view.

            from rest_framework import status
            from simple_response import simple_response
            class ExampleView(APIView):
               def post(self, request, format=None):
                   return simple_response(api_result=api_account.user_creation(request.DATA),
                                          success_status=status.HTTP_201_CREATED,
                                          error_status=status.HTTP_401_UNAUTHORIZED)

        Success status:
            200 means HTTP_200_OK when touching off function except creating new object
    """
    if "err_msg" not in api_result:
        # api_result stores a new value with status code
        api_result['code'] = success_status  # api_result['status'] = success_status
        return Response(api_result,
                        headers=HEADER,
                        status=success_status)

    # api_result stores a new value with status code
    api_result['code'] = error_status  # api_result['status'] = error_status
    return Response(api_result,
                    status=error_status)
