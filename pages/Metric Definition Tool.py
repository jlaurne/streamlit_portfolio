Mimport streamlit as st
import pandas as pd
import altair as alt

# --- IMPORTANT ---
# This import now works because the 'utils' folder is at the top level of your project.
# Streamlit runs this page from the project's root directory.
from utils.metrics import calculate_metric

# Set the title for this specific page.
# The styling from your main portfolio_app.py will be automatically applied.
st.markdown('<div class="section-header">Metric Definition Explorer</div>', unsafe_allow_html=True)
st.write("An interactive tool to compare different metric calculations on a dataset.")

st.markdown("---")

# File uploader with a default dataset
st.subheader("1. Upload Your Data")
st.write("Upload a CSV file or use the default sample data to begin.")
uploaded_file = st.file_uploader("Upload your data (CSV format)", type=["csv"])

# --- Pathing Note ---
# The path "data/sample_dataset.csv" works because the 'data' folder
# is at the top level of your project.
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    # Use a default dataset if no file is uploaded
    try:
        df = pd.read_csv("data/sample_dataset.csv")
    except FileNotFoundError:
        st.error("The default 'sample_dataset.csv' was not found. Please make sure it's in the 'data' folder at the project root.")
        st.stop()

st.dataframe(df.head())

st.markdown("---")

# Metric calculation and display
st.subheader("2. Calculate a Metric")
st.write("Select a metric definition to apply to the dataset.")
definition = st.selectbox(
    "Select Metric Definition", 
    ["Definition 1", "Definition 2", "Combined"],
    help="These definitions correspond to different business logic rules in the `calculate_metric` function."
)

if st.button("Calculate Metric"):
    metric_value = calculate_metric(df, definition)
    st.metric(label=f"Average Value ({definition})", value=round(metric_value, 2))

st.markdown("---")

# Data visualization
st.subheader("3. Visualize the Data")
st.write("Select a column to visualize across departments.")

# Making the chart dynamic based on a column selection
if 'Department' in df.columns:
    # Get a list of numeric columns to choose from
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if numeric_cols:
        y_axis_selection = st.selectbox("Select a metric to visualize:", numeric_cols)

        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X("Department:N", title="Department"),
            y=alt.Y(f"{y_axis_selection}:Q", title=f"Value of {y_axis_selection}"),
            color=alt.Color("Department:N", title="Department"),
            tooltip=["Department", y_axis_selection]
        ).properties(
            title=f"{y_axis_selection} by Department"
        ).interactive()

        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("No numeric columns found in the data to plot.")
else:
    st.warning("The dataset must contain a 'Department' column to create the visualization.")