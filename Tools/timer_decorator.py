from functools import wraps
import time

def timer_decorater(custom_name="", exec_time=1):
    def func_wrapper(func):
        #@wraps(func)
        def args_wrapper(*args,**kwargs):
            '''w'''
            # timer
            start = time.time()
            for num in range(exec_time):
                func()
            end = time.time()
            average = (end - start) / exec_time

            # print result
            if custom_name:
                print "{fun_name}:{avg}".format(fun_name=custom_name,
                                                avg=average)
            else:
                print "exec_avg_time:{avg}".format(fun_name=custom_name,
                                                   avg=average)
        return args_wrapper
    return func_wrapper


@timer_decorater(exec_time=10**6)
def test_make_dictionary():
    '''t'''
    a = {}

test_make_dictionary()
print test_make_dictionary.__doc__
print test_make_dictionary.__name__
print test_make_dictionary.__module__
