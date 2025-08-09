import streamlit as st
import pandas as pd
import altair as alt
from utils.metrics import calculate_metric

st.title("📊 Metric Definition Explorer")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("data/sample_dataset.csv")

definition = st.selectbox("Select Metric Definition", ["Definition 1", "Definition 2", "Combined"])

metric_value = calculate_metric(df, definition)
st.metric(label=f"Average ({definition})", value=round(metric_value, 2))

chart = alt.Chart(df).mark_bar().encode(
    x="Department",
    y="MetricA",
    color="Department"
)
st.altair_chart(chart, use_container_width=True)
