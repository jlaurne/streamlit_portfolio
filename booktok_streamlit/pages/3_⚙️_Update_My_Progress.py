import streamlit as st
from shared_functions import get_db_connection, update_user_progress, get_user_progress

st.set_page_config(page_title="Update Progress", page_icon="⚙️", layout="wide")

# --- Initial Setup ---
db = get_db_connection()
if not db:
    st.error("Database connection failed.")
    st.stop()

# Retrieve shared info from session state set on the main page
try:
    selected_series_title = st.session_state['selected_series_title']
    current_user = st.session_state['current_user']
    user_progress = st.session_state['user_progress']
    book_map = st.session_state['book_map']
    books = st.session_state['books']
except KeyError:
    st.warning("Please select a series from the 📖 Dashboard page first.")
    st.stop()


# --- Page UI and Logic ---
st.markdown(f'<div class="main-header">Update Reading Progress</div>', unsafe_allow_html=True)
st.markdown(f"### Updating progress for: **{current_user}** in **{selected_series_title}**")

# In pages/3_⚙️_Update_My_Progress.py, replace the 'with st.form(...)' block

with st.form("progress_update_form"):
    # Get a list of the book numbers for the selectbox options
    book_numbers = [b['num'] for b in books]
    
    # Find the index of the user's current book to set as the default
    try:
        current_book_index = book_numbers.index(user_progress.get('current_book_num', 1))
    except ValueError:
        current_book_index = 0

    # Book selection dropdown
    new_book_num = st.selectbox(
        "Which book are you reading now?",
        options=book_numbers,
        index=current_book_index,
        format_func=lambda x: f"Book {x}: {book_map.get(x, {}).get('title', 'N/A')}"
    )

    total_chapters = book_map.get(new_book_num, {}).get('chapters', 1)

    # Chapter number input
    new_chapter = st.number_input(
        f"What chapter are you on? (out of {total_chapters})",
        min_value=0,
        max_value=total_chapters,
        value=user_progress.get('current_chapter', 0)
    )

    # NEW: Checkbox to mark the book as completed
    is_completed = st.checkbox(f"I've finished this book! (Mark as complete)")

    # Submit button
    update_button = st.form_submit_button("Update My Progress")

    if update_button:
        # If the checkbox is ticked, override the chapter number with the total
        final_chapter = total_chapters if is_completed else new_chapter

        # Call the function to save the new chapter progress to the database
        update_user_progress(db, current_user, selected_series_title, new_book_num, final_chapter)
        st.success("Your progress has been saved!")

        # Immediately fetch the latest progress and update the session state
        st.session_state['user_progress'] = get_user_progress(db, current_user, selected_series_title)

        # Rerun the app to make the change appear instantly in the sidebar
        st.rerun()