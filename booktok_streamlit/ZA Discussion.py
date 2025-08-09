import streamlit as st
import pandas as pd
import datetime
from datetime import date
import plotly.express as px
import plotly.graph_objects as go

# Import Google Cloud libraries
from google.cloud import firestore
from google.oauth2 import service_account

# --- DATABASE CONNECTION ---
# This function uses Streamlit's secrets to securely connect to Firestore.
def get_db_connection():
    """Establishes a connection to the Firestore database."""
    try:
        # Get credentials from the secrets.toml file
        creds_dict = st.secrets["firestore"]
        creds = service_account.Credentials.from_service_account_info(creds_dict)
        db = firestore.Client(credentials=creds, project=creds_dict['project_id'])
        return db
    except Exception as e:
        st.error(f"Failed to connect to Firestore: {e}")
        st.info("Please ensure your `.streamlit/secrets.toml` file is configured correctly.")
        return None

# --- DATABASE HELPER FUNCTIONS ---
# These functions will replace your old session_state logic.

def get_user_progress(db, user_id):
    """Fetches a user's reading progress from Firestore."""
    doc_ref = db.collection('users').document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        # Default progress if user not found (e.g., first time running)
        return {'current_book_num': 1, 'progress_percent': 0, 'last_update': str(date.today())}

def update_user_progress(db, user_id, book_num, percentage):
    """Updates a user's progress in Firestore."""
    doc_ref = db.collection('users').document(user_id)
    doc_ref.set({
        'current_book_num': book_num,
        'progress_percent': percentage,
        'last_update': str(date.today())
    }, merge=True)

def add_discussion(db, book_num, chapter, author, content):
    """Adds a new discussion comment to Firestore."""
    # We use a unique ID for each comment by combining book, chapter, and timestamp
    doc_id = f"book{book_num}_ch{chapter}_{datetime.datetime.now().isoformat()}"
    doc_ref = db.collection('discussions').document(doc_id)
    doc_ref.set({
        'book_num': book_num,
        'chapter': chapter,
        'author': author,
        'content': content,
        'timestamp': datetime.datetime.now()
    })
    return True

def get_discussions(db, book_num, max_chapter):
    """Fetches discussions, now with error handling."""
    try:
        comments_ref = db.collection('discussions').where('book_num', '==', book_num)
        comments_ref = comments_ref.where('chapter', '<=', max_chapter).order_by('chapter').order_by('timestamp')
        docs = comments_ref.stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        # If an error occurs, display it on the app screen
        st.error(f"A database error occurred: {e}")
        return [] # Return an empty list so the app doesn't crash

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="Snick & Ketchup's Book Club",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Your amazing CSS (no changes needed here!)
st.markdown("""<style> ... </style>""", unsafe_allow_html=True) # Keeping your CSS collapsed for brevity

# --- APP LOGIC ---
db = get_db_connection()

if not db:
    st.stop() # Stop the app if DB connection fails

# Hardcoded book data (this is fine, as it doesn't change often)
books = [
    # Novellas & Prequels
    {"num": 0.5, "title": "Origins of an Academy Bully", "chapters": 10}, # TODO: Adjust chapter counts
    {"num": 5.5, "title": "The Big A.S.S. Party", "chapters": 15},
    {"num": 5.6, "title": "Seth on the Moon", "chapters": 5},
    
    # Main Series
    {"num": 1, "title": "The Awakening", "chapters": 25},
    {"num": 2, "title": "Ruthless Fae", "chapters": 30},
    {"num": 3, "title": "The Reckoning", "chapters": 32},
    {"num": 4, "title": "Shadow Princess", "chapters": 35},
    {"num": 5, "title": "Cursed Fates", "chapters": 40},
    {"num": 6, "title": "Fated Throne", "chapters": 42},
    {"num": 7, "title": "Heartless Sky", "chapters": 45},
    {"num": 8, "title": "Sorrow and Starlight", "chapters": 50},
    {"num": 9, "title": "Restless Stars", "chapters": 40}, # Assuming a number for the unnumbered book
    
    # Companion Books
    {"num": 1.5, "title": "The Awakening As Told By The Boys", "chapters": 25},
    {"num": 8.5, "title": "Beyond The Veil", "chapters": 20},
    {"num": 8.6, "title": "Live And Let Lionel", "chapters": 10},
]

# It's also helpful to sort the list by book number for display in dropdowns
books.sort(key=lambda x: x['num'])

# This map will still work perfectly to look up book details by number
book_map = {b['num']: b for b in books}

# --- USER AUTHENTICATION & SIDEBAR ---
st.sidebar.title("⭐ S&K Book Club")
st.sidebar.markdown("---")

# Simple user selection. This is our "login".
current_user = st.sidebar.selectbox("Who are you?", ["Snick", "Ketchup"], key="user_login")
other_user = "Ketchup" if current_user == "Snick" else "Snick"

# Load progress for both users from Firestore
snick_progress = get_user_progress(db, "Snick")
ketchup_progress = get_user_progress(db, "Ketchup")

# Get the logged-in user's progress details
user_progress = snick_progress if current_user == "Snick" else ketchup_progress
friend_progress = ketchup_progress if current_user == "Snick" else snick_progress

user_book_title = book_map.get(user_progress['current_book_num'], {}).get('title', 'N/A')
friend_book_title = book_map.get(friend_progress['current_book_num'], {}).get('title', 'N/A')

st.sidebar.markdown("### 📚 Reading Progress")
st.sidebar.markdown(f"**You ({current_user}):**")
st.sidebar.progress(user_progress['progress_percent'], text=f"Book {user_progress['current_book_num']}: {user_book_title}")

st.sidebar.markdown(f"**{other_user}:**")
st.sidebar.progress(friend_progress['progress_percent'], text=f"Book {friend_progress['current_book_num']}: {friend_book_title}")

st.sidebar.markdown("---")

# Navigation
page = st.sidebar.selectbox(
    "Navigate to:",
    ["📖 Dashboard", "💬 Book Discussions", "⚙️ Update My Progress"]
)

st.sidebar.info("🚨 Spoilers are hidden based on your current reading progress!")

# --- PAGE CONTENT ---

if page == "📖 Dashboard":
    st.markdown('<div class="main-header">Book Club Dashboard</div>', unsafe_allow_html=True)
    # ... Your dashboard UI, but now powered by live data ...
    st.markdown(f"### Welcome, {current_user}!")
    
    # You can rebuild your dashboard visuals here using the live progress variables.
    # For example, to show the safe discussion point:
    safe_to_discuss_book = min(user_progress['current_book_num'], friend_progress['current_book_num'])
    st.markdown(f"**Safe to discuss:** Everything through Book {safe_to_discuss_book}!")
    
elif page == "💬 Book Discussions":
    st.markdown('<div class="main-header">Book Discussions</div>', unsafe_allow_html=True)

    # Allow user to select which book to discuss
    selected_book_num = st.selectbox("Select a book to discuss:", [b['num'] for b in books])
    selected_book = book_map[selected_book_num]
    
    # Check if the user is allowed to see this discussion
    if selected_book_num > user_progress['current_book_num']:
        st.warning(f"🔒 You haven't started Book {selected_book_num} yet! Come back later to avoid spoilers.")
    else:
        st.markdown(f"### {selected_book['title']}")
        
        # Calculate which chapter the user is on
        user_chapters_read = int((user_progress['progress_percent'] / 100) * selected_book['chapters'])
        if user_progress['current_book_num'] > selected_book_num:
            user_chapters_read = selected_book['chapters'] # They finished the book

        # --- Display Existing Comments (Spoiler-Proof) ---
        st.markdown("#### Discussion Feed")
        comments = get_discussions(db, selected_book_num, user_chapters_read)
        if comments:
            for comment in comments:
                # Use columns for a nicer layout
                col1, col2 = st.columns([1, 5])
                with col1:
                    st.markdown(f"**{comment['author']}**")
                    st.caption(f"Ch. {comment['chapter']}")
                with col2:
                    st.info(comment['content'])
        else:
            st.info("No comments yet for the chapters you've read. Be the first!")
        
        st.markdown("---")

        # --- Add a New Comment ---
        st.markdown("#### Add Your Thoughts")
        with st.form("new_comment_form", clear_on_submit=True):
            # We ask for chapter number to tag the comment correctly
            chapter_num = st.number_input(
                "Chapter Number (for spoiler tag)", 
                min_value=1, 
                max_value=selected_book['chapters'], 
                value=max(1, user_chapters_read)
            )
            comment_text = st.text_area("Your comment:")
            
            submitted = st.form_submit_button("Add Comment")
            if submitted and comment_text:
                if chapter_num > user_chapters_read:
                    st.error("You can't comment on a chapter you haven't read yet!")
                else:
                    add_discussion(db, selected_book_num, chapter_num, current_user, comment_text)
                    st.success("Your comment was added!")
                    st.rerun()

elif page == "⚙️ Update My Progress":
    st.markdown('<div class="main-header">Update My Progress</div>', unsafe_allow_html=True)
    st.markdown(f"### Updating progress for: **{current_user}**")
    
    with st.form("progress_update_form"):
        new_book_num = st.selectbox(
            "Which book are you reading now?", 
            options=[b['num'] for b in books], 
            index=int(user_progress['current_book_num'] - 1)
        )
        
        new_percentage = st.slider("How far into the book are you (%)?", 0, 100, user_progress['progress_percent'])
        
        update_button = st.form_submit_button("Update My Progress")
        
        if update_button:
            update_user_progress(db, current_user, new_book_num, new_percentage)
            st.success("Your progress has been saved!")
            st.rerun()

# --- FOOTER ---
st.markdown("---")
st.markdown('<div style="text-align: center; color: #FF6B9D;">Built for book besties who need spoiler-free discussion space ⭐✨</div>', unsafe_allow_html=True)