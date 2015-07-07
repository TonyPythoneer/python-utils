import time


def exec_timer(func):
    def args_wrapper(*args, **kwargs):
        # timer
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        # output
        print ("=== {func_name} ===".format(func_name=func.__name__))
        print ("exec_time:" + str(end-start))
        print ("=== END ===")

        return result
    return args_wrapper
