#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150702
#  @date          20150702
#  @version       0.0
'''
Create Multipurpose Internet Mail Extensions (MIME) Mail
'''
import httplib2
from json import dumps


header = {'Content-Type': 'application/json; charset=UTF-8'}
pem_path = "/path/to/domainname.pem"
h = httplib2.Http(ca_certs=pem_path, disable_ssl_certificate_validation=True)

req_dict = {
    "url": "url",
    "method": "method",  # example: GET, POST, PUT/PATCH, DELETE
    "body": dumps({"key": "value"}),  # httplib2 only accepts a json-like string
    "headers": header  # You send a json-like string and need to set the header
}

resp, content = h.request(**req_dict)
print resp
print content
