#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150427
#  @date          20150427
#  @version       0.1
'''
Note: How to process datetime and time module
'''

import time
import datetime

s1 = "2015-04-23 07:58:31"
s2 = "2015-04-23 07:59:13"

# A datetime string converts to a datetime object
# strptime: string convert to object
# strftime: timestamp convert to object
d1 = datetime.datetime.strptime(s1, "%Y-%m-%d %H:%M:%S")
d2 = datetime.datetime.strptime(s2, "%Y-%m-%d %H:%M:%S")

print d1
print d2

"""
2015-04-23 07:58:31
2015-04-23 07:59:13
"""

# A datetime object converts to a timestamp object
t1 = time.mktime(d1.timetuple())
t2 = time.mktime(d2.timetuple())

print t1
print t2

"""
1429747111.0
1429747153.0
"""

# A timestamp object converts to a datetime string
ts1 = datetime.datetime.fromtimestamp(t1).strftime('%Y-%m-%d %H:%M:%S')
ts2 = datetime.datetime.fromtimestamp(t2).strftime('%Y-%m-%d %H:%M:%S')

print ts1
print ts2

"""
2015-04-23 07:58:31
2015-04-23 07:59:13
"""
