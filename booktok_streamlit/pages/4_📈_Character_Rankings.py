# pages/4_📈_Character_Rankings.py

import streamlit as st
import pandas as pd
from shared_functions import get_db_connection, save_character_ranking, get_character_rankings, SERIES_DATA

st.set_page_config(page_title="Character Rankings", page_icon="📈", layout="wide")

# --- Initial Setup ---
db = get_db_connection()
if not db:
    st.error("Database connection failed.")
    st.stop()

# Retrieve shared info from session state set on the main page
try:
    selected_series_title = st.session_state['selected_series_title']
    current_user = st.session_state['current_user']
    characters = SERIES_DATA[selected_series_title].get("characters", [])
except KeyError:
    st.warning("Please select a series from the 📖 Dashboard page first.")
    st.stop()

st.markdown(f'<div class="main-header">Character Power Rankings</div>', unsafe_allow_html=True)
st.markdown(f"### For {selected_series_title}")

if not characters:
    st.info("No characters have been added for this series yet.")
    st.stop()

# --- UI to Select and Rank a Character ---
selected_char = st.selectbox("Select a Character to Rank", options=characters)

with st.form(f"ranking_form_{selected_char}"):
    st.markdown(f"#### Your Rankings for {selected_char}")
    
    # Define the ranking categories
    rankings_data = {}
    rankings_data['therapy'] = st.slider("Most in Need of Therapy", 1, 10, 5)
    rankings_data['banter'] = st.slider("Best Banter / Sass", 1, 10, 5)
    rankings_data['badass'] = st.slider("Biggest Badass", 1, 10, 5)

    if st.form_submit_button("Save My Rankings"):
        save_character_ranking(db, selected_series_title, selected_char, current_user, rankings_data)
        st.success(f"Your rankings for {selected_char} have been saved!")
        st.rerun()

# --- UI to Display Average Rankings ---
st.markdown("---")
st.markdown(f"#### Community Average Rankings for {selected_char}")
all_rankings = get_character_rankings(db, selected_series_title, selected_char)

if all_rankings:
    # Use pandas to easily calculate the average for each ranking category
    df = pd.DataFrame([r['rankings'] for r in all_rankings])
    avg_rankings = df.mean().to_dict()

    col1, col2, col3 = st.columns(3)
    col1.metric("Avg. Therapy Need", f"{avg_rankings.get('therapy', 0):.1f} / 10")
    col2.metric("Avg. Banter", f"{avg_rankings.get('banter', 0):.1f} / 10")
    col3.metric("Avg. Badassery", f"{avg_rankings.get('badass', 0):.1f} / 10")

    # Display individual rankings in an expander
    with st.expander("See individual rankings"):
        for rank in all_rankings:
            st.write(f"**{rank['user']}'s Rankings:**")
            st.write(f"- Therapy Need: {rank['rankings'].get('therapy', 'N/A')}")
            st.write(f"- Banter: {rank['rankings'].get('banter', 'N/A')}")
            st.write(f"- Badassery: {rank['rankings'].get('badass', 'N/A')}")
else:
    st.info("Be the first to rank this character!")