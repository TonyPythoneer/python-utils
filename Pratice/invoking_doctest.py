#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150429
#  @date          20150429
#  @version       0.1
'''
Note:It a tool for scanning a module and validating tests embedded in a program’s docstrings.
'''
import doctest


def average(values):
    """Computes the arithmetic mean of a list of numbers.

    >>> print(average([20, 30, 70]))
    40
    >>> print(average([1, 2, 3]))
    2
    """
    return sum(values) // len(values)

doctest.testmod()
