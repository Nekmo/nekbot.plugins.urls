from newspaper import Article
import requests

__author__ = 'nekmo'

MAX_DATA = 1024 * 32

def generic(url):
    article = Article(url)
    r = requests.get(url, stream=True)
    # article.download()
    article.set_html(r.raw.read(MAX_DATA, decode_content=True))
    article.parse()
    return article