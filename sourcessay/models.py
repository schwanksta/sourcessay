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
                return choice, outlet_url
        return (None, None)

    def process_feed(self):
        feed = BaseFeed(self)
        data_list = feed.data_list
        for data in data_list:
            url = data.get('url')
            news_outlet, outlet_url = self.get_news_outlet(url)
            if not news_outlet:
                continue
            parser = getattr(parsers, "%sParser" % news_outlet)
            parsed = parser(url)
            outlet_obj = Outlet.objects.get(url=outlet_url)
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
                news_outlet = outlet_obj,
                source_feed = data.get('source'),
                line_used = anonymous
            )
            i.save()
    
    def __unicode__(self):
        return self.name

class Outlet(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    url = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name

class Byline(models.Model):
    name = models.CharField(max_length=255)
    news_outlet = models.ForeignKey(Outlet)

    def __unicode__(self):
        return self.name

class Item(models.Model):
    source_feed = models.ForeignKey(Source)
    NEWS_OUTLET_CHOICES = (
        ("new-york-times", "The New York Times"),
        ("los-angeles-times", "The Los Angeles Tims"),
        ("the-guardian", "The Guardian")
    )
    news_outlet = models.ForeignKey(Outlet)
    byline = models.ManyToManyField(Byline)
    title = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    line_used = models.CharField(max_length=255)
