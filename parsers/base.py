import re
import pytz
import random
import string
import requests
import feedparser
from datetime import datetime
from django.conf import settings
from BeautifulSoup import BeautifulSoup
from sourcessay.search import signs_of_weakness

UTC = pytz.timezone('UTC')
LOCAL = pytz.timezone(settings.TIME_ZONE)


class BaseParser(object):
    def __init__(self, url):
        self.url = url
        self.full_url = url
        self.content_tags = [
            {"id": "content"}
        ]

    def get_response(self):
        """
        Replace this with a method to get a full-text
        page, if needed.
        """
        return requests.get(self.url)

    def get_content(self):
        """
        This method should return a string that contains 
        just the main article content.
        """
        response = self.get_response()
        self.full_url = response.url
        soup = BeautifulSoup(response.text)
        for tag in self.content_tags:
            content = soup.find("div", tag)
            if content:
                return str(content)
        return None

    def uses_anonymous(self):
        """
        Returns the phrase used or False if it can't find one.
        """
        content = self.get_content()
        if content:
            content = content.lower()
            for phrase in signs_of_weakness:
                if phrase in content:
                    return phrase
        return False


class BaseFeed(object):
    """
    An RSS feed we want to aggregate.
    """
    def __init__(self, source):
        self.source = source
    
    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.source.name)
    
    def get_random_string(self, length=6):
        """
        Generate a random string of letters and numbers
        """
        return ''.join(random.choice(string.letters + string.digits) for i in xrange(length))
    
    def fetch(self):
        return feedparser.parse(self.source.feed_url + "&" + self.get_random_string())
    
    def utc_to_local_datetime(self, dt):
        """
        Map datetime as UTC object to it's localtime counterpart.
        """
        return dt.astimezone(LOCAL)
    
    def utc_to_local_timestamp(self, ts, orig_tz=UTC):
        """
        Convert a timestamp object into a tz-aware datetime object.
        """
        timestamp = datetime.fromtimestamp(ts,tz=orig_tz)
        return timestamp.astimezone(LOCAL)
    
    def utc_to_local_timestruct(self, ts, orig_tz=UTC):
        """
        Convert a timestruct object into a tz-aware datetime object.
        """
        return self.utc_to_local_timestamp(time.mktime(ts), orig_tz)
    
    def clean_pub_date(self, x):
       try:
           dt = datetime(*x.get('updated_parsed')[:6], tzinfo=UTC)
           return self.utc_to_local_datetime(dt)
       except:
           raise
           return None
    
    def get_content(self, e):
        try:
            return e['content'][0].get('value')
        except (IndexError, KeyError):
            return None
    
    def get_authors(self, e):
        byline = e.get('author', None)
        if not byline: 
            return None
        if not "By" in byline:
            # This is kinda crazy looking, but the 
            # [i for s in str for i in s] will flatten a list of lists,
            # and the map/split will just split out by commas and ands.
            return [item for sublist in map(lambda s: s.split(' and '), byline.split(', ')) for item in sublist]
        fallback_byline = re.compile("([\-\w.&; ]+)")
        single_byline = re.compile("By ([\-\w.&; ]+)")
        double_byline = re.compile("By ([\-\w.&; ]+) and ([\-\w.&; ]+)")
        triple_byline = re.compile("By ([\-\w.&; ]+), ([\-\w.&; ]+) and ([\-\w.&; ]+)")
        byline_res = (
            triple_byline,
            double_byline,
            single_byline,
            fallback_byline
        )
        # Scan through from more complex to less complex. Take
        # first match, because single_byline will match the first
        # name from both double and triples.
        for regex in byline_res:
            matches = regex.search(byline)
            if matches:
                return matches.groups()
        # If not matches, return full byline
        return (byline,)
        
    @property
    def data_list(self):
        """
        Cleans up the feed items so they are ready for the datastore.
        """
        # Pull the data
        data = self.fetch()
        # Loop through all the items in the feed
        data_list = []
        for entry in data['entries']:
            # Pull out the data we want to keep
            data_dict = {
                'source': self.source,
                'title': entry.get('title'),
                'authors': self.get_authors(entry),
                'url': entry.get('link'),
                'publication_date': self.clean_pub_date(entry),
                'description': entry.get('summary') or "",
                'content': self.get_content(entry) or "",
                'raw_feed': entry,
            }
            data_list.append(data_dict)
        return data_list
