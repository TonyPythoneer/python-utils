#!/usr/bin/env python
# -*- encoding: utf8 -*-

## @package test.amqp
#@brief  Stress Testing.
#@details  壓力測試.
#@authors Evan
#@version 2.1
#@date 2015-08-27

import sys
import time
import json
import optparse
import requests as rs

from threading import Thread

_success = [0]
_error = [0]

def touch(url, num):
    try:
        _l = (num, ) + time.localtime()[3:6]
        _data = {
            "exchange": "http.test.direct",
            "deliverymode": 0, "priority":99, "key":'s1',
            "body": "{'sn': %s, 'time': '%s:%s:%s'}" % _l
        }
        _r = rs.post(url, data=json.dumps(_data), verify=False)
        _success[0] += 1
    except:
        _error[0] += 1

    return _r.text

def main(options):

    st = time.time()
    _method = 'https' if options.https else 'http'
    url = '%s://%s:%s/publish' % (_method, options.host, options.port)
    times = options.times

    _pool = []
    for i in xrange(times):
        _t = Thread(target=touch, args=(url, i,))
        if options.thread: _t.start()
        else: _t.run()
        _pool.append(_t)

        if i % 200 == 0:
            print _success, _error, '%s per sec' % (_success[0]/(time.time() - st))

    if options.thread: map(lambda x: x.join(), _pool)


    print 'Done!', time.time() - st
    return 0

if __name__ == '__main__':
    #usage = "usage: %prog [options] arg1 arg2"
    #parser = optparse.OptionParser(usage=usage)
    parser = optparse.OptionParser(usage=main.__doc__)

    parser.add_option("--host", type="string",
                      help="Host Name or IP address",
                      dest="host", default="192.168.6.19")

    parser.add_option("-p", "--port", type="string",
                      help="Target Port",
                      dest="port", default="7379")

    parser.add_option("-t", "--times", type="int",
                      help="How many times do you want?",
                      dest="times", default=100000)

    parser.add_option("--thread", action="store_true",
                      help="Threading.",
                      dest="thread", default=True)

    parser.add_option("--https", action="store_true",
                      help="Threading.",
                      dest="https", default=False)
    """
    parser.add_option("-d", "--dir", type="string",
                      help="List of directory",
                      dest="inDir", default=".")

    """
    options, args = parser.parse_args()

    if len(args) != 0:
        parser.print_help()
        sys.exit(1)

    sys.exit(main(options))


