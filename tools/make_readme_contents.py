#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150803
#  @date          20150804
#  @version       0.1
'''Fast make contents of README.md of repo
'''
import sys
import os
import urllib2

from lxml import html


def web_crawler(url):
    '''Catch the web page
    '''
    res = urllib2.urlopen(url)
    web_page = res.read()
    return web_page


def get_contents_from_html(content):
    '''Parse the html tag
    '''
    tree = html.fromstring(content)

    # Declare: I appoint html tag its attribs is as follow
    html_tags = [{'tag': 'a',
                  'attribs': {'class': 'anchor',
                              'aria-hidden': 'true'}}]

    # Process: It coverts dict to str for xpath
    for index, tag in enumerate(html_tags):
        attribs = map(lambda x: '@{}="{}"'.format(*x),
                      tag['attribs'].items())
        attribs = ' and '.join(attribs)
        html_tags[index]['attribs'] = attribs
        html_tags[index] = '{tag}[{attribs}]'.format(**html_tags[index])

    # Process: Search out objectives of html
    path = '//' + '/'.join(html_tags)
    html_objs = tree.xpath(path)

    # process: Build elements of contents
    contents = []
    for html_obj in html_objs:
        parent_obj = html_obj.getparent()
        if parent_obj.tag in ['h1', 'h2']:
            contents.append({'tag': parent_obj.tag,
                             'title': parent_obj.text_content(),
                             'href': html_obj.attrib['href']})

    return contents


def make_contents(repo_name, contents):
    # Process: Build file path
    file_infos = {'file_name': repo_name + '-contents.md',
                  'base_dir': os.path.dirname(os.path.abspath(__file__))}
    file_path = '{base_dir}/{file_name}'.format(**file_infos)

    # Process: Start to write file
    print contents
    with open(file_path, 'w') as f:
        for content in contents:
            context = '- [{title}]({href})'.format(**content) + '\n'
            if 'h1' in content['tag']:
                f.write(context)
            elif 'h2' in content['tag']:
                f.write('    ' + context)


def cmd(*args):
    '''Enter command line in console
    '''
    # Inspect: It has to include at least one arg
    try:
        url = args[0]
    except IndexError:
        print "Error: No any arg."
        sys.exit()

    # Inspect url whether it is kuai xunlei
    split_list = args[0].split('/')
    if split_list[2] is 'github.com':
        print "Error: It only applies kuai xunlei."
        sys.exit()
    return split_list[4], url


if __name__ == "__main__":
    # Action: Enter command line
    if sys.argv[1:]:
        repo_name, url = cmd(*sys.argv[1:])
    else:
        repo_url = raw_input('>>> Input repo_url:')
        repo_name, url = cmd(repo_url)

    # Function: Process data
    web_page = web_crawler(url)
    contents = get_contents_from_html(web_page)
    make_contents(repo_name, contents)
