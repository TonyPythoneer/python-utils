#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150702
#  @date          20150702
#  @version       0.0
'''
If in django, you can use this function to confirm all urls.
'''

# You invoke the urls if you call `shell` of python in django settings
try:
    import urls
except ImportError:
    pass

# You invoke the urls if you call `shell` of manage.py of django
try:
    from website import urls
except ImportError:
    pass


def show_urls(urllist=urls.urlpatterns, depth=0):
    '''show all urls
    '''
    for entry in urllist:
        print "  " * depth, entry.regex.pattern
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)

#show_urls(urls.urlpatterns)
show_urls()
