import streamlit as st
from shared_functions import get_db_connection, get_discussions, add_discussion

st.set_page_config(page_title="Book Discussions", page_icon="💬", layout="wide")

db = get_db_connection()
if not db: st.stop()

# Pre-defined list of tags you can choose from
TAG_OPTIONS = [
    "LOVE ❤️", "EVIL 😈", "NEED MORE!", "Team Heirs", "Team Vegas",
    "Plot Twist 🤯", "Oh Brother THIS GUY SUCKS", "My Tears Ricochet 😭",
    "Character Growth 🌱", "Red Flag 🚩", "Green Flag ✅"
]

# Retrieve shared info from session state
try:
    selected_series_title = st.session_state['selected_series_title']
    current_user = st.session_state['current_user']
    user_progress = st.session_state['user_progress']
    book_map = st.session_state['book_map']
    books = st.session_state['books']
except KeyError:
    st.warning("Data not found. Please start from the 📖 Dashboard page.")
    st.stop()
    
# --- PAGE LOGIC ---
st.markdown(f'<div class="main-header">{selected_series_title} Discussions</div>', unsafe_allow_html=True)

selected_book_num = st.selectbox(
    "Select a book to discuss:",
    options=[b['num'] for b in books],
    format_func=lambda x: f"Book {x}: {book_map.get(x, {}).get('title', 'N/A')}"
)
selected_book = book_map.get(selected_book_num, {})

if not selected_book:
    st.warning("Please select a book."); st.stop()

if selected_book_num > user_progress.get('current_book_num', 0):
    st.warning(f"🔒 You haven't started Book {selected_book_num} yet!")
else:
    user_chapters_read = selected_book.get('chapters', 999)
    if user_progress.get('current_book_num') == selected_book_num:
        user_chapters_read = user_progress.get('current_chapter', 0)

    # --- Add a New Comment Form ---
    st.markdown("---")
    st.markdown("#### Add Your Thoughts")
    with st.form("new_comment_form", clear_on_submit=True):
        comment_text = st.text_area("Your thought:")
        chapter_num = st.number_input("Chapter Number (for spoiler tag)", min_value=1, max_value=selected_book.get('chapters', 999), value=max(1, user_chapters_read))
        
        # NEW: Multi-select widget for tags
        selected_tags = st.multiselect("Add some tags:", options=TAG_OPTIONS)

        submitted = st.form_submit_button("Add Comment")
        if submitted and comment_text:
            if chapter_num > user_chapters_read:
                st.error("You can't comment on a chapter you haven't read yet!")
            else:
                # Pass the selected_tags list to the function
                add_discussion(db, selected_series_title, selected_book_num, chapter_num, current_user, comment_text, selected_tags)
                st.success("Your comment was added!")
                st.rerun()

    # --- Discussion Feed ---
    st.markdown("---")
    st.markdown("#### Discussion Feed")
    comments = get_discussions(db, selected_series_title, selected_book_num, user_chapters_read)
    if comments:
        for comment in reversed(comments): # Show newest comments first
            # Create the HTML for the tags
            tags_html = "".join([f"<span class='tag'>{tag}</span>" for tag in comment.get('tags', [])])
            
            st.markdown(f"""
            <div class="book-card" style="margin: 0.5rem 0; border-color: #81007F;">
                <b>{comment['author']}</b> (Ch. {comment.get('chapter', '?')})
                <p style="font-style: italic; margin-top: 5px;">{comment['content']}</p>
                {tags_html}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No comments yet for the chapters you've read. Be the first!")