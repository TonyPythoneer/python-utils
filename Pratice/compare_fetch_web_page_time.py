"""
Result:
urllib3:0.130320000648
urllib2:0.0897999954224
urllib:0.0918000030518
httplib:0.0340799999237
requests:0.105320000648
"""
import time
import urllib
import urllib2
import httplib

import urllib3
import requests

def test_execution_time(module_func, module_name, select_param):
    # declare var
    excutenum = 50
    google_host = 'google.com'
    google_url = 'http://%s/' % google_host
    # select param
    if select_param == "host":
        use_this_var = google_host
    elif select_param == "url":
        use_this_var = google_url
    # calculate execution time
    start = time.time()
    for i in range(excutenum):
        r = module_func(use_this_var)
    end = time.time()
    during = (end - start)/excutenum
    # result
    return "%s:%s" % (module_name, during)


# test urllib3 execution time
def pack_urllib3(url):
    return urllib3.PoolManager().request('GET', url)
print test_execution_time(pack_urllib3, 'urllib3', 'url')

# test urllib2 execution time
print test_execution_time(urllib2.urlopen, 'urllib2', 'url')

# test urllib execution time
print test_execution_time(urllib.urlopen, 'urllib', 'url')

# test httplib execution time
def pack_httplib(host):
    conn=httplib.HTTPConnection(host)
    conn.request("GET", "/")
    return conn.getresponse()
print test_execution_time(pack_httplib, 'httplib', 'host')

# test requests execution time
print test_execution_time(requests.get, 'requests', 'url')