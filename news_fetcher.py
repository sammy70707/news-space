
import requests
import threading
import time
from datetime import datetime, timedelta
import models

API_URL = 'https://api.spaceflightnewsapi.net/v4/articles/'
FETCH_INTERVAL = 1800


def fetch_news_from_api():
    try:
        two_weeks_ago = (datetime.utcnow() - timedelta(days=14)).strftime('%Y-%m-%dT%H:%M:%SZ')
        params = {
            'published_at_gte': two_weeks_ago,
            'limit': 50,
            'ordering': '-published_at',
        }
        response = requests.get(API_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
    except Exception as e:
        print(f"[NewsFetcher] Error fetching news: {e}")
        return []


def store_articles(articles):
    count = 0
    for article in articles:
        title = article.get('title', '').strip()
        if not title:
            continue

        summary = article.get('summary', '')
        image_url = article.get('image_url', '')
        source_url = article.get('url', '')
        news_site = article.get('news_site', 'Unknown')
        published_at = article.get('published_at', '')
        if published_at:
            try:
                dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                published_at = dt.strftime('%Y-%m-%d %H:%M:%S')
            except (ValueError, AttributeError):
                pass

        category = news_site

        if models.insert_news_article(title, summary, category, image_url, source_url, published_at):
            count += 1

    if count > 0:
        print(f"[NewsFetcher] Stored {count} new articles.")
    return count


def refresh_news():
    articles = fetch_news_from_api()
    if articles:
        store_articles(articles)
        models.delete_old_news(days=14)


def start_background_fetcher():
    def _loop():
        while True:
            try:
                refresh_news()
            except Exception as e:
                print(f"[NewsFetcher] Background error: {e}")
            time.sleep(FETCH_INTERVAL)

    thread = threading.Thread(target=_loop, daemon=True)
    thread.start()
    print("[NewsFetcher] Background fetcher started (every 30 min).")
