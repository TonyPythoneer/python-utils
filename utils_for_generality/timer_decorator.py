#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150707
#  @date          20150707
#  @version       0.0
'''
It can detect program excution of function.
'''
import time


def exec_timer(func):
    def args_wrapper(*args, **kwargs):
        # timer
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        # output
        print ("=== {func_name} ===".format(func_name=func.__name__))
        print ("exec_time: " + str(end-start))
        print ("=== END ===")

        return result
    return args_wrapper
