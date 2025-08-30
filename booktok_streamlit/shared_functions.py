# shared_functions.py

import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import datetime
from datetime import date

# --- DATABASE CONNECTION ---
def get_db_connection():
    """Establishes a connection to the Firestore database using Streamlit secrets."""
    try:
        creds_dict = st.secrets["firestore"]
        creds = service_account.Credentials.from_service_account_info(creds_dict)
        return firestore.Client(credentials=creds, project=creds_dict['project_id'])
    except Exception as e:
        st.error(f"Failed to connect to Firestore: {e}")
        st.info("Ensure your secrets are configured correctly in the app settings.")
        return None

# --- PROGRESS & DISCUSSION FUNCTIONS ---
def get_user_progress(db, user_id, series_title):
    """Fetches a user's reading progress for a specific series from Firestore."""
    doc_ref = db.collection('users').document(user_id)
    doc = doc_ref.get()
    if doc.exists and doc.to_dict().get('progress', {}).get(series_title):
        return doc.to_dict()['progress'][series_title]
    else: # Default progress for a new user or series
        return {'current_book_num': 1, 'current_chapter': 0, 'last_update': str(date.today())}

def update_user_progress(db, user_id, series_title, book_num, chapter):
    """Updates a user's progress in Firestore, tracking by chapter."""
    doc_ref = db.collection('users').document(user_id)
    doc_ref.set({
        'progress': {
            series_title: {
                'current_book_num': book_num,
                'current_chapter': chapter,
                'last_update': str(date.today())
            }
        }
    }, merge=True)

def add_discussion(db, series_title, book_num, chapter, author, content, tags):
    """Adds a new discussion comment with tags to Firestore."""
    doc_ref = db.collection('discussions').document()
    doc_ref.set({
        'series': series_title,
        'book_num': book_num,
        'chapter': chapter,
        'author': author,
        'content': content,
        'tags': tags,  # NEW: Add the list of tags
        'timestamp': datetime.datetime.now()
    })
    return True

def get_discussions(db, series_title, book_num, max_chapter):
    """Fetches discussions for a book, respecting the user's progress to avoid spoilers."""
    try:
        comments_ref = db.collection('discussions').where('series', '==', series_title).where('book_num', '==', book_num).where('chapter', '<=', max_chapter).order_by('chapter').order_by('timestamp')
        docs = comments_ref.stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        st.error(f"A database error occurred: {e}")
        st.info("This might be due to a missing index in Firestore. Check the error details.")
        return []

# --- NEW FEATURE FUNCTIONS ---

# Character Ranking Functions
def save_character_ranking(db, series, char, user, rankings):
    doc_ref = db.collection('character_rankings').document(f"{series}-{char}-{user}")
    doc_ref.set({
        'series': series,
        'character': char,
        'user': user,
        'rankings': rankings,
        'last_update': datetime.datetime.now()
    })

def get_character_rankings(db, series, char):
    docs = db.collection('character_rankings').where('series', '==', series).where('character', '==', char).stream()
    return [doc.to_dict() for doc in docs]

# Emotional Damage Functions
def save_damage_report(db, series, book_num, chapter, user, report):
    doc_ref = db.collection('damage_reports').document()
    doc_ref.set({
        'series': series,
        'book_num': book_num,
        'chapter': chapter,
        'user': user,
        'report': report,
        'timestamp': datetime.datetime.now()
    })

def get_damage_reports(db, series, book_num):
    docs = db.collection('damage_reports').where('series', '==', series).where('book_num', '==', book_num).order_by('chapter').stream()
    return [doc.to_dict() for doc in docs]

# Fan Cast Functions
def save_fan_cast(db, series, char, user, image_url):
    doc_ref = db.collection('fan_casts').document(f"{series}-{char}")
    doc_ref.set({
        'series': series,
        'character': char,
        'picks': {
            user: image_url
        }
    }, merge=True)

def get_fan_cast(db, series, char):
    doc_ref = db.collection('fan_casts').document(f"{series}-{char}")
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get('picks', {})
    return {}


# --- DATA & STYLING ---

SERIES_DATA = {
    "Zodiac Academy Universe": {
        "characters": ["Tory", "Darcy", "Darius", "Caleb", "Seth", "Orion", "Gabriel", "Max", "Geraldine", "Lionel", "Clara"],
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
            {"num": 9, "title": "Restless Stars", "chapters": 35},
        ]
    },
     "Sins of the Zodiac": {
        "characters": ["???", "???", "???", "???"],
        "books": [
            {"num": 1, "title": "Never Keep", "chapters": 50},
            {"num": 2, "title": "Echo Fort", "chapters": 50},
            {"num": 3, "title": "Cinder Vale", "chapters": 60},
        ]
    },
    "Magnolia Parks (Books 1-5)": {
        "characters": ["Magnolia Parks", "BJ Ballentine", "Daisy Haites", "Christian Hemmes"],
        "books": [
            {"num": 1, "title": "Magnolia Parks", "chapters": 50},
            {"num": 2, "title": "Daisy Haites", "chapters": 50},
            {"num": 3, "title": "Magnolia Parks: The Long Way Home", "chapters": 60},
            {"num": 4, "title": "Daisy Haites: The Great Undoing", "chapters": 60},
            {"num": 5, "title": "Magnolia Parks: Into the Dark", "chapters": 70},
        ]
    },
    "Never": {
        "characters": ["Daphne Darling", "Peter Pan", "Jamison Hook", "Wendy and Mary Darling"],
        "books": [
            # Using a distinct book number to avoid clashes
            {"num": 1, "title": "Never", "chapters": 26},
        ]
    },
    "The Conditions of Will": {
        "characters": ["Georgia Carter", "Maryanne Carter", "Oliver Carter", "Hattie Ramsey", "Sam Penny", "Tennyson (Tenny) Carter"],
        "books": [
            # Using a distinct book number to avoid clashes
            {"num": 1, "title": "The Conditions of Will", "chapters": 60},
        ]
    },
     "time of your life": {
        "characters": ["???", "???", "???"],
        "books": [
            # Using a distinct book number to avoid clashes
            {"num": 1, "title": "time of your life", "chapters": 60},
        ]
    },
    "The Hunger Games": {
        "characters": ["Katniss Everdeen", "Peeta Mellark", "Gale Hawthorne", "Haymitch Abernathy"],
        "books": [
            {"num": 1, "title": "The Hunger Games", "chapters": 27},
            {"num": 2, "title": "Catching Fire", "chapters": 27},
            {"num": 3, "title": "Mockingjay", "chapters": 27},
            {"num": 4, "title": "The Ballad of Songbirds & Snakes", "chapters": 30},
        ]
    }
}

def load_css():
    """Loads custom CSS for styling the app."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
        html, body, [class*="css"] { font-family: 'Montserrat', sans-serif !important; }
        .main-header { font-size: 3rem; font-weight: 700; background: linear-gradient(45deg, #4A0E4E, #81007F, #FF6B9D); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 1rem; }
        .book-card { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; padding: 1.5rem; border-radius: 15px; border: 2px solid #FF6B9D; margin: 1rem 0; box-shadow: 0 8px 25px rgba(255, 107, 157, 0.3); }
        .safe-zone { background: linear-gradient(135deg, #0f4c75 0%, #3282b8 100%); color: white; padding: 1rem; border-radius: 10px; border-left: 5px solid #00ff88; }
        .spoiler-zone { background: linear-gradient(135deg, #8b0000 0%, #dc143c 100%); color: white; padding: 1rem; border-radius: 10px; border-left: 5px solid #ff4444; }
        .tag {
    display: inline-block;
    padding: 0.2em 0.6em;
    margin: 0.2em;
    font-size: 0.8em;
    font-weight: bold;
    border-radius: 10px;
    background-color: #4A0E4E;
    color: white;
}
    </style>
    """, unsafe_allow_html=True)