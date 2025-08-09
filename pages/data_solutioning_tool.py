import streamlit as st
import plotly.express as px
from utils.roadmap import generate_roadmap

st.title("🗺 Data Solutioning Roadmap Tool")

project_name = st.text_input("Project Name")
phases = st.text_area("Enter Phases (one per line)").split("\n")

if st.button("Generate Roadmap") and phases:
    roadmap = generate_roadmap(phases)
    fig = px.bar(roadmap, x="Phase", y="Duration (weeks)", title=project_name)
    st.plotly_chart(fig)
