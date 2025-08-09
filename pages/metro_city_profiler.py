import streamlit as st
import pandas as pd
import plotly.express as px
from utils.scoring import calculate_fit_score

st.title("🏙 Metro City Profiler")

df = pd.read_csv("data/cities.csv")
cities = st.multiselect("Select Cities", df["City"].tolist(), default=["Chicago", "New York"])

weights = {
    "affordability": st.slider("Weight: Affordability", 0, 10, 5),
    "culture": st.slider("Weight: Culture (Walk Score)", 0, 10, 3),
    "transportation": st.slider("Weight: Transportation", 0, 10, 2)
}

filtered = df[df["City"].isin(cities)].copy()
filtered["Fit_Score"] = filtered.apply(lambda row: calculate_fit_score(row, weights), axis=1)

st.dataframe(filtered)

fig = px.bar(filtered, x="City", y="Fit_Score", title="Lifestyle Fit Score")
st.plotly_chart(fig)
