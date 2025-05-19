import json
import feedparser # type: ignore
from flask_caching import Cache # type: ignore
from html import unescape
from dateutil import parser as dateparser

cache = Cache()

def init_cache(app):
    cache.init_app(app, config={
        'CACHE_TYPE': app.config['CACHE_TYPE'],
        'CACHE_DEFAULT_TIMEOUT': app.config['CACHE_DEFAULT_TIMEOUT']
    })

@cache.cached(key_prefix='all_feeds')
def get_all_feeds():
    with open('feed.json') as f:
        feeds = json.load(f)

    articles = []
    for feed in feeds:
        parsed = feedparser.parse(feed['url'])
        for entry in parsed.entries:
          pub = entry.get('published') or entry.get('updated', '')
          try:
              dt = dateparser.parse(pub)
          except Exception:
              dt = None
          raw = entry.get('summary') or entry.get('description', '')
          text = unescape(raw).replace('<p>', '').replace('</p>', '') 
          snippet = text[:150] + ('…' if len(text) > 150 else '')
          img = None
          if 'media_thumbnail' in entry:
              img = entry.media_thumbnail[0]['url']
          elif 'media_content' in entry:
              img = entry.media_content[0]['url']
          elif entry.get('enclosures'):
              for e in entry.enclosures:
                  if e.get('type', '').startswith('image'):
                      img = e.get('href')
                      break

          articles.append({
        'source':    feed['name'],
        'title':     entry.get('title', 'No title'),
        'link':      entry.get('link', '#'),
        'published': entry.get('published', 'No date'),
        'image':     img,
        'snippet': snippet,
        'published_dt': dt,
    })

    articles.sort(key=lambda x: x['published'], reverse=True)
    return articles
