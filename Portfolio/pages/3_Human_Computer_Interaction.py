import streamlit as st
from styles import apply_custom_styles, apply_page_config

# Apply page configuration and custom styling
apply_page_config()
# apply_custom_styles()

st.title("Human-Computer Interaction")
st.subheader("Project: Civic Impact Navigator")

st.markdown("""
**Context:**  
Civic processes are often abstract and hard to connect to daily life.  
This tool translates **government actions into human-centered narratives**.

**Key Features:**
- Interactive flowchart of legislative/judicial processes
- Plain-language translations of complex policies
- Personalized "impact stories" based on user profile
- Historical context comparisons
""")

st.warning("📖 Future Prototype: Select a civic event and generate a personalized impact narrative.")
