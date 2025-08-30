#pages/6_🎭_Fan_Cast.py
import streamlit as st
from shared_functions import get_db_connection, save_fan_cast, get_fan_cast, SERIES_DATA

st.set_page_config(page_title="Fan Cast", page_icon="🎭", layout="wide")

db = get_db_connection()
if not db: st.stop()

# Retrieve shared info from session state
try:
    selected_series_title = st.session_state['selected_series_title']
    current_user = st.session_state['current_user']
    other_user = st.session_state['other_user']
    characters = SERIES_DATA[selected_series_title].get("characters", [])
except KeyError:
    st.warning("Please select a series from the 📖 Dashboard first.")
    st.stop()

st.markdown(f'<div class="main-header">Fan Cast Couch</div>', unsafe_allow_html=True)

if not characters:
    st.info("No characters have been added for this series yet.")
    st.stop()

selected_char = st.selectbox("Select a Character to Cast", options=characters)

# --- UI to Display Existing Casts ---
st.markdown("---")
st.markdown(f"#### Current Picks for {selected_char}")

current_picks = get_fan_cast(db, selected_series_title, selected_char)
your_pick_url = current_picks.get(current_user, "")
friend_pick_url = current_picks.get(other_user, "")

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**Your Pick ({current_user})**")
    if your_pick_url:
        st.image(your_pick_url, use_column_width=True)
    else:
        st.info("You haven't made a pick yet.")

with col2:
    st.markdown(f"**{other_user}'s Pick**")
    if friend_pick_url:
        st.image(friend_pick_url, use_column_width=True)
    else:
        st.info(f"{other_user} hasn't made a pick yet.")

# --- UI to Submit a New Cast ---
st.markdown("---")
with st.form(f"cast_form_{selected_char}", clear_on_submit=True):
    st.markdown("#### Cast Your Actor")
    image_url = st.text_input("Paste Image URL of your actor", value=your_pick_url)

    if st.form_submit_button("Save My Cast"):
        if image_url:
            save_fan_cast(db, selected_series_title, selected_char, current_user, image_url)
            st.success(f"Your pick for {selected_char} has been saved!")
            st.rerun()
        else:
            st.warning("Please paste an image URL.")