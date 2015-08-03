'''
'''
import urllib2
from lxml import html


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

    print contents


content = web_crawler("https://github.com/rosarior/awesome-django/blob/master/README.md")
get_tag_attribute(content)
