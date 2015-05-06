#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150219
#  @date          20150506
#  @version       0.0
"""
When parsing html, it will get links of repos

Testing each module about time of program execution. It's as below:
sgmllib:0.0118350000381
lxml:0.00131200003624
bs4:0.0157369999886
"""
__author__ = 'TonyPythoneer'

from datetime import datetime
import time
import httplib
import sgmllib

from bs4 import BeautifulSoup
from lxml import html


def timer_decorater(custom_name="", exec_time=1):
    def func_wrapper(func):
        def args_wrapper(wp,*args,**kwargs):
            # timer
            start = time.time()
            for num in range(exec_time):
                func(wp)
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


class RepositoriesList(sgmllib.SGMLParser):
    """
    Get repositories list from github member.
    """
    def __init__(self, *args, **kwargs):
        # init
        sgmllib.SGMLParser.__init__(self, *args, **kwargs)
        # declare var about conditional statement of html tag
        self.is_li = ""
        self.is_h3 = ""
        self.is_p = ""
        # repository name
        self.repository_name = ""
        # arrange a dictionary
        self.repositories = {}
    def start_li(self, attrs):
        """
        A first objective element includes h3 and p elements.

        Requirement:
            A html tag that its class calls 'repo-list-item public source'
        """
        if attrs:
            for key, value in attrs:
                if key == 'class' and value == 'repo-list-item public source':
                    self.is_li = 1
    def end_li(self):
        self.is_li = ""
    def start_h3(self, attrs):
        """A second objective element includes a element.

        Requirement:
            A html tag that its class calls 'repo-list-name'
        """
        if attrs:
            for key, value in attrs:
                if key == 'class' and value == 'repo-list-name':
                    self.is_h3 = 1
    def end_h3(self):
        self.is_h3 = ""
    def start_a(self, attrs):
        """
        A third objective element.

        In order to confirm that the html tag has been included both h3 and li elements.

        Requirement:
            I need a tag about repository name and url information.
        """
        if self.is_li and self.is_h3:
            for key, value in attrs:
                if key == "href":
                    self.repository_name = value.split('/')[-1]
                    self.repositories[self.repository_name] = {'href': value}
    def start_p(self, attrs):
        """
        A second objective element includes time elements.

        In order to confirm that a tag inserts h3 and li tag both.

        Requirement:
            A html tag that its class calls 'repo-list-meta'
        """
        if self.is_li:
            for key, value in attrs:
                if key == "class" and value == "repo-list-meta":
                    self.is_p = 1
    def start_time(self, attrs):
        """
        A third objective element.

        In order to confirm that a tag inserts h3 and li tag both.

        Requirement:
            A html tag that its class calls 'repo-list-meta'
        """
        if self.is_p:
            for key, value in attrs:
                if key == "datetime":
                    datetime_val = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
                    self.repositories[self.repository_name]['datetime'] = datetime_val
            self.is_p = ""


@timer_decorater(custom_name="sgmllib", exec_time=1000)
def sgmllib_parse_html(web_page):
    # repositories information feed SGMLParser
    repositories_list = RepositoriesList()
    repositories_list.feed(web_page)

    # get href of repos
    repositories_list.feed(webpage_about_repositories)


@timer_decorater(custom_name="lxml", exec_time=1000)
def lxml_parse_html(web_page):
    tree = html.fromstring(webpage_about_repositories)
    a_tags = tree.xpath('//h3[@class="repo-list-name"]/a')


@timer_decorater(custom_name="bs4", exec_time=1000)
def bs4_parse_html(web_page):
    soup = BeautifulSoup(webpage_about_repositories)
    h3_tags = soup.find_all('h3', {'class':'repo-list-name'})
    a_tags = [ t.a for t in h3_tags ]

# read someone's repositories that host on github -- my repos for example.
conn = httplib.HTTPSConnection("github.com")
conn.request("GET", "/TonyPythoneer?tab=repositories")
webpage_about_repositories = conn.getresponse().read()

# test1: sgmllib
sgmllib_parse_html(webpage_about_repositories)

# test2: lxml
lxml_parse_html(webpage_about_repositories)

# test3: bs4
bs4_parse_html(webpage_about_repositories)
