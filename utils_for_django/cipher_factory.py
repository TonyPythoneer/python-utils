#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150713
#  @date          20150713
#  @version       0.0
"""
reset/token code factory
"""
import string
import random
import hashlib
import time

from django.conf import settings


def get_random_code(length=20):
    """Create a random string

    Args:
        length (int): length of output string

    Returns:
        string: random string

    Example:
        The recommended and main purpose of the function is to give user's reset code.

            active_code = get_random_code()
            user = User.objects.create_user(username=acc,
                                            password=active_code,
                                            email=acc)
    """
    hash_choice = string.digits + string.ascii_letters

    return ''.join([random.choice(hash_choice) for x in range(length)])


def get_hash(hide_str):
    """Create a SHA256 hash

    Args:
        hide_str (string): a string for hash

    Return:
        string: SHA256 hash

    Example:
        The recommended and main purpose of the function is to make user's token.

            access_token = get_hash(email)
    """
    maker = hashlib.sha256()
    maker.update(hide_str)
    maker.update(settings.SHA256_MAGIC)
    maker.update(str(time.time()))

    return maker.hexdigest()
