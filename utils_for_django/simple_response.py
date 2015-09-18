#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150709
#  @date          20150918
#  @version       0.3.0 - Add api_response_v3
"""
If developing api services in Django REST framework,
it help developer save time to code response of view and focus to write comment of view.
"""
from rest_framework.response import Response
from rest_framework import status


HEADER = {'X-XSS-Protection': '1;mode=block',
          'X-Content-Type-Options': 'nosniff'}


def simple_response(api_result, success_status, error_status):
    """Simplify rest api design in view.

    When coding a view function originally needs 6 lines which exclude
    class and def declarations, the simple function just needs 3 lines
    to complete the same feature.

    Design reason:
        Let's suppose the api will return a pair of (sucessful) dict and (failed) dict or
        a pair of (sucessful) list and (failed) dict. These failed dicts certainly have
        a key of `err_msg` after they will add two sets of `code` and `status`.

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
    result_status = success_status if "err_msg" not in api_result else error_status
    if isinstance(api_result, dict):
        # api_result stores a new value with status code if it's a dict obj
        api_result['code'] = result_status
        api_result['status'] = 'OK' if "err_msg" not in api_result else 'Error'

    return Response(api_result,
                    headers=HEADER,
                    status=result_status)


def api_response(filled_form, api_func, success_status, error_status):
    """Near-perfect api response. Let data verification and api function separate out fully.

    It separates out data verification and api function.

    It has finished to verified that form instance will make a dictionary-like object
    containing clean data (or error details) and a boolean object meaning form validity.

    Furthermore, form validity can be reuse one time because it can clearly point out
    True or False. Make error details expand more elastically when it sets expression in
    if-else statement.

    Args:
        filled_form (form instance): Populate form with data from the request
        api_func (function): Make data process by corresponding view's api function
        success_status (Int): Return successful status code, e.g. 200, 201
        error_status (Int): Return successful status code, e.g. 400, 401

    Returns:
        Response (List): list of responses include api result and success/error status.

    Example:
        from rest_framework import status
        from rest_framework.views import APIView

        from utils.simple_response import api_response

        class ExampleAPIView(APIView):
            res_status = {"success_status": status.HTTP_201_CREATED,
                          "error_status": status.HTTP_401_UNAUTHORIZED}
            def post(self, request, format=None):
                return api_response(filled_form=FormClass(request.DATA),
                                    api_func=api_func.example_func,
                                    **res_status)
    """
    # Verification process: Verify by validators of form class
    form_validity = filled_form.is_valid()
    api_result = api_func(filled_form.clean_data) if form_validify else filled_form.error

    # Data process: Customize api_result content
    result_status = success_status if form_validify else error_status
    if isinstance(api_result, dict):  # it's customization for dict
        api_result['code'] = result_status
        if form_validify:
            api_result['status'] = 'OK'
            api_result['detail'] = None
        else:
            api_result['status'] = 'Error'

    return Response(api_result, headers=HEADER, status=result_status)


def api_response_v3(form, api_func, method):
    """Near-perfect api response. Let data verification and api function separate out fully.

    It separates out data verification and api function.

    It has finished to verified that form instance will make a dictionary-like object
    containing clean data (or error details) and a boolean object meaning form validity.

    Furthermore, form validity can be reuse one time because it can clearly point out
    True or False. Make error details expand more elastically when it sets expression in
    if-else statement.

    Args:
        form (form): Populate form with data from the request
        api_func (function): Make data process by corresponding view's api function
        success_status (Int): Return successful status code, e.g. 200, 201
        error_status (Int): Return successful status code, e.g. 400, 401

    Returns:
        Response (List): list of responses include api result and success/error status.

    Example:
        from rest_framework import status
        from rest_framework.views import APIView

        from utils.simple_response import api_response

        class ExampleAPIView(APIView):
            res_status = {"success_status": status.HTTP_201_CREATED,
                          "error_status": status.HTTP_401_UNAUTHORIZED}
            def post(self, request, format=None):
                return api_response(filled_form=FormClass(request.DATA),
                                    api_func=api_func.example_func,
                                    **res_status)
    """
    # Local variables: There are necessary variables
    http_status_codes = {'GET': status.HTTP_200_OK,
                         'POST': status.HTTP_201_CREATED,
                         'PATCH': status.HTTP_200_OK,
                         'DELETE': status.HTTP_204_NO_CONTENT}

    # Verification process: Verify by validators of form class
    form_validity = form.is_valid()
    api_result = api_func(form.clean_data) if form_validify else form.error

    # Data process: Customize api_result content
    result_status = http_status_codes[method] if form_validify else status.HTTP_400_BAD_REQUEST
    if isinstance(api_result, dict):  # it's customization for dict
        api_result['code'] = result_status
        if form_validify:
            api_result['status'] = 'OK'
            api_result['detail'] = None
        else:
            api_result['status'] = 'Error'

    return Response(api_result, headers=HEADER, status=result_status)
