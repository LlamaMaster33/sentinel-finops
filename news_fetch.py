from newsapi import NewsApiClient
import feedparser
from config import NEWSAPI_KEY, NEWS_SOURCES, RSS_FEEDS

# 1) NewsAPI v2
newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

def fetch_news_api(query: str, page_size=20):
    resp = newsapi.get_everything(
        q=query, sources=",".join(NEWS_SOURCES),
        page_size=page_size
    )
    return [article["title"] + ": " + article["description"]
            for article in resp.get("articles", [])]

# 2) RSS fallback
def fetch_rss():
    entries = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for e in feed.entries[:20]:
            entries.append(e.title + ": " + getattr(e, "summary", ""))
    return entries
