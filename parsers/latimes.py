import urllib2
import requests
from parsers.base import BaseParser
from BeautifulSoup import BeautifulSoup

class LATimesParser(BaseParser):
    def __init__(self, *args, **kwargs):
        super(LATimesParser, self).__init__(*args, **kwargs)
        self.content_tags = [
            {"id": "story-body-text"},
            {"class": "entry-body"},
        ]

    @property
    def full_url(self):
        # We use the requests library to return the full URL.
        # then search the page for the 'single page' URL if it's 
        # got one.
        r = requests.get(self.url)
        soup = BeautifulSoup(urllib2.urlopen(r.url))
        for s in soup.findAll("a"):
            if "single page" in s.contents:
                return "http://www.latimes.com%s" % s['href']
        return r.url
