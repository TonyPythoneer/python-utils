import sys
import os
import urllib2
from lxml import html
import operator
'''
Note: It's just a small tool for kuai xunlei

For example:
python the_python.py http://kuai.xunlei.com/d/FhJHCAJdKgBIUTRV669
'''


def cmd(*args):
    '''it can type command line
    '''
    # Inspect args that it is valid
    try:
        url = args[0]
    except IndexError:
        print "Error: Please input kuai xunlei url."
        sys.exit()

    # Inspect url whether it is kuai xunlei
    if "http://kuai.xunlei.com/" not in args[0]:
        print "Error: It only applies kuai xunlei."
        sys.exit()
    return url


def crawler(url):
    '''Catch the web page
    '''
    res = urllib2.urlopen(url)
    content = res.read()
    return content


def get_tag_attribute(content):
    '''Analyze the html tag
    '''
    tree = html.fromstring(content)
    html_elements = ['li', 'div[@class="file_tr"]', 'span[@class="c_2"]', 'a']
    search_path = "//{0}".format('/'.join(html_elements))
    a_tags = tree.xpath(search_path)
    download_links = {}
    for a_tag in a_tags:
        a_kw = a_tag.attrib
        download_links.update({a_kw["download"]: a_kw["href"]})
    return download_links


if __name__ == "__main__":
    # Command line
    url = cmd(*sys.argv[1:])

    # Process data
    content = crawler(url)
    links = get_tag_attribute(content)

    sorted_links = sorted(links.items(), key=operator.itemgetter(0))
    base_dir = os.path.dirname(os.path.abspath(__file__))
    txt_path = "{dir}/xunlei_download_list.txt".format(dir=base_dir)
    with open(txt_path,"w") as f:
        for sorted_link in sorted_links:
            f.write(sorted_link[1] + '\n')
    print "Success: OK! It creates a links txt that locates {txt_path}".format(txt_path=txt_path)
