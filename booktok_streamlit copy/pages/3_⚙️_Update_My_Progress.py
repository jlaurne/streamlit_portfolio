# pages/3_⚙️_Update_My_Progress.py

import streamlit as st
from shared_functions import get_db_connection, update_user_progress

st.set_page_config(page_title="Update Progress", page_icon="⚙️", layout="wide")

# Connect to the database
db = get_db_connection()
if not db:
    st.error("Database connection failed.")
    st.stop()

# Retrieve shared info from session state set on the main page
# Use .get() with defaults to make the page robust
try:
    selected_series_title = st.session_state['selected_series_title']
    current_user = st.session_state['current_user']
    user_progress = st.session_state['user_progress']
    book_map = st.session_state['book_map']
    books = st.session_state['books']
except KeyError:
    st.warning("Please select a series and user from the 📖 Dashboard first.")
    st.stop()


# --- PAGE UI AND LOGIC ---
st.markdown(f'<div class="main-header">Update Progress for {selected_series_title}</div>', unsafe_allow_html=True)
st.markdown(f"### Updating progress for: **{current_user}**")

with st.form("progress_update_form"):
    # Get a list of the book numbers for the selectbox options
    book_numbers = [b['num'] for b in books]
    
    # Find the index of the user's current book to set as the default
    try:
        current_book_index = book_numbers.index(user_progress['current_book_num'])
    except ValueError:
        current_book_index = 0 # Default to the first book if not found

    # Book selection dropdown
    new_book_num = st.selectbox(
        "Which book are you reading now?",
        options=book_numbers,
        index=current_book_index,
        format_func=lambda x: f"Book {x}: {book_map.get(x, {}).get('title', 'N/A')}"
    )

    # Progress percentage slider
    new_percentage = st.slider(
        "How far into the book are you (%)?",
        0, 100,
        user_progress['progress_percent']
    )

    # Submit button
    update_button = st.form_submit_button("Update My Progress")

    if update_button:
        # Call the updated function with the series title
        update_user_progress(db, current_user, selected_series_title, new_book_num, new_percentage)
        st.success("Your progress has been saved!")
        # Rerun to update the progress bars in the sidebar immediately
        st.rerun()