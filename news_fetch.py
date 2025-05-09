import feedparser
import requests
from newspaper import Article
from config import RSS_FEEDS, NEWSAPI_KEY

def fetch_rss_news():
    headlines = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            headlines.append(entry.title)
    return headlines

def fetch_newsapi_headlines(query="stock"):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWSAPI_KEY}"
    res = requests.get(url)
    articles = res.json().get("articles", [])
    return [a["title"] for a in articles]

def fetch_article_text(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text