from pafy.pafy import Pafy
from nekbot import settings

__author__ = 'nekmo'

import pafy

if hasattr(settings, 'GOOGLE_API_KEY'):
    setattr(Pafy, 'api_key', settings.GOOGLE_API_KEY)


class YoutubeMetadata(object):
    source_url = 'youtube.com'

    def __init__(self, url):
        self.data = pafy.new(url)

    @property
    def title(self):
        return self.data.title

    @property
    def authors(self):
        return [self.data.author]

    @property
    def extra(self):
        return '[%s]' % self.data.duration

def youtube(url):
    return YoutubeMetadata(url)