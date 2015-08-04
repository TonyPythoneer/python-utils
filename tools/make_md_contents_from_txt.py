#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150804
#  @date          20150804
#  @version       0.1.1
"""Fast make contents of README.md

Example:

    How to use this python package. A first method enter command line:

        $ python make_readme_content.py
        $ >>> Input repo_url: <url>
"""
import os


def parse_line_to_dict(line):
    """Get important elements from line

    It's so complex logic process, so it need to be isolated.

    Arg:
        line (str): file's paragraph

    Return:
        dict: It can make contents
    """
    line = line.replace('\n', '')
    split_list = line.split(' ')
    sharps = split_list[0].count('#')

    # Process: Erase non-alpha and non-digit except space
    for word in line:
        is_space_or_hyphen = word.isspace() or (word is '-')
        if not is_space_or_hyphen:
            is_alpha_or_digit = word.isalpha() or word.isdigit()
            if not is_alpha_or_digit:
                line = line.replace(word, '')

    return {'sharps': sharps,
            'title': ' '.join(split_list[1:]),
            'href': '-'.join(line.split(' ')[1:]).lower()}


def get_contents_from_md(md_path):
    """Read file to get contents

    Arg:
        md_path (str): markdown path

    Return:
        contents (list): chapters and sections of contents
    """
    contents = []
    with open(md_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('#'):
                contents.append(parse_line_to_dict(line))
    return contents


def make_contents(md_path, contents):
    """Make a file

    Args:
        md_path (str): markdown path
        contents (list): chapters and sections of contents
    """
    # Process: Retain origin content of file
    with open(md_path, 'r') as f:
        origin_content = f.readlines()

    # Process: Combine of old and new contents
    with open(md_path, 'w') as f:
        for content in contents:
            context = '- [{title}](#{href})'.format(title=content['title'],
                                                    href=content['href'])
            context = 4 * (content['sharps'] - 1) * ' ' + context + '\n'
            f.write(context)
        f.write('\n')
        f.writelines(origin_content)

    # Process: Hint that file have been completed
    print 'SUCCESS!!'
    print 'Contents complete: ' + md_path


def input_md_directory():
    """Get files when extension is `.md`

    Return:
        md_list (list): A record of all md file paths
    """
    md_list = []
    directory = raw_input('>>> Input path: ')
    for each_file in os.listdir(directory):
        if each_file.endswith(".md"):
            md_list.append(os.path.join(directory, each_file))
    return md_list


if __name__ == "__main__":
    # Action: Enter command line
    md_list = input_md_directory()

    # Function: Process data
    for md_path in md_list:
        contents = get_contents_from_md(md_path)
        make_contents(md_path, contents)
