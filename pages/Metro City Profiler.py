import streamlit as st
import pandas as pd
import plotly.express as px

# --- MOCK FUNCTION ---
# This is a placeholder for your actual 'calculate_fit_score' function from utils.
# For this page to work, ensure your function takes a data row and weights dict and returns a score.
def calculate_fit_score(row, weights):
    """
    Generates a sample fit score.
    Replace this with your actual import: from utils.scoring import calculate_fit_score
    """
    import numpy as np
    score = (row['Affordability_idx'] * weights['affordability'] +
             row['Culture_idx'] * weights['culture'] +
             row['Transportation_idx'] * weights['transportation'])
    return score / sum(weights.values()) if sum(weights.values()) > 0 else 0
# --- END MOCK FUNCTION ---


# Use the custom CSS class for a consistent header style
st.markdown('<div class="section-header">Metro City Profiler</div>', unsafe_allow_html=True)
st.write("A tool to rank cities based on personal preferences for affordability, culture, and transportation.")

st.markdown("---")

# --- Step 1: Load Data ---
# Add a try-except block for robust file loading
try:
    df = pd.read_csv("data/cities.csv")
except FileNotFoundError:
    st.error("The default 'cities.csv' file was not found. Please place it in the 'data' folder at the project root.")
    st.stop()


# --- Step 2: User Selections ---
st.subheader("1. Select Cities to Compare")
cities = st.multiselect(
    "Select one or more cities from the list:", 
    df["City"].tolist(), 
    default=["New York", "Chicago", "Los Angeles", "New Orleans"]
)

st.markdown("---")

# --- Step 3: Set Preferences ---
st.subheader("2. Set Your Lifestyle Preferences")
st.write("Use the sliders to assign a weight to what matters most to you in a city.")

# Use columns for a cleaner layout
col1, col2, col3 = st.columns(3)
with col1:
    affordability_weight = st.slider("⚖️ Affordability", 0, 10, 5, help="How important is low cost of living?")
with col2:
    culture_weight = st.slider("🎭 Culture", 0, 10, 3, help="How important are cultural venues and walkability?")
with col3:
    transportation_weight = st.slider("🚇 Transportation", 0, 10, 7, help="How important is accessible public transit?")

weights = {
    "affordability": affordability_weight,
    "culture": culture_weight,
    "transportation": transportation_weight
}

st.markdown("---")


# --- Step 4: Calculate and Display Results ---
st.subheader("3. View Your Personalized City Rankings")

if not cities:
    st.warning("Please select at least one city to see the results.")
else:
    # Filter the dataframe based on user's city selection
    filtered_df = df[df["City"].isin(cities)].copy()

    # Calculate the 'Fit_Score' for each city
    filtered_df["Fit_Score"] = filtered_df.apply(lambda row: calculate_fit_score(row, weights), axis=1)
    
    # Sort by the new score for a clean presentation
    results_df = filtered_df.sort_values("Fit_Score", ascending=False)

    st.write("The table below shows the raw data alongside your calculated 'Fit Score'.")
    st.dataframe(results_df)

    # Create an enhanced bar chart
    fig = px.bar(
        results_df, 
        x="City", 
        y="Fit_Score",
        color="Fit_Score",
        color_continuous_scale=px.colors.sequential.Tealgrn,
        title="<b>Personalized Lifestyle Fit Score by City</b>",
        labels={"City": "City", "Fit_Score": "Your Personalized Fit Score"}
    )
    
    fig.update_layout(
        xaxis={'categoryorder':'total descending'},
        coloraxis_showscale=False
    )

    st.plotly_chart(fig, use_container_width=True)