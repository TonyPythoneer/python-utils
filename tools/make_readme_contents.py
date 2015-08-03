'''
'''
import sys
import os
import urllib2

from lxml import html


EXAMPLE = "https://github.com/rosarior/awesome-django/blob/master/README.md"


def web_crawler(url):
    '''Catch the web page
    '''
    res = urllib2.urlopen(url)
    content = res.read()
    return content

def get_tag_attribute(content):
    '''Analyze the html tag
    '''
    tree = html.fromstring(content)

    html_tags = [{'tag': 'a',
                  'attribs': {'class': 'anchor',
                              'aria-hidden': 'true'}}]

    #
    for index, tag in enumerate(html_tags):
        attribs = map(lambda x: '@{}="{}"'.format(*x),
                      tag['attribs'].items())
        attribs = ' and '.join(attribs)
        html_tags[index]['attribs'] = attribs

    xpath_list = map(lambda x: '{tag}[{attribs}]'.format(**x), html_tags)
    xpath_str = '//' + '/'.join(xpath_list)

    html_objs = tree.xpath(xpath_str)

    contents = []
    for html_obj in html_objs:
        parent_tag = html_obj.getparent().tag
        if parent_tag in ['h1','h2']:
            contents.append({parent_tag : html_obj.attrib["href"]})

    return contents


def make_contents(repo_url, contents):
    file_name = repo_url.split('/')[-1] + '-contents.md'
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = '{dir}/{file_name}'.format(dir=base_dir, file_name=file_name)

    with open(file_path, 'w') as f:
        for content in contents:
            context_dict = {'title_name': content.values()[0],
                            'link': content.values()[0]}
            context = '- [{title_name}]({link})'.format(**context_dict) + '\n'
            if 'h1' in content:
                f.write(context)
            elif 'h2' in content:
                f.write('    ' + context)


content = web_crawler(EXAMPLE)
contents = get_tag_attribute(content)
x = make_contents(EXAMPLE, contents)
