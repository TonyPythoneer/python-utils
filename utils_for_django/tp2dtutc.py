#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150713
#  @date          20150713
#  @version       0.0
from datetime import datetime
from time import time

from django.utils.timezone import utc


def tp2utcdt(the_time):
    """timestamp convets to UTC datetime

    Args:
        the_time (string, int, float): a timestamp

    Returns:
        datetime: datetime format of the_time

    Example:
        >>> tp2utcdt(time())
        >>> datetime.datetime(2015, 7, 13, 10, 33, 16, 95000, tzinfo=<UTC>)

    """
    utcdt = datetime.utcfromtimestamp(float(the_time)).replace(tzinfo=utc)

    return utcdt
