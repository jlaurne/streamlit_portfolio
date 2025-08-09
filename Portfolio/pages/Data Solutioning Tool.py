import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

# --- MOCK FUNCTION ---
# This is a placeholder for your actual 'generate_roadmap' function from utils.
# For this page to work, ensure your function returns a DataFrame with at least a 'Phase' and 'Duration (weeks)' column.
def generate_roadmap(phases):
    """
    Generates a sample roadmap DataFrame.
    Replace this with your actual import: from utils.roadmap import generate_roadmap
    """
    import numpy as np
    durations = np.random.randint(2, 8, len(phases))
    roadmap_df = pd.DataFrame({
        "Phase": phases,
        "Duration (weeks)": durations
    })
    return roadmap_df
# --- END MOCK FUNCTION ---


# Use the custom CSS class for a consistent header style
st.markdown('<div class="section-header">Data Solutioning Roadmap Tool</div>', unsafe_allow_html=True)
st.write("A simple tool to generate a project roadmap timeline from a list of phases.")

st.markdown("---")

# --- Step 1: Get User Input ---
st.subheader("1. Define Your Project")

project_name = st.text_input("Enter the Project Name", "New Data Platform Initiative")

# Use a default example in the text_area
default_phases = "Discovery & Scoping\nData Modeling & Architecture\nETL Pipeline Development\nDashboard Creation\nUser Acceptance Testing\nDeployment"
phases_input = st.text_area("Enter Project Phases (one per line)", value=default_phases, height=150)

# Clean up the input phases
phases = [phase.strip() for phase in phases_input.split("\n") if phase.strip()]

st.markdown("---")

# --- Step 2: Generate and Display Roadmap ---
st.subheader("2. Generate and View Roadmap")

if st.button("Generate Roadmap"):
    if not project_name:
        st.warning("Please enter a project name.")
    elif not phases:
        st.warning("Please enter at least one project phase.")
    else:
        with st.spinner("Generating your roadmap..."):
            # 1. Get the roadmap data from your utility function
            roadmap_df = generate_roadmap(phases)

            # 2. Calculate Start and Finish dates for the Gantt chart
            roadmap_df['Start'] = None
            roadmap_df['Finish'] = None
            
            start_date = datetime.now()
            for i, row in roadmap_df.iterrows():
                if i == 0:
                    roadmap_df.loc[i, 'Start'] = start_date
                else:
                    # Start the next phase after the previous one ends
                    roadmap_df.loc[i, 'Start'] = roadmap_df.loc[i-1, 'Finish']
                
                duration_weeks = row['Duration (weeks)']
                roadmap_df.loc[i, 'Finish'] = roadmap_df.loc[i, 'Start'] + timedelta(weeks=duration_weeks)

            # 3. Create the Gantt chart using Plotly Express
            fig = px.timeline(
                roadmap_df,
                x_start="Start",
                x_end="Finish",
                y="Phase",
                color="Phase",
                title=f"Roadmap: {project_name}",
                labels={"Phase": "Project Phase"}
            )

            # Improve layout and sort phases correctly
            fig.update_yaxes(categoryorder='total ascending')
            fig.update_layout(showlegend=False)

            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(roadmap_df)
