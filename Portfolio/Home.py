import streamlit as st
import os
from styles import apply_custom_styles, apply_page_config

# Apply page configuration and custom styling
apply_page_config()
apply_custom_styles()

# Profile section
col1, col2 = st.columns([1,3])
with col1:
    # Use the corrected relative path
    st.image("Portfolio/assets/IMG_1304.png")

with col2:
    st.title("Laurné Jones")
    st.markdown("""
    Hi! I'm a **Sr. Analytics Engineer at The Walt Disney Company** Passionate about **data strategy, design, and innovation** — I specialize in transforming raw data into meaningful 
    insights and creating tools that empower decision-making.  

    **Areas of Interest**:  
    - Strategic Innovation  
    - Urban Analytics  
    - Human-Computer Interaction
    """)

st.divider()

# --- Auto-generate page links from the "pages" folder ---
st.subheader("Explore My Work")

# Get directory of the current file (Home.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(BASE_DIR, "pages")

# List all files in the pages directory and sort them
page_files = sorted([f for f in os.listdir("Portfolio/pages") if f.endswith(".py")])

# Display in a single row using columns
cols = st.columns(len(page_files))

for i, f in enumerate(page_files):
    # Remove prefix numbers and .py for display
    clean_name = f.split("_", 1)[-1].replace(".py", "").replace("_", " ")
    clean_name = " ".join(word.capitalize() for word in clean_name.split())
    
    with cols[i]:
        st.markdown(f"### {clean_name}")
        # The corrected line for the page link
        st.page_link(f"pages/{f}", label="Explore Projects →")