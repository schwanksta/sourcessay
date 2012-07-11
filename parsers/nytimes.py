import requests
from parsers.base import BaseParser

class NYTimesParser(BaseParser):
    def __init__(self, *args, **kwargs):
        super(NYTimesParser, self).__init__(*args, **kwargs)
        self.content_tags = [
            {"id": "article"},
            {"id": "content"},
            {"class": "entry-content"}
        ]

    def get_response(self):
        # We use the requests library to return the full URL.
        r = requests.get(self.url)
        return requests.get(r.url, params={"pagewanted":"all"})
