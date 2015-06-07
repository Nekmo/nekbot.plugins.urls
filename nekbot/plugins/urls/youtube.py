import re
import requests
from nekbot import settings

__author__ = 'nekmo'

API_URL = 'https://www.googleapis.com/youtube/v3/videos'


def humanize_duration(duration):
    duration = duration[2:]
    parts = re.split('[HMS]', duration)[:-1]
    if len(parts) < 2:
        parts = ['0'] + parts
    parts = ['%02i' % part for part in map(int, parts)]
    duration = ':'.join(parts)
    return duration


def extract_video_id(url):
    """ Extract the video id from a url, return video id as str. From Pafy project."""
    ok = (r"\w-",) * 3
    regx = re.compile(r'(?:^|[^%s]+)([%s]{11})(?:[^%s]+|$)' % ok)
    url = str(url)
    m = regx.search(url)

    if not m:
        err = "Need 11 character video id or the URL of the video. Got %s"
        raise ValueError(err % url)

    vidid = m.group(1)
    return vidid


class YoutubeMetadata(object):
    source_url = 'youtube'

    def __init__(self, url):
        url_id = extract_video_id(url)
        self.data = requests.get(API_URL, params={'key': settings.GOOGLE_API_KEY,
                                                  'id': url_id,
                                                  'part': 'contentDetails,snippet'}).json()
        print(self.data)
        if not self.data.get('items') or not len(self.data['items']):
            raise Exception(self.data)
        else:
            self.data = self.data['items'][0]

    @property
    def title(self):
        return self.data['snippet']['title']

    @property
    def authors(self):
        return [self.data['snippet']['channelTitle']]

    @property
    def extra(self):
        return '[{duration}][{definition}]'.format(definition=self.data['contentDetails']['definition'].upper(),
                                                   duration=humanize_duration(self.data['contentDetails']['duration']))

def youtube(url):
    return YoutubeMetadata(url)