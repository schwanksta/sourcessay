import parsers
from django.db import models
from parsers.base import BaseFeed, BaseParser

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

    def parse(self, news_outlet, url):
        try:
            Parser = getattr(parsers, "%sParser" % news_outlet)
        except:
            Parser = BaseParser
        return Parser(url)

    def process_feed(self):
        feed = BaseFeed(self)
        data_list = feed.data_list
        for data in data_list:
            url = data.get('url')
            news_outlet, outlet_url = self.get_news_outlet(url)
            if not news_outlet:
                continue
            parsed = self.parse(news_outlet, url)
            outlet_obj = Outlet.objects.get(url=outlet_url)
            anonymous = parsed.uses_anonymous()
            print parsed.full_url
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
            for byline in data.get('authors'):
                by, c = Author.objects.get_or_create(name=byline.title(), news_outlet=outlet_obj)
                if c: by.save()
                i.authors.add(by)
            
    
    def __unicode__(self):
        return self.name

class Outlet(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    url = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=255)
    news_outlet = models.ForeignKey(Outlet)

    def __unicode__(self):
        return self.name

class Item(models.Model):
    source_feed = models.ForeignKey(Source)
    news_outlet = models.ForeignKey(Outlet)
    authors = models.ManyToManyField(Author, null=True, blank=True)
    title = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    line_used = models.CharField(max_length=255)

    def get_byline(self):
        return "By " + ", ".join([str(o) for o in self.authors.all()])

    def __unicode__(self):
        return "%s - %s" % (self.news_outlet, self.title)
