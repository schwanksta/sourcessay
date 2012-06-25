import parsers
from django.db import models
from parsers.base import BaseFeed

class Source(models.Model):
    """
    A data source
    """
    name = models.CharField(max_length=500)
    feed_url = models.CharField(max_length=500)
    FEED_HANDLER_CHOICES = (
        ("GoogleReaderFeed", "Google Reader - Sources Say"),
    )
    feed_handler = models.CharField(max_length=100,
        choices=FEED_HANDLER_CHOICES)
    NEWS_OUTLET_URLS = (
        ("nytimes.com", "NYTimes"),
        ("latimes.com", "LATimes"),
        ("guardian.co.uk", "Guardian")
    )

    class Meta:
        ordering = ("name",)

    def get_news_outlet(self, url):
        for outlet_url, choice in self.NEWS_OUTLET_URLS:
            if outlet_url in url:
                return choice

    def process_feed(self):
        feed = BaseFeed(self)
        data_list = feed.data_list
        for data in data_list:
            url = data.get('url')
            news_outlet = self.get_news_outlet(url)
            if not news_outlet:
                continue
            parser = getattr(parsers, "%sParser" % news_outlet)
            parsed = parser(url)
            print parsed.full_url
            anonymous = parsed.uses_anonymous()
            print anonymous
            if not anonymous:
                continue
            if Item.objects.filter(url=url):
                continue
            i = Item(
                url = parsed.full_url,
                title = data.get('title'),
                news_outlet = news_outlet,
                source_feed = data.get('source'),
                line_used = anonymous
            )
            i.save()
    
    def __unicode__(self):
        return self.name


class Item(models.Model):
    source_feed = models.ForeignKey(Source)
    NEWS_OUTLET_CHOICES = (
        ("NYTimes", "The New York Times"),
        ("LATimes", "The Los Angeles Tims"),
        ("Guardian", "The Guardian")
    )
    news_outlet = models.CharField(choices=NEWS_OUTLET_CHOICES, max_length=255)
    title = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    line_used = models.CharField(max_length=255)
    byline = models.
