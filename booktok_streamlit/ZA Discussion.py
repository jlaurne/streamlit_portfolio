# In ZA_Discussion.py

import streamlit as st
import streamlit_authenticator as stauth
import plotly.graph_objects as go
# We no longer need the 'copy' import
from shared_functions import get_db_connection, get_user_progress, SERIES_DATA, load_css

# --- PAGE CONFIGURATION & STYLING ---
st.set_page_config(page_title="Ketchup n Snick's Book Club", page_icon="⭐", layout="wide")
load_css()

# --- AUTHENTICATION ---
try:
    # Use the .to_dict() method to create a writable copy of the credentials
    credentials = st.secrets['credentials'].to_dict()
except KeyError:
    st.error("Credentials not found in secrets.toml. Please add them.")
    st.stop()

authenticator = stauth.Authenticate(
    credentials,
    'KetchupSnickCookie',
    'KetchupSnickSignatureKey',
    cookie_expiry_days=30
)

# This renders the login form and handles the logic
authenticator.login()

# --- MAIN APP LOGIC ---
# The user's information is now stored in st.session_state
if st.session_state["authentication_status"]:
    # Get the user's name from the session state
    name = st.session_state["name"]
    
    # Establish DB Connection
    db = get_db_connection()
    if not db:
        st.error("Database connection failed. Please check secrets configuration.")
        st.stop()

    # --- SIDEBAR SETUP ---
    st.sidebar.title(f"⭐ Welcome, {name}!")
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.markdown("---")

    # Series selection is the first and most important step
    series_options = list(SERIES_DATA.keys())
    try:
        default_index = series_options.index(st.session_state.get('selected_series_title'))
    except (KeyError, ValueError):
        default_index = 0
    selected_series_title = st.sidebar.selectbox("Select a Series", options=series_options, index=default_index)
    st.session_state['selected_series_title'] = selected_series_title

    # Dynamically get the book data for the chosen series
    current_series_data = SERIES_DATA[selected_series_title]
    books = current_series_data["books"]
    book_map = {b['num']: b for b in books}
    st.session_state['book_map'] = book_map
    st.session_state['books'] = books

    # Get user info from the authenticator
    current_user = name
    other_user = "Ketchup" if current_user == "Snick" else "Snick"
    st.session_state['current_user'] = current_user
    st.session_state['other_user'] = other_user

    # Load progress FOR THE SELECTED SERIES
    user_progress = get_user_progress(db, current_user, selected_series_title)
    friend_progress = get_user_progress(db, other_user, selected_series_title)
    st.session_state['user_progress'] = user_progress

    # --- Sidebar Progress Display (Calculated by Chapter) ---
    st.sidebar.markdown(f"### 📚 Progress for {selected_series_title}")

    user_book_data = book_map.get(user_progress.get('current_book_num', 1), {})
    user_book_title = user_book_data.get('title', 'N/A')
    user_current_chapter = user_progress.get('current_chapter', 0)
    if user_progress.get('current_book_num', 0) > user_book_data.get('num', 0):
        user_percent = 100
    else:
        user_total_chapters = user_book_data.get('chapters', 1)
        user_percent = int((user_current_chapter / user_total_chapters) * 100) if user_total_chapters > 0 else 0
    st.sidebar.progress(user_percent, text=f"You: Ch. {user_current_chapter} of {user_book_title}")

    friend_book_data = book_map.get(friend_progress.get('current_book_num', 1), {})
    friend_book_title = friend_book_data.get('title', 'N/A')
    friend_current_chapter = friend_progress.get('current_chapter', 0)
    if friend_progress.get('current_book_num', 0) > friend_book_data.get('num', 0):
        friend_percent = 100
    else:
        friend_total_chapters = friend_book_data.get('chapters', 1)
        friend_percent = int((friend_current_chapter / friend_total_chapters) * 100) if friend_total_chapters > 0 else 0
    st.sidebar.progress(friend_percent, text=f"{other_user}: Ch. {friend_current_chapter} of {friend_book_title}")


    # --- MAIN DASHBOARD CONTENT ---
    st.markdown(f'<div class="main-header">{selected_series_title}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="book-card">', unsafe_allow_html=True)
        st.markdown("### 📚 Series Progress")

        def get_status_val(progress, book):
            book_num = book.get('num', 0)
            current_book_num = progress.get('current_book_num', 0)
            if current_book_num > book_num:
                return 1.0
            elif current_book_num == book_num:
                total_chapters = book.get('chapters', 1)
                current_chapter = progress.get('current_chapter', 0)
                return (current_chapter / total_chapters) if total_chapters > 0 else 0.0
            else:
                return 0.0

        fig = go.Figure()
        fig.add_trace(go.Bar(name='You', x=[b['title'] for b in books], y=[get_status_val(user_progress, b) for b in books], marker_color='#FF6B9D'))
        fig.add_trace(go.Bar(name=other_user, x=[b['title'] for b in books], y=[get_status_val(friend_progress, b) for b in books], marker_color='#4A0E4E'))
        fig.update_layout(title="Reading Progress Comparison", yaxis_title="Completion Status", barmode='group', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white', legend_title_text='Reader')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="book-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Current Status")
        safe_book_num = min(user_progress.get('current_book_num', 1), friend_progress.get('current_book_num', 1))
        safe_book_title = book_map.get(safe_book_num, {}).get('title', 'N/A')
        st.markdown(f"**Safe to discuss:** Everything through **{safe_book_title}**!")
        st.metric("Your Current Book", f"{user_book_title}")
        st.metric(f"{other_user}'s Current Book", f"{friend_book_title}")
        st.markdown('</div>', unsafe_allow_html=True)

# --- Logic for non-logged-in users ---
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')