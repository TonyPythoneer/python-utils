import urllib2
import sgmllib
import time

tStart = time.time()

class RepositoriesList(sgmllib.SGMLParser):
    """
    Get repositories list from github member.
    """
    def __init__(self, *args, **kwargs):
        sgmllib.SGMLParser.__init__(self, *args, **kwargs)
        self.is_li = ""
        self.is_h3 = ""
        self.is_a = ""
        self.repositories = {}
    def start_li(self, attrs):
        """First objective html tag
        I need tagname that its name calls 'repo-list-item public source'
        """
        if attrs:
            for key, value in attrs:
                if value == 'repo-list-item public source':
                    self.is_li = 1
    def end_li(self):
        self.is_li = ""
    def start_h3(self, attrs):
        """Second objective html tag
        I need tagname that its name calls 'repo-list-name'
        """
        if attrs:
            for key, value in attrs:
                if value == 'repo-list-name':
                    self.is_h3 = 1
    def end_h3(self):
        self.is_h3 = ""
    def start_a(self, attrs):
        """Third objective html tag
        In order to confirm that a tag inserts h3 and li tag both.
        """
        if self.is_li and self.is_h3:
            for key, value in attrs:
                if key == "href":
                    repository_name = value.split('/')[-1]
                    repository_url = 'https://github.com' + value
                    self.repositories[repository_name] = repository_url
    def end_a(self):
        self.is_a = ""


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


# read that my repositories host on github
my_repositories = 'https://github.com/TonyPythoneer?tab=repositories'
my_repositories_content = urllib2.urlopen(my_repositories).read()

my_repositories = RepositoriesList()
my_repositories.feed(my_repositories_content)



for key in my_repositories.repositories.keys():
    print key
    
    each_repository_content = urllib2.urlopen(my_repositories.repositories[key]).read()

    my_repository = LangsList()
    my_repository.feed(each_repository_content)

    print my_repository.langs