# pages/2_💬_Book_Discussions.py


import streamlit as st
from shared_functions import get_db_connection, get_discussions, add_discussion, BOOKS, BOOK_MAP

st.set_page_config(page_title="Book Discussions", page_icon="💬", layout="wide")
st.title("Book Discussions")

# Connect to the database
db = get_db_connection()
if not db:
    st.stop()

# Retrieve shared info from session state
selected_series_title = st.session_state.get('selected_series_title', 'Zodiac Academy Universe')
current_user = st.session_state.get('current_user', 'Snick')
user_progress = st.session_state.get('user_progress', {'current_book_num': 1, 'progress_percent': 0})
book_map = st.session_state.get('book_map', {})
books = st.session_state.get('books', [])

# --- PAGE LOGIC ---
st.markdown(f'<div class="main-header">{selected_series_title} Discussions</div>', unsafe_allow_html=True)

# Allow user to select which book to discuss from the CURRENT series
selected_book_num = st.selectbox(
    "Select a book to discuss:",
    options=[b['num'] for b in books],
    format_func=lambda x: f"Book {x}: {book_map.get(x, {}).get('title', 'N/A')}"
)
selected_book = book_map.get(selected_book_num, {})

if not selected_book:
    st.warning("Please select a book.")
    st.stop()

# Spoiler Protection: Check if the user is allowed to see this discussion
if selected_book_num > user_progress['current_book_num']:
    st.warning(f"🔒 You haven't started Book {selected_book_num} yet!")
else:
    # Calculate which chapter the user is on
    user_chapters_read = selected_book.get('chapters', 999) # Assume complete
    if user_progress['current_book_num'] == selected_book_num:
        user_chapters_read = int((user_progress['progress_percent'] / 100) * selected_book.get('chapters', 1))


    
    # Display Existing Comments (Spoiler-Proof)
    st.markdown("#### Discussion Feed")
    comments = get_discussions(db, selected_book_num, user_chapters_read)
    if comments:
        for comment in comments:
            st.markdown(f"""
            <div class="book-card" style="margin: 0.5rem 0; border-color: #81007F;">
                <b>{comment['author']}</b> (Ch. {comment['chapter']})<br>
                <i>{comment['content']}</i>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No comments yet for the chapters you've read. Be the first!")
    
    st.markdown("---")

    # Add a New Comment
    st.markdown("#### Add Your Thoughts")
    with st.form("new_comment_form", clear_on_submit=True):
        chapter_num = st.number_input("Chapter Number (for spoiler tag)", min_value=1, max_value=selected_book['chapters'], value=max(1, user_chapters_read))
        comment_text = st.text_area("Your comment:")
        
        submitted = st.form_submit_button("Add Comment")
        if submitted and comment_text:
            if chapter_num > user_chapters_read:
                st.error("You can't comment on a chapter you haven't read yet!")
            else:
                add_discussion(db, selected_book_num, chapter_num, current_user, comment_text)
                st.success("Your comment was added!")
                st.rerun()