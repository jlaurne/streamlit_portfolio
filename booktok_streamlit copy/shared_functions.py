# shared_functions.py

import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import datetime
from datetime import date

# --- DATABASE CONNECTION (no changes here) ---
def get_db_connection():
    try:
        creds_dict = st.secrets["firestore"]
        creds = service_account.Credentials.from_service_account_info(creds_dict)
        return firestore.Client(credentials=creds, project=creds_dict['project_id'])
    except Exception as e:
        st.error(f"Failed to connect to Firestore: {e}")
        return None

# --- DATABASE SCHEMA EXPLANATION ---
# User progress is now stored in a 'progress' map within a user's document.
# discussions collection documents now include a 'series' field.

# --- UPDATED DATABASE FUNCTIONS ---
def get_user_progress(db, user_id, series_title):
    doc_ref = db.collection('users').document(user_id)
    doc = doc_ref.get()
    if doc.exists and doc.to_dict().get('progress', {}).get(series_title):
        return doc.to_dict()['progress'][series_title]
    else:
        return {'current_book_num': 1, 'progress_percent': 0, 'last_update': str(date.today())}

def update_user_progress(db, user_id, series_title, book_num, percentage):
    doc_ref = db.collection('users').document(user_id)
    # Use dotted notation to update a specific field in a map
    doc_ref.set({
        'progress': {
            series_title: {
                'current_book_num': book_num,
                'progress_percent': percentage,
                'last_update': str(date.today())
            }
        }
    }, merge=True)

def add_discussion(db, series_title, book_num, chapter, author, content):
    doc_ref = db.collection('discussions').document() # Let Firestore create a unique ID
    doc_ref.set({
        'series': series_title, # NEW: track the series
        'book_num': book_num,
        'chapter': chapter,
        'author': author,
        'content': content,
        'timestamp': datetime.datetime.now()
    })
    return True

def get_discussions(db, series_title, book_num, max_chapter):
    try:
        comments_ref = db.collection('discussions').where('series', '==', series_title).where('book_num', '==', book_num).where('chapter', '<=', max_chapter).order_by('chapter').order_by('timestamp')
        docs = comments_ref.stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        st.error(f"A database error occurred: {e}")
        return []

# --- NEW DATA STRUCTURE FOR ALL SERIES ---
SERIES_DATA = {
    "Zodiac Academy Universe": {
        "books": [
            {"num": 0.5, "title": "Origins of an Academy Bully", "chapters": 10},
            {"num": 1, "title": "The Awakening", "chapters": 25},
            {"num": 1.5, "title": "The Awakening As Told By The Boys", "chapters": 25},
            {"num": 2, "title": "Ruthless Fae", "chapters": 30},
            {"num": 3, "title": "The Reckoning", "chapters": 32},
            {"num": 4, "title": "Shadow Princess", "chapters": 35},
            {"num": 5, "title": "Cursed Fates", "chapters": 40},
            {"num": 5.5, "title": "The Big A.S.S. Party", "chapters": 15},
            {"num": 5.6, "title": "Seth on the Moon", "chapters": 5},
            {"num": 6, "title": "Fated Throne", "chapters": 42},
            {"num": 7, "title": "Heartless Sky", "chapters": 45},
            {"num": 8, "title": "Sorrow and Starlight", "chapters": 50},
            {"num": 8.5, "title": "Beyond The Veil", "chapters": 20},
            {"num": 8.6, "title": "Live And Let Lionel", "chapters": 10},
            {"num": 9, "title": "Sins of the Zodiac: Scorpio", "chapters": 35}, # Placeholder
            {"num": 10, "title": "Sins of the Zodiac: Pisces", "chapters": 35}, # Placeholder
        ]
    },
    "Savage Lands (Jessa Hastings)": {
        "books": [
            {"num": 1, "title": "Savage Lands", "chapters": 30},
            {"num": 2, "title": "Wild Lands", "chapters": 30},
            {"num": 3, "title": "Bad Lands", "chapters": 30},
        ]
    },
    "The Hunger Games": {
        "books": [
            {"num": 1, "title": "The Hunger Games", "chapters": 27},
            {"num": 2, "title": "Catching Fire", "chapters": 27},
            {"num": 3, "title": "Mockingjay", "chapters": 27},
            {"num": 4, "title": "The Ballad of Songbirds & Snakes", "chapters": 30},
        ]
    }
}

# --- STYLING (no changes here) ---
def load_css():
    # ... your full CSS block ...
    st.markdown("""<style>...</style>""", unsafe_allow_html=True)