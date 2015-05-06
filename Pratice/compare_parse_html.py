#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150219
#  @date          20150222
#  @version       0.0
"""
parse without langs:
sgmllib:0.00438080000877
lxml:0.00115759999752

parse with langs:
sgmllib:1.70899399996
lxml:1.62687300014
"""
__author__ = 'TonyPythoneer'

import time
from datetime import datetime
import httplib
import sgmllib

from lxml import html


excutenum = 1000


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


class LangsList(sgmllib.SGMLParser):
    def __init__(self, *args, **kwargs):
        sgmllib.SGMLParser.__init__(self, *args, **kwargs)
        self.is_span = ""
        self.langs = []
    def start_span(self, attrs):
        for key, value in attrs:
            if key == 'class' and value == 'lang':
                self.is_span = 1
    def end_span(self):
        self.is_span = ""
    def handle_data(self, text):
        if self.is_span:
            self.langs.append(text)

# read someone's repositories that host on github
conn = httplib.HTTPSConnection("github.com")
conn.request("GET", "/TonyPythoneer?tab=repositories")
webpage_about_repositories = conn.getresponse().read()

# repositories information feed SGMLParser
repositories_list = RepositoriesList()
repositories_list.feed(webpage_about_repositories)

# test1: use SGMLParser
start = time.time()
for i in range(excutenum):
    repositories_list.feed(webpage_about_repositories)
    for key in repositories_list.repositories.keys():
        # get langs information from repository
        conn.request("GET", repositories_list.repositories[key]['href'])
        webpage_about_repository = conn.getresponse().read()
        #
        langs_list = LangsList()
        langs_list.feed(webpage_about_repository)
        repositories_list.repositories[key]['langs'] = langs_list.langs
end = time.time()
print (end - start)/excutenum
print repositories_list.repositories

# test2: use lxml
start = time.time()
for i in range(excutenum):
    repository_dic = {}
    tree = html.fromstring(webpage_about_repositories)
    a_tags = tree.xpath('//h3[@class="repo-list-name"]/a')
    p_tags = tree.xpath('//p[@class="repo-list-meta"]/time')
    for index in range(len(a_tags)):
        a_tag = a_tags[index].attrib
        p_tag = p_tags[index].attrib
        # get name, href, datetime information from repositories
        repository_name = a_tag['href'].split('/')[-1]
        repository_href = a_tag['href']
        repository_datetime = datetime.strptime(p_tag['datetime'], "%Y-%m-%dT%H:%M:%SZ")
        # get langs information from repository
        conn.request("GET", repository_href)
        webpage_about_repository = conn.getresponse().read()
        tree = html.fromstring(webpage_about_repository)
        repository_langs = tree.xpath('//span[@class="lang"]/text()')
        # make a repository dic
        repository_dic[repository_name] = {'href': repository_href,
                                           'datetime': repository_datetime,
                                           'langs': repository_langs}
end = time.time()
print (end - start)/excutenum
print repository_dic

# same?
print repositories_list.repositories == repository_dic