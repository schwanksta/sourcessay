import pytz
import random
import string
import urllib2
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
        self.content_tags = [
            {"id": "content"}
        ]

    @property
    def full_url(self):
        """
        Replace this with a method to get a full-text
        page, if needed.
        """
        return self.url

    def get_content(self):
        """
        This method should return a string that contains 
        just the main article content.
        """
        soup = BeautifulSoup(urllib2.urlopen(self.full_url))
        for tag in self.content_tags:
            content = soup.find("div", tag)
            if content:
                return str(content)
        return None

    def uses_anonymous(self):
        """
        Returns the phrase used or False if it can't find one.
        """
        content = self.get_content().lower()
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
                'url': entry.get('link'),
                'publication_date': self.clean_pub_date(entry),
                'description': entry.get('summary') or "",
                'content': self.get_content(entry) or "",
                'raw_feed': entry,
            }
            data_list.append(data_dict)
        return data_list