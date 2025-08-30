# fetch_articles.py
import feedparser
import firebase_admin
from firebase_admin import credentials, firestore
import hashlib # To create a unique ID for each article

# --- Firebase Initialization ---
# This part changes depending on whether it's run locally or in GitHub Actions
import os
import json

try:
    # Running locally
    cred = credentials.Certificate("firebase_credentials.json")
except FileNotFoundError:
    # Running in GitHub Actions
    creds_json = os.environ.get("FIREBASE_CREDENTIALS")
    creds_dict = json.loads(creds_json)
    cred = credentials.Certificate(creds_dict)

firebase_admin.initialize_app(cred)
db = firestore.client()
articles_ref = db.collection('articles')

def fetch_and_store_articles(sources):
    for source_name, url in sources.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            # Create a unique ID for the article based on its link to prevent duplicates
            article_id = hashlib.sha256(entry.link.encode('utf-8')).hexdigest()
            doc_ref = articles_ref.document(article_id)

            if not doc_ref.get().exists:
                print(f"New article found: {entry.title}")
                # You'll need a library like 'requests' and 'BeautifulSoup4'
                # to fetch the full article text from entry.link
                # For now, we'll use the summary from the RSS feed
                article_data = {
                    'id': article_id,
                    'source': source_name,
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.get('published_parsed'),
                    'summary_raw': entry.summary,
                    'fetched_at': firestore.SERVER_TIMESTAMP,
                    'summarized': False, # A flag to track processing status
                }
                doc_ref.set(article_data)
            else:
                print(f"Skipping existing article: {entry.title}")

if __name__ == "__main__":
    from sources import RSS_SOURCES
    fetch_and_store_articles(RSS_SOURCES)