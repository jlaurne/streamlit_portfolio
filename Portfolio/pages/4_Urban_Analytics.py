import streamlit as st
from styles import apply_custom_styles, apply_page_config

# Apply page configuration and custom styling
apply_page_config()
# apply_custom_styles()

st.title("Urban Analytics")
st.subheader("Project: Urban Traffic & Commute Analytics Dashboard")

st.markdown("""
**Context:**  
Traffic congestion impacts commutes, productivity, and the environment.  
This dashboard helps **urban planners & commuters** understand traffic trends.

**Key Features:**
- Interactive real-time traffic maps
- Historical traffic pattern analysis
- Correlation with weather & events
- Congestion hotspot reports
""")

st.success("🌍 Planned Demo: Explore a live map with congestion overlays, time-series charts, and hotspot analysis.")
