#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150429
#  @date          20150429
#  @version       0.1
'''
Note: How to invoke attr of object with getattr and dir.
'''
import operator

is_call = []
is_not_call = []

for attr_string in dir(operator):
    attr = getattr(operator, attr_string)
    if hasattr(attr, "__call__"):
        is_call.append(attr_string)
    else:
        is_not_call.append(attr_string)

print "is_call:\n{0}".format(str(is_call))
print "is_not_call:\n{0}".format(str(is_not_call))
