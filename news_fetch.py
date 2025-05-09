import feedparser
import requests
from newspaper import Article
from config import RSS_FEEDS, NEWSAPI_KEY

def fetch_rss_news():
    headlines = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                headlines.append(entry.title)
        except Exception as e:
            print(f"[ERROR] RSS feed error: {e}")
    return headlines

def fetch_newsapi_headlines(query="stock"):
    try:
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWSAPI_KEY}"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        articles = res.json().get("articles", [])
        return [a["title"] for a in articles if "title" in a]
    except Exception as e:
        print(f"[ERROR] NewsAPI fetch failed: {e}")
        return []

def fetch_article_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"[ERROR] Failed to fetch article: {e}")
        return ""
